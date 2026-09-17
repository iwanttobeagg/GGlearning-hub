import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data.json"
TZ = ZoneInfo("Asia/Taipei")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}

FUNDS = {
    "DSP5": {
        "nav_url": "https://invest.fubonlife.com.tw/w/wb/wb02.djhtm?a=TLZ64-DSP5",
        "dist_url": "https://invest.fubonlife.com.tw/w/wb/wb05.djhtm?a=TLZ64-DSP5",
    },
    "DST3": {
        "nav_url": "https://invest.fubonlife.com.tw/w/wr/wr02.djhtm?a=ACDD154-DST3",
        "dist_url": "https://invest.fubonlife.com.tw/w/wr/wr10.djhtm?a=ACDD154-DST3",
    },
    "JFP11": {
        "nav_url": "https://invest.fubonlife.com.tw/w/wb/wb02.djhtm?a=JFZN3-JFP11",
        "dist_url": "https://invest.fubonlife.com.tw/w/wb/wb05.djhtm?a=JFZN3-JFP11",
    },
    "NGB1": {
        "nav_url": "https://invest.fubonlife.com.tw/w/wb/wb02.djhtm?a=ANZ89-NGB1",
        "dist_url": "https://invest.fubonlife.com.tw/w/wb/wb05.djhtm?a=ANZ89-NGB1",
    },
    "MLE24": {
        "nav_url": "https://invest.fubonlife.com.tw/w/wb/wb02.djhtm?a=SHZV9-MLE24",
        "dist_url": "https://invest.fubonlife.com.tw/w/wb/wb05.djhtm?a=SHZV9-MLE24",
    },
    "ACE17": {
        "nav_url": "https://fund.hncb.com.tw/w/wb/wb02.djhtm?a=ALBT8-16G7",
        "dist_url": "https://fund.hncb.com.tw/w/wb/wb05.djhtm?a=ALBT8-16G7",
    },
}

DATE_RE = re.compile(r"^(?:(\d{4})[/-])?(\d{1,2})[/-](\d{1,2})$")
NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")


def get_soup(url: str) -> BeautifulSoup:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = r.apparent_encoding
    return BeautifulSoup(r.text, "html.parser")


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def normalize_date(raw: str) -> str:
    raw = raw.strip()
    m = DATE_RE.match(raw)
    if not m:
        raise ValueError(f"unrecognized date: {raw}")
    y, mm, dd = m.groups()
    now = datetime.now(TZ)
    if y is None:
        year = now.year
        # Handles the year boundary if a December row is seen in January.
        if int(mm) > now.month + 1:
            year -= 1
    else:
        year = int(y)
    return f"{year:04d}-{int(mm):02d}-{int(dd):02d}"


def parse_nav(url: str):
    soup = get_soup(url)
    for tr in soup.find_all("tr"):
        cells = [clean(td.get_text(" ", strip=True)) for td in tr.find_all(["td", "th"])]
        if len(cells) < 2:
            continue
        if DATE_RE.match(cells[0]) and NUM_RE.match(cells[1].replace(",", "")):
            return float(cells[1].replace(",", "")), normalize_date(cells[0])
    # Fallback for pages whose table markup is flattened.
    text = clean(soup.get_text(" ", strip=True))
    m = re.search(r"((?:\d{4}[/-])?\d{1,2}[/-]\d{1,2})\s+([0-9]+(?:\.[0-9]+)?)", text)
    if not m:
        raise RuntimeError(f"NAV not found: {url}")
    return float(m.group(2)), normalize_date(m.group(1))


def parse_distribution(url: str):
    soup = get_soup(url)
    for tr in soup.find_all("tr"):
        cells = [clean(td.get_text(" ", strip=True)) for td in tr.find_all(["td", "th"])]
        if not cells:
            continue
        date_indexes = [i for i, c in enumerate(cells) if DATE_RE.match(c)]
        if not date_indexes:
            continue
        # Use the last date on the row as the ex-dividend date where available.
        date_idx = date_indexes[-1]
        ex_date = normalize_date(cells[date_idx])
        # Prefer the numeric field immediately before a USD/currency cell.
        for i, c in enumerate(cells):
            if ("美元" in c or c.upper() == "USD") and i > 0:
                prev = cells[i - 1].replace(",", "")
                if NUM_RE.match(prev):
                    return float(prev), ex_date
        # Otherwise pick the first positive decimal after the date/status fields.
        for c in cells[date_idx + 1 :]:
            x = c.replace(",", "")
            if NUM_RE.match(x):
                val = float(x)
                if 0 < val < 100:
                    return val, ex_date
    text = clean(soup.get_text(" ", strip=True))
    m = re.search(r"((?:\d{4}[/-])?\d{1,2}[/-]\d{1,2}).{0,50}?(\d+(?:\.\d+)?)\s*(?:美元|USD)", text)
    if not m:
        raise RuntimeError(f"distribution not found: {url}")
    return float(m.group(2)), normalize_date(m.group(1))


def parse_bot_fx():
    url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
    soup = get_soup(url)
    for tr in soup.find_all("tr"):
        txt = clean(tr.get_text(" ", strip=True))
        if "美金" not in txt or "USD" not in txt:
            continue
        nums = []
        for td in tr.find_all("td"):
            s = clean(td.get_text(" ", strip=True)).replace(",", "")
            if NUM_RE.match(s):
                nums.append(float(s))
        if len(nums) >= 4:
            # BOT order: cash buy, cash sell, spot buy, spot sell.
            return nums[2], nums[3], datetime.now(TZ).strftime("%Y-%m-%d")
    raise RuntimeError("USD spot rates not found on Bank of Taiwan page")


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    errors = {}

    try:
        buy, sell, fx_date = parse_bot_fx()
        data["fx"] = {
            "source": "臺灣銀行即期匯率",
            "usd_twd_buy": buy,
            "usd_twd_sell": sell,
            "date": fx_date,
        }
    except Exception as e:
        errors["FX"] = str(e)

    for code, src in FUNDS.items():
        fund = data["funds"][code]
        try:
            nav, nav_date = parse_nav(src["nav_url"])
            fund["nav"] = nav
            fund["nav_date"] = nav_date
        except Exception as e:
            errors[f"{code}_nav"] = str(e)
        try:
            dist, dist_date = parse_distribution(src["dist_url"])
            fund["distribution"] = dist
            fund["distribution_date"] = dist_date
        except Exception as e:
            errors[f"{code}_distribution"] = str(e)

    data["updated_at"] = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
    data["refresh_status"] = "partial" if errors else "ok"
    data["refresh_errors"] = errors
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if errors:
        print("Refresh completed with warnings:")
        for k, v in errors.items():
            print(f"- {k}: {v}")
    else:
        print("Refresh completed successfully")


if __name__ == "__main__":
    main()

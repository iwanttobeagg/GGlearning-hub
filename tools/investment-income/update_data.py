import argparse
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


def get_response(url: str) -> requests.Response:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r


def get_soup(url: str) -> BeautifulSoup:
    r = get_response(url)
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
        date_idx = date_indexes[-1]
        ex_date = normalize_date(cells[date_idx])
        for i, c in enumerate(cells):
            if ("美元" in c or c.upper() == "USD") and i > 0:
                prev = cells[i - 1].replace(",", "")
                if NUM_RE.match(prev):
                    return float(prev), ex_date
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


def parse_bot_fx_html():
    soup = get_soup("https://rate.bot.com.tw/xrt?Lang=zh-TW")
    for tr in soup.find_all("tr"):
        txt = clean(tr.get_text(" ", strip=True))
        if "美金" not in txt or "USD" not in txt:
            continue
        # BOT order on the USD row: cash buy, cash sell, spot buy, spot sell.
        nums = [float(x) for x in re.findall(r"(?<!\d)(\d+(?:\.\d+)?)(?!\d)", txt)]
        nums = [x for x in nums if 20 <= x <= 50]
        if len(nums) >= 4:
            return nums[2], nums[3]
    raise RuntimeError("USD spot rates not found in BOT HTML")


def parse_bot_fx_csv():
    r = get_response("https://rate.bot.com.tw/xrt/flcsv/0/day")
    raw = r.content
    text = None
    for enc in ("utf-8-sig", "big5", "cp950", "utf-8"):
        try:
            candidate = raw.decode(enc)
        except Exception:
            continue
        if "USD" in candidate:
            text = candidate
            break
    if text is None:
        text = raw.decode("utf-8", errors="replace")
    for line in text.splitlines():
        if "USD" not in line:
            continue
        nums = [float(x) for x in re.findall(r"(?<!\d)(\d+(?:\.\d+)?)(?!\d)", line)]
        nums = [x for x in nums if 20 <= x <= 50]
        if len(nums) >= 4:
            return nums[2], nums[3]
    raise RuntimeError("USD spot rates not found in BOT CSV")


def parse_bot_fx():
    errors = []
    for fn in (parse_bot_fx_html, parse_bot_fx_csv):
        try:
            buy, sell = fn()
            return buy, sell, datetime.now(TZ).strftime("%Y-%m-%d")
        except Exception as e:
            errors.append(str(e))
    raise RuntimeError("; ".join(errors))


def update_fx(data: dict, errors: dict):
    try:
        buy, sell, fx_date = parse_bot_fx()
        now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
        data["fx"] = {
            "source": "臺灣銀行即期匯率",
            "usd_twd_buy": buy,
            "usd_twd_sell": sell,
            "date": fx_date,
            "updated_at": now,
        }
    except Exception as e:
        errors["FX"] = str(e)


def update_funds(data: dict, errors: dict):
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
    data["funds_updated_at"] = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--fx-only", action="store_true")
    group.add_argument("--funds-only", action="store_true")
    args = parser.parse_args()

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    errors = {}

    if not args.funds_only:
        update_fx(data, errors)
    if not args.fx_only:
        update_funds(data, errors)

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

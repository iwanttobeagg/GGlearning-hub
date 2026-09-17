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
URL = "https://www.bot.com.tw/tw/personal-banking/foreign-exchange"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}


def fetch_usd_spot():
    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    text = " ".join(soup.stripped_strings)

    m = re.search(
        r"美金\s*USD.*?即期買進\s*([0-9]+(?:\.[0-9]+)?).*?即期賣出\s*([0-9]+(?:\.[0-9]+)?)",
        text,
        re.S,
    )
    if not m:
        raise RuntimeError("Could not parse USD spot rates from Bank of Taiwan new site")

    buy = float(m.group(1))
    sell = float(m.group(2))
    if not (20 <= buy <= 50 and 20 <= sell <= 50 and sell >= buy):
        raise RuntimeError(f"Parsed implausible BOT rates: buy={buy}, sell={sell}")

    time_match = re.search(r"掛牌時間[:：]\s*(\d{4}/\d{1,2}/\d{1,2})\s+(\d{1,2}:\d{2})", text)
    quoted_at = None
    if time_match:
        quoted_at = f"{time_match.group(1).replace('/', '-')} {time_match.group(2)}"
    return buy, sell, quoted_at


def main():
    buy, sell, quoted_at = fetch_usd_spot()
    now = datetime.now(TZ)

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data["fx"] = {
        "source": "臺灣銀行即期匯率",
        "usd_twd_buy": buy,
        "usd_twd_sell": sell,
        "date": (quoted_at[:10] if quoted_at else now.strftime("%Y-%m-%d")),
        "quoted_at": quoted_at,
        "updated_at": now.strftime("%Y-%m-%d %H:%M"),
    }
    data["updated_at"] = now.strftime("%Y-%m-%d %H:%M")
    data["refresh_status"] = "ok"
    data["refresh_errors"] = {}
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"USD/TWD BOT spot buy={buy}, sell={sell}, quote={quoted_at}, refreshed={now:%Y-%m-%d %H:%M}")


if __name__ == "__main__":
    main()

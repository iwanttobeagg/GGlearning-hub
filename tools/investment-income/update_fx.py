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
URL = "https://rate.bot.com.tw/xrt?Lang=en-US&redirect=true"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_usd_spot():
    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")

    for tr in soup.find_all("tr"):
        text = " ".join(tr.stripped_strings)
        if "USD" not in text:
            continue

        values = []
        for td in tr.find_all("td"):
            cell = " ".join(td.stripped_strings).replace(",", "")
            if re.fullmatch(r"\d+(?:\.\d+)?", cell):
                values.append(float(cell))

        values = [x for x in values if 20 <= x <= 50]
        if len(values) >= 4:
            # BOT order: cash buy, cash sell, spot buy, spot sell
            return values[2], values[3]

        # fallback: parse all visible numbers in the USD row
        values = [float(x) for x in re.findall(r"(?<!\d)(\d+(?:\.\d+)?)(?!\d)", text)]
        values = [x for x in values if 20 <= x <= 50]
        if len(values) >= 4:
            return values[2], values[3]

    raise RuntimeError("Could not parse USD spot rates from Bank of Taiwan")


def main():
    buy, sell = fetch_usd_spot()
    now = datetime.now(TZ)

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data["fx"] = {
        "source": "臺灣銀行即期匯率",
        "usd_twd_buy": buy,
        "usd_twd_sell": sell,
        "date": now.strftime("%Y-%m-%d"),
        "updated_at": now.strftime("%Y-%m-%d %H:%M"),
    }
    data["updated_at"] = now.strftime("%Y-%m-%d %H:%M")
    data["refresh_status"] = "ok"
    data["refresh_errors"] = {}
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"USD/TWD spot buy={buy}, sell={sell}, updated={now:%Y-%m-%d %H:%M}")


if __name__ == "__main__":
    main()

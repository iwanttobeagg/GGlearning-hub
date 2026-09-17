import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data.json"
TZ = ZoneInfo("Asia/Taipei")

SOURCES = [
    "https://cdn.jsdelivr.net/gh/haotool/app@data/public/rates/latest.json",
    "https://raw.githubusercontent.com/haotool/app/data/public/rates/latest.json",
]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept": "application/json",
}


def fetch_usd_spot():
    errors = []
    for url in SOURCES:
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            payload = r.json()
            usd = payload["details"]["USD"]["spot"]
            buy = float(usd["buy"])
            sell = float(usd["sell"])
            if not (20 <= buy <= 50 and 20 <= sell <= 50 and sell >= buy):
                raise RuntimeError(f"Implausible USD/TWD rates: buy={buy}, sell={sell}")
            return buy, sell, url
        except Exception as e:
            errors.append(f"{url}: {e}")
    raise RuntimeError(" | ".join(errors))


def main():
    buy, sell, source_url = fetch_usd_spot()
    now = datetime.now(TZ)

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data["fx"] = {
        "source": "HaoRate 公開匯率",
        "source_url": source_url,
        "usd_twd_buy": buy,
        "usd_twd_sell": sell,
        "date": now.strftime("%Y-%m-%d"),
        "updated_at": now.strftime("%Y-%m-%d %H:%M"),
    }
    data["updated_at"] = now.strftime("%Y-%m-%d %H:%M")
    data["refresh_status"] = "ok"
    data["refresh_errors"] = {}
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"USD/TWD spot buy={buy}, sell={sell}, source={source_url}, refreshed={now:%Y-%m-%d %H:%M}")


if __name__ == "__main__":
    main()

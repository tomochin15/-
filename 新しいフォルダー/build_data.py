
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

from scraper_pokemoncenter import scrape as scrape_pc
from scraper_yodobashi import scrape as scrape_yd
from scraper_joshin import scrape as scrape_js
from scraper_x import scrape as scrape_x

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data.json"

def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def load_base():
    if DATA_PATH.exists():
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return {
        "site": {
            "name": "ポケカ速報ラボ",
            "tagline": "抽選・再販・予約を、速く、正確に、見やすく。",
            "updatedAt": now_text(),
            "heroNote": "自動更新テンプレート。"
        },
        "lottery": [],
        "commerce": [],
        "social": [],
        "shops": [],
        "faq": [],
        "guides": []
    }

def main() -> None:
    payload = load_base()
    lottery = []
    errors = []

    for func in (scrape_pc, scrape_yd, scrape_js):
        try:
            rows = func()
            for row in rows:
                row["publishedAt"] = now_text()
            lottery.extend(rows)
        except Exception as e:
            errors.append(str(e))

    social = []
    try:
        social = scrape_x()
    except Exception as e:
        errors.append(str(e))

    payload["lottery"] = lottery
    payload["social"] = social
    payload["site"]["updatedAt"] = now_text()

    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if errors:
        print("completed with errors:")
        for e in errors:
            print(" -", e)
    else:
        print("completed")

if __name__ == "__main__":
    main()

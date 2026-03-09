
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).parent

# 実運用ではRSS/NitterやAPI等、利用条件に合う手段で取得してください。
# このテンプレートでは、手動投入用の social_source.json を読んで data.json に統合します。
#
# social_source.json の例:
# [
#   {
#     "source": "ポケゲトちゃんねる",
#     "title": "ポケカ抽選情報",
#     "url": "https://x.com/...",
#     "publishedAt": "2026-03-09 20:00",
#     "summary": "ポケポケ関連を除外した投稿"
#   }
# ]

SOCIAL_SOURCE = ROOT / "social_source.json"

EXCLUDE_KEYWORDS = ["ポケポケ"]
INCLUDE_KEYWORDS = ["ポケモンカード", "ポケカ", "抽選", "再販", "予約"]

def _allowed(item: Dict[str, Any]) -> bool:
    text = " ".join([
        str(item.get("title", "")),
        str(item.get("summary", "")),
    ])
    if any(x in text for x in EXCLUDE_KEYWORDS):
        return False
    if not any(x in text for x in INCLUDE_KEYWORDS):
        return False
    return True

def scrape() -> List[Dict[str, Any]]:
    if not SOCIAL_SOURCE.exists():
        return []
    raw = json.loads(SOCIAL_SOURCE.read_text(encoding="utf-8"))
    out: List[Dict[str, Any]] = []
    for item in raw:
        if not _allowed(item):
            continue
        out.append({
            "source": item.get("source", "X"),
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "publishedAt": item.get("publishedAt", ""),
            "summary": item.get("summary", ""),
        })
    return out

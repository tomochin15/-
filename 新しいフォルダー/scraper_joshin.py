
from __future__ import annotations

import re
from typing import Any, Dict, List
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PokekaMonitor/1.0)"}

def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def scrape(url: str = "https://joshinweb.jp/toy/top.html") -> List[Dict[str, Any]]:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    text = _clean(soup.get_text(" ", strip=True))

    status = "ポケモンカード抽選販売あり" if "ポケモンカード抽選販売" in text else "玩具ページ監視中"

    return [{
        "shop": "Joshin",
        "product": "おもちゃトップページ",
        "status": status,
        "start": "公式ページ確認",
        "end": "公式ページ確認",
        "result": "公式ページ確認",
        "url": url,
        "publishedAt": "",
        "summary": "Joshinおもちゃトップにあるポケモンカード抽選販売導線の有無を簡易判定。"
    }]

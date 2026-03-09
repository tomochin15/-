
from __future__ import annotations

from typing import Any, Dict, List
import requests
from bs4 import BeautifulSoup

from extractors import clean, extract_schedule

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PokekaMonitor/1.0)"}

def scrape(url: str = "https://joshinweb.jp/toy/top.html") -> List[Dict[str, Any]]:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    text = clean(soup.get_text(" ", strip=True))
    start, end, result = extract_schedule(text)

    status = "ポケモンカード抽選販売あり" if "ポケモンカード抽選販売" in text else "玩具ページ監視中"
    items: List[Dict[str, Any]] = [{
        "shop": "Joshin",
        "product": "おもちゃトップページ",
        "status": status,
        "start": start,
        "end": end,
        "result": result,
        "url": url,
        "publishedAt": "",
        "summary": "Joshinトップの抽選導線と日時文言を自動抽出。"
    }]

    for a in soup.select("a[href]"):
        label = clean(a.get_text(" ", strip=True))
        href = a.get("href", "")
        if ("ポケモンカード" in label or "抽選販売" in label) and href:
            full = href if href.startswith("http") else f"https://joshinweb.jp{href}"
            items.append({
                "shop": "Joshin",
                "product": label[:120] or "抽選販売ページ",
                "status": "抽選導線検出",
                "start": "公式ページ確認",
                "end": "公式ページ確認",
                "result": "公式ページ確認",
                "url": full,
                "publishedAt": "",
                "summary": "個別導線候補も保持。"
            })
    return items

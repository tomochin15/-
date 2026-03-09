
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PokekaMonitor/1.0)"}
BASE = "https://www.pokemoncenter-online.com/"

def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def _find_datetime_near(text: str, keywords: list[str]) -> str:
    lines = [x.strip() for x in re.split(r"[。\n\r]+", text) if x.strip()]
    dt_pattern = re.compile(r"(20\d{2}[/-]\d{1,2}[/-]\d{1,2}.*?\d{1,2}:\d{2}|20\d{2}年\d{1,2}月\d{1,2}日.*?\d{1,2}:\d{2})")
    for line in lines:
        if any(k in line for k in keywords):
            m = dt_pattern.search(line)
            if m:
                return m.group(1)
    return "商品ページ確認"

def _extract_schedule(text: str) -> tuple[str, str, str]:
    start = _find_datetime_near(text, ["応募受付開始", "受付開始", "応募開始"])
    end = _find_datetime_near(text, ["応募受付終了", "受付終了", "応募締切", "受付締切"])
    result = _find_datetime_near(text, ["当選発表", "抽選結果", "結果発表"])
    return start, end, result

def _candidate_links(soup: BeautifulSoup) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for a in soup.select("a[href]"):
        label = _clean(a.get_text(" ", strip=True))
        href = a.get("href", "").strip()
        if not href:
            continue
        full = href if href.startswith("http") else urljoin(BASE, href)
        if "pokemoncard" in full.lower() or "抽選" in label or "ポケモンカード" in label:
            if full not in seen:
                seen.add(full)
                out.append((label[:120] or "個別商品ページ", full))
    return out

def scrape(url: str = "https://www.pokemoncenter-online.com/lottery/apply.html") -> List[Dict[str, Any]]:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    page_text = _clean(soup.get_text(" ", strip=True))

    items: List[Dict[str, Any]] = [{
        "shop": "ポケモンセンターオンライン",
        "product": "抽選応募一覧ページ",
        "status": "応募受付中" if "応募" in page_text else "掲載あり",
        "start": "公式ページ確認",
        "end": "公式ページ確認",
        "result": "公式ページ確認",
        "url": url,
        "publishedAt": "",
        "summary": "抽選応募一覧ページを取得。下位の個別商品ページも順次解析。"
    }]

    for label, full in _candidate_links(soup)[:12]:
        try:
            r = requests.get(full, headers=HEADERS, timeout=20)
            r.raise_for_status()
            child = BeautifulSoup(r.text, "lxml")
            text = _clean(child.get_text(" ", strip=True))
            start, end, result = _extract_schedule(text)
            status = "抽選販売掲載" if ("抽選" in text or "応募" in text) else "商品ページ確認"
            title = label if label and label != "個別商品ページ" else _clean(child.title.get_text(" ", strip=True))[:120]
            items.append({
                "shop": "ポケモンセンターオンライン",
                "product": title,
                "status": status,
                "start": start,
                "end": end,
                "result": result,
                "url": full,
                "publishedAt": "",
                "summary": "個別商品ページを取得してスケジュール文を簡易抽出。"
            })
        except Exception:
            items.append({
                "shop": "ポケモンセンターオンライン",
                "product": label or "個別商品ページ",
                "status": "個別商品ページ確認",
                "start": "商品ページ確認",
                "end": "商品ページ確認",
                "result": "商品ページ確認",
                "url": full,
                "publishedAt": "",
                "summary": "リンク検出は成功。詳細抽出は未取得。"
            })
    return items

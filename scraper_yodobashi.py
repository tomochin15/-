
from __future__ import annotations

import re
from typing import Any, Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PokekaMonitor/1.0)"}
BASE = "https://limited.yodobashi.com/"

def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def _find_near_datetime(text: str, keywords: list[str]) -> str:
    lines = [x.strip() for x in re.split(r"[。\n\r]+", text) if x.strip()]
    dt_pattern = re.compile(r"(20\d{2}[/-]\d{1,2}[/-]\d{1,2}.*?\d{1,2}:\d{2}|20\d{2}年\d{1,2}月\d{1,2}日.*?\d{1,2}:\d{2})")
    for line in lines:
        if any(k in line for k in keywords):
            m = dt_pattern.search(line)
            if m:
                return m.group(1)
    return "公式ページ確認"

def _extract_schedule(text: str) -> tuple[str, str, str]:
    start = _find_near_datetime(text, ["お申し込み受付開始", "受付開始", "応募開始"])
    end = _find_near_datetime(text, ["お申し込み受付は終了", "お申し込み受付終了", "受付終了", "応募締切"])
    result = _find_near_datetime(text, ["当選発表", "抽選結果", "結果発表"])
    return start, end, result

def _candidate_links(soup: BeautifulSoup) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for a in soup.select("a[href]"):
        href = a.get("href", "").strip()
        label = _clean(a.get_text(" ", strip=True))
        if not href:
            continue
        full = href if href.startswith("http") else urljoin(BASE, href)
        joined = f"{label} {full}".lower()
        if any(k in joined for k in ["pokemon", "ポケモン", "ポケカ", "抽選"]):
            if full not in seen:
                seen.add(full)
                out.append((label[:120] or "商品ページ", full))
    return out

def scrape(url: str = "https://limited.yodobashi.com/") -> List[Dict[str, Any]]:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    page_text = _clean(soup.get_text(" ", strip=True))

    if "お申し込み受付は 終了" in page_text or "お申し込み受付は終了" in page_text:
        page_status = "受付終了"
    elif "抽選" in page_text:
        page_status = "抽選ページ掲載"
    else:
        page_status = "掲載確認"

    items: List[Dict[str, Any]] = [{
        "shop": "ヨドバシ.com",
        "product": "人気商品抽選ページ",
        "status": page_status,
        "start": "公式ページ確認",
        "end": "公式ページ確認",
        "result": "公式ページ確認",
        "url": url,
        "publishedAt": "",
        "summary": "ヨドバシ抽選トップを取得。個別候補リンクも順次解析。"
    }]

    for label, full in _candidate_links(soup)[:15]:
        try:
            r = requests.get(full, headers=HEADERS, timeout=20)
            r.raise_for_status()
            child = BeautifulSoup(r.text, "lxml")
            text = _clean(child.get_text(" ", strip=True))
            start, end, result = _extract_schedule(text)
            status = "抽選商品掲載" if ("抽選" in text or "お申し込み" in text) else "商品ページ確認"
            title = label if label and label != "商品ページ" else _clean(child.title.get_text(" ", strip=True))[:120]
            items.append({
                "shop": "ヨドバシ.com",
                "product": title,
                "status": status,
                "start": start,
                "end": end,
                "result": result,
                "url": full,
                "publishedAt": "",
                "summary": "個別候補ページを取得してスケジュール文言を簡易抽出。"
            })
        except Exception:
            items.append({
                "shop": "ヨドバシ.com",
                "product": label or "商品ページ",
                "status": "個別商品ページ確認",
                "start": "公式ページ確認",
                "end": "公式ページ確認",
                "result": "公式ページ確認",
                "url": full,
                "publishedAt": "",
                "summary": "候補リンク検出は成功。詳細抽出は未取得。"
            })
    return items

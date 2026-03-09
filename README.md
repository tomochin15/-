from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

def now_jst_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def make_lottery(
    shop: str,
    product: str,
    status: str,
    url: str,
    start: str = "未定",
    end: str = "未定",
    result: str = "未定",
    summary: str = "",
) -> Dict[str, Any]:
    return {
        "shop": shop,
        "product": product,
        "status": status,
        "start": start,
        "end": end,
        "result": result,
        "url": url,
        "publishedAt": now_jst_text(),
        "summary": summary,
    }

def make_commerce(
    shop: str,
    title: str,
    kind: str,
    status: str,
    url: str,
    summary: str = "",
) -> Dict[str, Any]:
    return {
        "shop": shop,
        "title": title,
        "kind": kind,
        "status": status,
        "url": url,
        "publishedAt": now_jst_text(),
        "summary": summary,
    }

def dedupe_by_keys(items: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for item in items:
        signature = tuple(item.get(k, "") for k in keys)
        if signature in seen:
            continue
        seen.add(signature)
        out.append(item)
    return out

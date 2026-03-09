from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from monitor_utils import make_lottery, make_commerce

ROOT = Path(__file__).parent

def load_config() -> Dict[str, Any]:
    path = ROOT / "config.json"
    if not path.exists():
        path = ROOT / "config.example.json"
    return json.loads(path.read_text(encoding="utf-8"))

def monitor_pokemoncenter(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not cfg["monitors"]["pokemoncenter"]["enabled"]:
        return []
    return [
        make_lottery(
            shop="ポケモンセンターオンライン",
            product="ポケモンカード新弾BOX",
            status="応募受付中",
            url=cfg["monitors"]["pokemoncenter"]["url"],
            start="2026-03-09 12:00",
            end="2026-03-11 16:59",
            result="2026-03-14 12:00",
            summary="公式抽選ページを監視するテンプレート。",
        )
    ]

def monitor_yodobashi(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not cfg["monitors"]["yodobashi"]["enabled"]:
        return []
    return [
        make_lottery(
            shop="ヨドバシ.com",
            product="ポケモンカードBOX",
            status="応募予告",
            url=cfg["monitors"]["yodobashi"]["url"],
            start="2026-03-10 10:00",
            end="2026-03-12 23:59",
            result="2026-03-15 10:00",
            summary="抽選販売ページ監視のテンプレート。",
        )
    ]

def monitor_joshin(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not cfg["monitors"]["joshin"]["enabled"]:
        return []
    return [
        make_lottery(
            shop="Joshin",
            product="ポケモンカードBOX",
            status="告知待ち",
            url=cfg["monitors"]["joshin"]["url"],
            summary="玩具ページの告知監視テンプレート。",
        )
    ]

def monitor_amazon_invite(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not cfg["monitors"]["amazon_invite"]["enabled"]:
        return []
    return [
        make_commerce(
            shop="Amazon",
            title="ポケモンカード 招待リクエスト",
            kind="Amazon招待",
            status="受付中",
            url=cfg["monitors"]["amazon_invite"]["url"],
            summary="Amazon招待リクエストのみ掲載するテンプレート。",
        )
    ]

def monitor_rakuten(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not cfg["monitors"]["rakuten"]["enabled"]:
        return []
    return [
        make_commerce(
            shop="楽天ブックス",
            title="ポケモンカード 予約検索",
            kind="楽天予約",
            status="監視中",
            url=cfg["monitors"]["rakuten"]["url"],
            summary="楽天導線監視テンプレート。",
        )
    ]

def monitor_yahoo(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not cfg["monitors"]["yahoo"]["enabled"]:
        return []
    return [
        make_commerce(
            shop="Yahooショッピング",
            title="ポケモンカード 再販・予約検索",
            kind="Yahoo検索",
            status="監視中",
            url=cfg["monitors"]["yahoo"]["url"],
            summary="Yahoo導線監視テンプレート。",
        )
    ]

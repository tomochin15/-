from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).parent

def load_config():
    path = ROOT / "config.json"
    if not path.exists():
        path = ROOT / "config.example.json"
    return json.loads(path.read_text(encoding="utf-8"))

def send_discord(message: str) -> None:
    cfg = load_config()
    if not cfg["notifications"]["enable_discord"]:
        print("discord disabled")
        return
    webhook = cfg["notifications"]["discord_webhook"]
    if not webhook:
        print("discord webhook missing")
        return
    body = json.dumps({"content": message}).encode("utf-8")
    req = Request(webhook, data=body, headers={"Content-Type": "application/json"})
    with urlopen(req) as res:
        print(res.status)

if __name__ == "__main__":
    send_discord("ポケカ速報ラボ: 更新を検知しました。")

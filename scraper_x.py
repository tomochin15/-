from pathlib import Path
import json

root = Path(__file__).parent
data = root / 'data.json'

# 実運用では各公開ページの情報を取得して data.json を更新します。
# ここではテンプレートとして data.json の存在確認のみ行います。

if data.exists():
    payload = json.loads(data.read_text(encoding='utf-8'))
    data.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print('data.json verified')
else:
    print('data.json not found')

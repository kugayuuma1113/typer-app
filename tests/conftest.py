import os
import sys
from pathlib import Path

# main.py は「読み込まれた瞬間」に環境変数 API_KEY を見に行く。
# テストが main を import するより前に、このファイルが読み込まれるので
# ここでダミーのキーを入れておく（実際の API 呼び出しテストではない限りこれで足りる）。
# 1) 実行ディレクトリに依存せず `from main import ...` を通すため、
#    プロジェクトルートを import パスに追加する。
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 2) API_KEY が未設定でも import 時に落ちないよう、テスト用ダミーを設定する。
os.environ.setdefault("API_KEY", "dummy-key-for-pytest")

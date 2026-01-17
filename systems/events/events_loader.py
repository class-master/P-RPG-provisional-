import json
from pathlib import Path


def load_events(path: str = 'input/events_day3.json') -> dict:
    """Day3 用の会話データを読み込むユーティリティ関数。"""
    event_path = Path(path)
    if not event_path.exists():
        raise FileNotFoundError(f'イベントファイルが見つかりません: {event_path}')

    with event_path.open(encoding='utf-8') as f:
        return json.load(f)

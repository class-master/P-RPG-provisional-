import json
from pathlib import Path


def load_events(path: str = 'input/events_day3.json') -> dict:
    """Day3 逕ｨ縺ｮ莨夊ｩｱ繝・・繧ｿ繧定ｪｭ縺ｿ霎ｼ繧繝ｦ繝ｼ繝・ぅ繝ｪ繝・ぅ髢｢謨ｰ縲・""
    event_path = Path(path)
    if not event_path.exists():
        raise FileNotFoundError(f'繧､繝吶Φ繝医ヵ繧｡繧､繝ｫ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {event_path}')

    with event_path.open(encoding='utf-8') as f:
        return json.load(f)

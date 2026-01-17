# -*- coding: utf-8 -*-
"""
RPG Rustic Master B 逕ｨ繝槭ャ繝励Ο繝ｼ繝繝ｼ・・ivy迚茨ｼ・

蠖ｹ蜑ｲ・・
- CSV 縺ｧ譖ｸ縺九ｌ縺溘ち繧､繝ｫ繝槭ャ繝励ｒ隱ｭ縺ｿ蜿悶ｊ縲∵紛謨ｰ縺ｮ2谺｡蜈・Μ繧ｹ繝医↓螟画鋤縺吶ｋ
- 繧ｿ繧､繝ｫ繧ｻ繝・ヨ逕ｻ蜒擾ｼ・ustic_tileset.png・峨ｒ TILE_SIZE 縺斐→縺ｫ蛻・牡縺励・
  Kivy 縺ｮ TextureRegion 縺ｮ繝ｪ繧ｹ繝医→縺励※霑斐☆

諠ｳ螳夲ｼ・
- 縺薙・繝輔ぃ繧､繝ｫ(map_loader_kivy.py)縺ｨ蜷後§繝輔か繝ｫ繝縺ｫ縲径ssets縲阪ョ繧｣繝ｬ繧ｯ繝医Μ縺後≠繧・
    P-RPG-provisional-/
        map_loader_kivy.py   竊・縺薙・繝輔ぃ繧､繝ｫ
        config.py
        assets/
            maps/
                rustic_map01.csv
                rustic_tileset.png
"""

from __future__ import annotations

import csv
from pathlib import Path

from kivy.core.image import Image as CoreImage
from config import TILE_SIZE  # 繧ｿ繧､繝ｫ1繝槭せ縺ｮ繝斐け繧ｻ繝ｫ繧ｵ繧､繧ｺ・井ｾ・ 32・・


# ----------------------------------------------------------------------
# 繝代せ險ｭ螳夲ｼ壹％縺ｮ繝輔ぃ繧､繝ｫ(map_loader_kivy.py)縺檎ｽｮ縺九ｌ縺ｦ縺・ｋ蝣ｴ謇繧定ｵｷ轤ｹ縺ｫ縺吶ｋ
# ----------------------------------------------------------------------
# BASE_DIR:
#   d:\...\P-RPG-provisional-\map_loader_kivy.py
# 縺ｮ縲訓-RPG-provisional-縲阪ヵ繧ｩ繝ｫ繝繧呈欠縺呎Φ螳・
BASE_DIR: Path = Path(__file__).resolve().parent

# 繝槭ャ繝佑SV 縺ｨ繧ｿ繧､繝ｫ繧ｻ繝・ヨ逕ｻ蜒上∈縺ｮ繝・ヵ繧ｩ繝ｫ繝医ヱ繧ｹ
DEFAULT_TILESET_PATH: Path = (BASE_DIR / "assets/maps/rustic_tileset.png").resolve()

# tileset 繧剃ｽ募ｺｦ繧りｪｭ縺ｿ逶ｴ縺輔↑縺・ｈ縺・↓邁｡譏薙く繝｣繝・す繝･
_tiles_cache = None  # type: ignore[assignment]

# map_loader_kivy.py
def load_map(*args, **kwargs):
    return load_csv_as_tilemap(*args, **kwargs)

# ----------------------------------------------------------------------
# 1. CSV 繝槭ャ繝苓ｪｭ縺ｿ霎ｼ縺ｿ
# ----------------------------------------------------------------------
def load_csv_as_tilemap(path: str):
    """
    CSV 蠖｢蠑上・繝槭ャ繝励ヵ繧｡繧､繝ｫ繧定ｪｭ縺ｿ霎ｼ繧薙〒縲・
    - grid: [ [int, int, ...], [int, int, ...], ... ] 蠖｢蠑上・2谺｡蜈・Μ繧ｹ繝・
    - rows: 陦梧焚
    - cols: 蛻玲焚
    繧定ｿ斐☆縲・

    蠑墓焚:
        path: "assets/maps/rustic_map01.csv" 縺ｮ繧医≧縺ｪ逶ｸ蟇ｾ繝代せ繧呈Φ螳壹・
              窶ｻ BASE_DIR・・縺薙・繝輔ぃ繧､繝ｫ縺ｮ縺ゅｋ繝輔か繝ｫ繝・峨°繧峨・逶ｸ蟇ｾ繝代せ縲・

    萓・
        grid, rows, cols = load_csv_as_tilemap("assets/maps/rustic_map01.csv")
    """
    # 縺薙・繝輔ぃ繧､繝ｫ縺九ｉ隕九◆邨ｶ蟇ｾ繝代せ縺ｫ螟画鋤縺吶ｋ縺薙→縺ｧ縲・
    # 縲後←縺ｮ繝輔か繝ｫ繝縺九ｉ python 繧貞ｮ溯｡後＠縺ｦ繧ゅ榊酔縺伜ｴ謇繧貞盾辣ｧ縺ｧ縺阪ｋ繧医≧縺ｫ縺吶ｋ
    csv_path: Path = (BASE_DIR / path).resolve()

    if not csv_path.exists():
        # 繝・ヰ繝・げ縺励ｄ縺吶＞繧医≧縺ｫ縲∵爾縺励↓陦後▲縺溷ｮ滄圀縺ｮ繝代せ繧ゅΓ繝・そ繝ｼ繧ｸ縺ｫ蜷ｫ繧√ｋ
        raise FileNotFoundError(f"繝槭ャ繝佑SV縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {csv_path}")

    grid: list[list[int]] = []

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            # 遨ｺ陦後・繧ｹ繧ｭ繝・・・亥ｿ・ｦ√↓蠢懊§縺ｦ隱ｿ謨ｴ・・
            if not row:
                continue
            # "0", "1", "2" ... 繧・int 縺ｫ螟画鋤
            grid.append([int(v) for v in row])

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    return grid, rows, cols


# ----------------------------------------------------------------------
# 2. 繧ｿ繧､繝ｫ繧ｻ繝・ヨ逕ｻ蜒上・蛻・牡
# ----------------------------------------------------------------------
def load_tileset_regions(tileset_path: Path | str = DEFAULT_TILESET_PATH):
    """
    繧ｿ繧､繝ｫ繧ｻ繝・ヨ逕ｻ蜒上ｒ TILE_SIZE 縺斐→縺ｫ蛻・牡縺励・
    Kivy 縺ｮ TextureRegion 縺ｮ繝ｪ繧ｹ繝医ｒ霑斐☆縲・

    - 謌ｻ繧雁､縺ｮ繝ｪ繧ｹ繝医・豺ｻ蟄・= CSV 縺ｧ菴ｿ縺・ち繧､繝ｫID・・,1,2,...・峨ｒ諠ｳ螳壹・
    - 逕ｻ蜒上・繧ｰ繝ｪ繝・ラ迥ｶ・亥ｷｦ荳九°繧牙承荳翫∈・峨↓荳ｦ繧薙〒縺・ｋ蜑肴署縲・

    蠑墓焚:
        tileset_path:
            繧ｿ繧､繝ｫ繧ｻ繝・ヨ逕ｻ蜒上∈縺ｮ繝代せ縲・
            逵∫払譎ゅ・ "assets/maps/rustic_tileset.png" 繧剃ｽｿ逕ｨ縲・
    """
    global _tiles_cache

    # 縺吶〒縺ｫ隱ｭ縺ｿ霎ｼ縺ｿ貂医∩縺ｪ繧峨√◎縺ｮ縺ｾ縺ｾ霑斐☆・域ｯ弱ヵ繝ｬ繝ｼ繝繝ｭ繝ｼ繝峨ｒ髦ｲ縺撰ｼ・
    if _tiles_cache is not None:
        return _tiles_cache

    # 繝代せ縺ｮ豁｣隕丞喧・・tr 縺ｧ繧・Path 縺ｧ繧ょ女縺大叙繧後ｋ繧医≧縺ｫ・・
    if isinstance(tileset_path, str):
        tileset_path = (BASE_DIR / tileset_path).resolve()
    else:
        tileset_path = tileset_path.resolve()

    if not tileset_path.exists():
        raise FileNotFoundError(f"繧ｿ繧､繝ｫ繧ｻ繝・ヨ逕ｻ蜒上′隕九▽縺九ｊ縺ｾ縺帙ｓ: {tileset_path}")

    # 逕ｻ蜒剰ｪｭ縺ｿ霎ｼ縺ｿ 竊・texture 繧貞叙蠕・
    img = CoreImage(str(tileset_path))
    texture = img.texture

    tex_w, tex_h = texture.size  # 繝・け繧ｹ繝√Ε蜈ｨ菴薙・繧ｵ繧､繧ｺ・医ヴ繧ｯ繧ｻ繝ｫ・・
    cols = int(tex_w // TILE_SIZE)
    rows = int(tex_h // TILE_SIZE)

    tiles = []

    # Kivy縺ｮ繝・け繧ｹ繝√Ε蠎ｧ讓吶・蟾ｦ荳・0,0)縺悟次轤ｹ縲・
    # 縺薙％縺ｧ縺ｯ縲悟ｷｦ荳九°繧牙承荳翫∈縲崎ｪｭ縺ｿ蜿悶▲縺ｦ ID 繧呈険繧九・
    for row in range(rows):
        for col in range(cols):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            region = texture.get_region(x, y, TILE_SIZE, TILE_SIZE)
            tiles.append(region)

    _tiles_cache = tiles
    return tiles

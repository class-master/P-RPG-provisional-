# -*- coding: utf-8 -*-
"""
RPG Rustic Master B 用マップローダー（Kivy版）

役割：
- CSV で書かれたタイルマップを読み取り、整数の2次元リストに変換する
- タイルセット画像（rustic_tileset.png）を TILE_SIZE ごとに分割し、
  Kivy の TextureRegion のリストとして返す

想定：
- このファイル(map_loader_kivy.py)と同じフォルダに「assets」ディレクトリがある
    P-RPG-provisional-/
        map_loader_kivy.py   ← このファイル
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
from config import TILE_SIZE  # タイル1マスのピクセルサイズ（例: 32）


# ----------------------------------------------------------------------
# パス設定：このファイル(map_loader_kivy.py)が置かれている場所を起点にする
# ----------------------------------------------------------------------
# BASE_DIR:
#   d:\...\P-RPG-provisional-\map_loader_kivy.py
# の「P-RPG-provisional-」フォルダを指す想定
BASE_DIR: Path = Path(__file__).resolve().parent

# マップCSV とタイルセット画像へのデフォルトパス
DEFAULT_TILESET_PATH: Path = (BASE_DIR / "assets/maps/rustic_tileset.png").resolve()

# tileset を何度も読み直さないように簡易キャッシュ
_tiles_cache = None  # type: ignore[assignment]


# ----------------------------------------------------------------------
# 1. CSV マップ読み込み
# ----------------------------------------------------------------------
def load_csv_as_tilemap(path: str):
    """
    CSV 形式のマップファイルを読み込んで、
    - grid: [ [int, int, ...], [int, int, ...], ... ] 形式の2次元リスト
    - rows: 行数
    - cols: 列数
    を返す。

    引数:
        path: "assets/maps/rustic_map01.csv" のような相対パスを想定。
              ※ BASE_DIR（=このファイルのあるフォルダ）からの相対パス。

    例:
        grid, rows, cols = load_csv_as_tilemap("assets/maps/rustic_map01.csv")
    """
    # このファイルから見た絶対パスに変換することで、
    # 「どのフォルダから python を実行しても」同じ場所を参照できるようにする
    csv_path: Path = (BASE_DIR / path).resolve()

    if not csv_path.exists():
        # デバッグしやすいように、探しに行った実際のパスもメッセージに含める
        raise FileNotFoundError(f"マップCSVが見つかりません: {csv_path}")

    grid: list[list[int]] = []

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            # 空行はスキップ（必要に応じて調整）
            if not row:
                continue
            # "0", "1", "2" ... を int に変換
            grid.append([int(v) for v in row])

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    return grid, rows, cols


# ----------------------------------------------------------------------
# 2. タイルセット画像の分割
# ----------------------------------------------------------------------
def load_tileset_regions(tileset_path: Path | str = DEFAULT_TILESET_PATH):
    """
    タイルセット画像を TILE_SIZE ごとに分割し、
    Kivy の TextureRegion のリストを返す。

    - 戻り値のリストの添字 = CSV で使うタイルID（0,1,2,...）を想定。
    - 画像はグリッド状（左下から右上へ）に並んでいる前提。

    引数:
        tileset_path:
            タイルセット画像へのパス。
            省略時は "assets/maps/rustic_tileset.png" を使用。
    """
    global _tiles_cache

    # すでに読み込み済みなら、そのまま返す（毎フレームロードを防ぐ）
    if _tiles_cache is not None:
        return _tiles_cache

    # パスの正規化（str でも Path でも受け取れるように）
    if isinstance(tileset_path, str):
        tileset_path = (BASE_DIR / tileset_path).resolve()
    else:
        tileset_path = tileset_path.resolve()

    if not tileset_path.exists():
        raise FileNotFoundError(f"タイルセット画像が見つかりません: {tileset_path}")

    # 画像読み込み → texture を取得
    img = CoreImage(str(tileset_path))
    texture = img.texture

    tex_w, tex_h = texture.size  # テクスチャ全体のサイズ（ピクセル）
    cols = int(tex_w // TILE_SIZE)
    rows = int(tex_h // TILE_SIZE)

    tiles = []

    # Kivyのテクスチャ座標は左下(0,0)が原点。
    # ここでは「左下から右上へ」読み取って ID を振る。
    for row in range(rows):
        for col in range(cols):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            region = texture.get_region(x, y, TILE_SIZE, TILE_SIZE)
            tiles.append(region)

    _tiles_cache = tiles
    return tiles

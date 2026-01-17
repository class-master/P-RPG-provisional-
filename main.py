# -*- coding: utf-8 -*-
"""
P-RPG provisional - main.py (統合版エントリ)
到達：
- フィールド移動（Day2ベース：衝突あり）
- 看板（Eで読む）
- Eで戦闘に入る（暫定：テストエンカウント）
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate
from kivy.uix.label import Label
from kivy.properties import ListProperty

from config import WIDTH, HEIGHT, TILE_SIZE, MAP_CSV, PLAYER_SPEED, BG

# ✅ 正規：CSVマップ読み込み（load_map は使わない）
from map_loader_kivy import load_csv_as_tilemap, load_tileset_regions

# ✅ 正規：バトル関連（移動後のパス）
from status_day4 import Status
from ui.battle_window import BattleWindow
from systems.battle.battle_engine import player_attack, enemy_attack


# ============================================================
# 衝突判定（Day2ベース）
# ============================================================
def rect_collides(px, py, w, h, grid, solid={1, 2, 3, 4}):
    ts = TILE_SIZE
    min_c = max(0, int(px) // ts)
    max_c = min(len(grid[0]) - 1, int((px + w - 1)) // ts)
    min_r = max(0, int(py) // ts)
    max_r = min(len(grid) - 1, int((py + h - 1)) // ts)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] in solid:
                wx, wy = c * ts, r * ts
                if not (px + w <= wx or wx + ts <= px or py + h <= wy or wy + ts <= py):
                    return True
    return False


class Game(Widget):
    cam = ListProperty([0, 0])

    def __init__(self, root_layout: FloatLayout, **kw):
        super().__init__(**kw)
        self.size = (WIDTH, HEIGHT)
        self.root_layout = root_layout

        # --- map ---
        self.grid, self.rows, self.cols = load_csv_as_tilemap(MAP_CSV)
        self.tiles = load_tileset_regions()
        self.ts = TILE_SIZE
        self.map_w = self.cols * self.ts
        self.map_h = self.rows * self.ts

        # --- player ---
        ts = self.ts
        self.px = ts * 3
        self.py = ts * 3
        self.w = ts - 6
        self.h = ts - 6

        # --- input ---
        self.keys = set()

        # --- HUD / sign ---
        self.sign = (ts * 10, ts * 6, ts, ts)  # x,y,w,h（例）
        self.msg = Label(text="矢印:移動 / E:看板 / B:戦闘テスト", pos=(12, HEIGHT - 28))
        self.add_widget(self.msg)

        # --- battle state ---
        self.mode = "field"  # "field" / "battle"
        self.player_status = Status("ゆうしゃ", max_hp=30, attack=8, defense=2)
        self.enemy_status: Optional[Status] = None

        self.battle_window = BattleWindow()
        self.root_layout.add_widget(self.battle_window)
        self.battle_window.opacity = 0.0  # 非表示

        Window.bind(on_key_down=self._kd, on_key_up=self._ku)
        Clock.schedule_interval(self.update, 1 / 60)

    # -----------------------------
    # key events
    # -----------------------------
    def _kd(self, win, key, scancode, codepoint, modifier):
        self.keys.add(key)
        # 方向キー/文字キー判定用に codepoint も扱えるが、
        # まずは keycode で最低限動かす
        return True

    def _ku(self, win, key, scancode):
        self.keys.discard(key)
        return True

    # -----------------------------
    # battle helpers
    # -----------------------------
    def load_enemy_status(self, enemy_id: str) -> Status:
        # ✅ data/input に移動した想定
        data_path = Path("data/input/enemies_day4.json")
        data = json.loads(data_path.read_text(encoding="utf-8"))
        info = data[enemy_id]
        return Status(
            name=info["name"],
            max_hp=info["max_hp"],
            attack=info["attack"],
            defense=info.get("defense", 0),
        )

    def start_battle(self, enemy_id: str) -> None:
        self.enemy_status = self.load_enemy_status(enemy_id)
        self.mode = "battle"
        self.battle_window.update_status(self.player_status, self.enemy_status)
        self.battle_window.show_message(f"{self.enemy_status.name} があらわれた！")
        self.battle_window.opacity = 1.0

    def end_battle(self, message: str) -> None:
        self.battle_window.show_message(message)
        self.battle_window.opacity = 0.0
        self.enemy_status = None
        self.mode = "field"

    def handle_battle_key(self, keycode: int) -> None:
        # Aキー＝97（環境差あり）。ここは “Bで攻撃” にして安定させるのも手。
        # まずは keycode 98 = 'b' で攻撃にしています。
        if keycode != 98:
            return
        if self.enemy_status is None:
            return

        # 1) player attack
        dmg = player_attack(self.player_status, self.enemy_status)
        self.battle_window.update_status(self.player_status, self.enemy_status)
        self.battle_window.show_message(
            f"{self.player_status.name}のこうげき！ {self.enemy_status.name}に {dmg} ダメージ！"
        )
        if self.enemy_status.is_dead():
            self.end_battle(f"{self.enemy_status.name}を たおした！")
            return

        # 2) enemy attack
        dmg2 = enemy_attack(self.enemy_status, self.player_status)
        self.battle_window.update_status(self.player_status, self.enemy_status)
        self.battle_window.show_message(
            f"{self.enemy_status.name}のこうげき！ {self.player_status.name}は {dmg2} ダメージ！"
        )
        if self.player_status.is_dead():
            # レベル上げ無し方針：敗北時は全回復で即戻す
            self.player_status.hp = self.player_status.max_hp
            self.end_battle("やられてしまった……（HP全回復で帰還）")

    # -----------------------------
    # update loop
    # -----------------------------
    def update(self, dt):
        if self.mode == "battle":
            # バトル中は操作をバトルに固定
            # 'b' で攻撃（keycode=98）
            if 98 in self.keys:
                # 押しっぱなし連打になるので、1回処理したら消す
                self.keys.discard(98)
                self.handle_battle_key(98)
            return

        # --- field mode ---
        left, right, down, up = 276, 275, 273, 274
        ekey = 101  # 'e'
        bkey = 98   # 'b'（戦闘テスト用）

        ax = (1 if right in self.keys else 0) - (1 if left in self.keys else 0)
        ay = (1 if down in self.keys else 0) - (1 if up in self.keys else 0)

        spd = PLAYER_SPEED
        nx = self.px + ax * spd
        if not rect_collides(nx, self.py, self.w, self.h, self.grid):
            self.px = nx
        ny = self.py + ay * spd
        if not rect_collides(self.px, ny, self.w, self.h, self.grid):
            self.py = ny

        # 看板
        sx, sy, sw, sh = self.sign
        is_sign = not (self.px + self.w <= sx or sx + sw <= self.px or self.py + self.h <= sy or sy + sh <= self.py)
        if ekey in self.keys and is_sign:
            self.msg.text = "【看板】ようこそ！ E=看板 / B=戦闘テスト"
        else:
            self.msg.text = "矢印:移動 / E:看板 / B:戦闘テスト"

        # 戦闘テスト（いったんキーで入れる）
        if bkey in self.keys:
            self.keys.discard(bkey)
            # enemies_day4.json に存在するIDへ（例：slime）
            self.start_battle("slime")

        # camera
        self.cam[0] = max(0, self.px - self.width / 2)
        self.cam[1] = max(0, self.py - self.height / 2)

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(*BG)
            Rectangle(pos=self.pos, size=self.size)

            PushMatrix()
            Translate(-self.cam[0], -self.cam[1], 0)

            ts = self.ts
            for r, row in enumerate(self.grid):
                for c, tid in enumerate(row):
                    Rectangle(texture=self.tiles[tid], pos=(c * ts, r * ts), size=(ts, ts))

            # 看板（見える化）
            Color(0.8, 0.6, 0.25, 1)
            Rectangle(pos=(self.sign[0], self.sign[1]), size=(self.sign[2], self.sign[3]))

            # プレイヤー
            Color(0.35, 0.67, 1, 1)
            Rectangle(pos=(self.px, self.py), size=(self.w, self.h))

            PopMatrix()


class MainApp(App):
    def build(self):
        root = FloatLayout(size=(WIDTH, HEIGHT))
        game = Game(root_layout=root)
        root.add_widget(game)
        return root


if __name__ == "__main__":
    MainApp().run()

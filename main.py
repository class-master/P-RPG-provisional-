# -*- coding: utf-8 -*-
"""
P-RPG provisional - main.py (邨ｱ蜷育沿繧ｨ繝ｳ繝医Μ)
蛻ｰ驕費ｼ・
- 繝輔ぅ繝ｼ繝ｫ繝臥ｧｻ蜍包ｼ・ay2繝吶・繧ｹ・夊｡晉ｪ√≠繧奇ｼ・
- 逵区攸・・縺ｧ隱ｭ繧・・
- E縺ｧ謌ｦ髣倥↓蜈･繧具ｼ域圻螳夲ｼ壹ユ繧ｹ繝医お繝ｳ繧ｫ繧ｦ繝ｳ繝茨ｼ・
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

# 笨・豁｣隕擾ｼ咾SV繝槭ャ繝苓ｪｭ縺ｿ霎ｼ縺ｿ・・oad_map 縺ｯ菴ｿ繧上↑縺・ｼ・
from field.map_loader_kivy import load_csv_as_tilemap, load_tileset_regions

# 笨・豁｣隕擾ｼ壹ヰ繝医Ν髢｢騾｣・育ｧｻ蜍募ｾ後・繝代せ・・
from status_day4 import Status
from ui.battle_window import BattleWindow
from systems.battle.battle_engine import player_attack, enemy_attack


# ============================================================
# 陦晉ｪ∝愛螳夲ｼ・ay2繝吶・繧ｹ・・
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
        self.sign = (ts * 10, ts * 6, ts, ts)  # x,y,w,h・井ｾ具ｼ・
        self.msg = Label(text="遏｢蜊ｰ:遘ｻ蜍・/ E:逵区攸 / B:謌ｦ髣倥ユ繧ｹ繝・, pos=(12, HEIGHT - 28))
        self.add_widget(self.msg)

        # --- battle state ---
        self.mode = "field"  # "field" / "battle"
        self.player_status = Status("繧・≧縺励ｃ", max_hp=30, attack=8, defense=2)
        self.enemy_status: Optional[Status] = None

        self.battle_window = BattleWindow()
        self.root_layout.add_widget(self.battle_window)
        self.battle_window.opacity = 0.0  # 髱櫁｡ｨ遉ｺ

        Window.bind(on_key_down=self._kd, on_key_up=self._ku)
        Clock.schedule_interval(self.update, 1 / 60)

    # -----------------------------
    # key events
    # -----------------------------
    def _kd(self, win, key, scancode, codepoint, modifier):
        self.keys.add(key)
        # 譁ｹ蜷代く繝ｼ/譁・ｭ励く繝ｼ蛻､螳夂畑縺ｫ codepoint 繧よ桶縺医ｋ縺後・
        # 縺ｾ縺壹・ keycode 縺ｧ譛菴朱剞蜍輔°縺・
        return True

    def _ku(self, win, key, scancode):
        self.keys.discard(key)
        return True

    # -----------------------------
    # battle helpers
    # -----------------------------
    def load_enemy_status(self, enemy_id: str) -> Status:
        # 笨・data/input 縺ｫ遘ｻ蜍輔＠縺滓Φ螳・
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
        self.battle_window.show_message(f"{self.enemy_status.name} 縺後≠繧峨ｏ繧後◆・・)
        self.battle_window.opacity = 1.0

    def end_battle(self, message: str) -> None:
        self.battle_window.show_message(message)
        self.battle_window.opacity = 0.0
        self.enemy_status = None
        self.mode = "field"

    def handle_battle_key(self, keycode: int) -> None:
        # A繧ｭ繝ｼ・・7・育腸蠅・ｷｮ縺ゅｊ・峨ゅ％縺薙・ 窶廝縺ｧ謾ｻ謦・・縺ｫ縺励※螳牙ｮ壹＆縺帙ｋ縺ｮ繧よ焔縲・
        # 縺ｾ縺壹・ keycode 98 = 'b' 縺ｧ謾ｻ謦・↓縺励※縺・∪縺吶・
        if keycode != 98:
            return
        if self.enemy_status is None:
            return

        # 1) player attack
        dmg = player_attack(self.player_status, self.enemy_status)
        self.battle_window.update_status(self.player_status, self.enemy_status)
        self.battle_window.show_message(
            f"{self.player_status.name}縺ｮ縺薙≧縺偵″・・{self.enemy_status.name}縺ｫ {dmg} 繝繝｡繝ｼ繧ｸ・・
        )
        if self.enemy_status.is_dead():
            self.end_battle(f"{self.enemy_status.name}繧・縺溘♀縺励◆・・)
            return

        # 2) enemy attack
        dmg2 = enemy_attack(self.enemy_status, self.player_status)
        self.battle_window.update_status(self.player_status, self.enemy_status)
        self.battle_window.show_message(
            f"{self.enemy_status.name}縺ｮ縺薙≧縺偵″・・{self.player_status.name}縺ｯ {dmg2} 繝繝｡繝ｼ繧ｸ・・
        )
        if self.player_status.is_dead():
            # 繝ｬ繝吶Ν荳翫￡辟｡縺玲婿驥晢ｼ壽風蛹玲凾縺ｯ蜈ｨ蝗槫ｾｩ縺ｧ蜊ｳ謌ｻ縺・
            self.player_status.hp = self.player_status.max_hp
            self.end_battle("繧・ｉ繧後※縺励∪縺｣縺溪ｦ窶ｦ・・P蜈ｨ蝗槫ｾｩ縺ｧ蟶ｰ驍・ｼ・)

    # -----------------------------
    # update loop
    # -----------------------------
    def update(self, dt):
        if self.mode == "battle":
            # 繝舌ヨ繝ｫ荳ｭ縺ｯ謫堺ｽ懊ｒ繝舌ヨ繝ｫ縺ｫ蝗ｺ螳・
            # 'b' 縺ｧ謾ｻ謦・ｼ・eycode=98・・
            if 98 in self.keys:
                # 謚ｼ縺励▲縺ｱ縺ｪ縺鈴｣謇薙↓縺ｪ繧九・縺ｧ縲・蝗槫・逅・＠縺溘ｉ豸医☆
                self.keys.discard(98)
                self.handle_battle_key(98)
            return

        # --- field mode ---
        left, right, down, up = 276, 275, 273, 274
        ekey = 101  # 'e'
        bkey = 98   # 'b'・域姶髣倥ユ繧ｹ繝育畑・・

        ax = (1 if right in self.keys else 0) - (1 if left in self.keys else 0)
        ay = (1 if down in self.keys else 0) - (1 if up in self.keys else 0)

        spd = PLAYER_SPEED
        nx = self.px + ax * spd
        if not rect_collides(nx, self.py, self.w, self.h, self.grid):
            self.px = nx
        ny = self.py + ay * spd
        if not rect_collides(self.px, ny, self.w, self.h, self.grid):
            self.py = ny

        # 逵区攸
        sx, sy, sw, sh = self.sign
        is_sign = not (self.px + self.w <= sx or sx + sw <= self.px or self.py + self.h <= sy or sy + sh <= self.py)
        if ekey in self.keys and is_sign:
            self.msg.text = "縲千恚譚ｿ縲代ｈ縺・％縺晢ｼ・E=逵区攸 / B=謌ｦ髣倥ユ繧ｹ繝・
        else:
            self.msg.text = "遏｢蜊ｰ:遘ｻ蜍・/ E:逵区攸 / B:謌ｦ髣倥ユ繧ｹ繝・

        # 謌ｦ髣倥ユ繧ｹ繝茨ｼ医＞縺｣縺溘ｓ繧ｭ繝ｼ縺ｧ蜈･繧後ｋ・・
        if bkey in self.keys:
            self.keys.discard(bkey)
            # enemies_day4.json 縺ｫ蟄伜惠縺吶ｋID縺ｸ・井ｾ具ｼ嘖lime・・
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

            # 逵区攸・郁ｦ九∴繧句喧・・
            Color(0.8, 0.6, 0.25, 1)
            Rectangle(pos=(self.sign[0], self.sign[1]), size=(self.sign[2], self.sign[3]))

            # 繝励Ξ繧､繝､繝ｼ
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

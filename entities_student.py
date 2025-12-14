# -*- coding: utf-8 -*-
"""
RPG Rustic Master B — Day2（生徒用）Kivy
到達：壁衝突／Eで看板を読む（会話ダミー）
発展：走る(Shift)／スタミナ／慣性／摩擦／宝箱／鍵と扉

ポイント（Kivy版の“pygame風”分割）
- Player : 入力→速度→移動（衝突は軸分離）
- Camera : プレイヤー追従（offset = cam）
- HUD    : 画面固定（Windowサイズに追従して、絶対に見える）
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate
from kivy.uix.label import Label
from kivy.properties import ListProperty

from config import WIDTH, HEIGHT, TILE_SIZE, MAP_CSV, PLAYER_SPEED, BG
from map_loader_kivy import load_csv_as_tilemap, load_tileset_regions

# ✅ HUDが画面外に飛ぶ事故を防止（WidgetサイズではなくWindowサイズを固定）
Window.size = (WIDTH, HEIGHT)

# --- 追加要素（configに無い前提で、ここで“講義用に”定数化） ---
RUN_MULTIPLIER = 1.8       # Shiftで走る倍率
STAMINA_MAX = 100.0        # スタミナ最大
STAMINA_RUN_COST = 0.9     # 走行中の減少（毎フレーム）
STAMINA_RECOVER = 0.6      # 非走行時の回復（毎フレーム）
PLAYER_ACCEL = 0.25        # 慣性の追従率（0〜1）
PLAYER_FRICTION = 0.88     # 摩擦（0〜1、1に近いほど滑る）

SOLID_TILES = {1, 2, 3, 4} # 壁扱いタイルID（必要に応じて調整）


def rect_collides(px, py, w, h, grid, solid=SOLID_TILES):
    """
    タイル衝突（矩形 vs 壁タイル）判定
    - px,py,w,h は “ワールド座標（ピクセル）”
    - grid は CSVのタイルID配列（grid[row][col]）
    """
    ts = TILE_SIZE
    cols = len(grid[0])
    rows = len(grid)

    # プレイヤー矩形が占めるタイル範囲だけ調べる（高速）
    min_c = max(0, int(px) // ts)
    max_c = min(cols - 1, int((px + w - 1)) // ts)
    min_r = max(0, int(py) // ts)
    max_r = min(rows - 1, int((py + h - 1)) // ts)

    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] in solid:
                wx, wy = c * ts, r * ts
                # AABB（矩形）の重なり
                if not (px + w <= wx or wx + ts <= px or py + h <= wy or wy + ts <= py):
                    return True
    return False


def aabb_intersect(ax, ay, aw, ah, bx, by, bw, bh):
    """矩形どうし（AABB）の重なり判定"""
    if ax + aw <= bx: return False
    if ax >= bx + bw: return False
    if ay + ah <= by: return False
    if ay >= by + bh: return False
    return True


class Player:
    """
    Player（pygame風の責務）
    - handle_input : 入力→目標速度→慣性＆摩擦
    - move_and_collide : 移動（軸分離で衝突）
    """
    def __init__(self, x, y, w, h):
        self.px = float(x)
        self.py = float(y)
        self.w = float(w)
        self.h = float(h)

        # 速度（慣性）
        self.vx = 0.0
        self.vy = 0.0

        # スタミナ
        self.stamina = STAMINA_MAX

    def handle_input(self, keys, mods):
        """
        keys: 押されているキーコード集合
        mods: 修飾キー集合（'shift'等） ※環境差があるのでShiftキーコードも併用
        """
        left = 276; right = 275; up = 273; down = 274
        ax = (1 if right in keys else 0) - (1 if left in keys else 0)
        ay = (1 if down  in keys else 0) - (1 if up   in keys else 0)

        # 斜め移動を速くしない（正規化）
        if ax != 0 and ay != 0:
            ax *= 0.7071
            ay *= 0.7071

        # Shift走り（modifierが取れない環境の保険：303/304）
        shift_keys = {303, 304}
        running = ('shift' in mods) or any(k in keys for k in shift_keys)

        # 走り＆スタミナ
        speed = PLAYER_SPEED
        if running and self.stamina > 0:
            speed *= RUN_MULTIPLIER
            self.stamina = max(0.0, self.stamina - STAMINA_RUN_COST)
        else:
            self.stamina = min(STAMINA_MAX, self.stamina + STAMINA_RECOVER)

        # 慣性（目標速度に“なめらかに”追従）
        target_vx = ax * speed
        target_vy = ay * speed
        self.vx = self.vx * (1.0 - PLAYER_ACCEL) + target_vx * PLAYER_ACCEL
        self.vy = self.vy * (1.0 - PLAYER_ACCEL) + target_vy * PLAYER_ACCEL

        # 摩擦（入力が切れた時に少しずつ止まる）
        self.vx *= PLAYER_FRICTION
        self.vy *= PLAYER_FRICTION

    def move_and_collide(self, grid):
        """
        軸分離（超重要）
        - Xを動かす→衝突したら巻き戻す
        - Yを動かす→衝突したら巻き戻す
        こうすると“角で引っかかってガタガタ”が減ります
        """
        # X
        nx = self.px + self.vx
        if not rect_collides(nx, self.py, self.w, self.h, grid):
            self.px = nx
        else:
            self.vx = 0.0  # 壁に当たったらX速度を止める（わかりやすい）

        # Y
        ny = self.py + self.vy
        if not rect_collides(self.px, ny, self.w, self.h, grid):
            self.py = ny
        else:
            self.vy = 0.0

    def rect(self):
        return (self.px, self.py, self.w, self.h)


class Camera:
    """プレイヤー中心追従カメラ（offset = cam）"""
    def __init__(self, screen_w, screen_h, map_w, map_h):
        self.cam = [0.0, 0.0]
        self.sw = screen_w
        self.sh = screen_h
        self.mw = map_w
        self.mh = map_h

    def follow(self, px, py):
        cx = px - self.sw / 2
        cy = py - self.sh / 2
        cam_max_x = max(0.0, self.mw - self.sw)
        cam_max_y = max(0.0, self.mh - self.sh)
        self.cam[0] = max(0.0, min(cx, cam_max_x))
        self.cam[1] = max(0.0, min(cy, cam_max_y))


class HUD:
    """
    画面固定HUD
    - “看板の文字”は、看板の上に描くのではなくHUDに出す（RPG定番）
    - Windowサイズが変わっても絶対に見えるように追従させる
    """
    def __init__(self):
        self.label = Label(text="", pos=(12, Window.height - 28))
        Window.bind(size=self._on_resize)

    def _on_resize(self, win, size):
        self.label.pos = (12, win.height - 28)

    def set_text(self, s: str):
        self.label.text = s


class Game(Widget):
    cam = ListProperty([0, 0])

    def __init__(self, **kw):
        super().__init__(**kw)
        self.size = (WIDTH, HEIGHT)

        # マップ読み込み
        self.grid, self.rows, self.cols = load_csv_as_tilemap(MAP_CSV)
        self.tiles = load_tileset_regions()

        # マップサイズ（ピクセル）
        self.map_w = self.cols * TILE_SIZE
        self.map_h = self.rows * TILE_SIZE

        # Player / Camera / HUD
        ts = TILE_SIZE
        self.player = Player(ts * 3, ts * 3, ts - 6, ts - 6)
        self.camera = Camera(WIDTH, HEIGHT, self.map_w, self.map_h)

        self.hud = HUD()
        self.add_widget(self.hud.label)

        # 入力状態
        self.keys = set()
        self.mods = set()
        Window.bind(on_key_down=self._kd, on_key_up=self._ku)

        # 看板（オレンジ四角）＝“当たり判定の目印”
        self.sign = (ts * 10, ts * 6, ts, ts)
        self.sign_text = "ようこそ、Rustic村へ！"
        self.sign_hold = 0.0  # 表示保持（チラつき防止）

        Clock.schedule_interval(self.update, 1 / 60)

    def _kd(self, win, key, scancode, codepoint, modifier):
        self.keys.add(key)
        self.mods = set(modifier) if modifier else set()
        return True

    def _ku(self, win, key, *a):
        self.keys.discard(key)
        return True

    def update(self, dt):
        # 入力→移動
        self.player.handle_input(self.keys, self.mods)
        self.player.move_and_collide(self.grid)

        # 看板：Eで読む（接触中のみ）
        ekey = ord('e')  # 101
        px, py, pw, ph = self.player.rect()
        sx, sy, sw, sh = self.sign
        touching = aabb_intersect(px, py, pw, ph, sx, sy, sw, sh)

        self.sign_hold = max(0.0, self.sign_hold - dt)

        if (ekey in self.keys) and touching:
            self.sign_hold = 0.20
            hud_text = f"矢印で移動 / Shiftで走る / E: 看板\n【看板】{self.sign_text}"
        else:
            if self.sign_hold > 0.0:
                hud_text = f"矢印で移動 / Shiftで走る / E: 看板\n【看板】{self.sign_text}"
            else:
                hud_text = "矢印で移動 / Shiftで走る / E: 看板"

        self.hud.set_text(hud_text)

        # カメラ追従（プレイヤー中心）
        self.camera.follow(px, py)
        self.cam[0], self.cam[1] = self.camera.cam[0], self.camera.cam[1]

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # 背景
            Color(*BG)
            Rectangle(pos=self.pos, size=self.size)

            # ワールド描画（カメラ適用）
            PushMatrix()
            Translate(-self.cam[0], -self.cam[1], 0)

            ts = TILE_SIZE
            for r, row in enumerate(self.grid):
                for c, tid in enumerate(row):
                    Rectangle(texture=self.tiles[tid], pos=(c * ts, r * ts), size=(ts, ts))

            # 看板（オレンジ）
            Color(0.8, 0.6, 0.25, 1)
            Rectangle(pos=(self.sign[0], self.sign[1]), size=(self.sign[2], self.sign[3]))

            # プレイヤ
            Color(0.35, 0.67, 1, 1)
            px, py, pw, ph = self.player.rect()
            Rectangle(pos=(px, py), size=(pw, ph))

            PopMatrix()
class NPC:
    def __init__(self, name, x, y, event_id):
        # name: NPCの名前（例: "村人A"）
        # x, y: マップ上のタイル座標
        # event_id: 会話イベントのID（例: "first_npc"）
        self.name = name
        self.x = x
        self.y = y
        self.event_id = event_id
villager1 = NPC("村人１",12,5,event_id ="1")

       

class Day2(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    Day2().run()

def is_adjacent(player, npc):
    # プレイヤーがNPCの上下左右どこか1マス隣にいるかどうかを返す。
    dx = abs(player.x - npc.x)
    dy = abs(player.y - npc.y)
    return dx + dy == 1
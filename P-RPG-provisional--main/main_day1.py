# -*- coding: utf-8 -*-
"""
RPG Rustic Master B — Day1（講師用）Kivy
到達：タイル描画＋移動（すり抜けOK）
解答例：Shift走る／ミニマップHUD／看板の当たり判定（AABB）
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


class Game(Widget):
    """
    Day1の考え方（超だいじ）
    - update(): 入力→移動→カメラ→draw() の順で「ゲームの状態」を更新
    - draw()  : canvas を一旦消して、今の状態を描き直す
    - Day1は衝突なし（すり抜けOK）なので、移動は「座標を足すだけ」でOK
    """

    cam = ListProperty([0, 0])  # [cam_x, cam_y] = カメラ左下（ワールド座標）

    def __init__(self, **kw):
        super().__init__(**kw)

        # ---------------------------------------------
        # 0) 画面サイズ（Widgetの大きさ）を確定する
        # ---------------------------------------------
        self.size = (WIDTH, HEIGHT)

        # ---------------------------------------------
        # 1) マップCSV（2次元のタイルID配列）を読み込む
        # ---------------------------------------------
        self.grid, self.rows, self.cols = load_csv_as_tilemap(MAP_CSV)

        # ---------------------------------------------
        # 2) タイルセット（tid -> texture）を読み込む
        # ---------------------------------------------
        self.tiles = load_tileset_regions()

        # ---------------------------------------------
        # 3) マップ全体のピクセルサイズ（カメラの制限に使う）
        # ---------------------------------------------
        self.ts = TILE_SIZE
        self.map_w = self.cols * self.ts
        self.map_h = self.rows * self.ts

        # ---------------------------------------------
        # 4) プレイヤー初期値
        # ---------------------------------------------
        # px, py : プレイヤー左下座標（ワールド座標）
        # w, h   : プレイヤー矩形サイズ（Day1では当たり判定しないが、サイズは持つ）
        self.px = self.ts * 2
        self.py = self.ts * 2
        self.w = self.ts - 6
        self.h = self.ts - 6

        # ---------------------------------------------
        # 5) 入力（押されているキー）管理
        # ---------------------------------------------
        # self.keys に keycode を入れて「押しっぱなし」を実現する
        # これにより、update() 側で「今押されてる方向」を毎フレーム読める
        self.keys = set()

        # Shift判定を安定させたいので、modifier（修飾キー）も覚えておく
        # Kivyの on_key_down には modifier のリストが来る（例: ['shift']）
        self.mods = set()

        Window.bind(on_key_down=self._kd, on_key_up=self._ku)

        # ---------------------------------------------
        # 6) HUD（画面固定のテキスト）
        # ---------------------------------------------
        self.hud = Label(
            text="矢印で移動 / Shiftで走る / 看板に触れると表示 / ミニマップ右上",
            pos=(12, HEIGHT - 28)
        )
        self.add_widget(self.hud)

        # ---------------------------------------------
        # 7) 看板（解答例）
        # ---------------------------------------------
        # Day1なので「タイル座標で置く」→ 分かりやすい
        # AABB当たり判定用に、pos/size をワールド座標（ピクセル）で保持する
        #
        # ここでは「見える化」も兼ねて draw() で看板を薄く描画します
        self.signs = [
            {
                "pos": (self.ts * 6, self.ts * 3),
                "size": (self.ts, self.ts),
                "text": "看板：ようこそ。Day1は『描画と移動』ができれば合格なのです。",
            },
            {
                "pos": (self.ts * 10, self.ts * 8),
                "size": (self.ts, self.ts),
                "text": "看板：Shiftで走る例を入れてあります（講師用の解答例）。",
            },
        ]
        self.sign_text = ""   # 今触れている看板メッセージ（無ければ空）
        self.sign_hold = 0.0  # HUDがチラつかないように少し保持する

        # ---------------------------------------------
        # 8) ミニマップ（解答例：雛形）
        # ---------------------------------------------
        # ミニマップの大きさ（画面内の矩形）
        self.mm_w = 220
        self.mm_h = 220
        self.mm_margin = 12  # 画面端からの余白
        # 右上に配置する（ミニマップ左下座標）
        self.mm_x = WIDTH - self.mm_w - self.mm_margin
        self.mm_y = HEIGHT - self.mm_h - self.mm_margin

        # ---------------------------------------------
        # 9) ループ開始
        # ---------------------------------------------
        Clock.schedule_interval(self.update, 1 / 60)

    # ------------------------------------------------------------
    # キー入力：押した/離した を状態として保持する
    # ------------------------------------------------------------
    def _kd(self, win, key, scancode, codepoint, modifier):
        """
        key      : キーコード（矢印キーなら 273〜276 など）
        modifier : 修飾キーのリスト（例: ['shift']）
        """
        self.keys.add(key)
        # modifier は毎回 “その時点で押されている修飾キー” が来ることが多いので
        # set に入れて保持しておく（Shift走りの判定に使う）
        self.mods = set(modifier) if modifier else set()
        return True

    def _ku(self, win, key, scancode):
        self.keys.discard(key)
        # key_up では modifier が来ないので、Shiftを離した瞬間に set が残ることがある
        # そのため update() 側で「Shiftキーコードも候補として見る」ことで安全側に倒す
        return True

    # ------------------------------------------------------------
    # update：移動・カメラ・看板判定・描画
    # ------------------------------------------------------------
    def update(self, dt):
        # ----------------------------
        # 1) 方向入力
        # ----------------------------
        left = 276
        right = 275
        up = 273
        down = 274

        ax = (1 if right in self.keys else 0) - (1 if left in self.keys else 0)
        ay = (1 if down in self.keys else 0) - (1 if up in self.keys else 0)

        # ----------------------------
        # 2) Shift走り（解答例）
        # ----------------------------
        # modifier が取れる環境では 'shift' が入る
        # 取れない/不安定な環境では、Shiftキーコード(303/304)も候補にする
        shift_keys = {303, 304}  # 環境により差あり（右/左Shift）
        is_shift = ('shift' in self.mods) or any(k in self.keys for k in shift_keys)

        spd = PLAYER_SPEED
        if is_shift:
            # 走り倍率：授業では 1.5〜2.0 の範囲が体感しやすい
            spd = PLAYER_SPEED * 1.8

        # ----------------------------
        # 3) 移動（Day1は衝突なし＝すり抜けOK）
        # ----------------------------
        self.px += ax * spd
        self.py += ay * spd

        # マップ外へ出ると迷子になるので “最低限” の制限（講師用は入れておくと安心）
        # clamp：値を min〜max に収める、という意味
        self.px = max(0, min(self.px, self.map_w - self.w))
        self.py = max(0, min(self.py, self.map_h - self.h))

        # ----------------------------
        # 4) カメラ（プレイヤー中心追従）＋ マップ端で制限
        # ----------------------------
        # 「プレイヤーが画面の真ん中に来る」ように cam を決める
        cx = self.px - self.width / 2
        cy = self.py - self.height / 2

        # カメラがマップ外を映さないように制限
        cam_max_x = max(0, self.map_w - self.width)
        cam_max_y = max(0, self.map_h - self.height)

        self.cam[0] = max(0, min(cx, cam_max_x))
        self.cam[1] = max(0, min(cy, cam_max_y))

        # ----------------------------
        # 5) 看板当たり判定（解答例：AABB）
        # ----------------------------
        self._check_sign(dt)

        # ----------------------------
        # 6) 描画
        # ----------------------------
        self.draw()

    # ------------------------------------------------------------
    # 看板当たり判定（AABB）
    # ------------------------------------------------------------
    def _check_sign(self, dt):
        """
        Day1なので、あくまで “簡易” な看板判定。
        - プレイヤー矩形と看板矩形が重なったらメッセージ表示
        - 触れていない時は少しだけ表示を保持（HUDがチラつくのを防ぐ）
        """
        # 保持時間を減らす
        self.sign_hold = max(0.0, self.sign_hold - dt)

        # プレイヤー矩形（左下 + サイズ）
        px, py, pw, ph = self.px, self.py, self.w, self.h

        hit_text = ""

        for s in self.signs:
            sx, sy = s["pos"]
            sw, sh = s["size"]

            if self._aabb_intersect(px, py, pw, ph, sx, sy, sw, sh):
                hit_text = s["text"]
                break

        if hit_text:
            self.sign_text = hit_text
            self.sign_hold = 0.20  # 0.2秒保持（お好みで）
        else:
            # 触れていない時は、保持が切れたら消す
            if self.sign_hold <= 0.0:
                self.sign_text = ""

        # HUD更新（毎フレーム書き換えてOK）
        base = "矢印で移動 / Shiftで走る / 看板に触れると表示 / ミニマップ右上"
        if self.sign_text:
            self.hud.text = f"{base}\n【看板】{self.sign_text}"
        else:
            self.hud.text = base

    @staticmethod
    def _aabb_intersect(ax, ay, aw, ah, bx, by, bw, bh):
        """
        AABB（軸に平行な四角形）同士の重なり判定。
        - 2つの矩形が “重なっている” なら True
        - まったく重なっていないなら False

        コツ：
        - 「離れている条件」を否定すると、判定が書きやすい
        """
        # a の右端が b の左端より左 → 離れている
        if ax + aw <= bx:
            return False
        # a の左端が b の右端より右 → 離れている
        if ax >= bx + bw:
            return False
        # a の上端が b の下端より下 → 離れている
        if ay + ah <= by:
            return False
        # a の下端が b の上端より上 → 離れている
        if ay >= by + bh:
            return False

        return True

    # ------------------------------------------------------------
    # draw：今の状態を描く
    # ------------------------------------------------------------
    def draw(self):
        self.canvas.clear()

        with self.canvas:
            # 0) 背景
            Color(*BG)
            Rectangle(pos=self.pos, size=self.size)

            # 1) ここから “ワールド描画” 開始（カメラでずらす）
            PushMatrix()
            Translate(-self.cam[0], -self.cam[1], 0)

            # 2) タイル描画
            ts = self.ts
            for r, row in enumerate(self.grid):
                for c, tid in enumerate(row):
                    # tid に対応する texture が無いと落ちるので、講師用では安全側に
                    tex = self.tiles.get(tid) if hasattr(self.tiles, "get") else self.tiles[tid]
                    if tex is None:
                        continue
                    Rectangle(texture=tex, pos=(c * ts, r * ts), size=(ts, ts))

            # 3) 看板を薄く描画（“そこにある”と分かるように）
            Color(1, 1, 1, 0.25)
            for s in self.signs:
                sx, sy = s["pos"]
                sw, sh = s["size"]
                Rectangle(pos=(sx, sy), size=(sw, sh))

            # 4) プレイヤー描画
            Color(0.35, 0.67, 1, 1)
            Rectangle(pos=(self.px, self.py), size=(self.w, self.h))

            # 5) ワールド描画ここまで
            PopMatrix()

            # 6) 画面固定：ミニマップ（解答例）
            self._draw_minimap()

    # ------------------------------------------------------------
    # ミニマップ（画面固定の簡易版）
    # ------------------------------------------------------------
    def _draw_minimap(self):
        """
        Day1のミニマップは “雛形” で十分です。
        - マップ全体：枠（半透明）
        - プレイヤー：点（小さな四角）
        - カメラ範囲：枠（任意。ここでは入れてあります）
        """
        # 1) ミニマップの枠
        Color(0, 0, 0, 0.45)
        Rectangle(pos=(self.mm_x, self.mm_y), size=(self.mm_w, self.mm_h))

        Color(1, 1, 1, 0.25)
        Rectangle(pos=(self.mm_x, self.mm_y), size=(self.mm_w, self.mm_h))

        # 2) ワールド座標 -> ミニマップ座標への変換
        #    比率：px/map_w を mm_w に写す、という考え方
        #    （map_w が 0 になることは通常ないが、念のため max(1, map_w)）
        mw = max(1, self.map_w)
        mh = max(1, self.map_h)

        # プレイヤー中心をミニマップへ
        pcx = self.px + self.w / 2
        pcy = self.py + self.h / 2

        mx = self.mm_x + (pcx / mw) * self.mm_w
        my = self.mm_y + (pcy / mh) * self.mm_h

        # 3) カメラ範囲の枠（ミニマップ上）
        # カメラの左下と、画面サイズ分をミニマップへ縮小して描く
        cx = self.mm_x + (self.cam[0] / mw) * self.mm_w
        cy = self.mm_y + (self.cam[1] / mh) * self.mm_h
        cw = (self.width / mw) * self.mm_w
        ch = (self.height / mh) * self.mm_h

        Color(1, 1, 1, 0.35)
        Rectangle(pos=(cx, cy), size=(cw, ch))

        # 4) プレイヤー点
        Color(0.35, 0.67, 1, 0.95)
        Rectangle(pos=(mx - 3, my - 3), size=(6, 6))


class Day1(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    Day1().run()

# -*- coding: utf-8 -*-
"""
RPG Rustic Master B — Day2（生徒用）Kivy
仕様：
- 看板に触れている間はメッセージ表示
- 離れたら消える
- 再び触れたときはもう一度Eキーを押す必要あり
- メッセージは2種類のみ
- 日本語フォント対応（GenShinGothic-Regular.ttf）
"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from config import WIDTH, HEIGHT, TILE_SIZE, MAP_CSV, PLAYER_SPEED, BG
from map_loader_kivy import load_csv_as_tilemap, load_tileset_regions

def rect_collides(px, py, w, h, grid, solid={1,2,3,4}):
    ts = TILE_SIZE
    min_c = max(0, int(px)//ts)
    max_c = min(len(grid[0])-1, int((px+w-1))//ts)
    min_r = max(0, int(py)//ts)
    max_r = min(len(grid)-1, int((py+h-1))//ts)
    for r in range(min_r, max_r+1):
        for c in range(min_c, max_c+1):
            if grid[r][c] in solid:
                wx, wy = c*ts, r*ts
                if not (px+w<=wx or wx+ts<=px or py+h<=wy or wy+ts<=py):
                    return True
    return False

class Game(Widget):
    cam = ListProperty([0,0])
    def __init__(self, **kw):
        super().__init__(**kw)
        self.size = (WIDTH, HEIGHT)
        self.grid, self.rows, self.cols = load_csv_as_tilemap(MAP_CSV)
        self.tiles = load_tileset_regions()
        ts = TILE_SIZE
        self.px = ts*3; self.py = ts*3; self.w = ts-6; self.h = ts-6
        self.keys = set()
        self.sign = (ts*10, ts*6, ts, ts)  # 看板の位置
        self.read_sign = False             # 看板を読んだかどうかのフラグ

        # HUDレイヤー（画面固定）
        self.hud = FloatLayout(size=self.size)
        self.msg = Label(
            text="矢印キーで移動, E: 看板を読む",
            size_hint=(None, None),
            size=(WIDTH, 50),          # 横幅を画面幅に、縦を50ピクセルに設定
            pos_hint={'x':0, 'top':1},
            font_size=20,
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle",
            text_size=(WIDTH, None),   # テキストを横幅に合わせて描画
            font_name="GenShinGothic-Regular.ttf"  # ← 日本語フォント指定
        )
        self.hud.add_widget(self.msg)
        self.add_widget(self.hud)

        Window.bind(on_key_down=self._kd, on_key_up=self._ku)
        Clock.schedule_interval(self.update, 1/60)
        self.cam = [0, 0]

    def _kd(self, win, key, scancode, codepoint, modifiers):
        if codepoint:
            self.keys.add(codepoint.lower())  # 'e'
        else:
            self.keys.add(key)
        return True

    def _ku(self, win, key, scancode, codepoint=None, modifiers=None):
        if key == 101:
            self.keys.discard('e')
        else:
            self.keys.discard(key)
        return True

    def update(self, dt):
        # 移動処理
        left=276; right=275; up=273; down=274
        ax=(1 if right in self.keys else 0)-(1 if left in self.keys else 0)
        ay=(1 if up  in self.keys else 0)-(1 if down   in self.keys else 0)
        spd=PLAYER_SPEED
        nx=self.px+ax*spd
        if not rect_collides(nx, self.py, self.w, self.h, self.grid): self.px=nx
        ny=self.py+ay*spd
        if not rect_collides(self.px, ny, self.w, self.h, self.grid): self.py=ny

        # 看板判定
        sx,sy,sw,sh=self.sign
        touching_sign = not (self.px+self.w<=sx or sx+sw<=self.px or self.py+self.h<=sy or sy+sh<=self.py)

        # Eキーを押した瞬間にフラグを立てる
        if 'e' in self.keys and touching_sign:
            self.read_sign = True

        # 看板から離れたらフラグをリセット
        if not touching_sign:
            self.read_sign = False

        # 表示制御（2種類のみ）
        if self.read_sign and touching_sign:
            self.msg.text = "【看板】ようこそ、Rustic村へ！"
        else:
            self.msg.text = "矢印キーで移動, E: 看板を読む"

        self.cam[0]=max(0,self.px-self.width/2)
        self.cam[1]=max(0,self.py-self.height/2)
        self.draw()

    def draw(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*BG); Rectangle(pos=self.pos,size=self.size)
            PushMatrix(); Translate(-self.cam[0],-self.cam[1],0)
            ts=TILE_SIZE
            for r,row in enumerate(self.grid):
                for c,tid in enumerate(row):
                    Rectangle(texture=self.tiles[tid], pos=(c*ts,r*ts), size=(ts,ts))
            # 看板
            Color(0.8,0.6,0.25,1)
            Rectangle(pos=(self.sign[0],self.sign[1]), size=(self.sign[2],self.sign[3]))
            # プレイヤー
            Color(0.35,0.67,1,1)
            Rectangle(pos=(self.px,self.py), size=(self.w,self.h))
            PopMatrix()

class Day2(App):
    def build(self): return Game()

if __name__=="__main__":
    Day2().run()

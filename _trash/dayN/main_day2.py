# -*- coding: utf-8 -*-
"""
RPG Rustic Master B 窶・Day2・育函蠕堤畑・卯ivy
蛻ｰ驕費ｼ壼｣∬｡晉ｪ・ｼ拾縺ｧ逵区攸繧定ｪｭ繧・井ｼ夊ｩｱ繝繝溘・・・
逋ｺ螻包ｼ夐嵯縺ｨ謇会ｼ・lag縺ｧ髢矩哩・会ｼ丞ｮ晉ｮｱ・亥叙蠕励〒HUD・・
"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate
from kivy.uix.label import Label
from kivy.properties import ListProperty
from config import WIDTH, HEIGHT, TILE_SIZE, MAP_CSV, PLAYER_SPEED, BG
from field.map_loader_kivy import load_csv_as_tilemap, load_tileset_regions

def rect_collides(px, py, w, h, grid, solid={1,2,3,4}): # 竊・solid蠑墓焚縺ｨ螢√ち繧､繝ｫID繧定ｿｽ蜉
    ts = TILE_SIZE
    min_c = max(0, int(px)//ts)
    max_c = min(len(grid[0])-1, int((px+w-1))//ts)
    min_r = max(0, int(py)//ts)
    max_r = min(len(grid)-1, int((py+h-1))//ts)
    for r in range(min_r, max_r+1):
        for c in range(min_c, max_c+1):
            if grid[r][c] in solid: # 竊・繧ｿ繧､繝ｫID縺悟｣√Μ繧ｹ繝医↓縺ゅｋ縺九メ繧ｧ繝・け
                wx, wy = c*ts, r*ts
                if not (px+w<=wx or wx+ts<=px or py+h<=wy or wy+ts<=py):
                    return True
    return False

class Game(Widget):
    cam=ListProperty([0,0])

    def __init__(self, **kw):
        super().__init__(**kw)
        self.size=(WIDTH,HEIGHT)
        self.grid,self.rows,self.cols = load_csv_as_tilemap(MAP_CSV)
        self.tiles = load_tileset_regions()
        ts=TILE_SIZE
        self.px=ts*3; self.py=ts*3; self.w=ts-6; self.h=ts-6
        self.keys=set()
        self.sign = (ts*10, ts*6, ts, ts)  # 逵区攸縺ｮ菴咲ｽｮ繧定ｨｭ螳・
        self.msg = Label(text="遏｢蜊ｰ繧ｭ繝ｼ縺ｧ遘ｻ蜍・ E: 逵区攸繧定ｪｭ繧", pos=(12,HEIGHT-28)) # HUD繝｡繝・そ繝ｼ繧ｸ繧定ｨｭ螳・
        self.add_widget(self.msg)

        Window.bind(on_key_down=self._kd, on_key_up=self._ku)
        Clock.schedule_interval(self.update, 1/60)
        
        self.cam = [0, 0]
    def _kd(self,win,key,*a):
        self.keys.add(key); return True

    def _ku(self,win,key,*a):
        self.keys.discard(key); return True

    def update(self,dt):
        left=276; right=275; up=274; down=273; ekey=101
        ax=(1 if right in self.keys else 0)-(1 if left in self.keys else 0)
        ay=(1 if down  in self.keys else 0)-(1 if up   in self.keys else 0)
        spd=PLAYER_SPEED
        nx=self.px+ax*spd
        if not rect_collides(nx, self.py, self.w, self.h, self.grid): self.px=nx
        ny=self.py+ay*spd
        if not rect_collides(self.px, ny, self.w, self.h, self.grid): self.py=ny
        
        # 逵区攸
        sx,sy,sw,sh=self.sign
        is_colliding_with_sign = not (self.px+self.w<=sx or sx+sw<=self.px or self.py+self.h<=sy or sy+sh<=self.py)
        if ekey in self.keys and is_colliding_with_sign:
            self.msg.text="縲千恚譚ｿ縲代ｈ縺・％縺昴ヽustic譚代∈・・
        else:
            self.msg.text="遏｢蜊ｰ繧ｭ繝ｼ縺ｧ遘ｻ蜍・ E: 逵区攸繧定ｪｭ繧"
        
        self.cam[0]=max(0,self.px-self.width/2); self.cam[1]=max(0,self.py-self.height/2)
        self.draw()
        
    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(*BG); Rectangle(pos=self.pos,size=self.size)
            PushMatrix(); Translate(-self.cam[0],-self.cam[1],0)
            ts=TILE_SIZE
            for r,row in enumerate(self.grid):
                for c,tid in enumerate(row):
                    Rectangle(texture=self.tiles[tid], pos=(c*ts,r*ts), size=(ts,ts))
            # 逵区攸
            Color(0.8,0.6,0.25,1); Rectangle(pos=(self.sign[0],self.sign[1]), size=(self.sign[2],self.sign[3]))
            # 繝励Ξ繧､繝､
            Color(0.35,0.67,1,1); Rectangle(pos=(self.px,self.py), size=(self.w,self.h))
            PopMatrix()
class Day2(App):
    def build(self): return Game()
if __name__=="__main__": Day2().run()

#逵区攸縺ｮ譁・ｭ励・陦ｨ遉ｺ縺後〒縺阪↑縺九▲縺溘

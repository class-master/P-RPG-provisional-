# -*- coding: utf-8 -*-
"""
RPG Rustic Master B 窶・Day2・育函蠕堤畑・卯ivy
蛻ｰ驕費ｼ壼｣∬｡晉ｪ・ｼ拾縺ｧ逵区攸繧定ｪｭ繧・井ｼ夊ｩｱ繝繝溘・・・
逋ｺ螻包ｼ夊ｵｰ繧・Shift)・上せ繧ｿ繝溘リ・乗・諤ｧ・乗束謫ｦ・丞ｮ晉ｮｱ・城嵯縺ｨ謇・

繝昴う繝ｳ繝茨ｼ・ivy迚医・窶徘ygame鬚ｨ窶晏・蜑ｲ・・
- Player : 蜈･蜉帚・騾溷ｺｦ竊堤ｧｻ蜍包ｼ郁｡晉ｪ√・霆ｸ蛻・屬・・
- Camera : 繝励Ξ繧､繝､繝ｼ霑ｽ蠕難ｼ・ffset = cam・・
- HUD    : 逕ｻ髱｢蝗ｺ螳夲ｼ・indow繧ｵ繧､繧ｺ縺ｫ霑ｽ蠕薙＠縺ｦ縲∫ｵｶ蟇ｾ縺ｫ隕九∴繧具ｼ・
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

# 笨・HUD縺檎判髱｢螟悶↓鬟帙・莠区腐繧帝亟豁｢・・idget繧ｵ繧､繧ｺ縺ｧ縺ｯ縺ｪ縺集indow繧ｵ繧､繧ｺ繧貞崋螳夲ｼ・
Window.size = (WIDTH, HEIGHT)

# --- 霑ｽ蜉隕∫ｴ・・onfig縺ｫ辟｡縺・燕謠舌〒縲√％縺薙〒窶懆ｬ帷ｾｩ逕ｨ縺ｫ窶晏ｮ壽焚蛹厄ｼ・---
RUN_MULTIPLIER = 1.8       # Shift縺ｧ襍ｰ繧句咲紫
STAMINA_MAX = 100.0        # 繧ｹ繧ｿ繝溘リ譛螟ｧ
STAMINA_RUN_COST = 0.9     # 襍ｰ陦御ｸｭ縺ｮ貂帛ｰ托ｼ域ｯ弱ヵ繝ｬ繝ｼ繝・・
STAMINA_RECOVER = 0.6      # 髱櫁ｵｰ陦梧凾縺ｮ蝗槫ｾｩ・域ｯ弱ヵ繝ｬ繝ｼ繝・・
PLAYER_ACCEL = 0.25        # 諷｣諤ｧ縺ｮ霑ｽ蠕鍋紫・・縲・・・
PLAYER_FRICTION = 0.88     # 鞫ｩ謫ｦ・・縲・縲・縺ｫ霑代＞縺ｻ縺ｩ貊代ｋ・・

SOLID_TILES = {1, 2, 3, 4} # 螢∵桶縺・ち繧､繝ｫID・亥ｿ・ｦ√↓蠢懊§縺ｦ隱ｿ謨ｴ・・

def rect_collides(px, py, w, h, grid, solid=SOLID_TILES):
    """
    繧ｿ繧､繝ｫ陦晉ｪ・ｼ育洸蠖｢ vs 螢√ち繧､繝ｫ・牙愛螳・
    - px,py,w,h 縺ｯ 窶懊Ρ繝ｼ繝ｫ繝牙ｺｧ讓呻ｼ医ヴ繧ｯ繧ｻ繝ｫ・俄・
    - grid 縺ｯ CSV縺ｮ繧ｿ繧､繝ｫID驟榊・・・rid[row][col]・・
    """
    ts = TILE_SIZE
    cols = len(grid[0])
    rows = len(grid)

    # 繝励Ξ繧､繝､繝ｼ遏ｩ蠖｢縺悟頃繧√ｋ繧ｿ繧､繝ｫ遽・峇縺縺題ｪｿ縺ｹ繧具ｼ磯ｫ倬滂ｼ・
    min_c = max(0, int(px) // ts)
    max_c = min(cols - 1, int((px + w - 1)) // ts)
    min_r = max(0, int(py) // ts)
    max_r = min(rows - 1, int((py + h - 1)) // ts)

    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] in solid:
                wx, wy = c * ts, r * ts
                # AABB・育洸蠖｢・峨・驥阪↑繧・
                if not (px + w <= wx or wx + ts <= px or py + h <= wy or wy + ts <= py):
                    return True
    return False

def aabb_intersect(ax, ay, aw, ah, bx, by, bw, bh):
    """遏ｩ蠖｢縺ｩ縺・＠・・ABB・峨・驥阪↑繧雁愛螳・""
    if ax + aw <= bx: return False
    if ax >= bx + bw: return False
    if ay + ah <= by: return False
    if ay >= by + bh: return False
    return True

class Player:
    """
    Player・・ygame鬚ｨ縺ｮ雋ｬ蜍呻ｼ・
    - handle_input : 蜈･蜉帚・逶ｮ讓咎溷ｺｦ竊呈・諤ｧ・・束謫ｦ
    - move_and_collide : 遘ｻ蜍包ｼ郁ｻｸ蛻・屬縺ｧ陦晉ｪ・ｼ・
    """
    def __init__(self, x, y, w, h):
        self.px = float(x)
        self.py = float(y)
        self.w = float(w)
        self.h = float(h)

        # 騾溷ｺｦ・域・諤ｧ・・
        self.vx = 0.0
        self.vy = 0.0

        # 繧ｹ繧ｿ繝溘リ
        self.stamina = STAMINA_MAX

    def handle_input(self, keys, mods):
        """
        keys: 謚ｼ縺輔ｌ縺ｦ縺・ｋ繧ｭ繝ｼ繧ｳ繝ｼ繝蛾寔蜷・
        mods: 菫ｮ鬟ｾ繧ｭ繝ｼ髮・粋・・shift'遲会ｼ・窶ｻ迺ｰ蠅・ｷｮ縺後≠繧九・縺ｧShift繧ｭ繝ｼ繧ｳ繝ｼ繝峨ｂ菴ｵ逕ｨ
        """
        left = 276; right = 275; up = 273; down = 274
        ax = (1 if right in keys else 0) - (1 if left in keys else 0)
        ay = (1 if down  in keys else 0) - (1 if up   in keys else 0)

        # 譁懊ａ遘ｻ蜍輔ｒ騾溘￥縺励↑縺・ｼ域ｭ｣隕丞喧・・
        if ax != 0 and ay != 0:
            ax *= 0.7071
            ay *= 0.7071

        # Shift襍ｰ繧奇ｼ・odifier縺悟叙繧後↑縺・腸蠅・・菫晞匱・・03/304・・
        shift_keys = {303, 304}
        running = ('shift' in mods) or any(k in keys for k in shift_keys)

        # 襍ｰ繧奇ｼ・せ繧ｿ繝溘リ
        speed = PLAYER_SPEED
        if running and self.stamina > 0:
            speed *= RUN_MULTIPLIER
            self.stamina = max(0.0, self.stamina - STAMINA_RUN_COST)
        else:
            self.stamina = min(STAMINA_MAX, self.stamina + STAMINA_RECOVER)

        # 諷｣諤ｧ・育岼讓咎溷ｺｦ縺ｫ窶懊↑繧√ｉ縺九↓窶晁ｿｽ蠕難ｼ・
        target_vx = ax * speed
        target_vy = ay * speed
        self.vx = self.vx * (1.0 - PLAYER_ACCEL) + target_vx * PLAYER_ACCEL
        self.vy = self.vy * (1.0 - PLAYER_ACCEL) + target_vy * PLAYER_ACCEL

        # 鞫ｩ謫ｦ・亥・蜉帙′蛻・ｌ縺滓凾縺ｫ蟆代＠縺壹▽豁｢縺ｾ繧具ｼ・
        self.vx *= PLAYER_FRICTION
        self.vy *= PLAYER_FRICTION

    def move_and_collide(self, grid):
        """
        霆ｸ蛻・屬・郁ｶ・㍾隕・ｼ・
        - X繧貞虚縺九☆竊定｡晉ｪ√＠縺溘ｉ蟾ｻ縺肴綾縺・
        - Y繧貞虚縺九☆竊定｡晉ｪ√＠縺溘ｉ蟾ｻ縺肴綾縺・
        縺薙≧縺吶ｋ縺ｨ窶懆ｧ偵〒蠑輔▲縺九°縺｣縺ｦ繧ｬ繧ｿ繧ｬ繧ｿ窶昴′貂帙ｊ縺ｾ縺・
        """
        # X
        nx = self.px + self.vx
        if not rect_collides(nx, self.py, self.w, self.h, grid):
            self.px = nx
        else:
            self.vx = 0.0  # 螢√↓蠖薙◆縺｣縺溘ｉX騾溷ｺｦ繧呈ｭ｢繧√ｋ・医ｏ縺九ｊ繧・☆縺・ｼ・

        # Y
        ny = self.py + self.vy
        if not rect_collides(self.px, ny, self.w, self.h, grid):
            self.py = ny
        else:
            self.vy = 0.0

    def rect(self):
        return (self.px, self.py, self.w, self.h)


class Camera:
    """繝励Ξ繧､繝､繝ｼ荳ｭ蠢・ｿｽ蠕薙き繝｡繝ｩ・・ffset = cam・・""
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
    逕ｻ髱｢蝗ｺ螳唏UD
    - 窶懃恚譚ｿ縺ｮ譁・ｭ冷昴・縲∫恚譚ｿ縺ｮ荳翫↓謠上￥縺ｮ縺ｧ縺ｯ縺ｪ縺秋UD縺ｫ蜃ｺ縺呻ｼ・PG螳夂分・・
    - Window繧ｵ繧､繧ｺ縺悟､峨ｏ縺｣縺ｦ繧らｵｶ蟇ｾ縺ｫ隕九∴繧九ｈ縺・↓霑ｽ蠕薙＆縺帙ｋ
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

        # 繝槭ャ繝苓ｪｭ縺ｿ霎ｼ縺ｿ
        self.grid, self.rows, self.cols = load_csv_as_tilemap(MAP_CSV)
        self.tiles = load_tileset_regions()

        # 繝槭ャ繝励し繧､繧ｺ・医ヴ繧ｯ繧ｻ繝ｫ・・
        self.map_w = self.cols * TILE_SIZE
        self.map_h = self.rows * TILE_SIZE

        # Player / Camera / HUD
        ts = TILE_SIZE
        self.player = Player(ts * 3, ts * 3, ts - 6, ts - 6)
        self.camera = Camera(WIDTH, HEIGHT, self.map_w, self.map_h)

        self.hud = HUD()
        self.add_widget(self.hud.label)

        # 蜈･蜉帷憾諷・
        self.keys = set()
        self.mods = set()
        Window.bind(on_key_down=self._kd, on_key_up=self._ku)

        # 逵区攸・医が繝ｬ繝ｳ繧ｸ蝗幄ｧ抵ｼ会ｼ昶懷ｽ薙◆繧雁愛螳壹・逶ｮ蜊ｰ窶・
        self.sign = (ts * 10, ts * 6, ts, ts)
        self.sign_text = "繧医≧縺薙◎縲ヽustic譚代∈・・
        self.sign_hold = 0.0  # 陦ｨ遉ｺ菫晄戟・医メ繝ｩ縺､縺埼亟豁｢・・

        Clock.schedule_interval(self.update, 1 / 60)

    def _kd(self, win, key, scancode, codepoint, modifier):
        self.keys.add(key)
        self.mods = set(modifier) if modifier else set()
        return True

    def _ku(self, win, key, *a):
        self.keys.discard(key)
        return True

    def update(self, dt):
        # 蜈･蜉帚・遘ｻ蜍・
        self.player.handle_input(self.keys, self.mods)
        self.player.move_and_collide(self.grid)

        # 逵区攸・哘縺ｧ隱ｭ繧・域磁隗ｦ荳ｭ縺ｮ縺ｿ・・
        ekey = ord('e')  # 101
        px, py, pw, ph = self.player.rect()
        sx, sy, sw, sh = self.sign
        touching = aabb_intersect(px, py, pw, ph, sx, sy, sw, sh)

        self.sign_hold = max(0.0, self.sign_hold - dt)

        if (ekey in self.keys) and touching:
            self.sign_hold = 0.20
            hud_text = f"遏｢蜊ｰ縺ｧ遘ｻ蜍・/ Shift縺ｧ襍ｰ繧・/ E: 逵区攸\n縲千恚譚ｿ縲捜self.sign_text}"
        else:
            if self.sign_hold > 0.0:
                hud_text = f"遏｢蜊ｰ縺ｧ遘ｻ蜍・/ Shift縺ｧ襍ｰ繧・/ E: 逵区攸\n縲千恚譚ｿ縲捜self.sign_text}"
            else:
                hud_text = "遏｢蜊ｰ縺ｧ遘ｻ蜍・/ Shift縺ｧ襍ｰ繧・/ E: 逵区攸"

        self.hud.set_text(hud_text)

        # 繧ｫ繝｡繝ｩ霑ｽ蠕難ｼ医・繝ｬ繧､繝､繝ｼ荳ｭ蠢・ｼ・
        self.camera.follow(px, py)
        self.cam[0], self.cam[1] = self.camera.cam[0], self.camera.cam[1]

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # 閭梧勹
            Color(*BG)
            Rectangle(pos=self.pos, size=self.size)

            # 繝ｯ繝ｼ繝ｫ繝画緒逕ｻ・医き繝｡繝ｩ驕ｩ逕ｨ・・
            PushMatrix()
            Translate(-self.cam[0], -self.cam[1], 0)

            ts = TILE_SIZE
            for r, row in enumerate(self.grid):
                for c, tid in enumerate(row):
                    Rectangle(texture=self.tiles[tid], pos=(c * ts, r * ts), size=(ts, ts))

            # 逵区攸・医が繝ｬ繝ｳ繧ｸ・・
            Color(0.8, 0.6, 0.25, 1)
            Rectangle(pos=(self.sign[0], self.sign[1]), size=(self.sign[2], self.sign[3]))

            # 繝励Ξ繧､繝､
            Color(0.35, 0.67, 1, 1)
            px, py, pw, ph = self.player.rect()
            Rectangle(pos=(px, py), size=(pw, ph))

            PopMatrix()
class NPC:
    def __init__(self, name, x, y, event_id):
        # name: NPC縺ｮ蜷榊燕・井ｾ・ "譚台ｺｺA"・・
        # x, y: 繝槭ャ繝嶺ｸ翫・繧ｿ繧､繝ｫ蠎ｧ讓・
        # event_id: 莨夊ｩｱ繧､繝吶Φ繝医・ID・井ｾ・ "first_npc"・・
        self.name = name
        self.x = x
        self.y = y
        self.event_id = event_id
villager1 = NPC("譚台ｺｺ・・,12,5,event_id ="1")


class Day2(App):
    def build(self):
        return Game()


def is_adjacent(player, npc):
    # 繝励Ξ繧､繝､繝ｼ縺君PC縺ｮ荳贋ｸ句ｷｦ蜿ｳ縺ｩ縺薙°1繝槭せ髫｣縺ｫ縺・ｋ縺九←縺・°繧定ｿ斐☆縲・
    dx = abs(player.x - npc.x)
    dy = abs(player.y - npc.y)
    return dx + dy == 1

if __name__ == "__main__":
    Day2().run()

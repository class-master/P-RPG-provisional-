# -*- coding: utf-8 -*-
"""
RPG Rustic Master B 窶・Day1・郁ｬ帛ｸｫ逕ｨ・卯ivy
蛻ｰ驕費ｼ壹ち繧､繝ｫ謠冗判・狗ｧｻ蜍包ｼ医☆繧頑栢縺前K・・
隗｣遲比ｾ具ｼ售hift襍ｰ繧具ｼ上Α繝九・繝・・HUD・冗恚譚ｿ縺ｮ蠖薙◆繧雁愛螳夲ｼ・ABB・・
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


class Game(Widget):
    """
    Day1縺ｮ閠・∴譁ｹ・郁ｶ・□縺・§・・
    - update(): 蜈･蜉帚・遘ｻ蜍補・繧ｫ繝｡繝ｩ竊壇raw() 縺ｮ鬆・〒縲後ご繝ｼ繝縺ｮ迥ｶ諷九阪ｒ譖ｴ譁ｰ
    - draw()  : canvas 繧剃ｸ譌ｦ豸医＠縺ｦ縲∽ｻ翫・迥ｶ諷九ｒ謠上″逶ｴ縺・
    - Day1縺ｯ陦晉ｪ√↑縺暦ｼ医☆繧頑栢縺前K・峨↑縺ｮ縺ｧ縲∫ｧｻ蜍輔・縲悟ｺｧ讓吶ｒ雜ｳ縺吶□縺代阪〒OK
    """

    cam = ListProperty([0, 0])  # [cam_x, cam_y] = 繧ｫ繝｡繝ｩ蟾ｦ荳具ｼ医Ρ繝ｼ繝ｫ繝牙ｺｧ讓呻ｼ・

    def __init__(self, **kw):
        super().__init__(**kw)

        # ---------------------------------------------
        # 0) 逕ｻ髱｢繧ｵ繧､繧ｺ・・idget縺ｮ螟ｧ縺阪＆・峨ｒ遒ｺ螳壹☆繧・
        # ---------------------------------------------
        self.size = (WIDTH, HEIGHT)

        # ---------------------------------------------
        # 1) 繝槭ャ繝佑SV・・谺｡蜈・・繧ｿ繧､繝ｫID驟榊・・峨ｒ隱ｭ縺ｿ霎ｼ繧
        # ---------------------------------------------
        self.grid, self.rows, self.cols = load_csv_as_tilemap(MAP_CSV)

        # ---------------------------------------------
        # 2) 繧ｿ繧､繝ｫ繧ｻ繝・ヨ・・id -> texture・峨ｒ隱ｭ縺ｿ霎ｼ繧
        # ---------------------------------------------
        self.tiles = load_tileset_regions()

        # ---------------------------------------------
        # 3) 繝槭ャ繝怜・菴薙・繝斐け繧ｻ繝ｫ繧ｵ繧､繧ｺ・医き繝｡繝ｩ縺ｮ蛻ｶ髯舌↓菴ｿ縺・ｼ・
        # ---------------------------------------------
        self.ts = TILE_SIZE
        self.map_w = self.cols * self.ts
        self.map_h = self.rows * self.ts

        # ---------------------------------------------
        # 4) 繝励Ξ繧､繝､繝ｼ蛻晄悄蛟､
        # ---------------------------------------------
        # px, py : 繝励Ξ繧､繝､繝ｼ蟾ｦ荳句ｺｧ讓呻ｼ医Ρ繝ｼ繝ｫ繝牙ｺｧ讓呻ｼ・
        # w, h   : 繝励Ξ繧､繝､繝ｼ遏ｩ蠖｢繧ｵ繧､繧ｺ・・ay1縺ｧ縺ｯ蠖薙◆繧雁愛螳壹＠縺ｪ縺・′縲√し繧､繧ｺ縺ｯ謖√▽・・
        self.px = self.ts * 2
        self.py = self.ts * 2
        self.w = self.ts - 6
        self.h = self.ts - 6

        # ---------------------------------------------
        # 5) 蜈･蜉幢ｼ域款縺輔ｌ縺ｦ縺・ｋ繧ｭ繝ｼ・臥ｮ｡逅・
        # ---------------------------------------------
        # self.keys 縺ｫ keycode 繧貞・繧後※縲梧款縺励▲縺ｱ縺ｪ縺励阪ｒ螳溽樟縺吶ｋ
        # 縺薙ｌ縺ｫ繧医ｊ縲「pdate() 蛛ｴ縺ｧ縲御ｻ頑款縺輔ｌ縺ｦ繧区婿蜷代阪ｒ豈弱ヵ繝ｬ繝ｼ繝隱ｭ繧√ｋ
        self.keys = set()

        # Shift蛻､螳壹ｒ螳牙ｮ壹＆縺帙◆縺・・縺ｧ縲［odifier・井ｿｮ鬟ｾ繧ｭ繝ｼ・峨ｂ隕壹∴縺ｦ縺翫￥
        # Kivy縺ｮ on_key_down 縺ｫ縺ｯ modifier 縺ｮ繝ｪ繧ｹ繝医′譚･繧具ｼ井ｾ・ ['shift']・・
        self.mods = set()

        Window.bind(on_key_down=self._kd, on_key_up=self._ku)

        # ---------------------------------------------
        # 6) HUD・育判髱｢蝗ｺ螳壹・繝・く繧ｹ繝茨ｼ・
        # ---------------------------------------------
        self.hud = Label(
            text="遏｢蜊ｰ縺ｧ遘ｻ蜍・/ Shift縺ｧ襍ｰ繧・/ 逵区攸縺ｫ隗ｦ繧後ｋ縺ｨ陦ｨ遉ｺ / 繝溘ル繝槭ャ繝怜承荳・,
            pos=(12, HEIGHT - 28)
        )
        self.add_widget(self.hud)

        # ---------------------------------------------
        # 7) 逵区攸・郁ｧ｣遲比ｾ具ｼ・
        # ---------------------------------------------
        # Day1縺ｪ縺ｮ縺ｧ縲後ち繧､繝ｫ蠎ｧ讓吶〒鄂ｮ縺上坂・ 蛻・°繧翫ｄ縺吶＞
        # AABB蠖薙◆繧雁愛螳夂畑縺ｫ縲｝os/size 繧偵Ρ繝ｼ繝ｫ繝牙ｺｧ讓呻ｼ医ヴ繧ｯ繧ｻ繝ｫ・峨〒菫晄戟縺吶ｋ
        #
        # 縺薙％縺ｧ縺ｯ縲瑚ｦ九∴繧句喧縲阪ｂ蜈ｼ縺ｭ縺ｦ draw() 縺ｧ逵区攸繧定埋縺乗緒逕ｻ縺励∪縺・
        self.signs = [
            {
                "pos": (self.ts * 6, self.ts * 3),
                "size": (self.ts, self.ts),
                "text": "逵区攸・壹ｈ縺・％縺昴・ay1縺ｯ縲取緒逕ｻ縺ｨ遘ｻ蜍輔上′縺ｧ縺阪ｌ縺ｰ蜷域ｼ縺ｪ縺ｮ縺ｧ縺吶・,
            },
            {
                "pos": (self.ts * 10, self.ts * 8),
                "size": (self.ts, self.ts),
                "text": "逵区攸・售hift縺ｧ襍ｰ繧倶ｾ九ｒ蜈･繧後※縺ゅｊ縺ｾ縺呻ｼ郁ｬ帛ｸｫ逕ｨ縺ｮ隗｣遲比ｾ具ｼ峨・,
            },
        ]
        self.sign_text = ""   # 莉願ｧｦ繧後※縺・ｋ逵区攸繝｡繝・そ繝ｼ繧ｸ・育┌縺代ｌ縺ｰ遨ｺ・・
        self.sign_hold = 0.0  # HUD縺後メ繝ｩ縺､縺九↑縺・ｈ縺・↓蟆代＠菫晄戟縺吶ｋ

        # ---------------------------------------------
        # 8) 繝溘ル繝槭ャ繝暦ｼ郁ｧ｣遲比ｾ具ｼ夐屁蠖｢・・
        # ---------------------------------------------
        # 繝溘ル繝槭ャ繝励・螟ｧ縺阪＆・育判髱｢蜀・・遏ｩ蠖｢・・
        self.mm_w = 220
        self.mm_h = 220
        self.mm_margin = 12  # 逕ｻ髱｢遶ｯ縺九ｉ縺ｮ菴咏區
        # 蜿ｳ荳翫↓驟咲ｽｮ縺吶ｋ・医Α繝九・繝・・蟾ｦ荳句ｺｧ讓呻ｼ・
        self.mm_x = WIDTH - self.mm_w - self.mm_margin
        self.mm_y = HEIGHT - self.mm_h - self.mm_margin

        # ---------------------------------------------
        # 9) 繝ｫ繝ｼ繝鈴幕蟋・
        # ---------------------------------------------
        Clock.schedule_interval(self.update, 1 / 60)

    # ------------------------------------------------------------
    # 繧ｭ繝ｼ蜈･蜉幢ｼ壽款縺励◆/髮｢縺励◆ 繧堤憾諷九→縺励※菫晄戟縺吶ｋ
    # ------------------------------------------------------------
    def _kd(self, win, key, scancode, codepoint, modifier):
        """
        key      : 繧ｭ繝ｼ繧ｳ繝ｼ繝会ｼ育泙蜊ｰ繧ｭ繝ｼ縺ｪ繧・273縲・76 縺ｪ縺ｩ・・
        modifier : 菫ｮ鬟ｾ繧ｭ繝ｼ縺ｮ繝ｪ繧ｹ繝茨ｼ井ｾ・ ['shift']・・
        """
        self.keys.add(key)
        # modifier 縺ｯ豈主屓 窶懊◎縺ｮ譎らせ縺ｧ謚ｼ縺輔ｌ縺ｦ縺・ｋ菫ｮ鬟ｾ繧ｭ繝ｼ窶・縺梧擂繧九％縺ｨ縺悟､壹＞縺ｮ縺ｧ
        # set 縺ｫ蜈･繧後※菫晄戟縺励※縺翫￥・・hift襍ｰ繧翫・蛻､螳壹↓菴ｿ縺・ｼ・
        self.mods = set(modifier) if modifier else set()
        return True

    def _ku(self, win, key, scancode):
        self.keys.discard(key)
        # key_up 縺ｧ縺ｯ modifier 縺梧擂縺ｪ縺・・縺ｧ縲ヾhift繧帝屬縺励◆迸ｬ髢薙↓ set 縺梧ｮ九ｋ縺薙→縺後≠繧・
        # 縺昴・縺溘ａ update() 蛛ｴ縺ｧ縲郡hift繧ｭ繝ｼ繧ｳ繝ｼ繝峨ｂ蛟呵｣懊→縺励※隕九ｋ縲阪％縺ｨ縺ｧ螳牙・蛛ｴ縺ｫ蛟偵☆
        return True

    # ------------------------------------------------------------
    # update・夂ｧｻ蜍輔・繧ｫ繝｡繝ｩ繝ｻ逵区攸蛻､螳壹・謠冗判
    # ------------------------------------------------------------
    def update(self, dt):
        # ----------------------------
        # 1) 譁ｹ蜷大・蜉・
        # ----------------------------
        left = 276
        right = 275
        up = 273
        down = 274

        ax = (1 if right in self.keys else 0) - (1 if left in self.keys else 0)
        ay = (1 if down in self.keys else 0) - (1 if up in self.keys else 0)

        # ----------------------------
        # 2) Shift襍ｰ繧奇ｼ郁ｧ｣遲比ｾ具ｼ・
        # ----------------------------
        # modifier 縺悟叙繧後ｋ迺ｰ蠅・〒縺ｯ 'shift' 縺悟・繧・
        # 蜿悶ｌ縺ｪ縺・荳榊ｮ牙ｮ壹↑迺ｰ蠅・〒縺ｯ縲ヾhift繧ｭ繝ｼ繧ｳ繝ｼ繝・303/304)繧ょ呵｣懊↓縺吶ｋ
        shift_keys = {303, 304}  # 迺ｰ蠅・↓繧医ｊ蟾ｮ縺ゅｊ・亥承/蟾ｦShift・・
        is_shift = ('shift' in self.mods) or any(k in self.keys for k in shift_keys)

        spd = PLAYER_SPEED
        if is_shift:
            # 襍ｰ繧雁咲紫・壽肢讌ｭ縺ｧ縺ｯ 1.5縲・.0 縺ｮ遽・峇縺御ｽ捺─縺励ｄ縺吶＞
            spd = PLAYER_SPEED * 1.8

        # ----------------------------
        # 3) 遘ｻ蜍包ｼ・ay1縺ｯ陦晉ｪ√↑縺暦ｼ昴☆繧頑栢縺前K・・
        # ----------------------------
        self.px += ax * spd
        self.py += ay * spd

        # 繝槭ャ繝怜､悶∈蜃ｺ繧九→霑ｷ蟄舌↓縺ｪ繧九・縺ｧ 窶懈怙菴朱剞窶・縺ｮ蛻ｶ髯撰ｼ郁ｬ帛ｸｫ逕ｨ縺ｯ蜈･繧後※縺翫￥縺ｨ螳牙ｿ・ｼ・
        # clamp・壼､繧・min縲徇ax 縺ｫ蜿弱ａ繧九√→縺・≧諢丞袖
        self.px = max(0, min(self.px, self.map_w - self.w))
        self.py = max(0, min(self.py, self.map_h - self.h))

        # ----------------------------
        # 4) 繧ｫ繝｡繝ｩ・医・繝ｬ繧､繝､繝ｼ荳ｭ蠢・ｿｽ蠕難ｼ会ｼ・繝槭ャ繝礼ｫｯ縺ｧ蛻ｶ髯・
        # ----------------------------
        # 縲後・繝ｬ繧､繝､繝ｼ縺檎判髱｢縺ｮ逵溘ｓ荳ｭ縺ｫ譚･繧九阪ｈ縺・↓ cam 繧呈ｱｺ繧√ｋ
        cx = self.px - self.width / 2
        cy = self.py - self.height / 2

        # 繧ｫ繝｡繝ｩ縺後・繝・・螟悶ｒ譏縺輔↑縺・ｈ縺・↓蛻ｶ髯・
        cam_max_x = max(0, self.map_w - self.width)
        cam_max_y = max(0, self.map_h - self.height)

        self.cam[0] = max(0, min(cx, cam_max_x))
        self.cam[1] = max(0, min(cy, cam_max_y))

        # ----------------------------
        # 5) 逵区攸蠖薙◆繧雁愛螳夲ｼ郁ｧ｣遲比ｾ具ｼ哂ABB・・
        # ----------------------------
        self._check_sign(dt)

        # ----------------------------
        # 6) 謠冗判
        # ----------------------------
        self.draw()

    # ------------------------------------------------------------
    # 逵区攸蠖薙◆繧雁愛螳夲ｼ・ABB・・
    # ------------------------------------------------------------
    def _check_sign(self, dt):
        """
        Day1縺ｪ縺ｮ縺ｧ縲√≠縺上∪縺ｧ 窶懃ｰ｡譏凪・縺ｪ逵区攸蛻､螳壹・
        - 繝励Ξ繧､繝､繝ｼ遏ｩ蠖｢縺ｨ逵区攸遏ｩ蠖｢縺碁㍾縺ｪ縺｣縺溘ｉ繝｡繝・そ繝ｼ繧ｸ陦ｨ遉ｺ
        - 隗ｦ繧後※縺・↑縺・凾縺ｯ蟆代＠縺縺題｡ｨ遉ｺ繧剃ｿ晄戟・・UD縺後メ繝ｩ縺､縺上・繧帝亟縺撰ｼ・
        """
        # 菫晄戟譎る俣繧呈ｸ帙ｉ縺・
        self.sign_hold = max(0.0, self.sign_hold - dt)

        # 繝励Ξ繧､繝､繝ｼ遏ｩ蠖｢・亥ｷｦ荳・+ 繧ｵ繧､繧ｺ・・
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
            self.sign_hold = 0.20  # 0.2遘剃ｿ晄戟・医♀螂ｽ縺ｿ縺ｧ・・
        else:
            # 隗ｦ繧後※縺・↑縺・凾縺ｯ縲∽ｿ晄戟縺悟・繧後◆繧画ｶ医☆
            if self.sign_hold <= 0.0:
                self.sign_text = ""

        # HUD譖ｴ譁ｰ・域ｯ弱ヵ繝ｬ繝ｼ繝譖ｸ縺肴鋤縺医※OK・・
        base = "遏｢蜊ｰ縺ｧ遘ｻ蜍・/ Shift縺ｧ襍ｰ繧・/ 逵区攸縺ｫ隗ｦ繧後ｋ縺ｨ陦ｨ遉ｺ / 繝溘ル繝槭ャ繝怜承荳・
        if self.sign_text:
            self.hud.text = f"{base}\n縲千恚譚ｿ縲捜self.sign_text}"
        else:
            self.hud.text = base

    @staticmethod
    def _aabb_intersect(ax, ay, aw, ah, bx, by, bw, bh):
        """
        AABB・郁ｻｸ縺ｫ蟷ｳ陦後↑蝗幄ｧ貞ｽ｢・牙酔螢ｫ縺ｮ驥阪↑繧雁愛螳壹・
        - 2縺､縺ｮ遏ｩ蠖｢縺・窶憺㍾縺ｪ縺｣縺ｦ縺・ｋ窶・縺ｪ繧・True
        - 縺ｾ縺｣縺溘￥驥阪↑縺｣縺ｦ縺・↑縺・↑繧・False

        繧ｳ繝・ｼ・
        - 縲碁屬繧後※縺・ｋ譚｡莉ｶ縲阪ｒ蜷ｦ螳壹☆繧九→縲∝愛螳壹′譖ｸ縺阪ｄ縺吶＞
        """
        # a 縺ｮ蜿ｳ遶ｯ縺・b 縺ｮ蟾ｦ遶ｯ繧医ｊ蟾ｦ 竊・髮｢繧後※縺・ｋ
        if ax + aw <= bx:
            return False
        # a 縺ｮ蟾ｦ遶ｯ縺・b 縺ｮ蜿ｳ遶ｯ繧医ｊ蜿ｳ 竊・髮｢繧後※縺・ｋ
        if ax >= bx + bw:
            return False
        # a 縺ｮ荳顔ｫｯ縺・b 縺ｮ荳狗ｫｯ繧医ｊ荳・竊・髮｢繧後※縺・ｋ
        if ay + ah <= by:
            return False
        # a 縺ｮ荳狗ｫｯ縺・b 縺ｮ荳顔ｫｯ繧医ｊ荳・竊・髮｢繧後※縺・ｋ
        if ay >= by + bh:
            return False

        return True

    # ------------------------------------------------------------
    # draw・壻ｻ翫・迥ｶ諷九ｒ謠上￥
    # ------------------------------------------------------------
    def draw(self):
        self.canvas.clear()

        with self.canvas:
            # 0) 閭梧勹
            Color(*BG)
            Rectangle(pos=self.pos, size=self.size)

            # 1) 縺薙％縺九ｉ 窶懊Ρ繝ｼ繝ｫ繝画緒逕ｻ窶・髢句ｧ具ｼ医き繝｡繝ｩ縺ｧ縺壹ｉ縺呻ｼ・
            PushMatrix()
            Translate(-self.cam[0], -self.cam[1], 0)

            # 2) 繧ｿ繧､繝ｫ謠冗判
            ts = self.ts
            for r, row in enumerate(self.grid):
                for c, tid in enumerate(row):
                    # tid 縺ｫ蟇ｾ蠢懊☆繧・texture 縺檎┌縺・→關ｽ縺｡繧九・縺ｧ縲∬ｬ帛ｸｫ逕ｨ縺ｧ縺ｯ螳牙・蛛ｴ縺ｫ
                    tex = self.tiles.get(tid) if hasattr(self.tiles, "get") else self.tiles[tid]
                    if tex is None:
                        continue
                    Rectangle(texture=tex, pos=(c * ts, r * ts), size=(ts, ts))

            # 3) 逵区攸繧定埋縺乗緒逕ｻ・遺懊◎縺薙↓縺ゅｋ窶昴→蛻・°繧九ｈ縺・↓・・
            Color(1, 1, 1, 0.25)
            for s in self.signs:
                sx, sy = s["pos"]
                sw, sh = s["size"]
                Rectangle(pos=(sx, sy), size=(sw, sh))

            # 4) 繝励Ξ繧､繝､繝ｼ謠冗判
            Color(0.35, 0.67, 1, 1)
            Rectangle(pos=(self.px, self.py), size=(self.w, self.h))

            # 5) 繝ｯ繝ｼ繝ｫ繝画緒逕ｻ縺薙％縺ｾ縺ｧ
            PopMatrix()

            # 6) 逕ｻ髱｢蝗ｺ螳夲ｼ壹Α繝九・繝・・・郁ｧ｣遲比ｾ具ｼ・
            self._draw_minimap()

    # ------------------------------------------------------------
    # 繝溘ル繝槭ャ繝暦ｼ育判髱｢蝗ｺ螳壹・邁｡譏鍋沿・・
    # ------------------------------------------------------------
    def _draw_minimap(self):
        """
        Day1縺ｮ繝溘ル繝槭ャ繝励・ 窶憺屁蠖｢窶・縺ｧ蜊∝・縺ｧ縺吶・
        - 繝槭ャ繝怜・菴難ｼ壽棧・亥濠騾乗・・・
        - 繝励Ξ繧､繝､繝ｼ・夂せ・亥ｰ上＆縺ｪ蝗幄ｧ抵ｼ・
        - 繧ｫ繝｡繝ｩ遽・峇・壽棧・井ｻｻ諢上ゅ％縺薙〒縺ｯ蜈･繧後※縺ゅｊ縺ｾ縺呻ｼ・
        """
        # 1) 繝溘ル繝槭ャ繝励・譫
        Color(0, 0, 0, 0.45)
        Rectangle(pos=(self.mm_x, self.mm_y), size=(self.mm_w, self.mm_h))

        Color(1, 1, 1, 0.25)
        Rectangle(pos=(self.mm_x, self.mm_y), size=(self.mm_w, self.mm_h))

        # 2) 繝ｯ繝ｼ繝ｫ繝牙ｺｧ讓・-> 繝溘ル繝槭ャ繝怜ｺｧ讓吶∈縺ｮ螟画鋤
        #    豈皮紫・嗔x/map_w 繧・mm_w 縺ｫ蜀吶☆縲√→縺・≧閠・∴譁ｹ
        #    ・・ap_w 縺・0 縺ｫ縺ｪ繧九％縺ｨ縺ｯ騾壼ｸｸ縺ｪ縺・′縲∝ｿｵ縺ｮ縺溘ａ max(1, map_w)・・
        mw = max(1, self.map_w)
        mh = max(1, self.map_h)

        # 繝励Ξ繧､繝､繝ｼ荳ｭ蠢・ｒ繝溘ル繝槭ャ繝励∈
        pcx = self.px + self.w / 2
        pcy = self.py + self.h / 2

        mx = self.mm_x + (pcx / mw) * self.mm_w
        my = self.mm_y + (pcy / mh) * self.mm_h

        # 3) 繧ｫ繝｡繝ｩ遽・峇縺ｮ譫・医Α繝九・繝・・荳奇ｼ・
        # 繧ｫ繝｡繝ｩ縺ｮ蟾ｦ荳九→縲∫判髱｢繧ｵ繧､繧ｺ蛻・ｒ繝溘ル繝槭ャ繝励∈邵ｮ蟆上＠縺ｦ謠上￥
        cx = self.mm_x + (self.cam[0] / mw) * self.mm_w
        cy = self.mm_y + (self.cam[1] / mh) * self.mm_h
        cw = (self.width / mw) * self.mm_w
        ch = (self.height / mh) * self.mm_h

        Color(1, 1, 1, 0.35)
        Rectangle(pos=(cx, cy), size=(cw, ch))

        # 4) 繝励Ξ繧､繝､繝ｼ轤ｹ
        Color(0.35, 0.67, 1, 0.95)
        Rectangle(pos=(mx - 3, my - 3), size=(6, 6))


class Day1(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    Day1().run()

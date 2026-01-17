# -*- coding: utf-8 -*-
"""
逶ｮ逧・ 繝繝ｳ繧ｸ繝ｧ繝ｳ逕ｻ髱｢縺ｮ荳句慍縲よ婿菴攻I・医さ繝ｳ繝代せ・峨→迴ｾ蝨ｨ蝨ｰ陦ｨ遉ｺ縲√く繝ｼ繝懊・繝牙・蜉帙・蝓ｺ譛ｬ縲・
縺ｪ縺・ 縲後←縺ｮ譁ｹ蜷代ｒ蜷代＞縺ｦ縺・※縲√←縺薙↓縺・ｋ縺九阪ｒUI縺ｧ遒ｺ縺九ａ繧峨ｌ繧九ｈ縺・↓縺吶ｋ縺溘ａ縲・
蜑肴署: Compass繧ｦ繧｣繧ｸ繧ｧ繝・ヨ・・i/widgets/compass.py・峨′菴ｿ縺医ｋ縲・
蜈･蜃ｺ蜉・ maps/dungeon_01.json・井ｻ雁屓縺ｯ隱ｭ縺ｿ霎ｼ縺ｾ縺壹√ユ繧ｭ繧ｹ繝医・繝・・繧堤函謌撰ｼ峨・
蜑ｯ菴懃畑: 繧ｭ繝ｼ繝懊・繝峨ヵ繧ｩ繝ｼ繧ｫ繧ｹ隕∵ｱゑｼ・indow.request_keyboard・峨・
萓句､・ 荳驛ｨ縺ｮ迺ｰ蠅・〒縺ｯ繝輔か繝ｼ繧ｫ繧ｹ縺悟叙繧後★縺ｫ蜈･蜉帙′蜉ｹ縺九↑縺・ｴ蜷医≠繧翫・
"""
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from ui.widgets.compass import Compass

MAP_W, MAP_H = 10, 10  # 笘・ヲ繝ｳ繝・ 縺ｾ縺壹・10ﾃ・0縺ｮ邂ｱ蠎ｭ縺ｧOK・・

class DungeonScreen(MDScreen):
    # 笘・ヲ繝ｳ繝・ 繝励Ξ繧､繝､縺ｮ迴ｾ蝨ｨ蝨ｰ縺ｨ蜷代″繧偵・繝ｭ繝代ユ繧｣縺ｫ縺励※UI縺ｨ騾｣蜍輔＆縺帙ｋ縲・
    x = NumericProperty(1)
    y = NumericProperty(1)
    facing = StringProperty("N")

    def on_pre_enter(self, *args):
        self.clear_widgets()

        # --- STEP1: 荳企ΚHUD・域婿菴・+ 迴ｾ蝨ｨ蝨ｰ・・---
        root = MDBoxLayout(orientation="vertical", padding="12dp", spacing="8dp")
        hud = MDBoxLayout(orientation="horizontal", spacing="8dp", size_hint_y=None, height="48dp")
        self.compass = Compass(direction=self.facing)  # 笘・ヲ繝ｳ繝・ direction縺悟､峨ｏ繧九→陦ｨ遉ｺ縺梧峩譁ｰ縺輔ｌ繧九ｈ縲・
        self.status = MDLabel(text=self._status_text(), halign="left")
        hud.add_widget(self.compass)
        hud.add_widget(self.status)

        # --- STEP2: 繝槭ャ繝暦ｼ井ｻ雁屓縺ｯ繝・く繧ｹ繝医〒OK・・---
        self.map_label = MDLabel(text=self._map_ascii(), halign="left")
        root.add_widget(hud)
        root.add_widget(self.map_label)
        self.add_widget(root)

        # --- STEP3: 繧ｭ繝ｼ繝懊・繝会ｼ・ASD/遏｢蜊ｰ・・---
        # 繝輔か繝ｼ繧ｫ繧ｹ縺悟ｿ・ｦ√ゅえ繧｣繝ｳ繝峨え繧剃ｸ蠎ｦ繧ｯ繝ｪ繝・け縺励※縺九ｉ謚ｼ縺吶→縺・∪縺上＞縺上％縺ｨ縺悟､壹＞繧茨ｼ・
        self._keyboard = Window.request_keyboard(self._kb_closed, self, 'text')
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_key_down)

    # 繝輔か繝ｼ繧ｫ繧ｹ隗｣髯､譎・
    def _kb_closed(self):
        self._keyboard = None

    def on_leave(self, *args):
        if getattr(self, "_keyboard", None):
            self._keyboard.unbind(on_key_down=self._on_key_down)
            self._keyboard = None

    def _on_key_down(self, *args):
        # args: (keyboard, keycode, text, modifiers)
        _, keycode, text, modifiers = args
        key = keycode[1]

        # 笘・ヲ繝ｳ繝・ 縺薙・if蛻・ｲ舌ｒ隱ｭ縺ｿ隗｣縺薙≧・∬・蛻・〒 elif 繧呈嶌縺崎ｶｳ縺励※繧り憶縺・・
        dx = dy = 0
        if key in ("up", "w"):
            dy = -1; self.facing = "N"
        elif key in ("down", "s"):
            dy = 1; self.facing = "S"
        elif key in ("left", "a"):
            dx = -1; self.facing = "W"
        elif key in ("right", "d"):
            dx = 1; self.facing = "E"
        else:
            return False  # 莉悶・繧ｭ繝ｼ縺ｯ辟｡隕・

        # 笘・ヲ繝ｳ繝・ 縺ｾ縺壹・遽・峇繝√ぉ繝・け縺縺代ょ｣√・蠖薙◆繧雁愛螳壹・谺｡蝗槭ｄ縺｣縺ｦ縺ｿ繧医≧縲・
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < MAP_W and 0 <= ny < MAP_H:
            self.x, self.y = nx, ny

        self._refresh_hud()
        return True

    # --- 繝倥Ν繝醍ｾ､ ---
    def _refresh_hud(self):
        self.status.text = self._status_text()
        self.compass.direction = self.facing
        self.map_label.text = self._map_ascii()

    def _status_text(self):
        return f"Pos: ({self.x},{self.y})  Facing: {self.facing}"

    def _map_ascii(self):
        # 笘・ヲ繝ｳ繝・ '#'縺悟｣√・.'縺碁夊ｷｯ縲・P'縺後・繝ｬ繧､繝､縲・
        rows = []
        for j in range(MAP_H):
            row = []
            for i in range(MAP_W):
                if i == self.x and j == self.y:
                    row.append("P")
                elif i in (0, MAP_W-1) or j in (0, MAP_H-1):
                    row.append("#")
                else:
                    row.append(".")
            rows.append("".join(row))
        return "\\n".join(rows)

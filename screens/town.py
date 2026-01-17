# -*- coding: utf-8 -*-
"""
逶ｮ逧・ Town逕ｻ髱｢縺ｮ譛蟆丞ｮ溯｣・・ungeon 縺ｸ騾ｲ繧縺溘ａ縺ｮ繝懊ち繝ｳ繧堤畑諢上☆繧九・
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

class TownScreen(MDScreen):
    def on_pre_enter(self, *args):
        self.clear_widgets()
        layout = MDBoxLayout(orientation="vertical", spacing="16dp", padding="24dp")
        layout.add_widget(MDLabel(text="Town Screen", halign="center", font_style="H5"))
        layout.add_widget(MDLabel(text="陬・ｙ螻具ｼ丞ｮｿ螻具ｼ医・繝ｬ繝ｼ繧ｹ繝帙Ν繝・・, halign="center"))
        # 笘・ヲ繝ｳ繝・ 縺ｾ縺壹・ Dungeon 縺ｫ陦後￠繧九％縺ｨ繧貞━蜈医る峅蝗ｲ豌嶺ｽ懊ｊ縺ｯ蠕後〒OK・・
        layout.add_widget(MDRectangleFlatButton(text="Enter Dungeon", pos_hint={"center_x": 0.5}, on_release=self.go_dungeon))
        self.add_widget(layout)

    def go_dungeon(self, *args):
        self.manager.current = "dungeon"

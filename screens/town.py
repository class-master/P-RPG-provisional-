# -*- coding: utf-8 -*-
"""
目的: Town画面の最小実装。Dungeon へ進むためのボタンを用意する。
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
        layout.add_widget(MDLabel(text="装備屋／宿屋（プレースホルダ）", halign="center"))
        # ★ヒント: まずは Dungeon に行けることを優先。雰囲気作りは後でOK！
        layout.add_widget(MDRectangleFlatButton(text="Enter Dungeon", pos_hint={"center_x": 0.5}, on_release=self.go_dungeon))
        self.add_widget(layout)

    def go_dungeon(self, *args):
        self.manager.current = "dungeon"

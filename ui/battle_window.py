# ui/battle_window.py
# Day4 用：バトル中のHPとメッセージを表示するウィンドウ。

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class BattleWindow(BoxLayout):
    """Day4用の簡易バトル画面。HPとメッセージだけを扱う。"""

    player_name = StringProperty("")
    player_hp = StringProperty("")
    enemy_name = StringProperty("")
    enemy_hp = StringProperty("")
    message = StringProperty("")

    def update_status(self, player_status, enemy_status):
        """Status インスタンスから名前とHPの表示を更新する。"""
        self.player_name = player_status.name
        self.player_hp = f"HP: {player_status.hp}/{player_status.max_hp}"
        self.enemy_name = enemy_status.name
        self.enemy_hp = f"HP: {enemy_status.hp}/{enemy_status.max_hp}"

    def show_message(self, text: str):
        """画面下部のメッセージを1行だけ表示する。"""
        self.message = text

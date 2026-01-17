# ui/battle_window.py
# Day4 逕ｨ・壹ヰ繝医Ν荳ｭ縺ｮHP縺ｨ繝｡繝・そ繝ｼ繧ｸ繧定｡ｨ遉ｺ縺吶ｋ繧ｦ繧｣繝ｳ繝峨え縲・

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class BattleWindow(BoxLayout):
    """Day4逕ｨ縺ｮ邁｡譏薙ヰ繝医Ν逕ｻ髱｢縲・P縺ｨ繝｡繝・そ繝ｼ繧ｸ縺縺代ｒ謇ｱ縺・・""

    player_name = StringProperty("")
    player_hp = StringProperty("")
    enemy_name = StringProperty("")
    enemy_hp = StringProperty("")
    message = StringProperty("")

    def update_status(self, player_status, enemy_status):
        """Status 繧､繝ｳ繧ｹ繧ｿ繝ｳ繧ｹ縺九ｉ蜷榊燕縺ｨHP縺ｮ陦ｨ遉ｺ繧呈峩譁ｰ縺吶ｋ縲・""
        self.player_name = player_status.name
        self.player_hp = f"HP: {player_status.hp}/{player_status.max_hp}"
        self.enemy_name = enemy_status.name
        self.enemy_hp = f"HP: {enemy_status.hp}/{enemy_status.max_hp}"

    def show_message(self, text: str):
        """逕ｻ髱｢荳矩Κ縺ｮ繝｡繝・そ繝ｼ繧ｸ繧・陦後□縺題｡ｨ遉ｺ縺吶ｋ縲・""
        self.message = text

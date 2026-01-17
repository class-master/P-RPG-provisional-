# main_day4.py
# Day4 逕ｨ・壹ヵ繧｣繝ｼ繝ｫ繝峨→繝舌ヨ繝ｫ繧貞・繧頑崛縺医ｋ蜿ｸ莉､蝪斐・縺溘◆縺榊床縲・
#
# 螳滄圀縺ｮ繝励Ο繧ｸ繧ｧ繧ｯ繝医・ App繧ｯ繝ｩ繧ｹ繧・Player/NPC/繝槭ャ繝苓ｪｭ縺ｿ霎ｼ縺ｿ髢｢謨ｰ縺ｮ
# 蜷榊燕縺ｫ蜷医ｏ縺帙※譖ｸ縺肴鋤縺医※菴ｿ縺｣縺ｦ縺上□縺輔＞縲・

from typing import Optional

# 螳溘・繝ｭ繧ｸ繧ｧ繧ｯ繝医↓蜷医ｏ縺帙※ import 繧呈嶌縺肴鋤縺医※縺上□縺輔＞縲・
from status_day4 import Status
from systems.battle.battle_engine import player_attack, enemy_attack
from ui.battle_window import BattleWindow
import json
from pathlib import Path

mode = "field"  # "field" 縺ｾ縺溘・ "battle"

player_status = None      # Status
enemy_status: Optional["Status"] = None
battle_window = None      # BattleWindow 繧､繝ｳ繧ｹ繧ｿ繝ｳ繧ｹ

def setup_game():
    """Day4 逕ｨ縺ｮ蛻晄悄蛹悶ゅヵ繧｣繝ｼ繝ｫ繝牙・縺ｮ繧ｻ繝・ヨ繧｢繝・・・九せ繝・・繧ｿ繧ｹ貅門ｙ縲・""
    global player_status, battle_window
    # TODO: Day3 縺ｨ蜷梧ｧ倥↓繝輔ぅ繝ｼ繝ｫ繝峨・貅門ｙ繧定｡後≧縲・
    # 萓・ setup_field() 縺ｮ繧医≧縺ｪ髢｢謨ｰ繧貞他縺ｳ蜃ｺ縺吶・

    # TODO: 螳滄圀縺ｮ繝励Ξ繧､繝､繝ｼ蜷阪ｄ繝代Λ繝｡繝ｼ繧ｿ縺ｫ蜷医ｏ縺帙※隱ｿ謨ｴ縺吶ｋ縲・
    # player_status = Status("繧・≧縺励ｃ", max_hp=30, attack=8, defense=2)

    # TODO: 繝ｬ繧､繧｢繧ｦ繝医↓蜷医ｏ縺帙※ BattleWindow 繧堤函謌舌＠縺ｦ霑ｽ蜉縺吶ｋ縲・
    battle_window = BattleWindow()
    root_layout.add_widget(battle_window)
    battle_window.opacity = 0  # 譛蛻昴・髱櫁｡ｨ遉ｺ縺ｫ縺励※縺翫￥

def load_enemy_status(enemy_id: str):
    """enemies_day4.json 縺九ｉ謨ｵ繧ｹ繝・・繧ｿ繧ｹ繧・菴灘・隱ｭ縺ｿ霎ｼ繧薙〒 Status 繧定ｿ斐☆諠ｳ螳壹・""
    from status_day4 import Status
    import json
    from pathlib import Path

    data_path = Path("input/enemies_day4.json")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    info = data[enemy_id]
    return Status(
        name=info["name"],
        max_hp=info["max_hp"],
        attack=info["attack"],
        defense=info.get("defense", 0),
    )

def start_battle(enemy_id: str):
    """Day4 縺ｮ繝舌ヨ繝ｫ髢句ｧ句・逅・よ雰繧ｹ繝・・繧ｿ繧ｹ繧堤畑諢上＠縲ゞI繧偵ヰ繝医Ν繝｢繝ｼ繝峨↓縺吶ｋ縲・""
    global mode, enemy_status

    enemy_status = load_enemy_status(enemy_id)
    mode = "battle"

    if battle_window is not None and player_status is not None:
        battle_window.update_status(player_status, enemy_status)
        battle_window.show_message(f"{enemy_status.name} 縺後≠繧峨ｏ繧後◆・・)
        # battle_window.opacity = 1

def end_battle(message: str):
    """繝舌ヨ繝ｫ邨ゆｺ・・逅・ゅΓ繝・そ繝ｼ繧ｸ繧貞・縺励※縺九ｉ繝輔ぅ繝ｼ繝ｫ繝峨↓謌ｻ繧区Φ螳壹・""
    global mode, enemy_status
    mode = "field"

    if battle_window is not None:
        battle_window.show_message(message)
        # battle_window.opacity = 0

    enemy_status = None
    # TODO: 蜍晏茜譎ゅ↓NPC繧呈ｶ医☆縲√・繝ｬ繧､繝､繝ｼHP繧貞屓蠕ｩ縺吶ｋ縲√↑縺ｩ縺ｮ蜃ｦ逅・ｒ縺薙％縺ｫ蜈･繧後※繧ゅｈ縺・・

def handle_battle_key(key: str):
    """繝舌ヨ繝ｫ荳ｭ縺ｮ繧ｭ繝ｼ蜈･蜉帙ｒ蜃ｦ逅・☆繧九ゆｻ翫・ A繧ｭ繝ｼ縺ｧ謾ｻ謦・□縺代ｒ諠ｳ螳壹・""
    global player_status, enemy_status

    if key.lower() != "a":
        return

    if player_status is None or enemy_status is None:
        return

    from battle_engine import player_attack, enemy_attack

    # 1) 繝励Ξ繧､繝､繝ｼ縺ｮ謾ｻ謦・
    dmg = player_attack(player_status, enemy_status)
    if battle_window is not None:
        battle_window.update_status(player_status, enemy_status)
        battle_window.show_message(
            f"{player_status.name} 縺ｮ縺薙≧縺偵″・・{enemy_status.name} 縺ｫ {dmg} 繝繝｡繝ｼ繧ｸ・・
        )

    if enemy_status.is_dead():
        end_battle(f"{enemy_status.name} 繧・縺溘♀縺励◆・・)
        return

    # 2) 謨ｵ縺ｮ蜿肴茶
    dmg2 = enemy_attack(enemy_status, player_status)
    if battle_window is not None:
        battle_window.update_status(player_status, enemy_status)
        battle_window.show_message(
            f"{enemy_status.name} 縺ｮ縺薙≧縺偵″・・{player_status.name} 縺ｯ {dmg2} 繝繝｡繝ｼ繧ｸ繧偵≧縺代◆・・
        )

    if player_status.is_dead():
        end_battle("繧・ｉ繧後※縺励∪縺｣縺溪ｦ窶ｦ")
        # TODO: 繝励Ξ繧､繝､繝ｼ縺ｮHP繝ｪ繧ｻ繝・ヨ繧・ｾｩ豢ｻ蜃ｦ逅・↑縺ｩ繧偵％縺薙〒陦後≧縲・

def on_key_press(key: str):
    """蜈ｨ菴薙・繧ｭ繝ｼ蜈･蜉帙ワ繝ｳ繝峨Λ縲ゅヵ繧｣繝ｼ繝ｫ繝峨Δ繝ｼ繝・繝舌ヨ繝ｫ繝｢繝ｼ繝峨〒蜃ｦ逅・ｒ蛻・￠繧九・""
    if mode == "battle":
        handle_battle_key(key)
        return

    # mode == "field" 縺ｮ縺ｨ縺阪・縲∽ｻ翫∪縺ｧ騾壹ｊ縺ｮ遘ｻ蜍輔↑縺ｩ繧定｡後≧縲・
    if key in ("up", "down", "left", "right"):
        # move_player(key)  # 譌｢蟄倥・遘ｻ蜍輔Ο繧ｸ繝・け繧貞他縺ｳ蜃ｺ縺・
        return

    # 萓九∴縺ｰ Day3 縺ｮ縲君PC縺ｫ隧ｱ縺励°縺代ｋ縲榊・逅・・荳驛ｨ縺九ｉ
    # start_battle("slime") 繧貞他縺ｶ縺ｨ繝舌ヨ繝ｫ縺ｫ蜈･繧後ｋ繧､繝｡繝ｼ繧ｸ縺ｧ縺吶・

if __name__ == "__main__":
    print("Day4 逕ｨ縺ｮ main_day4.py 縺溘◆縺榊床縺ｧ縺吶・)
    print("螳溘・繝ｭ繧ｸ繧ｧ繧ｯ繝医・ App 繧ｯ繝ｩ繧ｹ縺ｫ邨・∩霎ｼ繧薙〒縺贋ｽｿ縺・￥縺縺輔＞縲・)

# -*- coding: utf-8 -*-
'''
RPG Rustic Master B 窶・Day5・育函蠕堤畑・・
蛻ｰ驕費ｼ壹ヵ繧｣繝ｼ繝ｫ繝・竊・繝舌ヨ繝ｫ縺ｮ豬√ｌ繧偵後Ο繧ｸ繝・け縲阪→縺励※邨・∩遶九※繧・
TODO・嘖tart_battle / end_battle / handle_battle_key 繧定・蛻・◆縺｡縺ｧ螳溯｣・☆繧・
'''
from __future__ import annotations

from typing import Optional

# 笘・縺薙％縺ｧ縺ｯ縲√≠縺医※縲景mport 繧貞・驛ｨ譖ｸ縺九↑縺・咲憾諷九°繧峨せ繧ｿ繝ｼ繝医＠縺ｾ縺吶・
#    Day5 縺ｮ隱ｲ鬘後→縺励※縲∬・蛻・◆縺｡縺ｧ蠢・ｦ√↑ import 繧定・∴縺ｦ霑ｽ險倥＠縺ｦ縺ｿ縺ｦ縺上□縺輔＞縲・
#
# 蛟呵｣懊→縺ｪ繧九Δ繧ｸ繝･繝ｼ繝ｫ縺溘■・医ヲ繝ｳ繝茨ｼ会ｼ・
# - status_day4  窶ｦ Status 繧ｯ繝ｩ繧ｹ・・P繝ｻ謾ｻ謦・鴨縺ｪ縺ｩ・・
# - battle_engine 窶ｦ player_attack / enemy_attack 髢｢謨ｰ
# - ui.battle_window 窶ｦ BattleWindow 繧ｯ繝ｩ繧ｹ・医ヰ繝医Ν逕ｻ髱｢縺ｮ繝ｬ繧､繧｢繧ｦ繝茨ｼ・
# - json, pathlib.Path 窶ｦ 謨ｵ繝・・繧ｿ JSON 繧定ｪｭ縺ｿ霎ｼ繧縺ｨ縺阪↓菴ｿ縺・

# === 繝｢繝ｼ繝臥ｮ｡逅・畑縺ｮ繧ｰ繝ｭ繝ｼ繝舌Ν螟画焚縺溘■ =====================================

#: 莉翫ご繝ｼ繝縺後後ヵ繧｣繝ｼ繝ｫ繝我ｸｭ縲阪°縲後ヰ繝医Ν荳ｭ縲阪°繧定｡ｨ縺吶ヵ繝ｩ繧ｰ
mode: str = "field"  # "field" / "battle"

#: 繝励Ξ繧､繝､繝ｼ縺ｮ繧ｹ繝・・繧ｿ繧ｹ・・ay4 縺ｮ Status 繧ｯ繝ｩ繧ｹ繧呈Φ螳夲ｼ・
player_status: Optional["Status"] = None

#: 莉翫ヰ繝医Ν縺励※縺・ｋ謨ｵ 1 菴薙・繧薙・繧ｹ繝・・繧ｿ繧ｹ
enemy_status: Optional["Status"] = None

#: Kivy 荳翫〒繝舌ヨ繝ｫ逕ｻ髱｢繧定｡ｨ遉ｺ縺吶ｋ繧ｦ繧｣繧ｸ繧ｧ繝・ヨ
battle_window: Optional["BattleWindow"] = None

#: Kivy 縺ｮ root 繝ｬ繧､繧｢繧ｦ繝茨ｼ・attleWindow 繧・add_widget 縺吶ｋ蝣ｴ謇・・
root_layout = None


# === 繧ｻ繝・ヨ繧｢繝・・縺ｾ繧上ｊ =====================================================

def setup_battle_layer(layout, player: "Status") -> None:
    '''
    Day5 縺ｧ霑ｽ蜉縺吶ｋ縲後ヰ繝医Ν逕ｨ繝ｬ繧､繝､縲阪ｒ貅門ｙ縺吶ｋ髢｢謨ｰ縲・

    - Kivy 繧｢繝励Μ縺ｮ build() 縺ｪ縺ｩ縺九ｉ 1 蝗槭□縺大他縺ｳ蜃ｺ縺呎Φ螳・
    - BattleWindow 繧堤函謌舌＠縲∵怙蛻昴・髱櫁｡ｨ遉ｺ縺ｧ繝ｬ繧､繧｢繧ｦ繝医↓霑ｽ蜉縺励※縺翫￥
    - 繝励Ξ繧､繝､繝ｼ縺ｮ Status 繧偵％縺薙〒菫晄戟縺励※縺翫″縲√ヰ繝医Ν荳ｭ縺ｫ蜿ら・縺ｧ縺阪ｋ繧医≧縺ｫ縺吶ｋ

    layout:
        譌｢蟄倥・繝輔ぅ繝ｼ繝ｫ繝臥判髱｢・・ay1/Day2・峨・荳翫↓驥阪・繧九◆繧√・繝ｬ繧､繧｢繧ｦ繝・
        萓具ｼ壹ヵ繧｣繝ｼ繝ｫ繝臥畑縺ｮ Widget 繧剃ｹ励○縺ｦ縺・ｋ FloatLayout 縺ｪ縺ｩ
    player:
        繝励Ξ繧､繝､繝ｼ縺ｮ迴ｾ蝨ｨ縺ｮ HP / 謾ｻ謦・鴨縺ｪ縺ｩ繧呈戟縺､ Status 繧､繝ｳ繧ｹ繧ｿ繝ｳ繧ｹ
    '''
    global root_layout, player_status, battle_window

    root_layout = layout
    player_status = player

    # TODO: Day4 縺ｧ菴懊▲縺・BattleWindow 繧・import 縺励※縺薙％縺ｧ逕滓・縺吶ｋ縲・
    #  萓具ｼ・from ui.battle_window import BattleWindow
    #       window = BattleWindow()
    #       layout.add_widget(window)
    #       window.opacity = 0.0  # 譛蛻昴・騾乗・・・隕九∴縺ｪ縺・ｼ峨↓縺励※縺翫￥
    #
    # 縺薙・髢｢謨ｰ縺ｮ繧ｴ繝ｼ繝ｫ・・
    #   - battle_window 螟画焚縺ｫ BattleWindow 縺ｮ繧､繝ｳ繧ｹ繧ｿ繝ｳ繧ｹ縺悟・縺｣縺ｦ縺・ｋ縺薙→
    #
    # 螳溯｣・ｾ九・ main_day5_teacher.py 繧貞盾辣ｧ縺励※縺上□縺輔＞縲・
    raise NotImplementedError("Day5 隱ｲ鬘・ setup_battle_layer() 繧貞ｮ溯｣・＠繧医≧")


# === 謨ｵ繧ｹ繝・・繧ｿ繧ｹ縺ｮ隱ｭ縺ｿ霎ｼ縺ｿ =================================================

def load_enemy_status(enemy_id: str) -> "Status":
    '''
    謨ｵ ID 縺九ｉ 1 菴薙・繧薙・ Status 繧剃ｽ懊▲縺ｦ霑斐☆縲・

    enemy_id:
        JSON 繝輔ぃ繧､繝ｫ `input/enemies_day4.json` 縺ｫ譖ｸ縺九ｌ縺ｦ縺・ｋ繧ｭ繝ｼ繧呈Φ螳壹・
        萓具ｼ・"slime", "bat", "goblin" 縺ｪ縺ｩ縲・

    謌ｻ繧雁､:
        Status 繧ｯ繝ｩ繧ｹ縺ｮ繧､繝ｳ繧ｹ繧ｿ繝ｳ繧ｹ・・ame / max_hp / attack / defense 繧呈戟縺､・峨・
    '''
    # TODO:
    #   1. pathlib.Path 繧剃ｽｿ縺｣縺ｦ JSON 繝輔ぃ繧､繝ｫ (`input/enemies_day4.json`) 繧帝幕縺・
    #   2. json.loads() 縺ｧ dict 蝙九↓螟画鋤縺吶ｋ
    #   3. enemy_id 縺ｫ蟇ｾ蠢懊☆繧九ョ繝ｼ繧ｿ繧貞叙繧雁・縺励ヾtatus(...) 繧剃ｽ懊▲縺ｦ霑斐☆
    #
    # 繝偵Φ繝茨ｼ・
    #   from pathlib import Path
    #   import json
    #
    #   data_path = Path("input/enemies_day4.json")
    #   data = json.loads(data_path.read_text(encoding="utf-8"))
    #   info = data[enemy_id]
    #
    #   return Status(
    #       name=info["name"],
    #       max_hp=info["max_hp"],
    #       attack=info["attack"],
    #       defense=info.get("defense", 0),
    #   )
    #
    # 螳溯｣・◎縺ｮ繧ゅ・縺ｯ縲［ain_day5_teacher.py 縺ｫ螳梧・迚医′霈峨▲縺ｦ縺・∪縺吶・
    raise NotImplementedError("Day5 隱ｲ鬘・ load_enemy_status() 繧貞ｮ溯｣・＠繧医≧")


# === 繝舌ヨ繝ｫ髢句ｧ・/ 邨ゆｺ・・逅・===================================================

def start_battle(enemy_id: str) -> None:
    '''
    繝輔ぅ繝ｼ繝ｫ繝峨°繧峨ヰ繝医Ν縺ｫ蜈･繧九→縺阪↓蜻ｼ縺ｳ蜃ｺ縺咎未謨ｰ縲・

    諠ｳ螳壹す繝ｼ繝ｳ:
        - Day3 縺ｮ縲君PC 縺ｫ隧ｱ縺励°縺代◆縲阪→縺・
        - 迚ｹ螳壹・繝槭せ縺ｫ荵励▲縺溘→縺・
        縺ｪ縺ｩ縲√ヵ繧｣繝ｼ繝ｫ繝牙・縺ｮ繧､繝吶Φ繝亥・逅・°繧牙他縺ｳ蜃ｺ縺輔ｌ繧九・

    縺薙％縺ｧ繧・ｊ縺溘＞縺薙→・医＊縺｣縺上ｊ・・

    1. enemy_id 縺九ｉ謨ｵ縺ｮ Status 繧剃ｽ懊ｋ・・oad_enemy_status 繧貞他縺ｳ蜃ｺ縺呻ｼ・
    2. battle_window 縺ｫ繝励Ξ繧､繝､繝ｼ / 謨ｵ縺ｮ繧ｹ繝・・繧ｿ繧ｹ繧定｡ｨ遉ｺ縺吶ｋ
    3. 縲後懊′縺ゅｉ繧上ｌ縺滂ｼ√阪↑縺ｩ縺ｮ繝｡繝・そ繝ｼ繧ｸ繧貞・縺・
    4. battle_window 縺ｮ opacity 繧・1.0 縺ｫ縺励※逕ｻ髱｢縺ｫ陦ｨ遉ｺ縺吶ｋ
    5. mode 繧・"battle" 縺ｫ蛻・ｊ譖ｿ縺医ｋ
    '''
    global mode, enemy_status

    # TODO: 荳翫・ 1縲・ 縺ｮ謇矩・↓縺ｪ繧九ｈ縺・↓縲∝・逅・ｒ譖ｸ縺・※縺ｿ縺ｾ縺励ｇ縺・・
    #
    # 縺薙％縺・Day5 縺ｮ縲悟・繧雁哨縲阪↓縺ｪ繧句､ｧ莠九↑髢｢謨ｰ縺ｧ縺吶・
    # 縺ｾ縺壹・ print() 縺縺代〒蜍穂ｽ懃｢ｺ隱・竊・縺昴・縺ゅ→ BattleWindow 縺ｫ縺､縺ｪ縺舌・
    # 縺ｨ谿ｵ髫守噪縺ｫ螳溯｣・☆繧九→螳牙・縺ｧ縺吶・
    raise NotImplementedError("Day5 隱ｲ鬘・ start_battle() 繧貞ｮ溯｣・＠繧医≧")


def end_battle(message: str) -> None:
    '''
    繝舌ヨ繝ｫ縺檎ｵゅｏ縺｣縺溘→縺阪↓蜻ｼ縺ｳ蜃ｺ縺咎未謨ｰ縲・

    繧・ｊ縺溘＞縺薙→・井ｾ具ｼ・

    - 蠑墓焚 message 繧・battle_window 縺ｫ陦ｨ遉ｺ縺吶ｋ
    - battle_window 繧帝撼陦ｨ遉ｺ縺ｫ縺吶ｋ・・pacity 繧・0.0 縺ｫ謌ｻ縺呻ｼ・
    - 謨ｵ繧ｹ繝・・繧ｿ繧ｹ enemy_status 繧・None 縺ｫ謌ｻ縺・
    - mode 繧・"field" 縺ｫ謌ｻ縺・
    - 蠢・ｦ√〒縺ゅｌ縺ｰ縲√・繝ｬ繧､繝､繝ｼ縺ｮ HP 繧貞・蝗槫ｾｩ縺吶ｋ・域風蛹玲凾縺ｪ縺ｩ・・
    '''
    global mode, enemy_status

    # TODO: 荳翫・繧ｳ繝｡繝ｳ繝医ｒ隕九↑縺後ｉ縲√ヰ繝医Ν邨ゆｺ・凾縺ｮ蜃ｦ逅・ｒ邨・∩遶九※縺ｦ縺ｿ縺ｾ縺励ｇ縺・・
    #
    # Day5 縺ｧ縺ｯ縲悟享蛻ｩ譎ゅ阪→縲梧風蛹玲凾縲阪〒蟆代＠謖ｯ繧玖・縺・ｒ螟峨∴繧九→讌ｽ縺励＞縺ｧ縺吶′縲・
    # 縺ｾ縺壹・縲後←縺｡繧峨〒繧ゅヵ繧｣繝ｼ繝ｫ繝峨↓謌ｻ繧後ｋ縲阪％縺ｨ繧貞━蜈医＠縺ｦ OK 縺ｧ縺吶・
    raise NotImplementedError("Day5 隱ｲ鬘・ end_battle() 繧貞ｮ溯｣・＠繧医≧")


# === 繝舌ヨ繝ｫ荳ｭ縺ｮ繧ｭ繝ｼ蜈･蜉帛・逅・===============================================

def handle_battle_key(key: str) -> None:
    '''
    繝舌ヨ繝ｫ荳ｭ縺ｫ繧ｭ繝ｼ縺梧款縺輔ｌ縺溘→縺阪・蜃ｦ逅・ｒ陦後≧縲・

    莉雁屓縺ｮ Day5 縺ｧ縺ｯ縲∵怙菴朱剞縲窟 繧ｭ繝ｼ縺ｧ謾ｻ謦・阪′縺ｧ縺阪ｌ縺ｰ OK 縺ｧ縺吶・
    菴吝鴨縺後≠繧後・縲沓 繧ｭ繝ｼ縺ｧ髦ｲ蠕｡縲阪靴 繧ｭ繝ｼ縺ｧ騾・￡繧九阪↑縺ｩ繧定ｿｽ蜉縺励※繧よｧ九＞縺ｾ縺帙ｓ縲・
    '''
    global player_status, enemy_status

    if key.lower() != "a":
        # A 繧ｭ繝ｼ莉･螟悶・縲∽ｻ雁屓縺ｯ菴輔ｂ縺励↑縺・
        return

    if player_status is None or enemy_status is None:
        # 縺ｾ縺繝舌ヨ繝ｫ縺ｮ貅門ｙ縺後〒縺阪※縺・↑縺・ｴ蜷医・菴輔ｂ縺励↑縺・
        return

    # TODO:
    #   1. battle_engine.player_attack() 繧貞他繧薙〒縲∵雰縺ｫ繝繝｡繝ｼ繧ｸ繧剃ｸ弱∴繧・
    #   2. BattleWindow 繧剃ｽｿ縺｣縺ｦ HP 陦ｨ遉ｺ縺ｨ繝｡繝・そ繝ｼ繧ｸ繧呈峩譁ｰ縺吶ｋ
    #   3. 謨ｵ縺悟偵ｌ縺溘ｉ end_battle("縲懊ｒ 縺溘♀縺励◆・・) 繧貞他繧薙〒邨ゆｺ・☆繧・
    #   4. 蛟偵ｌ縺ｦ縺・↑縺代ｌ縺ｰ縲‘nemy_attack() 縺ｧ蜿肴茶縺輔○繧・
    #   5. 繝励Ξ繧､繝､繝ｼ縺悟偵ｌ縺溘ｉ縲？P 繧貞・蝗槫ｾｩ縺輔○縺ｦ縺九ｉ end_battle("繧・ｉ繧後※縺励∪縺｣縺溪ｦ") 繧貞他縺ｶ
    #
    # 縺薙■繧峨ｂ縲∝ｮ溯｣・ｾ九・ main_day5_teacher.py 縺ｫ霈峨▲縺ｦ縺・∪縺吶・
    raise NotImplementedError("Day5 隱ｲ鬘・ handle_battle_key() 繧貞ｮ溯｣・＠繧医≧")


# === 蜈ｨ菴薙・繧ｭ繝ｼ蜈･蜉帙ワ繝ｳ繝峨Λ ===============================================

def on_key_press(key: str) -> None:
    '''
    繧ｲ繝ｼ繝蜈ｨ菴薙〒繧ｭ繝ｼ縺梧款縺輔ｌ縺溘→縺阪↓蜻ｼ縺ｳ蜃ｺ縺輔ｌ繧区Φ螳壹・髢｢謨ｰ縲・

    - mode 縺・"battle" 縺ｮ縺ｨ縺・竊・繝舌ヨ繝ｫ逕ｨ縺ｮ handle_battle_key() 縺ｫ蜃ｦ逅・ｒ貂｡縺・
    - mode 縺・"field" 縺ｮ縺ｨ縺・竊・蠕捺擂縺ｩ縺翫ｊ縲∫ｧｻ蜍輔ｄ莨夊ｩｱ蜃ｦ逅・ｒ陦後≧

    螳滄圀縺ｮ繝励Ο繧ｸ繧ｧ繧ｯ繝医〒縺ｯ縲．ay1/Day2 縺ｮ App 繧ｯ繝ｩ繧ｹ繧・
    Window.bind(on_key_down=...) 縺ｮ繧ｳ繝ｼ繝ｫ繝舌ャ繧ｯ縺九ｉ縺薙・髢｢謨ｰ繧貞他縺ｳ蜃ｺ縺吝ｽ｢繧呈Φ螳壹＠縺ｦ縺・∪縺吶・
    '''
    if mode == "battle":
        # 繝舌ヨ繝ｫ荳ｭ縺ｯ縲√☆縺ｹ縺ｦ縺ｮ繧ｭ繝ｼ蜈･蜉帙ｒ繝舌ヨ繝ｫ縺ｫ蟆ょｿｵ縺輔○繧・
        handle_battle_key(key)
        return

    # 縺薙％縺九ｉ荳九・縲後ヵ繧｣繝ｼ繝ｫ繝峨Δ繝ｼ繝峨阪・縺ｨ縺阪↓縺縺大ｮ溯｡後＆繧後ｋ縲・
    if key in ("up", "down", "left", "right"):
        # TODO: 譌｢蟄倥・繝励Ξ繧､繝､繝ｼ遘ｻ蜍募・逅・↓讖区ｸ｡縺励☆繧九・
        # 萓具ｼ・move_player(key) 縺ｪ縺ｩ縺ｮ髢｢謨ｰ繧貞他縺ｶ縲・
        return

    if key == "e":
        # TODO: Day3 縺ｧ菴懊▲縺溘君PC 縺ｫ隧ｱ縺励°縺代ｋ縲榊・逅・・荳驛ｨ縺九ｉ
        #       start_battle("slime") 縺ｪ縺ｩ繧貞他縺ｳ蜃ｺ縺励※縺ｿ縺ｾ縺励ｇ縺・・
        #
        # 縺ｩ縺ｮ NPC / 繧､繝吶Φ繝医°繧峨←縺ｮ謨ｵ ID 繧貞他縺ｶ縺九・縲√メ繝ｼ繝縺ｧ逶ｸ隲・＠縺ｦ豎ｺ繧√※ OK 縺ｧ縺吶・
        return


if __name__ == "__main__":
    print("Day5 逕ｨ縺ｮ main_day5.py 縺ｧ縺吶・)
    print("螳滄圀縺ｮ繧ｲ繝ｼ繝縺ｧ縺ｯ縲、pp 繧ｯ繝ｩ繧ｹ縺九ｉ setup_battle_layer() / on_key_press() 繧貞他縺ｳ蜃ｺ縺励※菴ｿ縺・∪縺吶・)

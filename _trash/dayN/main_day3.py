# Day3 逕ｨ縺ｮ襍ｷ蜍輔せ繧ｯ繝ｪ繝励ヨ縺ｮ縺溘◆縺榊床縲・
# 螳滄圀縺ｮ繝励Ο繧ｸ繧ｧ繧ｯ繝医・ Player / NPC / 繝槭ャ繝苓ｪｭ縺ｿ霎ｼ縺ｿ / 逕ｻ髱｢繧ｯ繝ｩ繧ｹ縺ｮ蜷榊燕縺ｫ
# 蜷医ｏ縺帙※譖ｸ縺肴鋤縺医※縺上□縺輔＞縲・

from typing import List

from entities_student import Player, NPC
from field.map_loader_kivy import load_map
from ui.message_window import MessageWindow
from systems.events.events_loader import load_events
from entities_student import is_adjacent

player = None
npcs: List[object] = []
events: dict = {}
message_window = None


def setup_game():
    # Day3 逕ｨ縺ｮ繝輔ぅ繝ｼ繝ｫ繝峨→NPC縲∽ｼ夊ｩｱ繝・・繧ｿ繧貞・譛溷喧縺吶ｋ髢｢謨ｰ縲・
    global player, npcs, events, message_window
    game_map = load_map('maps/village01.map')
    player = Player(x=5, y=5)
    npcs = [
        NPC('譚台ｺｺA', 8, 5, 'first_npc'),
        NPC('縺雁ｺ励・蟄・, 10, 7, 'shop_girl'),
    ]
    events = load_events()
    message_window = MessageWindow()


def is_adjacent(player, npc) -> bool:
    dx = abs(player.x - npc.x)
    dy = abs(player.y - npc.y)
    return dx + dy == 1


def open_talk_window(event_id: str) -> None:
    if event_id not in events:
        print(f'[WARN] 譛ｪ逋ｻ骭ｲ event_id: {event_id}')
        return
    lines = events[event_id]
    if message_window is not None:
        message_window.show_message(lines)
    else:
        print('[TALK]')
        for line in lines:
            print(' ', line)


def on_key_press(key: str) -> None:
    if key in ('up', 'down', 'left', 'right'):
        # move_player(key)  # 譌｢蟄倥・遘ｻ蜍輔Ο繧ｸ繝・け縺ｫ讖区ｸ｡縺励☆繧・
        return
    if key == 'e':
        for npc in npcs:
            if is_adjacent(player, npc):
                open_talk_window(npc.event_id)
                break


if __name__ == '__main__':
    print('Day3 逕ｨ縺ｮ main_day3.py 縺溘◆縺榊床縺ｧ縺吶・)
    print('螳溘・繝ｭ繧ｸ繧ｧ繧ｯ繝医・ App 繧ｯ繝ｩ繧ｹ縺ｫ邨・∩霎ｼ繧薙〒縺贋ｽｿ縺・￥縺縺輔＞縲・)

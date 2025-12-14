# Day3 用の起動スクリプトのたたき台。
# 実際のプロジェクトの Player / NPC / マップ読み込み / 画面クラスの名前に
# 合わせて書き換えてください。

from typing import List

# from entities_student import Player, NPC
# from map_loader_kivy import load_map
# from ui.message_window import MessageWindow
# from events_loader import load_events
# from entities_student import is_adjacent

player = None
npcs: List[object] = []
events: dict = {}
message_window = None


def setup_game():
    # Day3 用のフィールドとNPC、会話データを初期化する関数。
    global player, npcs, events, message_window
    # game_map = load_map('maps/village01.map')
    # player = Player(x=5, y=5)
    # npcs = [
    #     NPC('村人A', 8, 5, 'first_npc'),
    #     NPC('お店の子', 10, 7, 'shop_girl'),
    # ]
    # events = load_events()
    # message_window = MessageWindow()


def is_adjacent(player, npc) -> bool:
    dx = abs(player.x - npc.x)
    dy = abs(player.y - npc.y)
    return dx + dy == 1


def open_talk_window(event_id: str) -> None:
    if event_id not in events:
        print(f'[WARN] 未登録 event_id: {event_id}')
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
        # move_player(key)  # 既存の移動ロジックに橋渡しする
        return
    if key == 'e':
        for npc in npcs:
            if is_adjacent(player, npc):
                open_talk_window(npc.event_id)
                break


if __name__ == '__main__':
    print('Day3 用の main_day3.py たたき台です。')
    print('実プロジェクトの App クラスに組み込んでお使いください。')

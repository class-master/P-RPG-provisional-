# main_day4.py
# Day4 用：フィールドとバトルを切り替える司令塔のたたき台。
#
# 実際のプロジェクトの Appクラスや Player/NPC/マップ読み込み関数の
# 名前に合わせて書き換えて使ってください。

from typing import Optional

# 実プロジェクトに合わせて import を書き換えてください。
# from status_day4 import Status
# from battle_engine import player_attack, enemy_attack
# from ui.battle_window import BattleWindow
# import json
# from pathlib import Path

mode = "field"  # "field" または "battle"

player_status = None      # Status
enemy_status: Optional["Status"] = None
battle_window = None      # BattleWindow インスタンス

def setup_game():
    """Day4 用の初期化。フィールド側のセットアップ＋ステータス準備。"""
    global player_status, battle_window
    # TODO: Day3 と同様にフィールドの準備を行う。
    # 例: setup_field() のような関数を呼び出す。

    # TODO: 実際のプレイヤー名やパラメータに合わせて調整する。
    # player_status = Status("ゆうしゃ", max_hp=30, attack=8, defense=2)

    # TODO: レイアウトに合わせて BattleWindow を生成して追加する。
    # battle_window = BattleWindow()
    # root_layout.add_widget(battle_window)
    # battle_window.opacity = 0  # 最初は非表示にしておく

def load_enemy_status(enemy_id: str):
    """enemies_day4.json から敵ステータスを1体分読み込んで Status を返す想定。"""
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
    """Day4 のバトル開始処理。敵ステータスを用意し、UIをバトルモードにする。"""
    global mode, enemy_status

    enemy_status = load_enemy_status(enemy_id)
    mode = "battle"

    if battle_window is not None and player_status is not None:
        battle_window.update_status(player_status, enemy_status)
        battle_window.show_message(f"{enemy_status.name} があらわれた！")
        # battle_window.opacity = 1

def end_battle(message: str):
    """バトル終了処理。メッセージを出してからフィールドに戻る想定。"""
    global mode, enemy_status
    mode = "field"

    if battle_window is not None:
        battle_window.show_message(message)
        # battle_window.opacity = 0

    enemy_status = None
    # TODO: 勝利時にNPCを消す、プレイヤーHPを回復する、などの処理をここに入れてもよい。

def handle_battle_key(key: str):
    """バトル中のキー入力を処理する。今は Aキーで攻撃だけを想定。"""
    global player_status, enemy_status

    if key.lower() != "a":
        return

    if player_status is None or enemy_status is None:
        return

    from battle_engine import player_attack, enemy_attack

    # 1) プレイヤーの攻撃
    dmg = player_attack(player_status, enemy_status)
    if battle_window is not None:
        battle_window.update_status(player_status, enemy_status)
        battle_window.show_message(
            f"{player_status.name} のこうげき！ {enemy_status.name} に {dmg} ダメージ！"
        )

    if enemy_status.is_dead():
        end_battle(f"{enemy_status.name} を たおした！")
        return

    # 2) 敵の反撃
    dmg2 = enemy_attack(enemy_status, player_status)
    if battle_window is not None:
        battle_window.update_status(player_status, enemy_status)
        battle_window.show_message(
            f"{enemy_status.name} のこうげき！ {player_status.name} は {dmg2} ダメージをうけた！"
        )

    if player_status.is_dead():
        end_battle("やられてしまった……")
        # TODO: プレイヤーのHPリセットや復活処理などをここで行う。

def on_key_press(key: str):
    """全体のキー入力ハンドラ。フィールドモード/バトルモードで処理を分ける。"""
    if mode == "battle":
        handle_battle_key(key)
        return

    # mode == "field" のときは、今まで通りの移動などを行う。
    if key in ("up", "down", "left", "right"):
        # move_player(key)  # 既存の移動ロジックを呼び出す
        return

    # 例えば Day3 の「NPCに話しかける」処理の一部から
    # start_battle("slime") を呼ぶとバトルに入れるイメージです。

if __name__ == "__main__":
    print("Day4 用の main_day4.py たたき台です。")
    print("実プロジェクトの App クラスに組み込んでお使いください。")

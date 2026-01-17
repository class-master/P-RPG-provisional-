# -*- coding: utf-8 -*-
'''
RPG Rustic Master B — Day5（生徒用）
到達：フィールド ↔ バトルの流れを「ロジック」として組み立てる
TODO：start_battle / end_battle / handle_battle_key を自分たちで実装する
'''
from __future__ import annotations

from typing import Optional

# ★ ここでは、あえて「import を全部書かない」状態からスタートします。
#    Day5 の課題として、自分たちで必要な import を考えて追記してみてください。
#
# 候補となるモジュールたち（ヒント）：
# - status_day4  … Status クラス（HP・攻撃力など）
# - battle_engine … player_attack / enemy_attack 関数
# - ui.battle_window … BattleWindow クラス（バトル画面のレイアウト）
# - json, pathlib.Path … 敵データ JSON を読み込むときに使う

# === モード管理用のグローバル変数たち =====================================

#: 今ゲームが「フィールド中」か「バトル中」かを表すフラグ
mode: str = "field"  # "field" / "battle"

#: プレイヤーのステータス（Day4 の Status クラスを想定）
player_status: Optional["Status"] = None

#: 今バトルしている敵 1 体ぶんのステータス
enemy_status: Optional["Status"] = None

#: Kivy 上でバトル画面を表示するウィジェット
battle_window: Optional["BattleWindow"] = None

#: Kivy の root レイアウト（BattleWindow を add_widget する場所）
root_layout = None


# === セットアップまわり =====================================================

def setup_battle_layer(layout, player: "Status") -> None:
    '''
    Day5 で追加する「バトル用レイヤ」を準備する関数。

    - Kivy アプリの build() などから 1 回だけ呼び出す想定
    - BattleWindow を生成し、最初は非表示でレイアウトに追加しておく
    - プレイヤーの Status をここで保持しておき、バトル中に参照できるようにする

    layout:
        既存のフィールド画面（Day1/Day2）の上に重ねるためのレイアウト
        例：フィールド用の Widget を乗せている FloatLayout など
    player:
        プレイヤーの現在の HP / 攻撃力などを持つ Status インスタンス
    '''
    global root_layout, player_status, battle_window

    root_layout = layout
    player_status = player

    # TODO: Day4 で作った BattleWindow を import してここで生成する。
    #  例） from ui.battle_window import BattleWindow
    #       window = BattleWindow()
    #       layout.add_widget(window)
    #       window.opacity = 0.0  # 最初は透明（=見えない）にしておく
    #
    # この関数のゴール：
    #   - battle_window 変数に BattleWindow のインスタンスが入っていること
    #
    # 実装例は main_day5_teacher.py を参照してください。
    raise NotImplementedError("Day5 課題: setup_battle_layer() を実装しよう")


# === 敵ステータスの読み込み =================================================

def load_enemy_status(enemy_id: str) -> "Status":
    '''
    敵 ID から 1 体ぶんの Status を作って返す。

    enemy_id:
        JSON ファイル `input/enemies_day4.json` に書かれているキーを想定。
        例： "slime", "bat", "goblin" など。

    戻り値:
        Status クラスのインスタンス（name / max_hp / attack / defense を持つ）。
    '''
    # TODO:
    #   1. pathlib.Path を使って JSON ファイル (`input/enemies_day4.json`) を開く
    #   2. json.loads() で dict 型に変換する
    #   3. enemy_id に対応するデータを取り出し、Status(...) を作って返す
    #
    # ヒント：
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
    # 実装そのものは、main_day5_teacher.py に完成版が載っています。
    raise NotImplementedError("Day5 課題: load_enemy_status() を実装しよう")


# === バトル開始 / 終了処理 ===================================================

def start_battle(enemy_id: str) -> None:
    '''
    フィールドからバトルに入るときに呼び出す関数。

    想定シーン:
        - Day3 の「NPC に話しかけた」とき
        - 特定のマスに乗ったとき
        など、フィールド側のイベント処理から呼び出される。

    ここでやりたいこと（ざっくり）:

    1. enemy_id から敵の Status を作る（load_enemy_status を呼び出す）
    2. battle_window にプレイヤー / 敵のステータスを表示する
    3. 「〜があらわれた！」などのメッセージを出す
    4. battle_window の opacity を 1.0 にして画面に表示する
    5. mode を "battle" に切り替える
    '''
    global mode, enemy_status

    # TODO: 上の 1〜5 の手順になるように、処理を書いてみましょう。
    #
    # ここが Day5 の「入り口」になる大事な関数です。
    # まずは print() だけで動作確認 → そのあと BattleWindow につなぐ、
    # と段階的に実装すると安全です。
    raise NotImplementedError("Day5 課題: start_battle() を実装しよう")


def end_battle(message: str) -> None:
    '''
    バトルが終わったときに呼び出す関数。

    やりたいこと（例）:

    - 引数 message を battle_window に表示する
    - battle_window を非表示にする（opacity を 0.0 に戻す）
    - 敵ステータス enemy_status を None に戻す
    - mode を "field" に戻す
    - 必要であれば、プレイヤーの HP を全回復する（敗北時など）
    '''
    global mode, enemy_status

    # TODO: 上のコメントを見ながら、バトル終了時の処理を組み立ててみましょう。
    #
    # Day5 では「勝利時」と「敗北時」で少し振る舞いを変えると楽しいですが、
    # まずは「どちらでもフィールドに戻れる」ことを優先して OK です。
    raise NotImplementedError("Day5 課題: end_battle() を実装しよう")


# === バトル中のキー入力処理 ===============================================

def handle_battle_key(key: str) -> None:
    '''
    バトル中にキーが押されたときの処理を行う。

    今回の Day5 では、最低限「A キーで攻撃」ができれば OK です。
    余力があれば「B キーで防御」「C キーで逃げる」などを追加しても構いません。
    '''
    global player_status, enemy_status

    if key.lower() != "a":
        # A キー以外は、今回は何もしない
        return

    if player_status is None or enemy_status is None:
        # まだバトルの準備ができていない場合は何もしない
        return

    # TODO:
    #   1. battle_engine.player_attack() を呼んで、敵にダメージを与える
    #   2. BattleWindow を使って HP 表示とメッセージを更新する
    #   3. 敵が倒れたら end_battle("〜を たおした！") を呼んで終了する
    #   4. 倒れていなければ、enemy_attack() で反撃させる
    #   5. プレイヤーが倒れたら、HP を全回復させてから end_battle("やられてしまった…") を呼ぶ
    #
    # こちらも、実装例は main_day5_teacher.py に載っています。
    raise NotImplementedError("Day5 課題: handle_battle_key() を実装しよう")


# === 全体のキー入力ハンドラ ===============================================

def on_key_press(key: str) -> None:
    '''
    ゲーム全体でキーが押されたときに呼び出される想定の関数。

    - mode が "battle" のとき → バトル用の handle_battle_key() に処理を渡す
    - mode が "field" のとき → 従来どおり、移動や会話処理を行う

    実際のプロジェクトでは、Day1/Day2 の App クラスや
    Window.bind(on_key_down=...) のコールバックからこの関数を呼び出す形を想定しています。
    '''
    if mode == "battle":
        # バトル中は、すべてのキー入力をバトルに専念させる
        handle_battle_key(key)
        return

    # ここから下は「フィールドモード」のときにだけ実行される。
    if key in ("up", "down", "left", "right"):
        # TODO: 既存のプレイヤー移動処理に橋渡しする。
        # 例） move_player(key) などの関数を呼ぶ。
        return

    if key == "e":
        # TODO: Day3 で作った「NPC に話しかける」処理の一部から
        #       start_battle("slime") などを呼び出してみましょう。
        #
        # どの NPC / イベントからどの敵 ID を呼ぶかは、チームで相談して決めて OK です。
        return


if __name__ == "__main__":
    print("Day5 用の main_day5.py です。")
    print("実際のゲームでは、App クラスから setup_battle_layer() / on_key_press() を呼び出して使います。")

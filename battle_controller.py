# -*- coding: utf-8 -*-
"""
battle_controller.py
戦闘は「戦闘だけ」を担当するためのコントローラ。

目的
- フィールド側（main）は「開始を呼ぶ」「キー入力を渡す」「結果を受け取る」だけにする
- 戦闘の中身（ターン進行・計算・表示更新・勝敗）はここで完結させる

入力（最小）
- "a" / "A": 攻撃
- "d" / "D": 防御（次の敵攻撃を軽減）

AIっぽさ（軽量）
- 連続行動（攻撃連打・防御連打）をカウント
- 敵が「癖を読んだ」行動を混ぜる（ため攻撃／ガード崩し）

依存
- status_day4.Status
- battle_engine.calc_damage
- ui.battle_window.BattleWindow（任意：渡されればUIを更新する）
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
import json
import random

from status_day4 import Status
from battle_engine import calc_damage


@dataclass
class BattleResult:
    win: bool
    player_hp: int
    enemy_id: str


class BattleController:
    """
    戦闘の責務をまとめたクラス。

    フィールド側は：
      - controller.start("slime")
      - controller.handle_key("a") / controller.handle_key("d")
      - controller.is_active / controller.last_result を見る
    だけで結合できる。
    """

    def __init__(
        self,
        player_status: Status,
        battle_window=None,
        enemy_db_path: str = "input/enemies_day4.json",
        rng: Optional[random.Random] = None,
    ) -> None:
        self.player: Status = player_status
        self.window = battle_window
        self.enemy_db_path = enemy_db_path
        self.rng = rng or random.Random()

        self.enemy: Optional[Status] = None
        self.enemy_id: str = ""
        self.is_active: bool = False
        self.last_result: Optional[BattleResult] = None

        # --- 連続行動カウント（AIっぽさの種） ---
        self.guard_streak: int = 0   # D連打
        self.attack_streak: int = 0  # A連打

        # --- ターン内の状態 ---
        self._player_guarding: bool = False  # 次の敵攻撃軽減（1ターン限定）
        self._enemy_charging: bool = False   # 「ため」完了フラグ（次の攻撃が強い）

        # --- 調整用パラメータ（授業で触りやすい） ---
        self.crit_rate = 0.10          # 会心率
        self.crit_mul = 1.50           # 会心倍率
        self.miss_rate = 0.08          # 通常攻撃のミス率
        self.variance = 0.20           # ダメージのブレ幅（±20%）

        # AI行動の頻度（読みすぎないように控えめ）
        self.charge_trigger_streak = 3  # Aを3連続で「ため」を混ぜやすく
        self.guard_break_trigger_streak = 2  # Dを2連続で「崩し」を混ぜやすく

        self.p_charge_base = 0.18
        self.p_guard_break_base = 0.22

    # ----------------------------
    # Public API
    # ----------------------------
    def start(self, enemy_id: str) -> None:
        """敵IDから戦闘を開始する。"""
        self.enemy_id = enemy_id
        self.enemy = self._load_enemy(enemy_id)

        self.is_active = True
        self.last_result = None

        # リセット
        self.guard_streak = 0
        self.attack_streak = 0
        self._player_guarding = False
        self._enemy_charging = False

        self._ui_refresh(f"{self.enemy.name} があらわれた！")

    def handle_key(self, key: str) -> None:
        """戦闘中の入力を処理する（A=攻撃, D=防御）。"""
        if not self.is_active or not self.enemy:
            return

        k = (key or "").lower()

        if k == "a":
            self._on_player_attack()
        elif k == "d":
            self._on_player_guard()
        else:
            # 他のキーは無視（授業で拡張可能）
            return

    # ----------------------------
    # Player actions
    # ----------------------------
    def _on_player_attack(self) -> None:
        assert self.enemy is not None

        # 連続行動カウント
        self.attack_streak += 1
        self.guard_streak = 0

        # 防御は1ターン限定なので、攻撃したら解除
        self._player_guarding = False

        dmg, tag = self._deal_damage(attacker=self.player, defender=self.enemy, allow_miss=True)
        if dmg == 0:
            self._ui_refresh(f"{self.player.name} の攻撃！ …外れた！")
        else:
            self._ui_refresh(f"{self.player.name} の攻撃！ {tag}{dmg} ダメージ！")

        # 勝利判定
        if self.enemy.is_dead():
            self._finish(win=True, msg=f"{self.enemy.name} をたおした！")
            return

        # 敵ターン
        self._enemy_turn()

    def _on_player_guard(self) -> None:
        assert self.enemy is not None

        # 連続行動カウント
        self.guard_streak += 1
        self.attack_streak = 0

        # 1ターンだけ守る
        self._player_guarding = True
        self._ui_refresh(f"{self.player.name} はみをまもった！")

        # 敵ターン
        self._enemy_turn()

    # ----------------------------
    # Enemy AI (lightweight)
    # ----------------------------
    def _enemy_turn(self) -> None:
        assert self.enemy is not None

        # すでに「ため」状態なら、強攻撃を放つ（ここが“考えさせる”要）
        if self._enemy_charging:
            self._enemy_charging = False
            self._enemy_attack(power_mul=1.50, msg_prefix="（ため攻撃）")
            return

        # 「癖読み」：プレイヤーの連続行動を見て、行動を変える
        p_charge = self.p_charge_base
        p_guard_break = self.p_guard_break_base

        # A連打が続く → 「ため」を混ぜる（次のターンに強攻撃＝Dを切る判断が生まれる）
        if self.attack_streak >= self.charge_trigger_streak:
            p_charge += 0.22  # 読む強さ

        # D連打が続く → 「ガード崩し」を混ぜる（守りすぎは危ない）
        if self.guard_streak >= self.guard_break_trigger_streak:
            p_guard_break += 0.28

        # 行動選択（ガード崩し優先 → ため → 通常）
        r = self.rng.random()
        if r < p_guard_break:
            self._enemy_guard_break()
        elif r < p_guard_break + p_charge:
            self._enemy_charge()
        else:
            self._enemy_attack()

    def _enemy_charge(self) -> None:
        """次の攻撃が強くなる“ため”。"""
        self._enemy_charging = True
        self._ui_refresh(f"{self.enemy.name} は力をためている…！")

    def _enemy_guard_break(self) -> None:
        """ガード崩し：ガードの軽減を無視しやすい／少し強いが外れやすい。"""
        # ガード崩しは命中が少し低い（外しやすい）
        miss = self.rng.random() < 0.18
        if miss:
            self._ui_refresh(f"{self.enemy.name} のガード崩し！ …しかし外れた！")
            self._player_guarding = False  # 守りは消費（読み合いを成立させる）
            return

        # ガード軽減を「貫通」：防御中でも軽減率を小さくする
        self._enemy_attack(
            power_mul=1.20,
            ignore_guard=True,
            msg_prefix="（ガード崩し）",
        )

    def _enemy_attack(self, power_mul: float = 1.0, ignore_guard: bool = False, msg_prefix: str = "") -> None:
        """敵の攻撃（ガード軽減や会心/ブレを含む）。"""
        assert self.enemy is not None

        # ダメージ計算（敵→プレイヤー）
        dmg, tag = self._deal_damage(attacker=self.enemy, defender=self.player, allow_miss=True)

        # ため攻撃・崩しの倍率
        dmg = int(round(dmg * power_mul))

        # ガード軽減（1回だけ）
        if self._player_guarding:
            if ignore_guard:
                # 貫通：軽減を弱める（完全無視だと理不尽になりがち）
                dmg = int(round(dmg * 0.80))
            else:
                dmg = int(round(dmg * 0.50))
            self._player_guarding = False

        # 実適用（HPは0未満にならない）
        if dmg <= 0:
            self._ui_refresh(f"{self.enemy.name} の攻撃！ …外れた！")
        else:
            self.player.take_damage(dmg)
            self._ui_refresh(f"{self.enemy.name} の攻撃！ {msg_prefix}{tag}{dmg} ダメージ！")

        # 敗北判定
        if self.player.is_dead():
            self._finish(win=False, msg=f"{self.player.name} はたおれた…")
            return

        self._ui_refresh("")  # メッセージは最新で上書きされるので、空でもOK

    # ----------------------------
    # Damage / UI / Finish
    # ----------------------------
    def _deal_damage(self, attacker: Status, defender: Status, allow_miss: bool) -> tuple[int, str]:
        """
        calc_damage をベースに、ブレ・会心・ミスを付与して返す。
        戻り値:
          (damage, tag_text)
        """
        # ミス
        if allow_miss and (self.rng.random() < self.miss_rate):
            return 0, ""

        base = calc_damage(attacker, defender)

        # ブレ（±variance）
        if self.variance > 0:
            lo = 1.0 - self.variance
            hi = 1.0 + self.variance
            base = int(round(base * self.rng.uniform(lo, hi)))

        # 会心
        tag = ""
        if self.rng.random() < self.crit_rate:
            base = int(round(base * self.crit_mul))
            tag = "CRIT!! "

        # 最低1（ミスで0は許可）
        return max(base, 1), tag

    def _finish(self, win: bool, msg: str) -> None:
        """勝敗確定。戦闘を終了して結果を保持する。"""
        if not self.is_active:
            return  # 二重終了防止

        self.is_active = False
        self.last_result = BattleResult(
            win=win,
            player_hp=self.player.hp,
            enemy_id=self.enemy_id,
        )
        self._ui_refresh(msg)

    def _ui_refresh(self, message: str) -> None:
        """UIがある場合だけ更新する。"""
        if self.window and self.enemy:
            try:
                self.window.update_status(self.player, self.enemy)
                if message:
                    self.window.show_message(message)
            except Exception:
                # UI依存で戦闘が止まるのが一番まずいので握りつぶす
                pass

    # ----------------------------
    # Enemy DB
    # ----------------------------
    def _load_enemy(self, enemy_id: str) -> Status:
        try:
            with open(self.enemy_db_path, "r", encoding="utf-8") as f:
                db = json.load(f)
        except Exception:
            db = {}

        if enemy_id not in db:
            # フォールバック（壊れないこと優先）
            return Status(name="なぞの敵", max_hp=12, attack=4, defense=0)

        d = db[enemy_id]
        return Status(
            name=d.get("name", enemy_id),
            max_hp=int(d.get("max_hp", 12)),
            attack=int(d.get("attack", 4)),
            defense=int(d.get("defense", 0)),
        )

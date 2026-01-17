# battle_engine.py
# Day4 用：ダメージ計算と攻撃処理をまとめたモジュール。
#
# 既存API（calc_damage / player_attack / enemy_attack）を壊さないまま、
# Day5以降で「会心・ブレ幅・ミス」などの“楽しい味付け”を追加できるように拡張します。

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Optional

from status_day4 import Status


# ----------------------------
# 既存（Day4）互換API
# ----------------------------
def calc_damage(attacker: Status, defender: Status, base_power: int = 5) -> int:
    """攻撃側と防御側からダメージ量を計算する簡単な式（Day4互換）。"""
    raw = attacker.attack + base_power - defender.defense
    return max(raw, 1)  # 最低1ダメージは入るようにする


def player_attack(player: Status, enemy: Status) -> int:
    """プレイヤーから敵への攻撃（Day4互換）。"""
    dmg = calc_damage(player, enemy)
    enemy.take_damage(dmg)
    return dmg


def enemy_attack(enemy: Status, player: Status) -> int:
    """敵からプレイヤーへの攻撃（Day4互換）。"""
    dmg = calc_damage(enemy, player)
    player.take_damage(dmg)
    return dmg


# ----------------------------
# 拡張（Day5+）: “楽しさ”のための追加API
# ----------------------------
@dataclass(frozen=True)
class BattleTuning:
    """戦闘の味付けパラメータ。小さく調整しやすいようにまとめる。"""
    base_power: int = 5

    # 乱数味付け
    variance_min: float = 0.85   # ダメージ最小倍率
    variance_max: float = 1.15   # ダメージ最大倍率

    # 会心
    crit_chance: float = 0.10    # 10%会心
    crit_multiplier: float = 1.50

    # ミス
    miss_chance: float = 0.05    # 5%ミス（0ダメ）


@dataclass(frozen=True)
class AttackResult:
    """1回の攻撃結果。UIメッセージに使える情報をまとめる。"""
    damage: int
    is_crit: bool = False
    is_miss: bool = False


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def attack(attacker: Status, defender: Status, *, tuning: Optional[BattleTuning] = None, rng: Optional[random.Random] = None) -> AttackResult:
    """会心・ブレ幅・ミスを含む攻撃処理（HPを減らす）。"""
    t = tuning or BattleTuning()
    r = rng or random

    miss_p = _clamp01(t.miss_chance)
    crit_p = _clamp01(t.crit_chance)

    # ミス判定
    if r.random() < miss_p:
        return AttackResult(damage=0, is_crit=False, is_miss=True)

    # ベースダメージ（最低1）
    base = calc_damage(attacker, defender, base_power=t.base_power)

    # ブレ幅
    lo = min(t.variance_min, t.variance_max)
    hi = max(t.variance_min, t.variance_max)
    dmg = int(round(base * r.uniform(lo, hi)))
    dmg = max(dmg, 1)

    # 会心判定
    is_crit = (r.random() < crit_p)
    if is_crit:
        dmg = int(round(dmg * t.crit_multiplier))
        dmg = max(dmg, 1)

    defender.take_damage(dmg)
    return AttackResult(damage=dmg, is_crit=is_crit, is_miss=False)

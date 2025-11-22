# battle_engine.py
# Day4 用：ダメージ計算と攻撃処理をまとめたモジュール。

from status_day4 import Status

def calc_damage(attacker: Status, defender: Status, base_power: int = 5) -> int:
    """攻撃側と防御側からダメージ量を計算する簡単な式。"""
    raw = attacker.attack + base_power - defender.defense
    return max(raw, 1)  # 最低1ダメージは入るようにする

def player_attack(player: Status, enemy: Status) -> int:
    """プレイヤーから敵への攻撃。実際にHPを減らしてダメージ量を返す。"""
    dmg = calc_damage(player, enemy)
    enemy.take_damage(dmg)
    return dmg

def enemy_attack(enemy: Status, player: Status) -> int:
    """敵からプレイヤーへの攻撃。"""
    dmg = calc_damage(enemy, player)
    player.take_damage(dmg)
    return dmg

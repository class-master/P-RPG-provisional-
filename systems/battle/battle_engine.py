# systems/battle/battle_engine.py
# 戦闘の計算ロジックを管理するモジュールです。

import random

def player_attack(player, enemy):
    """
    プレイヤーが敵に攻撃した時のダメージ計算です。
    """
    # 基本ダメージ = 攻撃力 - 防御力（最低1ダメージ）
    base_damage = max(1, player.attack - enemy.defense)
    # 少しのランダム要素（乱数）を加えます
    actual_damage = base_damage + random.randint(0, 2)
    
    enemy.hp -= actual_damage
    if enemy.hp < 0:
        enemy.hp = 0
    return actual_damage

def enemy_attack(enemy, player):
    """
    敵がプレイヤーに攻撃した時のダメージ計算です。
    """
    base_damage = max(1, enemy.attack - player.defense)
    actual_damage = base_damage + random.randint(0, 1)
    
    player.hp -= actual_damage
    if player.hp < 0:
        player.hp = 0
    return actual_damage
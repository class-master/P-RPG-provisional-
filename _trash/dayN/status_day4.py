# status_day4.py
# Day4 用：プレイヤーや敵のステータスを扱うクラス定義。

class Status:
    """プレイヤーや敵のステータスを表すシンプルなクラス。"""

    def __init__(self, name, max_hp, attack, defense=0):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense

    def is_dead(self) -> bool:
        """HPが0以下なら倒れているとみなす。"""
        return self.hp <= 0

    def take_damage(self, amount: int) -> int:
        """ダメージを受けてHPを減らす（0未満にはならない）。"""
        if amount < 0:
            amount = 0
        self.hp = max(self.hp - amount, 0)
        return self.hp

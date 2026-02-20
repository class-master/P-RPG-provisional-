# entities/status.py

class Status:
    """
    キャラクターの状態モデル（HP / 攻撃力など）
    ロジックは持たない。純粋なデータ構造。
    """

    def __init__(self, name: str, max_hp: int, attack: int, defense: int):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense

    def is_dead(self) -> bool:
        """戦闘不能判定"""
        return self.hp <= 0

    def take_damage(self, damage: int):
        """ダメージを受ける（0未満にはならない）"""
        self.hp = max(0, self.hp - damage)

    def heal(self, amount: int):
        """回復（最大HPを超えない）"""
        self.hp = min(self.max_hp, self.hp + amount)

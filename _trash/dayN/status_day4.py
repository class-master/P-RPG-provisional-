# status_day4.py
# Day4 逕ｨ・壹・繝ｬ繧､繝､繝ｼ繧・雰縺ｮ繧ｹ繝・・繧ｿ繧ｹ繧呈桶縺・け繝ｩ繧ｹ螳夂ｾｩ縲・

class Status:
    """繝励Ξ繧､繝､繝ｼ繧・雰縺ｮ繧ｹ繝・・繧ｿ繧ｹ繧定｡ｨ縺吶す繝ｳ繝励Ν縺ｪ繧ｯ繝ｩ繧ｹ縲・""

    def __init__(self, name, max_hp, attack, defense=0):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense

    def is_dead(self) -> bool:
        """HP縺・莉･荳九↑繧牙偵ｌ縺ｦ縺・ｋ縺ｨ縺ｿ縺ｪ縺吶・""
        return self.hp <= 0

    def take_damage(self, amount: int) -> int:
        """繝繝｡繝ｼ繧ｸ繧貞女縺代※HP繧呈ｸ帙ｉ縺呻ｼ・譛ｪ貅縺ｫ縺ｯ縺ｪ繧峨↑縺・ｼ峨・""
        if amount < 0:
            amount = 0
        self.hp = max(self.hp - amount, 0)
        return self.hp

# battle_engine.py
# Day4 逕ｨ・壹ム繝｡繝ｼ繧ｸ險育ｮ励→謾ｻ謦・・逅・ｒ縺ｾ縺ｨ繧√◆繝｢繧ｸ繝･繝ｼ繝ｫ縲・
#
# 譌｢蟄連PI・・alc_damage / player_attack / enemy_attack・峨ｒ螢翫＆縺ｪ縺・∪縺ｾ縲・
# Day5莉･髯阪〒縲御ｼ壼ｿ・・繝悶Ξ蟷・・繝溘せ縲阪↑縺ｩ縺ｮ窶懈･ｽ縺励＞蜻ｳ莉倥￠窶昴ｒ霑ｽ蜉縺ｧ縺阪ｋ繧医≧縺ｫ諡｡蠑ｵ縺励∪縺吶・

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Optional

from status_day4 import Status


# ----------------------------
# 譌｢蟄假ｼ・ay4・我ｺ呈鋤API
# ----------------------------
def calc_damage(attacker: Status, defender: Status, base_power: int = 5) -> int:
    """謾ｻ謦・・縺ｨ髦ｲ蠕｡蛛ｴ縺九ｉ繝繝｡繝ｼ繧ｸ驥上ｒ險育ｮ励☆繧狗ｰ｡蜊倥↑蠑擾ｼ・ay4莠呈鋤・峨・""
    raw = attacker.attack + base_power - defender.defense
    return max(raw, 1)  # 譛菴・繝繝｡繝ｼ繧ｸ縺ｯ蜈･繧九ｈ縺・↓縺吶ｋ


def player_attack(player: Status, enemy: Status) -> int:
    """繝励Ξ繧､繝､繝ｼ縺九ｉ謨ｵ縺ｸ縺ｮ謾ｻ謦・ｼ・ay4莠呈鋤・峨・""
    dmg = calc_damage(player, enemy)
    enemy.take_damage(dmg)
    return dmg


def enemy_attack(enemy: Status, player: Status) -> int:
    """謨ｵ縺九ｉ繝励Ξ繧､繝､繝ｼ縺ｸ縺ｮ謾ｻ謦・ｼ・ay4莠呈鋤・峨・""
    dmg = calc_damage(enemy, player)
    player.take_damage(dmg)
    return dmg


# ----------------------------
# 諡｡蠑ｵ・・ay5+・・ 窶懈･ｽ縺励＆窶昴・縺溘ａ縺ｮ霑ｽ蜉API
# ----------------------------
@dataclass(frozen=True)
class BattleTuning:
    """謌ｦ髣倥・蜻ｳ莉倥￠繝代Λ繝｡繝ｼ繧ｿ縲ょｰ上＆縺剰ｪｿ謨ｴ縺励ｄ縺吶＞繧医≧縺ｫ縺ｾ縺ｨ繧√ｋ縲・""
    base_power: int = 5

    # 荵ｱ謨ｰ蜻ｳ莉倥￠
    variance_min: float = 0.85   # 繝繝｡繝ｼ繧ｸ譛蟆丞咲紫
    variance_max: float = 1.15   # 繝繝｡繝ｼ繧ｸ譛螟ｧ蛟咲紫

    # 莨壼ｿ・
    crit_chance: float = 0.10    # 10%莨壼ｿ・
    crit_multiplier: float = 1.50

    # 繝溘せ
    miss_chance: float = 0.05    # 5%繝溘せ・・繝繝｡・・


@dataclass(frozen=True)
class AttackResult:
    """1蝗槭・謾ｻ謦・ｵ先棡縲６I繝｡繝・そ繝ｼ繧ｸ縺ｫ菴ｿ縺医ｋ諠・ｱ繧偵∪縺ｨ繧√ｋ縲・""
    damage: int
    is_crit: bool = False
    is_miss: bool = False


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def attack(attacker: Status, defender: Status, *, tuning: Optional[BattleTuning] = None, rng: Optional[random.Random] = None) -> AttackResult:
    """莨壼ｿ・・繝悶Ξ蟷・・繝溘せ繧貞性繧謾ｻ謦・・逅・ｼ・P繧呈ｸ帙ｉ縺呻ｼ峨・""
    t = tuning or BattleTuning()
    r = rng or random

    miss_p = _clamp01(t.miss_chance)
    crit_p = _clamp01(t.crit_chance)

    # 繝溘せ蛻､螳・
    if r.random() < miss_p:
        return AttackResult(damage=0, is_crit=False, is_miss=True)

    # 繝吶・繧ｹ繝繝｡繝ｼ繧ｸ・域怙菴・・・
    base = calc_damage(attacker, defender, base_power=t.base_power)

    # 繝悶Ξ蟷・
    lo = min(t.variance_min, t.variance_max)
    hi = max(t.variance_min, t.variance_max)
    dmg = int(round(base * r.uniform(lo, hi)))
    dmg = max(dmg, 1)

    # 莨壼ｿ・愛螳・
    is_crit = (r.random() < crit_p)
    if is_crit:
        dmg = int(round(dmg * t.crit_multiplier))
        dmg = max(dmg, 1)

    defender.take_damage(dmg)
    return AttackResult(damage=dmg, is_crit=is_crit, is_miss=False)

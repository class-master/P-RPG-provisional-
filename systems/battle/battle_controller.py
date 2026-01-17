# -*- coding: utf-8 -*-
"""
battle_controller.py
謌ｦ髣倥・縲梧姶髣倥□縺代阪ｒ諡・ｽ薙☆繧九◆繧√・繧ｳ繝ｳ繝医Ο繝ｼ繝ｩ縲・

逶ｮ逧・
- 繝輔ぅ繝ｼ繝ｫ繝牙・・・ain・峨・縲碁幕蟋九ｒ蜻ｼ縺ｶ縲阪後く繝ｼ蜈･蜉帙ｒ貂｡縺吶阪檎ｵ先棡繧貞女縺大叙繧九阪□縺代↓縺吶ｋ
- 謌ｦ髣倥・荳ｭ霄ｫ・医ち繝ｼ繝ｳ騾ｲ陦後・險育ｮ励・陦ｨ遉ｺ譖ｴ譁ｰ繝ｻ蜍晄風・峨・縺薙％縺ｧ螳檎ｵ舌＆縺帙ｋ

蜈･蜉幢ｼ域怙蟆擾ｼ・
- "a" / "A": 謾ｻ謦・
- "d" / "D": 髦ｲ蠕｡・域ｬ｡縺ｮ謨ｵ謾ｻ謦・ｒ霆ｽ貂幢ｼ・

AI縺｣縺ｽ縺包ｼ郁ｻｽ驥擾ｼ・
- 騾｣邯夊｡悟虚・域判謦・｣謇薙・髦ｲ蠕｡騾｣謇難ｼ峨ｒ繧ｫ繧ｦ繝ｳ繝・
- 謨ｵ縺後檎剿繧定ｪｭ繧薙□縲崎｡悟虚繧呈ｷｷ縺懊ｋ・医◆繧∵判謦・ｼ上ぎ繝ｼ繝牙ｴｩ縺暦ｼ・

萓晏ｭ・
- status_day4.Status
- battle_engine.calc_damage
- ui.battle_window.BattleWindow・井ｻｻ諢擾ｼ壽ｸ｡縺輔ｌ繧後・UI繧呈峩譁ｰ縺吶ｋ・・
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
    謌ｦ髣倥・雋ｬ蜍吶ｒ縺ｾ縺ｨ繧√◆繧ｯ繝ｩ繧ｹ縲・

    繝輔ぅ繝ｼ繝ｫ繝牙・縺ｯ・・
      - controller.start("slime")
      - controller.handle_key("a") / controller.handle_key("d")
      - controller.is_active / controller.last_result 繧定ｦ九ｋ
    縺縺代〒邨仙粋縺ｧ縺阪ｋ縲・
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

        # --- 騾｣邯夊｡悟虚繧ｫ繧ｦ繝ｳ繝茨ｼ・I縺｣縺ｽ縺輔・遞ｮ・・---
        self.guard_streak: int = 0   # D騾｣謇・
        self.attack_streak: int = 0  # A騾｣謇・

        # --- 繧ｿ繝ｼ繝ｳ蜀・・迥ｶ諷・---
        self._player_guarding: bool = False  # 谺｡縺ｮ謨ｵ謾ｻ謦・ｻｽ貂幢ｼ・繧ｿ繝ｼ繝ｳ髯仙ｮ夲ｼ・
        self._enemy_charging: bool = False   # 縲後◆繧√榊ｮ御ｺ・ヵ繝ｩ繧ｰ・域ｬ｡縺ｮ謾ｻ謦・′蠑ｷ縺・ｼ・

        # --- 隱ｿ謨ｴ逕ｨ繝代Λ繝｡繝ｼ繧ｿ・域肢讌ｭ縺ｧ隗ｦ繧翫ｄ縺吶＞・・---
        self.crit_rate = 0.10          # 莨壼ｿ・紫
        self.crit_mul = 1.50           # 莨壼ｿ・咲紫
        self.miss_rate = 0.08          # 騾壼ｸｸ謾ｻ謦・・繝溘せ邇・
        self.variance = 0.20           # 繝繝｡繝ｼ繧ｸ縺ｮ繝悶Ξ蟷・ｼ按ｱ20%・・

        # AI陦悟虚縺ｮ鬆ｻ蠎ｦ・郁ｪｭ縺ｿ縺吶℃縺ｪ縺・ｈ縺・↓謗ｧ縺医ａ・・
        self.charge_trigger_streak = 3  # A繧・騾｣邯壹〒縲後◆繧√阪ｒ豺ｷ縺懊ｄ縺吶￥
        self.guard_break_trigger_streak = 2  # D繧・騾｣邯壹〒縲悟ｴｩ縺励阪ｒ豺ｷ縺懊ｄ縺吶￥

        self.p_charge_base = 0.18
        self.p_guard_break_base = 0.22

    # ----------------------------
    # Public API
    # ----------------------------
    def start(self, enemy_id: str) -> None:
        """謨ｵID縺九ｉ謌ｦ髣倥ｒ髢句ｧ九☆繧九・""
        self.enemy_id = enemy_id
        self.enemy = self._load_enemy(enemy_id)

        self.is_active = True
        self.last_result = None

        # 繝ｪ繧ｻ繝・ヨ
        self.guard_streak = 0
        self.attack_streak = 0
        self._player_guarding = False
        self._enemy_charging = False

        self._ui_refresh(f"{self.enemy.name} 縺後≠繧峨ｏ繧後◆・・)

    def handle_key(self, key: str) -> None:
        """謌ｦ髣倅ｸｭ縺ｮ蜈･蜉帙ｒ蜃ｦ逅・☆繧具ｼ・=謾ｻ謦・ D=髦ｲ蠕｡・峨・""
        if not self.is_active or not self.enemy:
            return

        k = (key or "").lower()

        if k == "a":
            self._on_player_attack()
        elif k == "d":
            self._on_player_guard()
        else:
            # 莉悶・繧ｭ繝ｼ縺ｯ辟｡隕厄ｼ域肢讌ｭ縺ｧ諡｡蠑ｵ蜿ｯ閭ｽ・・
            return

    # ----------------------------
    # Player actions
    # ----------------------------
    def _on_player_attack(self) -> None:
        assert self.enemy is not None

        # 騾｣邯夊｡悟虚繧ｫ繧ｦ繝ｳ繝・
        self.attack_streak += 1
        self.guard_streak = 0

        # 髦ｲ蠕｡縺ｯ1繧ｿ繝ｼ繝ｳ髯仙ｮ壹↑縺ｮ縺ｧ縲∵判謦・＠縺溘ｉ隗｣髯､
        self._player_guarding = False

        dmg, tag = self._deal_damage(attacker=self.player, defender=self.enemy, allow_miss=True)
        if dmg == 0:
            self._ui_refresh(f"{self.player.name} 縺ｮ謾ｻ謦・ｼ・窶ｦ螟悶ｌ縺滂ｼ・)
        else:
            self._ui_refresh(f"{self.player.name} 縺ｮ謾ｻ謦・ｼ・{tag}{dmg} 繝繝｡繝ｼ繧ｸ・・)

        # 蜍晏茜蛻､螳・
        if self.enemy.is_dead():
            self._finish(win=True, msg=f"{self.enemy.name} 繧偵◆縺翫＠縺滂ｼ・)
            return

        # 謨ｵ繧ｿ繝ｼ繝ｳ
        self._enemy_turn()

    def _on_player_guard(self) -> None:
        assert self.enemy is not None

        # 騾｣邯夊｡悟虚繧ｫ繧ｦ繝ｳ繝・
        self.guard_streak += 1
        self.attack_streak = 0

        # 1繧ｿ繝ｼ繝ｳ縺縺大ｮ医ｋ
        self._player_guarding = True
        self._ui_refresh(f"{self.player.name} 縺ｯ縺ｿ繧偵∪繧ゅ▲縺滂ｼ・)

        # 謨ｵ繧ｿ繝ｼ繝ｳ
        self._enemy_turn()

    # ----------------------------
    # Enemy AI (lightweight)
    # ----------------------------
    def _enemy_turn(self) -> None:
        assert self.enemy is not None

        # 縺吶〒縺ｫ縲後◆繧√咲憾諷九↑繧峨∝ｼｷ謾ｻ謦・ｒ謾ｾ縺､・医％縺薙′窶懆・∴縺輔○繧銀晁ｦ・ｼ・
        if self._enemy_charging:
            self._enemy_charging = False
            self._enemy_attack(power_mul=1.50, msg_prefix="・医◆繧∵判謦・ｼ・)
            return

        # 縲檎剿隱ｭ縺ｿ縲搾ｼ壹・繝ｬ繧､繝､繝ｼ縺ｮ騾｣邯夊｡悟虚繧定ｦ九※縲∬｡悟虚繧貞､峨∴繧・
        p_charge = self.p_charge_base
        p_guard_break = self.p_guard_break_base

        # A騾｣謇薙′邯壹￥ 竊・縲後◆繧√阪ｒ豺ｷ縺懊ｋ・域ｬ｡縺ｮ繧ｿ繝ｼ繝ｳ縺ｫ蠑ｷ謾ｻ謦・ｼ戰繧貞・繧句愛譁ｭ縺檎函縺ｾ繧後ｋ・・
        if self.attack_streak >= self.charge_trigger_streak:
            p_charge += 0.22  # 隱ｭ繧蠑ｷ縺・

        # D騾｣謇薙′邯壹￥ 竊・縲後ぎ繝ｼ繝牙ｴｩ縺励阪ｒ豺ｷ縺懊ｋ・亥ｮ医ｊ縺吶℃縺ｯ蜊ｱ縺ｪ縺・ｼ・
        if self.guard_streak >= self.guard_break_trigger_streak:
            p_guard_break += 0.28

        # 陦悟虚驕ｸ謚橸ｼ医ぎ繝ｼ繝牙ｴｩ縺怜━蜈・竊・縺溘ａ 竊・騾壼ｸｸ・・
        r = self.rng.random()
        if r < p_guard_break:
            self._enemy_guard_break()
        elif r < p_guard_break + p_charge:
            self._enemy_charge()
        else:
            self._enemy_attack()

    def _enemy_charge(self) -> None:
        """谺｡縺ｮ謾ｻ謦・′蠑ｷ縺上↑繧銀懊◆繧≫昴・""
        self._enemy_charging = True
        self._ui_refresh(f"{self.enemy.name} 縺ｯ蜉帙ｒ縺溘ａ縺ｦ縺・ｋ窶ｦ・・)

    def _enemy_guard_break(self) -> None:
        """繧ｬ繝ｼ繝牙ｴｩ縺暦ｼ壹ぎ繝ｼ繝峨・霆ｽ貂帙ｒ辟｡隕悶＠繧・☆縺・ｼ丞ｰ代＠蠑ｷ縺・′螟悶ｌ繧・☆縺・・""
        # 繧ｬ繝ｼ繝牙ｴｩ縺励・蜻ｽ荳ｭ縺悟ｰ代＠菴弱＞・亥､悶＠繧・☆縺・ｼ・
        miss = self.rng.random() < 0.18
        if miss:
            self._ui_refresh(f"{self.enemy.name} 縺ｮ繧ｬ繝ｼ繝牙ｴｩ縺暦ｼ・窶ｦ縺励°縺怜､悶ｌ縺滂ｼ・)
            self._player_guarding = False  # 螳医ｊ縺ｯ豸郁ｲｻ・郁ｪｭ縺ｿ蜷医＞繧呈・遶九＆縺帙ｋ・・
            return

        # 繧ｬ繝ｼ繝芽ｻｽ貂帙ｒ縲瑚ｲｫ騾壹搾ｼ夐亟蠕｡荳ｭ縺ｧ繧りｻｽ貂帷紫繧貞ｰ上＆縺上☆繧・
        self._enemy_attack(
            power_mul=1.20,
            ignore_guard=True,
            msg_prefix="・医ぎ繝ｼ繝牙ｴｩ縺暦ｼ・,
        )

    def _enemy_attack(self, power_mul: float = 1.0, ignore_guard: bool = False, msg_prefix: str = "") -> None:
        """謨ｵ縺ｮ謾ｻ謦・ｼ医ぎ繝ｼ繝芽ｻｽ貂帙ｄ莨壼ｿ・繝悶Ξ繧貞性繧・峨・""
        assert self.enemy is not None

        # 繝繝｡繝ｼ繧ｸ險育ｮ暦ｼ域雰竊偵・繝ｬ繧､繝､繝ｼ・・
        dmg, tag = self._deal_damage(attacker=self.enemy, defender=self.player, allow_miss=True)

        # 縺溘ａ謾ｻ謦・・蟠ｩ縺励・蛟咲紫
        dmg = int(round(dmg * power_mul))

        # 繧ｬ繝ｼ繝芽ｻｽ貂幢ｼ・蝗槭□縺托ｼ・
        if self._player_guarding:
            if ignore_guard:
                # 雋ｫ騾夲ｼ夊ｻｽ貂帙ｒ蠑ｱ繧√ｋ・亥ｮ悟・辟｡隕悶□縺ｨ逅・ｸ榊ｰｽ縺ｫ縺ｪ繧翫′縺｡・・
                dmg = int(round(dmg * 0.80))
            else:
                dmg = int(round(dmg * 0.50))
            self._player_guarding = False

        # 螳滄←逕ｨ・・P縺ｯ0譛ｪ貅縺ｫ縺ｪ繧峨↑縺・ｼ・
        if dmg <= 0:
            self._ui_refresh(f"{self.enemy.name} 縺ｮ謾ｻ謦・ｼ・窶ｦ螟悶ｌ縺滂ｼ・)
        else:
            self.player.take_damage(dmg)
            self._ui_refresh(f"{self.enemy.name} 縺ｮ謾ｻ謦・ｼ・{msg_prefix}{tag}{dmg} 繝繝｡繝ｼ繧ｸ・・)

        # 謨怜圏蛻､螳・
        if self.player.is_dead():
            self._finish(win=False, msg=f"{self.player.name} 縺ｯ縺溘♀繧後◆窶ｦ")
            return

        self._ui_refresh("")  # 繝｡繝・そ繝ｼ繧ｸ縺ｯ譛譁ｰ縺ｧ荳頑嶌縺阪＆繧後ｋ縺ｮ縺ｧ縲∫ｩｺ縺ｧ繧０K

    # ----------------------------
    # Damage / UI / Finish
    # ----------------------------
    def _deal_damage(self, attacker: Status, defender: Status, allow_miss: bool) -> tuple[int, str]:
        """
        calc_damage 繧偵・繝ｼ繧ｹ縺ｫ縲√ヶ繝ｬ繝ｻ莨壼ｿ・・繝溘せ繧剃ｻ倅ｸ弱＠縺ｦ霑斐☆縲・
        謌ｻ繧雁､:
          (damage, tag_text)
        """
        # 繝溘せ
        if allow_miss and (self.rng.random() < self.miss_rate):
            return 0, ""

        base = calc_damage(attacker, defender)

        # 繝悶Ξ・按ｱvariance・・
        if self.variance > 0:
            lo = 1.0 - self.variance
            hi = 1.0 + self.variance
            base = int(round(base * self.rng.uniform(lo, hi)))

        # 莨壼ｿ・
        tag = ""
        if self.rng.random() < self.crit_rate:
            base = int(round(base * self.crit_mul))
            tag = "CRIT!! "

        # 譛菴・・医Α繧ｹ縺ｧ0縺ｯ險ｱ蜿ｯ・・
        return max(base, 1), tag

    def _finish(self, win: bool, msg: str) -> None:
        """蜍晄風遒ｺ螳壹よ姶髣倥ｒ邨ゆｺ・＠縺ｦ邨先棡繧剃ｿ晄戟縺吶ｋ縲・""
        if not self.is_active:
            return  # 莠碁㍾邨ゆｺ・亟豁｢

        self.is_active = False
        self.last_result = BattleResult(
            win=win,
            player_hp=self.player.hp,
            enemy_id=self.enemy_id,
        )
        self._ui_refresh(msg)

    def _ui_refresh(self, message: str) -> None:
        """UI縺後≠繧句ｴ蜷医□縺第峩譁ｰ縺吶ｋ縲・""
        if self.window and self.enemy:
            try:
                self.window.update_status(self.player, self.enemy)
                if message:
                    self.window.show_message(message)
            except Exception:
                # UI萓晏ｭ倥〒謌ｦ髣倥′豁｢縺ｾ繧九・縺御ｸ逡ｪ縺ｾ縺壹＞縺ｮ縺ｧ謠｡繧翫▽縺ｶ縺・
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
            # 繝輔か繝ｼ繝ｫ繝舌ャ繧ｯ・亥｣翫ｌ縺ｪ縺・％縺ｨ蜆ｪ蜈茨ｼ・
            return Status(name="縺ｪ縺槭・謨ｵ", max_hp=12, attack=4, defense=0)

        d = db[enemy_id]
        return Status(
            name=d.get("name", enemy_id),
            max_hp=int(d.get("max_hp", 12)),
            attack=int(d.get("attack", 4)),
            defense=int(d.get("defense", 0)),
        )

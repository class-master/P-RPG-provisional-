�ｻｿ# -*- coding: utf-8 -*-
"""
battle_controller.py
隰鯉ｽｦ鬮｣蛟･繝ｻ邵ｲ譴ｧ蟋ｶ鬮｣蛟･笆｡邵ｺ莉｣ﾂ髦ｪ�ｽ定ｫ｡繝ｻ�ｽｽ阮吮��郢ｧ荵昶螺郢ｧ竏壹�ｻ郢ｧ�ｽｳ郢晢ｽｳ郢晏現ﾎ溽ｹ晢ｽｼ郢晢ｽｩ邵ｲ繝ｻ

騾ｶ�ｽｮ騾ｧ繝ｻ
- 郢晁ｼ斐≦郢晢ｽｼ郢晢ｽｫ郢晉甥繝ｻ繝ｻ繝ｻain繝ｻ蟲ｨ繝ｻ邵ｲ遒∝ｹ戊沂荵晢ｽ定惱�ｽｼ邵ｺ�ｽｶ邵ｲ髦ｪﾂ蠕後￥郢晢ｽｼ陷茨ｽ･陷牙ｸ呻ｽ定ｲゑｽ｡邵ｺ蜷ｶﾂ髦ｪﾂ讙趣ｽｵ蜈域｣｡郢ｧ雋槫･ｳ邵ｺ螟ｧ蜿咏ｹｧ荵敖髦ｪ笆｡邵ｺ莉｣竊鍋ｸｺ蜷ｶ�ｽ�
- 隰鯉ｽｦ鬮｣蛟･繝ｻ闕ｳ�ｽｭ髴��ｽｫ繝ｻ蛹ｻ縺｡郢晢ｽｼ郢晢ｽｳ鬨ｾ�ｽｲ髯ｦ蠕後�ｻ髫ｪ閧ｲ�ｽｮ蜉ｱ繝ｻ髯ｦ�ｽｨ驕会ｽｺ隴厄ｽｴ隴��ｽｰ郢晢ｽｻ陷肴刋鬚ｨ繝ｻ蟲ｨ繝ｻ邵ｺ阮呻ｼ�邵ｺ�ｽｧ陞ｳ讙趣ｽｵ闊鯉ｼ�邵ｺ蟶呻ｽ�

陷茨ｽ･陷牙ｹ｢�ｽｼ蝓滓呵氣謫ｾ�ｽｼ繝ｻ
- "a" / "A": 隰ｾ�ｽｻ隰ｦ繝ｻ
- "d" / "D": 鬮ｦ�ｽｲ陟包ｽ｡繝ｻ蝓滂ｽｬ�ｽ｡邵ｺ�ｽｮ隰ｨ�ｽｵ隰ｾ�ｽｻ隰ｦ繝ｻ�ｽ帝怕�ｽｽ雋ょｹ｢�ｽｼ繝ｻ

AI邵ｺ�ｽ｣邵ｺ�ｽｽ邵ｺ蛹��ｽｼ驛��ｽｻ�ｽｽ鬩･謫ｾ�ｽｼ繝ｻ
- 鬨ｾ�ｽ｣驍ｯ螟奇ｽ｡謔溯劒繝ｻ蝓溷愛隰ｦ繝ｻﾂ�ｽ｣隰�阮吶�ｻ鬮ｦ�ｽｲ陟包ｽ｡鬨ｾ�ｽ｣隰�髮｣�ｽｼ蟲ｨ�ｽ堤ｹｧ�ｽｫ郢ｧ�ｽｦ郢晢ｽｳ郢昴�ｻ
- 隰ｨ�ｽｵ邵ｺ蠕個讙主価郢ｧ螳夲ｽｪ�ｽｭ郢ｧ阮吮味邵ｲ蟠趣ｽ｡謔溯劒郢ｧ蜻茨ｽｷ�ｽｷ邵ｺ諛奇ｽ九�ｻ蛹ｻ笳�郢ｧ竏ｵ蛻､隰ｦ繝ｻ�ｽｼ荳翫℃郢晢ｽｼ郢晉甥�ｽｴ�ｽｩ邵ｺ證ｦ�ｽｼ繝ｻ

關捺剌�ｽｭ繝ｻ
- status_day4.Status
- battle_engine.calc_damage
- ui.battle_window.BattleWindow繝ｻ莠包ｽｻ�ｽｻ隲｢謫ｾ�ｽｼ螢ｽ�ｽｸ�ｽ｡邵ｺ霈費ｽ檎ｹｧ蠕後�ｻUI郢ｧ蜻亥ｳｩ隴��ｽｰ邵ｺ蜷ｶ�ｽ九�ｻ繝ｻ
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
    隰鯉ｽｦ鬮｣蛟･繝ｻ髮具ｽｬ陷榊生�ｽ堤ｸｺ�ｽｾ邵ｺ�ｽｨ郢ｧ竏壺螺郢ｧ�ｽｯ郢晢ｽｩ郢ｧ�ｽｹ邵ｲ繝ｻ

    郢晁ｼ斐≦郢晢ｽｼ郢晢ｽｫ郢晉甥繝ｻ邵ｺ�ｽｯ繝ｻ繝ｻ
      - controller.start("slime")
      - controller.handle_key("a") / controller.handle_key("d")
      - controller.is_active / controller.last_result 郢ｧ螳夲ｽｦ荵晢ｽ�
    邵ｺ�｣ｰ邵ｺ莉｣縲帝お莉咏ｲ狗ｸｺ�ｽｧ邵ｺ髦ｪ�ｽ狗ｸｲ繝ｻ
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

        # --- 鬨ｾ�ｽ｣驍ｯ螟奇ｽ｡謔溯劒郢ｧ�ｽｫ郢ｧ�ｽｦ郢晢ｽｳ郢晁肩�ｽｼ繝ｻI邵ｺ�ｽ｣邵ｺ�ｽｽ邵ｺ霈斐�ｻ驕橸ｽｮ繝ｻ繝ｻ---
        self.guard_streak: int = 0   # D鬨ｾ�ｽ｣隰�繝ｻ
        self.attack_streak: int = 0  # A鬨ｾ�ｽ｣隰�繝ｻ

        # --- 郢ｧ�ｽｿ郢晢ｽｼ郢晢ｽｳ陷繝ｻ繝ｻ霑･�ｽｶ隲ｷ繝ｻ---
        self._player_guarding: bool = False  # 隹ｺ�ｽ｡邵ｺ�ｽｮ隰ｨ�ｽｵ隰ｾ�ｽｻ隰ｦ繝ｻ�ｽｻ�ｽｽ雋ょｹ｢�ｽｼ繝ｻ郢ｧ�ｽｿ郢晢ｽｼ郢晢ｽｳ鬮ｯ莉呻ｽｮ螟ｲ�ｽｼ繝ｻ
        self._enemy_charging: bool = False   # 邵ｲ蠕娯螺郢ｧ竏堋讎奇ｽｮ蠕｡�ｽｺ繝ｻ繝ｵ郢晢ｽｩ郢ｧ�ｽｰ繝ｻ蝓滂ｽｬ�ｽ｡邵ｺ�ｽｮ隰ｾ�ｽｻ隰ｦ繝ｻ窶ｲ陟托ｽｷ邵ｺ繝ｻ�ｽｼ繝ｻ

        # --- 髫ｱ�ｽｿ隰ｨ�ｽｴ騾包ｽｨ郢昜ｻ｣ﾎ帷ｹ晢ｽ｡郢晢ｽｼ郢ｧ�ｽｿ繝ｻ蝓溯い隶鯉ｽｭ邵ｺ�ｽｧ髫暦ｽｦ郢ｧ鄙ｫ�ｽ�邵ｺ蜷ｶ�ｼ槭�ｻ繝ｻ---
        self.crit_rate = 0.10          # 闔ｨ螢ｼ�ｽｿ繝ｻ邏ｫ
        self.crit_mul = 1.50           # 闔ｨ螢ｼ�ｽｿ繝ｻﾂ蜥ｲ邏ｫ
        self.miss_rate = 0.08          # 鬨ｾ螢ｼ�ｽｸ�ｽｸ隰ｾ�ｽｻ隰ｦ繝ｻ繝ｻ郢晄ｺ倥○驍�繝ｻ
        self.variance = 0.20           # 郢敖郢晢ｽ｡郢晢ｽｼ郢ｧ�ｽｸ邵ｺ�ｽｮ郢晄じﾎ櫁濤繝ｻ�ｽｼ謖会ｽｱ20%繝ｻ繝ｻ

        # AI髯ｦ謔溯劒邵ｺ�ｽｮ鬯��ｽｻ陟趣ｽｦ繝ｻ驛��ｽｪ�ｽｭ邵ｺ�ｽｿ邵ｺ蜷ｶ邃�邵ｺ�ｽｪ邵ｺ繝ｻ�ｽ育ｸｺ繝ｻ竊楢ｬ暦ｽｧ邵ｺ蛹ｻ�ｽ√�ｻ繝ｻ
        self.charge_trigger_streak = 3  # A郢ｧ繝ｻ鬨ｾ�ｽ｣驍ｯ螢ｹ縲堤ｸｲ蠕娯螺郢ｧ竏堋髦ｪ�ｽ定ｱｺ�ｽｷ邵ｺ諛奇ｽ�邵ｺ蜷ｶ�ｿ･
        self.guard_break_trigger_streak = 2  # D郢ｧ繝ｻ鬨ｾ�ｽ｣驍ｯ螢ｹ縲堤ｸｲ謔滂ｽｴ�ｽｩ邵ｺ蜉ｱﾂ髦ｪ�ｽ定ｱｺ�ｽｷ邵ｺ諛奇ｽ�邵ｺ蜷ｶ�ｿ･

        self.p_charge_base = 0.18
        self.p_guard_break_base = 0.22

    # ----------------------------
    # Public API
    # ----------------------------
    def start(self, enemy_id: str) -> None:
        """隰ｨ�ｽｵID邵ｺ荵晢ｽ芽ｬ鯉ｽｦ鬮｣蛟･�ｽ帝ｫ｢蜿･�ｽｧ荵昶��郢ｧ荵敖繝ｻ""
        self.enemy_id = enemy_id
        self.enemy = self._load_enemy(enemy_id)

        self.is_active = True
        self.last_result = None

        # 郢晢ｽｪ郢ｧ�ｽｻ郢昴�ｻ繝ｨ
        self.guard_streak = 0
        self.attack_streak = 0
        self._player_guarding = False
        self._enemy_charging = False

        self._ui_refresh(f"{self.enemy.name} 邵ｺ蠕娯旺郢ｧ蟲ｨ�ｽ冗ｹｧ蠕娯螺繝ｻ繝ｻ)

    def handle_key(self, key: str) -> None:
        """隰鯉ｽｦ鬮｣蛟��ｽｸ�ｽｭ邵ｺ�ｽｮ陷茨ｽ･陷牙ｸ呻ｽ定怎�ｽｦ騾�繝ｻ笘�郢ｧ蜈ｷ�ｽｼ繝ｻ=隰ｾ�ｽｻ隰ｦ繝ｻ D=鬮ｦ�ｽｲ陟包ｽ｡繝ｻ蟲ｨﾂ繝ｻ""
        if not self.is_active or not self.enemy:
            return

        k = (key or "").lower()

        if k == "a":
            self._on_player_attack()
        elif k == "d":
            self._on_player_guard()
        else:
            # 闔画じ繝ｻ郢ｧ�ｽｭ郢晢ｽｼ邵ｺ�ｽｯ霎滂ｽ｡髫募私�ｽｼ蝓溯い隶鯉ｽｭ邵ｺ�ｽｧ隲｡�ｽ｡陟托ｽｵ陷ｿ�ｽｯ髢ｭ�ｽｽ繝ｻ繝ｻ
            return

    # ----------------------------
    # Player actions
    # ----------------------------
    def _on_player_attack(self) -> None:
        assert self.enemy is not None

        # 鬨ｾ�ｽ｣驍ｯ螟奇ｽ｡謔溯劒郢ｧ�ｽｫ郢ｧ�ｽｦ郢晢ｽｳ郢昴�ｻ
        self.attack_streak += 1
        self.guard_streak = 0

        # 鬮ｦ�ｽｲ陟包ｽ｡邵ｺ�ｽｯ1郢ｧ�ｽｿ郢晢ｽｼ郢晢ｽｳ鬮ｯ莉呻ｽｮ螢ｹ竊醍ｸｺ�ｽｮ邵ｺ�ｽｧ邵ｲ竏ｵ蛻､隰ｦ繝ｻ�ｼ邵ｺ貅假ｽ蛾囓�ｽ｣鬮ｯ�ｽ､
        self._player_guarding = False

        dmg, tag = self._deal_damage(attacker=self.player, defender=self.enemy, allow_miss=True)
        if dmg == 0:
            self._ui_refresh(f"{self.player.name} 邵ｺ�ｽｮ隰ｾ�ｽｻ隰ｦ繝ｻ�ｽｼ繝ｻ遯ｶ�ｽｦ陞滓じ�ｽ檎ｸｺ貊ゑｽｼ繝ｻ)
        else:
            self._ui_refresh(f"{self.player.name} 邵ｺ�ｽｮ隰ｾ�ｽｻ隰ｦ繝ｻ�ｽｼ繝ｻ{tag}{dmg} 郢敖郢晢ｽ｡郢晢ｽｼ郢ｧ�ｽｸ繝ｻ繝ｻ)

        # 陷肴剌闌懆崕�ｽ､陞ｳ繝ｻ
        if self.enemy.is_dead():
            self._finish(win=True, msg=f"{self.enemy.name} 郢ｧ蛛ｵ笳�邵ｺ鄙ｫ�ｼ邵ｺ貊ゑｽｼ繝ｻ)
            return

        # 隰ｨ�ｽｵ郢ｧ�ｽｿ郢晢ｽｼ郢晢ｽｳ
        self._enemy_turn()

    def _on_player_guard(self) -> None:
        assert self.enemy is not None

        # 鬨ｾ�ｽ｣驍ｯ螟奇ｽ｡謔溯劒郢ｧ�ｽｫ郢ｧ�ｽｦ郢晢ｽｳ郢昴�ｻ
        self.guard_streak += 1
        self.attack_streak = 0

        # 1郢ｧ�ｽｿ郢晢ｽｼ郢晢ｽｳ邵ｺ�｣ｰ邵ｺ螟ｧ�ｽｮ蛹ｻ�ｽ�
        self._player_guarding = True
        self._ui_refresh(f"{self.player.name} 邵ｺ�ｽｯ邵ｺ�ｽｿ郢ｧ蛛ｵ竏ｪ郢ｧ繧�笆ｲ邵ｺ貊ゑｽｼ繝ｻ)

        # 隰ｨ�ｽｵ郢ｧ�ｽｿ郢晢ｽｼ郢晢ｽｳ
        self._enemy_turn()

    # ----------------------------
    # Enemy AI (lightweight)
    # ----------------------------
    def _enemy_turn(self) -> None:
        assert self.enemy is not None

        # 邵ｺ蜷ｶ縲堤ｸｺ�ｽｫ邵ｲ蠕娯螺郢ｧ竏堋蜥ｲ諞ｾ隲ｷ荵昶�醍ｹｧ蟲ｨﾂ竏晢ｽｼ�ｽｷ隰ｾ�ｽｻ隰ｦ繝ｻ�ｽ定ｬｾ�ｽｾ邵ｺ�ｽ､繝ｻ蛹ｻ�ｼ�邵ｺ阮吮ｲ遯ｶ諛�ﾂ繝ｻ竏ｴ邵ｺ霈披雷郢ｧ驫ﾂ譎��ｽｦ繝ｻ�ｽｼ繝ｻ
        if self._enemy_charging:
            self._enemy_charging = False
            self._enemy_attack(power_mul=1.50, msg_prefix="繝ｻ蛹ｻ笳�郢ｧ竏ｵ蛻､隰ｦ繝ｻ�ｽｼ繝ｻ)
            return

        # 邵ｲ讙主価髫ｱ�ｽｭ邵ｺ�ｽｿ邵ｲ謳ｾ�ｽｼ螢ｹ繝ｻ郢晢ｽｬ郢ｧ�ｽ､郢晢ｽ､郢晢ｽｼ邵ｺ�ｽｮ鬨ｾ�ｽ｣驍ｯ螟奇ｽ｡謔溯劒郢ｧ螳夲ｽｦ荵昶ｻ邵ｲ竏ｬ�ｽ｡謔溯劒郢ｧ雋橸ｽ､蟲ｨ竏ｴ郢ｧ繝ｻ
        p_charge = self.p_charge_base
        p_guard_break = self.p_guard_break_base

        # A鬨ｾ�ｽ｣隰�阮吮ｲ驍ｯ螢ｹ�ｿ･ 遶翫�ｻ邵ｲ蠕娯螺郢ｧ竏堋髦ｪ�ｽ定ｱｺ�ｽｷ邵ｺ諛奇ｽ九�ｻ蝓滂ｽｬ�ｽ｡邵ｺ�ｽｮ郢ｧ�ｽｿ郢晢ｽｼ郢晢ｽｳ邵ｺ�ｽｫ陟托ｽｷ隰ｾ�ｽｻ隰ｦ繝ｻ�ｽｼ謌ｰ郢ｧ雋槭�ｻ郢ｧ蜿･諢幄ｭ��ｽｭ邵ｺ讙主�ｽ邵ｺ�ｽｾ郢ｧ蠕鯉ｽ九�ｻ繝ｻ
        if self.attack_streak >= self.charge_trigger_streak:
            p_charge += 0.22  # 髫ｱ�ｽｭ郢ｧﾂ陟托ｽｷ邵ｺ繝ｻ

        # D鬨ｾ�ｽ｣隰�阮吮ｲ驍ｯ螢ｹ�ｿ･ 遶翫�ｻ邵ｲ蠕後℃郢晢ｽｼ郢晉甥�ｽｴ�ｽｩ邵ｺ蜉ｱﾂ髦ｪ�ｽ定ｱｺ�ｽｷ邵ｺ諛奇ｽ九�ｻ莠･�ｽｮ蛹ｻ�ｽ顔ｸｺ蜷ｶ邃�邵ｺ�ｽｯ陷奇ｽｱ邵ｺ�ｽｪ邵ｺ繝ｻ�ｽｼ繝ｻ
        if self.guard_streak >= self.guard_break_trigger_streak:
            p_guard_break += 0.28

        # 髯ｦ謔溯劒鬩包ｽｸ隰壽ｩｸ�ｽｼ蛹ｻ縺守ｹ晢ｽｼ郢晉甥�ｽｴ�ｽｩ邵ｺ諤懌煤陷医�ｻ遶翫�ｻ邵ｺ貅假ｽ� 遶翫�ｻ鬨ｾ螢ｼ�ｽｸ�ｽｸ繝ｻ繝ｻ
        r = self.rng.random()
        if r < p_guard_break:
            self._enemy_guard_break()
        elif r < p_guard_break + p_charge:
            self._enemy_charge()
        else:
            self._enemy_attack()

    def _enemy_charge(self) -> None:
        """隹ｺ�ｽ｡邵ｺ�ｽｮ隰ｾ�ｽｻ隰ｦ繝ｻ窶ｲ陟托ｽｷ邵ｺ荳岩�醍ｹｧ驫ﾂ諛岩螺郢ｧ竕ｫﾂ譏ｴﾂ繝ｻ""
        self._enemy_charging = True
        self._ui_refresh(f"{self.enemy.name} 邵ｺ�ｽｯ陷牙ｸ呻ｽ堤ｸｺ貅假ｽ∫ｸｺ�ｽｦ邵ｺ繝ｻ�ｽ狗ｪｶ�ｽｦ繝ｻ繝ｻ)

    def _enemy_guard_break(self) -> None:
        """郢ｧ�ｽｬ郢晢ｽｼ郢晉甥�ｽｴ�ｽｩ邵ｺ證ｦ�ｽｼ螢ｹ縺守ｹ晢ｽｼ郢晏ｳｨ繝ｻ髴��ｽｽ雋ょｸ呻ｽ定ｾ滂ｽ｡髫墓じ�ｼ郢ｧ繝ｻ笘�邵ｺ繝ｻ�ｽｼ荳橸ｽｰ莉｣�ｼ陟托ｽｷ邵ｺ繝ｻ窶ｲ陞滓じ�ｽ檎ｹｧ繝ｻ笘�邵ｺ繝ｻﾂ繝ｻ""
        # 郢ｧ�ｽｬ郢晢ｽｼ郢晉甥�ｽｴ�ｽｩ邵ｺ蜉ｱ繝ｻ陷ｻ�ｽｽ闕ｳ�ｽｭ邵ｺ謔滂ｽｰ莉｣�ｼ闖ｴ蠑ｱ�ｼ槭�ｻ莠･�ｽ､謔ｶ�ｼ郢ｧ繝ｻ笘�邵ｺ繝ｻ�ｽｼ繝ｻ
        miss = self.rng.random() < 0.18
        if miss:
            self._ui_refresh(f"{self.enemy.name} 邵ｺ�ｽｮ郢ｧ�ｽｬ郢晢ｽｼ郢晉甥�ｽｴ�ｽｩ邵ｺ證ｦ�ｽｼ繝ｻ遯ｶ�ｽｦ邵ｺ蜉ｱﾂｰ邵ｺ諤懶ｽ､謔ｶ�ｽ檎ｸｺ貊ゑｽｼ繝ｻ)
            self._player_guarding = False  # 陞ｳ蛹ｻ�ｽ顔ｸｺ�ｽｯ雎ｸ驛��ｽｲ�ｽｻ繝ｻ驛��ｽｪ�ｽｭ邵ｺ�ｽｿ陷ｷ蛹ｻ�ｼ樒ｹｧ蜻医�ｻ驕ｶ荵晢ｼ�邵ｺ蟶呻ｽ九�ｻ繝ｻ
            return

        # 郢ｧ�ｽｬ郢晢ｽｼ郢晁歓�ｽｻ�ｽｽ雋ょｸ呻ｽ堤ｸｲ迹夲ｽｲ�ｽｫ鬨ｾ螢ｹﾂ謳ｾ�ｽｼ螟蝉ｺ溯包ｽ｡闕ｳ�ｽｭ邵ｺ�ｽｧ郢ｧ繧奇ｽｻ�ｽｽ雋ょｸｷ邏ｫ郢ｧ雋橸ｽｰ荳奇ｼ�邵ｺ荳岩��郢ｧ繝ｻ
        self._enemy_attack(
            power_mul=1.20,
            ignore_guard=True,
            msg_prefix="繝ｻ蛹ｻ縺守ｹ晢ｽｼ郢晉甥�ｽｴ�ｽｩ邵ｺ證ｦ�ｽｼ繝ｻ,
        )

    def _enemy_attack(self, power_mul: float = 1.0, ignore_guard: bool = False, msg_prefix: str = "") -> None:
        """隰ｨ�ｽｵ邵ｺ�ｽｮ隰ｾ�ｽｻ隰ｦ繝ｻ�ｽｼ蛹ｻ縺守ｹ晢ｽｼ郢晁歓�ｽｻ�ｽｽ雋ょｸ呻ｽ�闔ｨ螢ｼ�ｽｿ繝ｻ郢晄じﾎ樒ｹｧ雋樊ｧ郢ｧﾂ繝ｻ蟲ｨﾂ繝ｻ""
        assert self.enemy is not None

        # 郢敖郢晢ｽ｡郢晢ｽｼ郢ｧ�ｽｸ髫ｪ閧ｲ�ｽｮ證ｦ�ｽｼ蝓滄峅遶雁�ｵ繝ｻ郢晢ｽｬ郢ｧ�ｽ､郢晢ｽ､郢晢ｽｼ繝ｻ繝ｻ
        dmg, tag = self._deal_damage(attacker=self.enemy, defender=self.player, allow_miss=True)

        # 邵ｺ貅假ｽ∬ｬｾ�ｽｻ隰ｦ繝ｻ繝ｻ陝�ｽｩ邵ｺ蜉ｱ繝ｻ陋溷調邏ｫ
        dmg = int(round(dmg * power_mul))

        # 郢ｧ�ｽｬ郢晢ｽｼ郢晁歓�ｽｻ�ｽｽ雋ょｹ｢�ｽｼ繝ｻ陜玲ｧｭ笆｡邵ｺ謇假ｽｼ繝ｻ
        if self._player_guarding:
            if ignore_guard:
                # 髮具ｽｫ鬨ｾ螟ｲ�ｽｼ螟奇ｽｻ�ｽｽ雋ょｸ呻ｽ定托ｽｱ郢ｧ竏夲ｽ九�ｻ莠･�ｽｮ謔溘�ｻ霎滂ｽ｡髫墓じ笆｡邵ｺ�ｽｨ騾�繝ｻ�ｽｸ讎奇ｽｰ�ｽｽ邵ｺ�ｽｫ邵ｺ�ｽｪ郢ｧ鄙ｫ窶ｲ邵ｺ�ｽ｡繝ｻ繝ｻ
                dmg = int(round(dmg * 0.80))
            else:
                dmg = int(round(dmg * 0.50))
            self._player_guarding = False

        # 陞ｳ貊�竊宣包ｽｨ繝ｻ繝ｻP邵ｺ�ｽｯ0隴幢ｽｪ雋�ﾂ邵ｺ�ｽｫ邵ｺ�ｽｪ郢ｧ蟲ｨ竊醍ｸｺ繝ｻ�ｽｼ繝ｻ
        if dmg <= 0:
            self._ui_refresh(f"{self.enemy.name} 邵ｺ�ｽｮ隰ｾ�ｽｻ隰ｦ繝ｻ�ｽｼ繝ｻ遯ｶ�ｽｦ陞滓じ�ｽ檎ｸｺ貊ゑｽｼ繝ｻ)
        else:
            self.player.take_damage(dmg)
            self._ui_refresh(f"{self.enemy.name} 邵ｺ�ｽｮ隰ｾ�ｽｻ隰ｦ繝ｻ�ｽｼ繝ｻ{msg_prefix}{tag}{dmg} 郢敖郢晢ｽ｡郢晢ｽｼ郢ｧ�ｽｸ繝ｻ繝ｻ)

        # 隰ｨ諤懷恟陋ｻ�ｽ､陞ｳ繝ｻ
        if self.player.is_dead():
            self._finish(win=False, msg=f"{self.player.name} 邵ｺ�ｽｯ邵ｺ貅倪凰郢ｧ蠕娯螺遯ｶ�ｽｦ")
            return

        self._ui_refresh("")  # 郢晢ｽ｡郢昴�ｻ縺晉ｹ晢ｽｼ郢ｧ�ｽｸ邵ｺ�ｽｯ隴崢隴��ｽｰ邵ｺ�ｽｧ闕ｳ鬆大ｶ檎ｸｺ髦ｪ�ｼ�郢ｧ蠕鯉ｽ狗ｸｺ�ｽｮ邵ｺ�ｽｧ邵ｲ竏ｫ�ｽｩ�ｽｺ邵ｺ�ｽｧ郢ｧ�ｼ尻

    # ----------------------------
    # Damage / UI / Finish
    # ----------------------------
    def _deal_damage(self, attacker: Status, defender: Status, allow_miss: bool) -> tuple[int, str]:
        """
        calc_damage 郢ｧ蛛ｵ繝ｻ郢晢ｽｼ郢ｧ�ｽｹ邵ｺ�ｽｫ邵ｲ竏壹Ω郢晢ｽｬ郢晢ｽｻ闔ｨ螢ｼ�ｽｿ繝ｻ繝ｻ郢晄ｺ倥○郢ｧ蜑��ｽｻ蛟��ｽｸ蠑ｱ�ｼ邵ｺ�ｽｦ髴第鱒笘�邵ｲ繝ｻ
        隰鯉ｽｻ郢ｧ髮�ﾂ�ｽ､:
          (damage, tag_text)
        """
        # 郢晄ｺ倥○
        if allow_miss and (self.rng.random() < self.miss_rate):
            return 0, ""

        base = calc_damage(attacker, defender)

        # 郢晄じﾎ槭�ｻ謖会ｽｱvariance繝ｻ繝ｻ
        if self.variance > 0:
            lo = 1.0 - self.variance
            hi = 1.0 + self.variance
            base = int(round(base * self.rng.uniform(lo, hi)))

        # 闔ｨ螢ｼ�ｽｿ繝ｻ
        tag = ""
        if self.rng.random() < self.crit_rate:
            base = int(round(base * self.crit_mul))
            tag = "CRIT!! "

        # 隴崢闖ｴ繝ｻ繝ｻ蛹ｻﾎ醍ｹｧ�ｽｹ邵ｺ�ｽｧ0邵ｺ�ｽｯ髫ｪ�ｽｱ陷ｿ�ｽｯ繝ｻ繝ｻ
        return max(base, 1), tag

    def _finish(self, win: bool, msg: str) -> None:
        """陷肴刋鬚ｨ驕抵ｽｺ陞ｳ螢ｹﾂ繧亥ｧｶ鬮｣蛟･�ｽ帝お繧��ｽｺ繝ｻ�ｼ邵ｺ�ｽｦ驍ｨ蜈域｣｡郢ｧ蜑��ｽｿ譎�謌溽ｸｺ蜷ｶ�ｽ狗ｸｲ繝ｻ""
        if not self.is_active:
            return  # 闔遒√裟驍ｨ繧��ｽｺ繝ｻ莠溯ｱ��ｽ｢

        self.is_active = False
        self.last_result = BattleResult(
            win=win,
            player_hp=self.player.hp,
            enemy_id=self.enemy_id,
        )
        self._ui_refresh(msg)

    def _ui_refresh(self, message: str) -> None:
        """UI邵ｺ蠕娯旺郢ｧ蜿･�｣ｰ�ｽｴ陷ｷ蛹ｻ笆｡邵ｺ隨ｬ蟲ｩ隴��ｽｰ邵ｺ蜷ｶ�ｽ狗ｸｲ繝ｻ""
        if self.window and self.enemy:
            try:
                self.window.update_status(self.player, self.enemy)
                if message:
                    self.window.show_message(message)
            except Exception:
                # UI關捺剌�ｽｭ蛟･縲定ｬ鯉ｽｦ鬮｣蛟･窶ｲ雎��ｽ｢邵ｺ�ｽｾ郢ｧ荵昴�ｻ邵ｺ蠕｡�ｽｸﾂ騾｡�ｽｪ邵ｺ�ｽｾ邵ｺ螢ｹ�ｼ樒ｸｺ�ｽｮ邵ｺ�ｽｧ隰�ｽ｡郢ｧ鄙ｫ笆ｽ邵ｺ�ｽｶ邵ｺ繝ｻ
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
            # 郢晁ｼ斐°郢晢ｽｼ郢晢ｽｫ郢晁�後Ε郢ｧ�ｽｯ繝ｻ莠･�ｽ｣鄙ｫ�ｽ檎ｸｺ�ｽｪ邵ｺ繝ｻ�ｼ�邵ｺ�ｽｨ陷��ｽｪ陷郁肩�ｽｼ繝ｻ
            return Status(name="邵ｺ�ｽｪ邵ｺ讒ｭ繝ｻ隰ｨ�ｽｵ", max_hp=12, attack=4, defense=0)

        d = db[enemy_id]
        return Status(
            name=d.get("name", enemy_id),
            max_hp=int(d.get("max_hp", 12)),
            attack=int(d.get("attack", 4)),
            defense=int(d.get("defense", 0)),
        )

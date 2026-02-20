# systems/battle/battle_controller.py

from entities.status import Status
from systems.battle.battle_engine import BattleEngine


class BattleController:
    """
    戦闘の制御担当（ロジックは持たない）
    - Engineに処理を委譲
    - UIに表示を依頼
    """

    def __init__(self, player: Status, enemy: Status, ui=None):
        self.player = player
        self.enemy = enemy
        self.engine = BattleEngine(player, enemy)
        self.ui = ui
        self._is_finished = False
        self._result = None

    def start(self):
        """戦闘開始処理"""
        if self.ui:
            self.ui.show_message(f"{self.enemy.name} が現れた！")

    def update(self):
        """
        1ターン進行
        """
        if self._is_finished:
            return

        log = self.engine.process_turn()

        if self.ui:
            self.ui.show_message(log)

        if self.engine.is_finished():
            self._is_finished = True
            self._result = self.engine.get_result()

    def is_finished(self) -> bool:
        return self._is_finished

    def get_result(self):
        return self._result

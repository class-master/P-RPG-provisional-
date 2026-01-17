# -*- coding: utf-8 -*-
"""
逶ｮ逧・ 譁ｹ蜷代ｒ譁・ｭ励〒蛻・°繧翫ｄ縺吶￥陦ｨ遉ｺ縺吶ｋ譛蟆上さ繝ｳ繝代せ縲・
莨ｸ縺ｳ縺励ｍ: 逕ｻ蜒上い繧､繧ｳ繝ｳ縺ｫ蟾ｮ縺玲崛縺医◆繧翫√い繝九Γ繝ｼ繧ｷ繝ｧ繝ｳ縺輔○縺溘ｊ縺ｧ縺阪ｋ繧医・
"""
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

ARROWS = {"N":"竊・,"E":"竊・,"S":"竊・,"W":"竊・}  # 笘・ヲ繝ｳ繝・ 縺薙％繧・逕ｻ蜒・縺ｫ螟峨∴繧九・繧ゅい繝ｪ・・

class Compass(MDBoxLayout):
    direction = StringProperty("N")

    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", spacing="4dp", **kwargs)
        self.label = MDLabel(text=self._text(), halign="left")
        self.add_widget(self.label)
        # 笘・ヲ繝ｳ繝・ direction 縺悟､峨ｏ繧九◆縺ｳ縺ｫ _update 繧貞他縺ｶ縺ｨ縲∫判髱｢縺梧怙譁ｰ迥ｶ諷九↓縺ｪ繧九ｈ縲・
        self.bind(direction=lambda *_: self._update())

    def _text(self):
        return f"Dir: {self.direction} {ARROWS.get(self.direction, '?')}"

    def _update(self):
        self.label.text = self._text()

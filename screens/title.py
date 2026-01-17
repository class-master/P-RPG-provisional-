# -*- coding: utf-8 -*-
"""
逶ｮ逧・ Title逕ｻ髱｢縺ｮ譛蟆丞ｮ溯｣・ゅ・繧ｿ繝ｳ1縺､縺ｧ Town 縺ｸ遘ｻ蜍輔〒縺阪ｌ縺ｰOK縲・
蜑肴署: ScreenManager 縺ｫ "town" 縺ｨ縺・≧蜷榊燕縺ｮ逕ｻ髱｢縺檎匳骭ｲ縺輔ｌ縺ｦ縺・ｋ縺薙→縲・
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

class TitleScreen(MDScreen):
    def on_pre_enter(self, *args):
        # 笘・ヲ繝ｳ繝・ 逕ｻ髱｢縺悟・繧狗峩蜑阪↓ UI 繧剃ｽ懊ｋ縺ｨ縲∵綾縺｣縺ｦ縺阪◆譎ゅｂ豈主屓邯ｺ鮗励↓謠上″逶ｴ縺帙ｋ縲・
        self.clear_widgets()
        layout = MDBoxLayout(orientation="vertical", spacing="16dp", padding="24dp")
        layout.add_widget(MDLabel(text="RPG Rustic - MasterB", halign="center", font_style="H4"))
        layout.add_widget(MDLabel(text="Title Screen", halign="center"))
        # 笘・ヲ繝ｳ繝・ 繝懊ち繝ｳ縺ｮ on_release 縺ｧ self.go_town 繧貞他縺ｶ 竊・manager.current 繧呈嶌縺肴鋤縺医ｋ縲・
        layout.add_widget(MDRectangleFlatButton(text="Start (Go Town)", pos_hint={"center_x": 0.5}, on_release=self.go_town))
        self.add_widget(layout)

    def go_town(self, *args):
        self.manager.current = "town"

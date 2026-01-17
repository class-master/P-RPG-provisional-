from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class MessageWindow(BoxLayout):
    # 逕ｻ髱｢荳矩Κ縺ｫ繝｡繝・そ繝ｼ繧ｸ繧定｡ｨ遉ｺ縺吶ｋ繧ｷ繝ｳ繝励Ν縺ｪ繧ｦ繧｣繝ｳ繝峨え
    text = StringProperty("")

    def show_message(self, text_list):
        # 繧ｻ繝ｪ繝輔・繝ｪ繧ｹ繝医ｒ蜿励￠蜿悶ｊ縲∵怙蛻昴・1陦後□縺題｡ｨ遉ｺ縺吶ｋ邁｡譏鍋沿縲・
        if not text_list:
            self.text = ""
            return
        self.text = text_list[0]

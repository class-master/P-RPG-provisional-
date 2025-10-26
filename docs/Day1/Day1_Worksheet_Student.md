# Day1 生徒用ワークシート（RPG Rustic B／Kivy）
## 目標（DoD）
- タイルマップ上をプレイヤが移動（すり抜けOK）
## 手順
1. `pip install kivy kivymd`
2. `python main_day1.py` 起動
3. TODOから1つ以上実装（走る/ミニマップ/看板）
## ヒント
- タイル描画は `Rectangle(texture=..., pos=..., size=(ts,ts))`
- カメラは `Translate(-cam.x,-cam.y)`

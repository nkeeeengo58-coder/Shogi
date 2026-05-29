"""保存・読み込み機能"""
import json
import os
from datetime import datetime


class SaveLoad:
    """保存・読み込みクラス"""

    @staticmethod
    def get_save_dir():
        save_dir = os.path.join(os.path.expanduser("~"), ".shogi_game", "saves")
        os.makedirs(save_dir, exist_ok=True)
        return save_dir

    @staticmethod
    def save_game(save_data, filename=None):
        save_dir = SaveLoad.get_save_dir()

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode = save_data.get('game_mode', 'unknown')
            filename = f"save_{mode}_{timestamp}.json"

        filepath = os.path.join(save_dir, filename)
        save_data['saved_at'] = datetime.now().isoformat()

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

        return filepath

    @staticmethod
    def _ensure_app():
        from PySide6.QtWidgets import QApplication
        return QApplication.instance() or QApplication([])

    @staticmethod
    def load_game(filename=None, parent=None, selector=None):
        save_dir = SaveLoad.get_save_dir()

        if not filename:
            if selector is not None:
                filepath = selector(save_dir)
            else:
                SaveLoad._ensure_app()
                from PySide6.QtWidgets import QFileDialog
                filepath, _ = QFileDialog.getOpenFileName(
                    parent,
                    "保存データを選択",
                    save_dir,
                    "JSON files (*.json);;All files (*)",
                )
            if not filepath:
                return None
        else:
            filepath = os.path.join(save_dir, filename)

        if not os.path.exists(filepath):
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"読み込みエラー: {e}")
            return None

    @staticmethod
    def list_save_files():
        save_dir = SaveLoad.get_save_dir()
        files = []

        for filename in os.listdir(save_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(save_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        files.append(
                            {
                                'filename': filename,
                                'mode': data.get('game_mode'),
                                'difficulty': data.get('difficulty'),
                                'saved_at': data.get('saved_at'),
                            }
                        )
                except Exception:
                    pass

        files.sort(key=lambda x: x.get('saved_at', ''), reverse=True)
        return files

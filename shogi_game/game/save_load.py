"""
保存・読み込み機能
"""
import json
import os
from datetime import datetime
from tkinter import filedialog

class SaveLoad:
    """保存・読み込みクラス"""
    
    @staticmethod
    def get_save_dir():
        """保存ディレクトリを取得"""
        save_dir = os.path.join(os.path.expanduser("~"), ".shogi_game", "saves")
        os.makedirs(save_dir, exist_ok=True)
        return save_dir
    
    @staticmethod
    def save_game(save_data, filename=None):
        """
        ゲームを保存
        
        Args:
            save_data: 保存データ（辞書）
            filename: ファイル名（Noneの場合は自動生成）
        """
        save_dir = SaveLoad.get_save_dir()
        
        if not filename:
            # ファイル名を自動生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode = save_data.get('game_mode', 'unknown')
            filename = f"save_{mode}_{timestamp}.json"
        
        filepath = os.path.join(save_dir, filename)
        
        # タイムスタンプを追加
        save_data['saved_at'] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    @staticmethod
    def load_game(filename=None):
        """
        ゲームを読み込む
        
        Args:
            filename: ファイル名（Noneの場合はダイアログで選択）
        
        Returns:
            dict: 保存データ
        """
        save_dir = SaveLoad.get_save_dir()
        
        if not filename:
            # ファイル選択ダイアログ
            filepath = filedialog.askopenfilename(
                title="保存データを選択",
                initialdir=save_dir,
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
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
        """保存ファイルのリストを取得"""
        save_dir = SaveLoad.get_save_dir()
        files = []
        
        for filename in os.listdir(save_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(save_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        files.append({
                            'filename': filename,
                            'mode': data.get('game_mode'),
                            'difficulty': data.get('difficulty'),
                            'saved_at': data.get('saved_at')
                        })
                except:
                    pass
        
        # 保存日時でソート
        files.sort(key=lambda x: x.get('saved_at', ''), reverse=True)
        return files

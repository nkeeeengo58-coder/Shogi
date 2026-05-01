"""
将棋ゲーム - アプリケーションメインクラス
"""
import tkinter as tk
from tkinter import messagebox
import os
import json
from ui.screens import ModeSelectScreen, DifficultySelectScreen, ConfirmScreen, GameScreen, ResultScreen
from ui.menu import MenuBar
from ui.customize import CustomizeDialog
from game.save_load import SaveLoad

class ShogiApp:
    """将棋ゲームのメインアプリケーションクラス"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("将棋ゲーム")
        self.root.geometry("1024x768")
        
        # 設定を読み込み
        self.config = self.load_config()
        
        # 現在の画面
        self.current_screen = None
        
        # ゲーム状態
        self.game_mode = None  # 'normal' or 'tsume'
        self.difficulty = None  # 'beginner', 'intermediate', 'advanced', 'expert'
        
        # メニューバーを作成
        self.menu_bar = MenuBar(self.root, self)
        
        # モード選択画面を表示
        self.show_mode_select()
    
    def load_config(self):
        """設定を読み込む"""
        config_path = os.path.join(os.path.expanduser("~"), ".shogi_game", "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # デフォルト設定
        return {
            'board_theme': 'default',
            'piece_set': 'default',
            'font_size': 12,
            'sound_enabled': True,
            'highlight_opacity': 0.5
        }
    
    def save_config(self):
        """設定を保存"""
        config_dir = os.path.join(os.path.expanduser("~"), ".shogi_game")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "config.json")
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def clear_screen(self):
        """現在の画面をクリア"""
        if self.current_screen:
            self.current_screen.destroy()
            self.current_screen = None
    
    def show_mode_select(self):
        """モード選択画面を表示"""
        self.clear_screen()
        self.current_screen = ModeSelectScreen(self.root, self)
        self.current_screen.pack(fill=tk.BOTH, expand=True)
    
    def show_difficulty_select(self, mode):
        """難易度選択画面を表示"""
        self.game_mode = mode
        self.clear_screen()
        self.current_screen = DifficultySelectScreen(self.root, self, mode)
        self.current_screen.pack(fill=tk.BOTH, expand=True)
    
    def show_confirm(self, mode, difficulty):
        """確認画面を表示"""
        self.game_mode = mode
        self.difficulty = difficulty
        self.clear_screen()
        self.current_screen = ConfirmScreen(self.root, self, mode, difficulty)
        self.current_screen.pack(fill=tk.BOTH, expand=True)
    
    def start_game(self):
        """ゲームを開始"""
        self.clear_screen()
        self.current_screen = GameScreen(self.root, self, self.game_mode, self.difficulty)
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def show_result_screen(self, result_type, game_mode=None, difficulty=None):
        """結果画面を表示"""
        if game_mode is not None:
            self.game_mode = game_mode
        if difficulty is not None:
            self.difficulty = difficulty

        self.clear_screen()
        self.current_screen = ResultScreen(
            self.root,
            self,
            result_type,
            self.game_mode,
            self.difficulty
        )
        self.current_screen.pack(fill=tk.BOTH, expand=True)
    
    def new_game(self):
        """新規ゲーム"""
        self.show_mode_select()
    
    def save_game(self):
        """ゲームを保存"""
        if self.current_screen and hasattr(self.current_screen, 'get_save_data'):
            save_data = self.current_screen.get_save_data()
            SaveLoad.save_game(save_data)
            messagebox.showinfo("保存", "ゲームを保存しました")
        else:
            messagebox.showwarning("保存", "保存できるゲームがありません")
    
    def load_game(self):
        """ゲームを読み込む"""
        save_data = SaveLoad.load_game()
        if save_data:
            self.game_mode = save_data.get('game_mode')
            self.difficulty = save_data.get('difficulty')
            self.clear_screen()
            self.current_screen = GameScreen(self.root, self, self.game_mode, self.difficulty, save_data)
            self.current_screen.pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showwarning("読み込み", "保存データが見つかりません")
    
    def show_customize(self):
        """UIカスタマイズダイアログを表示"""
        CustomizeDialog(self.root, self)
    
    def run(self):
        """アプリケーションを実行"""
        self.root.mainloop()

"""
UIカスタマイズダイアログ
"""
import tkinter as tk
from tkinter import ttk

class CustomizeDialog:
    """UIカスタマイズダイアログクラス"""
    
    def __init__(self, parent, app):
        """
        Args:
            parent: 親ウィンドウ
            app: アプリケーションインスタンス
        """
        self.app = app
        
        self.window = tk.Toplevel(parent)
        self.window.title("UIカスタマイズ")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()
        
        # ノートブック（タブ）
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 各タブを作成
        self._create_appearance_tab(notebook)
        self._create_sound_tab(notebook)
        
        # ボタンフレーム
        button_frame = tk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="適用", command=self.apply_settings).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="キャンセル", command=self.window.destroy).pack(side=tk.RIGHT)
    
    def _create_appearance_tab(self, notebook):
        """外観タブを作成"""
        tab = tk.Frame(notebook)
        notebook.add(tab, text="外観")
        
        # 盤のテーマ
        tk.Label(tab, text="盤のテーマ:", font=("", 12)).grid(row=0, column=0, sticky=tk.W, padx=20, pady=10)
        self.board_theme_var = tk.StringVar(value=self.app.config.get('board_theme', 'default'))
        board_theme_combo = ttk.Combobox(tab, textvariable=self.board_theme_var, state='readonly')
        board_theme_combo['values'] = ('default', 'classic', 'modern', 'wood')
        board_theme_combo.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 駒画像セット
        tk.Label(tab, text="駒画像セット:", font=("", 12)).grid(row=1, column=0, sticky=tk.W, padx=20, pady=10)
        self.piece_set_var = tk.StringVar(value=self.app.config.get('piece_set', 'default'))
        piece_set_combo = ttk.Combobox(tab, textvariable=self.piece_set_var, state='readonly')
        piece_set_combo['values'] = ('default', 'simple', 'traditional')
        piece_set_combo.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 文字サイズ
        tk.Label(tab, text="文字サイズ:", font=("", 12)).grid(row=2, column=0, sticky=tk.W, padx=20, pady=10)
        self.font_size_var = tk.IntVar(value=self.app.config.get('font_size', 12))
        font_size_scale = tk.Scale(tab, from_=10, to=20, orient=tk.HORIZONTAL, variable=self.font_size_var)
        font_size_scale.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        
        # ハイライト透明度
        tk.Label(tab, text="ハイライト透明度:", font=("", 12)).grid(row=3, column=0, sticky=tk.W, padx=20, pady=10)
        self.highlight_opacity_var = tk.DoubleVar(value=self.app.config.get('highlight_opacity', 0.5))
        opacity_scale = tk.Scale(tab, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.highlight_opacity_var)
        opacity_scale.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
    
    def _create_sound_tab(self, notebook):
        """音声タブを作成"""
        tab = tk.Frame(notebook)
        notebook.add(tab, text="音声")
        
        # 音声ON/OFF
        self.sound_enabled_var = tk.BooleanVar(value=self.app.config.get('sound_enabled', True))
        tk.Checkbutton(tab, text="効果音を有効にする", variable=self.sound_enabled_var, font=("", 12)).pack(anchor=tk.W, padx=20, pady=20)
        
        # 音量
        tk.Label(tab, text="音量:", font=("", 12)).pack(anchor=tk.W, padx=20, pady=10)
        self.volume_var = tk.DoubleVar(value=self.app.config.get('volume', 0.5))
        volume_scale = tk.Scale(tab, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.volume_var, length=300)
        volume_scale.pack(anchor=tk.W, padx=40, pady=10)
    
    def apply_settings(self):
        """設定を適用"""
        self.app.config['board_theme'] = self.board_theme_var.get()
        self.app.config['piece_set'] = self.piece_set_var.get()
        self.app.config['font_size'] = self.font_size_var.get()
        self.app.config['highlight_opacity'] = self.highlight_opacity_var.get()
        self.app.config['sound_enabled'] = self.sound_enabled_var.get()
        self.app.config['volume'] = self.volume_var.get()
        
        self.app.save_config()
        
        # 設定を反映（画面を再描画）
        if self.app.current_screen and hasattr(self.app.current_screen, 'refresh'):
            self.app.current_screen.refresh()
        
        self.window.destroy()

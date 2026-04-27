"""
メニューバー
"""
import tkinter as tk

class MenuBar:
    """メニューバークラス"""
    
    def __init__(self, root, app):
        """
        Args:
            root: ルートウィンドウ
            app: アプリケーションインスタンス
        """
        self.root = root
        self.app = app
        
        # メニューバーを作成
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # ファイルメニュー
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        file_menu.add_command(label="新規ゲーム", command=self.app.new_game)
        file_menu.add_command(label="保存", command=self.app.save_game)
        file_menu.add_command(label="読み込み", command=self.app.load_game)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.root.quit)
        
        # 設定メニュー
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="設定", menu=settings_menu)
        settings_menu.add_command(label="UIカスタマイズ", command=self.app.show_customize)
        
        # ヘルプメニュー
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ヘルプ", menu=help_menu)
        help_menu.add_command(label="操作方法", command=self.show_help)
        help_menu.add_command(label="バージョン情報", command=self.show_about)
    
    def show_help(self):
        """操作方法を表示"""
        help_window = tk.Toplevel(self.root)
        help_window.title("操作方法")
        help_window.geometry("500x400")
        
        text = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text.pack(fill=tk.BOTH, expand=True)
        
        help_text = """
【操作方法】

■ 駒の動かし方
1. 動かしたい駒をクリックして選択
2. 移動先のマスをクリック
3. 成れる場合はダイアログで選択

■ 持ち駒を打つ
1. 持ち駒エリアの駒をクリック
2. 打ちたいマスをクリック

■ メニュー
- 新規ゲーム：新しいゲームを開始
- 保存：現在のゲームを保存
- 読み込み：保存したゲームを読み込む
- UIカスタマイズ：盤や駒の見た目を変更

■ キーボードショートカット
- Ctrl+N：新規ゲーム
- Ctrl+S：保存
- Ctrl+O：読み込み

■ ゲームルール
- 二歩禁止：同じ列に2つの歩を置けません
- 王手放置禁止：王手されたら必ず防ぐ必要があります
- 打ち歩詰め禁止：歩を打って即詰みにはできません
- 行き所のない駒：歩・香・桂を進めない位置には置けません
        """
        
        text.insert(1.0, help_text)
        text.config(state=tk.DISABLED)
    
    def show_about(self):
        """バージョン情報を表示"""
        about_window = tk.Toplevel(self.root)
        about_window.title("バージョン情報")
        about_window.geometry("400x250")
        
        frame = tk.Frame(about_window, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="将棋ゲーム", font=("", 20, "bold")).pack(pady=10)
        tk.Label(frame, text="Version 1.0.0").pack()
        tk.Label(frame, text="").pack(pady=10)
        tk.Label(frame, text="Python + Tkinterで作成された将棋ソフト").pack()
        tk.Label(frame, text="通常将棋と詰将棋の両方を楽しめます").pack()
        
        tk.Button(frame, text="閉じる", command=about_window.destroy).pack(pady=20)

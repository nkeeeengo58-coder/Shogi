"""
各種画面クラス
"""
import tkinter as tk
from tkinter import messagebox
from ui.board_view import BoardView
from game.board import Board
from game.engine import Engine
from game.tsume import TsumeManager
from game.rules import Rules

class ModeSelectScreen(tk.Frame):
    """モード選択画面"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        self.config(bg='#f0f0f0')
        
        # タイトル
        title_label = tk.Label(self, text="将棋ゲーム", font=("", 36, "bold"), bg='#f0f0f0')
        title_label.pack(pady=50)
        
        # モード選択ボタン
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        normal_btn = tk.Button(
            button_frame, 
            text="通常将棋モード", 
            font=("", 18),
            width=20,
            height=3,
            command=lambda: self.app.show_difficulty_select('normal')
        )
        normal_btn.pack(pady=15)
        
        tsume_btn = tk.Button(
            button_frame,
            text="詰将棋モード",
            font=("", 18),
            width=20,
            height=3,
            command=lambda: self.app.show_difficulty_select('tsume')
        )
        tsume_btn.pack(pady=15)


class DifficultySelectScreen(tk.Frame):
    """難易度選択画面"""
    
    DIFFICULTY_LABELS = {
        'beginner': '初級',
        'intermediate': '中級',
        'advanced': '上級',
        'expert': '超上級'
    }
    
    DIFFICULTY_DESCRIPTIONS = {
        'normal': {
            'beginner': '合法手からランダムに選択',
            'intermediate': '1〜2手読み',
            'advanced': '3〜4手読み（ミニマックス）',
            'expert': '4手以上の探索'
        },
        'tsume': {
            'beginner': '1手詰め',
            'intermediate': '3手詰め',
            'advanced': '5手詰め',
            'expert': '7手詰め以上'
        }
    }
    
    def __init__(self, parent, app, mode):
        super().__init__(parent)
        self.app = app
        self.mode = mode
        
        self.config(bg='#f0f0f0')
        
        # タイトル
        mode_text = "通常将棋" if mode == 'normal' else "詰将棋"
        title_label = tk.Label(self, text=f"{mode_text} - 難易度選択", font=("", 28, "bold"), bg='#f0f0f0')
        title_label.pack(pady=40)
        
        # 難易度ボタン
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        for difficulty in ['beginner', 'intermediate', 'advanced', 'expert']:
            label = self.DIFFICULTY_LABELS[difficulty]
            desc = self.DIFFICULTY_DESCRIPTIONS[mode][difficulty]
            
            btn_frame = tk.Frame(button_frame, bg='#f0f0f0')
            btn_frame.pack(pady=10)
            
            btn = tk.Button(
                btn_frame,
                text=label,
                font=("", 16),
                width=15,
                height=2,
                command=lambda d=difficulty: self.app.show_confirm(self.mode, d)
            )
            btn.pack()
            
            desc_label = tk.Label(btn_frame, text=desc, font=("", 10), bg='#f0f0f0', fg='#666')
            desc_label.pack()
        
        # 戻るボタン
        back_btn = tk.Button(
            self,
            text="戻る",
            font=("", 12),
            command=self.app.show_mode_select
        )
        back_btn.pack(pady=20)


class ConfirmScreen(tk.Frame):
    """確認画面"""
    
    def __init__(self, parent, app, mode, difficulty):
        super().__init__(parent)
        self.app = app
        self.mode = mode
        self.difficulty = difficulty
        
        self.config(bg='#f0f0f0')
        
        # 選択内容を表示
        mode_text = "通常将棋" if mode == 'normal' else "詰将棋"
        difficulty_text = DifficultySelectScreen.DIFFICULTY_LABELS[difficulty]
        
        info_frame = tk.Frame(self, bg='#f0f0f0')
        info_frame.pack(expand=True)
        
        tk.Label(info_frame, text="ゲーム設定", font=("", 24, "bold"), bg='#f0f0f0').pack(pady=30)
        
        tk.Label(info_frame, text=f"モード: {mode_text}", font=("", 16), bg='#f0f0f0').pack(pady=10)
        tk.Label(info_frame, text=f"難易度: {difficulty_text}", font=("", 16), bg='#f0f0f0').pack(pady=10)
        
        tk.Label(info_frame, text="", bg='#f0f0f0').pack(pady=20)
        tk.Label(info_frame, text="ゲームを開始しますか？", font=("", 18), bg='#f0f0f0').pack(pady=20)
        
        # ボタン
        button_frame = tk.Frame(info_frame, bg='#f0f0f0')
        button_frame.pack(pady=30)
        
        yes_btn = tk.Button(
            button_frame,
            text="はい",
            font=("", 16),
            width=10,
            height=2,
            command=self.app.start_game
        )
        yes_btn.pack(side=tk.LEFT, padx=20)
        
        no_btn = tk.Button(
            button_frame,
            text="いいえ",
            font=("", 16),
            width=10,
            height=2,
            command=lambda: self.app.show_difficulty_select(self.mode)
        )
        no_btn.pack(side=tk.LEFT, padx=20)


class GameScreen(tk.Frame):
    """ゲーム画面"""
    
    def __init__(self, parent, app, game_mode, difficulty, save_data=None):
        super().__init__(parent)
        self.app = app
        self.game_mode = game_mode
        self.difficulty = difficulty
        
        # ゲームボードを初期化
        if save_data:
            self.board = Board.from_dict(save_data['board'])
        else:
            self.board = Board()
            if game_mode == 'normal':
                self.board.initialize_normal_game()
            elif game_mode == 'tsume':
                # 詰将棋問題を読み込む
                self.tsume_manager = TsumeManager()
                self.current_problem_index = save_data.get('current_problem_index', 0) if save_data else 0
                problem = self.tsume_manager.get_problem(difficulty, self.current_problem_index)
                if problem:
                    self.board = problem.get_board()
                    self.current_problem = problem
                else:
                    messagebox.showwarning("警告", "問題が見つかりません")
                    self.app.show_mode_select()
                    return
        
        # CPUエンジン（通常将棋のみ）
        self.engine = None
        if game_mode == 'normal':
            self.engine = Engine(difficulty)
        
        # 詰将棋用
        self.tsume_manager = None
        self.current_problem = None
        self.current_problem_index = 0
        if game_mode == 'tsume':
            self.tsume_manager = TsumeManager()
        
        # UIを構築
        self._build_ui()
        
        # CPUの手番なら考える
        if game_mode == 'normal' and self.board.turn == 'white':
            self.board_view.set_enabled(False)
            self.after(500, self.cpu_move)
    
    def _build_ui(self):
        """UIを構築"""
        # 上部フレーム（情報表示）
        top_frame = tk.Frame(self, bg='#f0f0f0', height=50)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        mode_text = "通常将棋" if self.game_mode == 'normal' else "詰将棋"
        difficulty_text = DifficultySelectScreen.DIFFICULTY_LABELS[self.difficulty]
        
        self.info_label = tk.Label(
            top_frame,
            text=f"{mode_text} - {difficulty_text}",
            font=("", 14),
            bg='#f0f0f0'
        )
        self.info_label.pack(side=tk.LEFT, padx=20)
        
        self.turn_label = tk.Label(
            top_frame,
            text=self._get_turn_text(),
            font=("", 14, "bold"),
            bg='#f0f0f0'
        )
        self.turn_label.pack(side=tk.RIGHT, padx=20)
        
        # メインフレーム（盤面）
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 盤面ビューを作成
        self.board_view = BoardView(main_frame, self.board, self.app.config, self.on_move)
        self.board_view.pack(fill=tk.BOTH, expand=True)
        
        # 下部フレーム（ボタン）
        bottom_frame = tk.Frame(self, bg='#f0f0f0', height=60)
        bottom_frame.pack(fill=tk.X)
        bottom_frame.pack_propagate(False)
        
        if self.game_mode == 'normal':
            tk.Button(
                bottom_frame,
                text="投了",
                font=("", 12),
                command=self.resign
            ).pack(side=tk.LEFT, padx=10, pady=10)
        elif self.game_mode == 'tsume':
            tk.Button(
                bottom_frame,
                text="正解を見る",
                font=("", 12),
                command=self.show_solution
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            tk.Button(
                bottom_frame,
                text="次の問題",
                font=("", 12),
                command=self.next_problem
            ).pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(
            bottom_frame,
            text="メニューに戻る",
            font=("", 12),
            command=self.back_to_menu
        ).pack(side=tk.RIGHT, padx=10, pady=10)
    
    def _get_turn_text(self):
        """手番テキストを取得"""
        if self.game_mode == 'tsume':
            return "先手（あなた）の手番"
        else:
            if self.board.turn == 'black':
                return "先手（あなた）の手番"
            else:
                return "後手（CPU）の手番"
    
    def on_move(self, move):
        """駒が動かされた時の処理"""
        # ゲームオーバーチェック
        if self.game_mode == 'normal':
            # 詰みチェック
            opponent = 'white' if self.board.turn == 'black' else 'black'
            if Rules.is_checkmate(self.board, opponent):
                winner = "先手" if self.board.turn == 'white' else "後手"
                messagebox.showinfo("ゲーム終了", f"{winner}の勝ちです！")
                return
            
            # 千日手チェック
            if Rules.is_stalemate(self.board):
                messagebox.showinfo("ゲーム終了", "千日手により引き分けです")
                return
            
            # 王手チェック
            if Rules.is_in_check(self.board, self.board.turn):
                self.turn_label.config(text=f"{self._get_turn_text()} - 王手！", fg='red')
            else:
                self.turn_label.config(text=self._get_turn_text(), fg='black')
            
            # CPUの手番
            if self.board.turn == 'white':
                # 入力を無効化してからCPUの手を実行
                self.board_view.set_enabled(False)
                self.after(500, self.cpu_move)
        
        elif self.game_mode == 'tsume':
            # 詰将棋の正解チェック
            opponent = 'white'
            if Rules.is_checkmate(self.board, opponent):
                messagebox.showinfo("正解", "詰みです！正解です！")
                self.next_problem()
            else:
                # 相手の手番（詰将棋では相手も最善手を指す想定）
                if self.board.turn == 'white':
                    # 簡易的に合法手があるかチェック
                    has_move = False
                    for row in range(9):
                        for col in range(9):
                            piece = self.board.get_piece(row, col)
                            if piece and piece.owner == 'white':
                                if Rules.get_piece_moves(self.board, row, col):
                                    has_move = True
                                    break
                        if has_move:
                            break
                    
                    if not has_move:
                        messagebox.showinfo("正解", "正解です！")
                        self.next_problem()
                    else:
                        messagebox.showwarning("不正解", "まだ詰んでいません")
                        self.board.undo_move()
                        self.board_view.refresh()
    
    def cpu_move(self):
        """CPUが手を指す"""
        if self.engine is None:
            return
        
        try:
            move = self.engine.get_best_move(self.board)
            if move:
                self.board.move_piece(move)
                self.board_view.refresh()
                
                # 詰みチェック
                if Rules.is_checkmate(self.board, 'black'):
                    messagebox.showinfo("ゲーム終了", "後手（CPU）の勝ちです")
                    return
                
                # 王手チェック
                if Rules.is_in_check(self.board, 'black'):
                    self.turn_label.config(text=f"{self._get_turn_text()} - 王手！", fg='red')
                else:
                    self.turn_label.config(text=self._get_turn_text(), fg='black')
                
                # プレイヤーの手番になったので入力を有効化
                self.board_view.set_enabled(True)
            else:
                messagebox.showinfo("ゲーム終了", "先手（あなた）の勝ちです")
                self.board_view.set_enabled(True)
        except Exception as e:
            messagebox.showerror("エラー", f"CPU処理中にエラーが発生しました:\n{str(e)}")
            import traceback
            traceback.print_exc()
            self.board_view.set_enabled(True)
    
    def resign(self):
        """投了"""
        result = messagebox.askyesno("投了", "投了しますか？")
        if result:
            messagebox.showinfo("ゲーム終了", "あなたの負けです")
            self.app.show_mode_select()
    
    def show_solution(self):
        """正解を表示"""
        if self.current_problem:
            messagebox.showinfo("正解手順", "正解手順の表示機能は未実装です")
    
    def next_problem(self):
        """次の問題へ"""
        if self.tsume_manager:
            self.current_problem_index += 1
            problem = self.tsume_manager.get_problem(self.difficulty, self.current_problem_index)
            
            if problem:
                self.board = problem.get_board()
                self.current_problem = problem
                self.board_view.set_board(self.board)
                self.board_view.refresh()
                self.turn_label.config(text=self._get_turn_text())
            else:
                messagebox.showinfo("完了", "全ての問題をクリアしました！")
                self.app.show_mode_select()
    
    def back_to_menu(self):
        """メニューに戻る"""
        result = messagebox.askyesno("確認", "ゲームを終了してメニューに戻りますか？")
        if result:
            self.app.show_mode_select()
    
    def get_save_data(self):
        """保存データを取得"""
        data = {
            'game_mode': self.game_mode,
            'difficulty': self.difficulty,
            'board': self.board.to_dict()
        }
        
        if self.game_mode == 'tsume':
            data['current_problem_index'] = self.current_problem_index
        
        return data
    
    def refresh(self):
        """画面を再描画"""
        self.board_view.refresh()

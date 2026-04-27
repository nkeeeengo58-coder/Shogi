"""
将棋ゲーム - メインエントリーポイント
"""
import sys
from app import ShogiApp

def main():
    """アプリケーションを起動"""
    app = ShogiApp()
    app.run()

if __name__ == "__main__":
    main()

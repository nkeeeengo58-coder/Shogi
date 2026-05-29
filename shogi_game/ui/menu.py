"""PySide6メニューバー"""
from PySide6.QtWidgets import QMessageBox


class MenuBar:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        menubar = root.menuBar()

        file_menu = menubar.addMenu("ファイル")
        file_menu.addAction("新規ゲーム", self.app.new_game)
        file_menu.addAction("保存", self.app.save_game)
        file_menu.addAction("読み込み", self.app.load_game)
        file_menu.addSeparator()
        file_menu.addAction("終了", self.root.close)

        settings_menu = menubar.addMenu("設定")
        settings_menu.addAction("UIカスタマイズ", self.app.show_customize)

        help_menu = menubar.addMenu("ヘルプ")
        help_menu.addAction("操作方法", self.show_help)
        help_menu.addAction("バージョン情報", self.show_about)

    def show_info(self, title, message):
        QMessageBox.information(self.root, title, message)

    def show_warning(self, title, message):
        QMessageBox.warning(self.root, title, message)

    def show_help(self):
        QMessageBox.information(
            self.root,
            "操作方法",
            "駒の移動は画面の案内に従って操作してください。\n"
            "新規ゲーム・保存・読み込みはメニューから実行できます。",
        )

    def show_about(self):
        QMessageBox.information(
            self.root,
            "バージョン情報",
            "将棋ゲーム\nVersion 1.0.0\nPython + PySide6で作成された将棋ソフト",
        )

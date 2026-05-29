"""UIカスタマイズダイアログ"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class CustomizeDialog(QDialog):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("UIカスタマイズ")
        self.resize(500, 400)

        root_layout = QVBoxLayout(self)
        tabs = QTabWidget(self)
        root_layout.addWidget(tabs)

        appearance_tab = QWidget()
        appearance_form = QFormLayout(appearance_tab)
        self.board_theme = QComboBox()
        self.board_theme.addItems(['default', 'wood', 'modern'])
        self.board_theme.setCurrentText(self.app.config.get('board_theme', 'default'))
        appearance_form.addRow("盤のテーマ", self.board_theme)

        self.piece_set = QComboBox()
        self.piece_set.addItems(['default', 'traditional', 'modern'])
        self.piece_set.setCurrentText(self.app.config.get('piece_set', 'default'))
        appearance_form.addRow("駒画像セット", self.piece_set)

        self.font_size = QSpinBox()
        self.font_size.setRange(10, 20)
        self.font_size.setValue(self.app.config.get('font_size', 12))
        appearance_form.addRow("文字サイズ", self.font_size)

        self.highlight_opacity = QDoubleSpinBox()
        self.highlight_opacity.setRange(0.1, 1.0)
        self.highlight_opacity.setSingleStep(0.1)
        self.highlight_opacity.setValue(self.app.config.get('highlight_opacity', 0.5))
        appearance_form.addRow("ハイライト透明度", self.highlight_opacity)

        tabs.addTab(appearance_tab, "表示")

        sound_tab = QWidget()
        sound_form = QFormLayout(sound_tab)
        self.sound_enabled = QCheckBox("効果音を有効にする")
        self.sound_enabled.setChecked(self.app.config.get('sound_enabled', True))
        self.volume = QDoubleSpinBox()
        self.volume.setRange(0.0, 1.0)
        self.volume.setSingleStep(0.1)
        self.volume.setValue(self.app.config.get('volume', 0.5))
        sound_form.addRow(self.sound_enabled)
        sound_form.addRow("音量", self.volume)
        tabs.addTab(sound_tab, "音声")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.apply_settings)
        buttons.rejected.connect(self.reject)
        root_layout.addWidget(buttons)

    def apply_settings(self):
        self.app.config.update(
            {
                'board_theme': self.board_theme.currentText(),
                'piece_set': self.piece_set.currentText(),
                'font_size': self.font_size.value(),
                'highlight_opacity': self.highlight_opacity.value(),
                'sound_enabled': self.sound_enabled.isChecked(),
                'volume': self.volume.value(),
            }
        )
        self.app.save_config()
        self.accept()

# -*- mode: python ; coding: utf-8 -*-
"""
将棋ゲーム PyInstaller設定ファイル

使用方法:
    pyinstaller shogi_game.spec
"""

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),           # 画像ファイルを含める
        ('data', 'data'),                # 詰将棋問題を含める
    ],
    hiddenimports=[
        'PIL._tkinter_finder',          # Pillowのtkinter連携
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',                    # 不要なモジュールを除外
        'numpy',
        'pandas',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='将棋ゲーム',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,              # コンソールウィンドウを表示しない
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/shogi_icon.ico'  # アイコンを設定
)

# ディレクトリ版を作成する場合は以下をコメント解除
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='将棋ゲーム',
# )

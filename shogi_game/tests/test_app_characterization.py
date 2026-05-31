from types import SimpleNamespace

import app as app_module


class FakeRoot:
    def __init__(self):
        self.window_title = None
        self.window_geometry = None
        self.menu = None
        self.mainloop_called = False

    def title(self, value):
        self.window_title = value

    def geometry(self, value):
        self.window_geometry = value

    def config(self, **kwargs):
        self.menu = kwargs.get('menu')

    def mainloop(self):
        self.mainloop_called = True


class FakeScreen:
    def __init__(self, parent, app, *args):
        self.parent = parent
        self.app = app
        self.args = args
        self.pack_calls = []
        self.destroy_called = False

    def pack(self, **kwargs):
        self.pack_calls.append(kwargs)

    def destroy(self):
        self.destroy_called = True


class FakeModeSelectScreen(FakeScreen):
    pass


class FakeDifficultySelectScreen(FakeScreen):
    pass


class FakeConfirmScreen(FakeScreen):
    pass


class FakeGameScreen(FakeScreen):
    pass


class FakeResultScreen(FakeScreen):
    pass


def create_app(monkeypatch):
    fake_root = FakeRoot()
    menu_instances = []

    monkeypatch.setattr(app_module.tk, 'Tk', lambda: fake_root)
    monkeypatch.setattr(app_module, 'MenuBar', lambda root, app: menu_instances.append((root, app)) or SimpleNamespace())
    monkeypatch.setattr(app_module.ShogiApp, 'load_config', lambda self: {'sound_enabled': True})
    monkeypatch.setattr(app_module, 'ModeSelectScreen', FakeModeSelectScreen)
    monkeypatch.setattr(app_module, 'DifficultySelectScreen', FakeDifficultySelectScreen)
    monkeypatch.setattr(app_module, 'ConfirmScreen', FakeConfirmScreen)
    monkeypatch.setattr(app_module, 'GameScreen', FakeGameScreen)
    monkeypatch.setattr(app_module, 'ResultScreen', FakeResultScreen)

    return app_module.ShogiApp(), fake_root, menu_instances


def test_app_initializes_root_and_mode_select_screen(monkeypatch):
    application, fake_root, menu_instances = create_app(monkeypatch)

    assert fake_root.window_title == '将棋ゲーム'
    assert fake_root.window_geometry == '1024x768'
    assert len(menu_instances) == 1
    assert isinstance(application.current_screen, FakeModeSelectScreen)
    assert application.current_screen.pack_calls == [{'fill': 'both', 'expand': True}]


def test_screen_transitions_replace_current_screen(monkeypatch):
    application, _, _ = create_app(monkeypatch)
    initial_screen = application.current_screen

    application.show_difficulty_select('normal')
    difficulty_screen = application.current_screen
    assert initial_screen.destroy_called is True
    assert isinstance(difficulty_screen, FakeDifficultySelectScreen)
    assert difficulty_screen.args == ('normal',)
    assert application.game_mode == 'normal'

    application.show_confirm('tsume', 'expert')
    confirm_screen = application.current_screen
    assert difficulty_screen.destroy_called is True
    assert isinstance(confirm_screen, FakeConfirmScreen)
    assert confirm_screen.args == ('tsume', 'expert')
    assert application.game_mode == 'tsume'
    assert application.difficulty == 'expert'

    application.start_game()
    game_screen = application.current_screen
    assert confirm_screen.destroy_called is True
    assert isinstance(game_screen, FakeGameScreen)
    assert game_screen.args == ('tsume', 'expert')

    application.show_result_screen('win', 'normal', 'beginner')
    result_screen = application.current_screen
    assert game_screen.destroy_called is True
    assert isinstance(result_screen, FakeResultScreen)
    assert result_screen.args == ('win', 'normal', 'beginner')


def test_save_game_uses_current_screen_save_data(monkeypatch):
    application, _, _ = create_app(monkeypatch)
    calls = []
    infos = []

    application.current_screen = SimpleNamespace(get_save_data=lambda: {'game_mode': 'normal'})
    monkeypatch.setattr(app_module.SaveLoad, 'save_game', lambda payload: calls.append(payload))
    monkeypatch.setattr(app_module.messagebox, 'showinfo', lambda title, message: infos.append((title, message)))

    application.save_game()

    assert calls == [{'game_mode': 'normal'}]
    assert infos == [('保存', 'ゲームを保存しました')]


def test_load_game_creates_game_screen_from_save_data(monkeypatch):
    application, _, _ = create_app(monkeypatch)
    load_payload = {'game_mode': 'normal', 'difficulty': 'advanced', 'board': {'state': 'ignored'}}
    call_arguments = []

    monkeypatch.setattr(
        app_module.SaveLoad,
        'load_game',
        lambda **kwargs: call_arguments.append(kwargs) or load_payload,
    )

    application.load_game()

    assert call_arguments == [{'file_selector': application.select_save_file}]
    assert isinstance(application.current_screen, FakeGameScreen)
    assert application.current_screen.args == ('normal', 'advanced', load_payload)
    assert application.game_mode == 'normal'
    assert application.difficulty == 'advanced'


def test_load_game_warns_when_save_is_missing(monkeypatch):
    application, _, _ = create_app(monkeypatch)
    warnings = []

    monkeypatch.setattr(app_module.SaveLoad, 'load_game', lambda **kwargs: None)
    monkeypatch.setattr(app_module.messagebox, 'showwarning', lambda title, message: warnings.append((title, message)))

    application.load_game()

    assert warnings == [('読み込み', '保存データが見つかりません')]


def test_select_save_file_uses_tkinter_dialog(monkeypatch):
    application, _, _ = create_app(monkeypatch)
    dialog_calls = []

    monkeypatch.setattr(
        app_module.filedialog,
        'askopenfilename',
        lambda **kwargs: dialog_calls.append(kwargs) or '/tmp/example.json',
    )

    selected = application.select_save_file('/tmp/saves', [('JSON files', '*.json')])

    assert selected == '/tmp/example.json'
    assert dialog_calls == [{
        'title': '保存データを選択',
        'initialdir': '/tmp/saves',
        'filetypes': [('JSON files', '*.json')],
    }]

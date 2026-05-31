import json

from game.save_load import SaveLoad


def test_save_game_persists_timestamped_json(tmp_path, monkeypatch):
    monkeypatch.setattr(SaveLoad, 'get_save_dir', staticmethod(lambda: str(tmp_path)))
    save_data = {'game_mode': 'normal', 'difficulty': 'beginner'}

    output_path = SaveLoad.save_game(save_data, filename='sample.json')

    assert output_path == str(tmp_path / 'sample.json')
    assert 'saved_at' in save_data

    persisted = json.loads((tmp_path / 'sample.json').read_text(encoding='utf-8'))
    assert persisted['game_mode'] == 'normal'
    assert persisted['difficulty'] == 'beginner'
    assert persisted['saved_at'] == save_data['saved_at']


def test_load_game_reads_named_file_from_save_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(SaveLoad, 'get_save_dir', staticmethod(lambda: str(tmp_path)))
    expected = {'game_mode': 'tsume', 'difficulty': 'expert'}
    (tmp_path / 'existing.json').write_text(json.dumps(expected, ensure_ascii=False), encoding='utf-8')

    loaded = SaveLoad.load_game('existing.json')

    assert loaded == expected


def test_load_game_uses_dialog_selection_when_filename_is_omitted(tmp_path, monkeypatch):
    monkeypatch.setattr(SaveLoad, 'get_save_dir', staticmethod(lambda: str(tmp_path)))
    expected = {'game_mode': 'normal', 'difficulty': 'advanced'}
    dialog_target = tmp_path / 'dialog-save.json'
    dialog_target.write_text(json.dumps(expected, ensure_ascii=False), encoding='utf-8')
    dialog_calls = []

    loaded = SaveLoad.load_game(
        file_selector=lambda **kwargs: dialog_calls.append(kwargs) or str(dialog_target),
    )

    assert loaded == expected
    assert dialog_calls == [{
        'initialdir': str(tmp_path),
        'filetypes': [('JSON files', '*.json'), ('All files', '*.*')],
    }]


def test_load_game_returns_none_without_selector_or_filename(tmp_path, monkeypatch):
    monkeypatch.setattr(SaveLoad, 'get_save_dir', staticmethod(lambda: str(tmp_path)))

    assert SaveLoad.load_game() is None


def test_list_save_files_returns_newest_first(tmp_path, monkeypatch):
    monkeypatch.setattr(SaveLoad, 'get_save_dir', staticmethod(lambda: str(tmp_path)))
    older = {
        'game_mode': 'normal',
        'difficulty': 'beginner',
        'saved_at': '2026-05-31T10:00:00',
    }
    newer = {
        'game_mode': 'tsume',
        'difficulty': 'expert',
        'saved_at': '2026-05-31T11:00:00',
    }
    (tmp_path / 'older.json').write_text(json.dumps(older, ensure_ascii=False), encoding='utf-8')
    (tmp_path / 'newer.json').write_text(json.dumps(newer, ensure_ascii=False), encoding='utf-8')

    listed = SaveLoad.list_save_files()

    assert listed == [
        {
            'filename': 'newer.json',
            'mode': 'tsume',
            'difficulty': 'expert',
            'saved_at': '2026-05-31T11:00:00',
        },
        {
            'filename': 'older.json',
            'mode': 'normal',
            'difficulty': 'beginner',
            'saved_at': '2026-05-31T10:00:00',
        },
    ]
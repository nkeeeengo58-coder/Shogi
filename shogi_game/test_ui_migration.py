import ast
import os
import tempfile
import unittest
from pathlib import Path

from game.save_load import SaveLoad


class TkinterRemovalTests(unittest.TestCase):
    def test_python_sources_do_not_import_tkinter(self):
        project_root = Path(__file__).resolve().parent
        offenders = []

        for path in project_root.rglob('*.py'):
            if path.name.startswith('test_'):
                continue
            source = path.read_text(encoding='utf-8')
            tree = ast.parse(source, filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == 'tkinter' or alias.name.startswith('tkinter.'):
                            offenders.append(str(path.relative_to(project_root)))
                elif isinstance(node, ast.ImportFrom):
                    if node.module == 'tkinter' or (node.module and node.module.startswith('tkinter.')):
                        offenders.append(str(path.relative_to(project_root)))

        self.assertEqual(sorted(set(offenders)), [])


class SaveLoadQtBehaviorTests(unittest.TestCase):
    def test_load_game_supports_dialog_selector_override(self):
        with tempfile.TemporaryDirectory() as tmp_home:
            original_home = os.environ.get('HOME')
            os.environ['HOME'] = tmp_home
            try:
                payload = {'game_mode': 'normal', 'difficulty': 'beginner'}
                saved_path = SaveLoad.save_game(payload.copy(), filename='manual.json')

                loaded = SaveLoad.load_game(selector=lambda _save_dir: saved_path)
                self.assertIsNotNone(loaded)
                self.assertEqual(loaded['game_mode'], 'normal')
                self.assertEqual(loaded['difficulty'], 'beginner')
            finally:
                if original_home is None:
                    os.environ.pop('HOME', None)
                else:
                    os.environ['HOME'] = original_home


if __name__ == '__main__':
    unittest.main()

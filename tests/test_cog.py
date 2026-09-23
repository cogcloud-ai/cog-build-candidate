import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
import cog_core

class BuildContractTests(unittest.TestCase):
    def test_invalid_input_never_materializes(self):
        for bundle in ({}, {'author_request': None}, {'command': 'anything'}):
            with self.subTest(bundle=bundle), patch.object(cog_core.task_logic, 'run') as run:
                result = cog_core.invoke(bundle)
                self.assertFalse(result['ok'])
                run.assert_not_called()

    def test_changed_contract_acceptance_never_materializes(self):
        bundle = json.loads((ROOT/'examples/sample-bundle.json').read_text())
        bundle['accepted_contract_sha256'] = '0'*64
        with patch.object(cog_core.task_logic, 'run') as run:
            result = cog_core.invoke(bundle)
        self.assertFalse(result['ok'])
        self.assertEqual(result['problems'][0]['check'], 'build-contract')
        run.assert_not_called()

    def test_sample_is_valid_input(self):
        bundle = json.loads((ROOT/'examples/sample-bundle.json').read_text())
        self.assertEqual(cog_core.validate_input(bundle), [])

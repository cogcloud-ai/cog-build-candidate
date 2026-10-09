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

    def test_receipt_schema_accepts_valid_shape_and_refuses_malformed(self):
        import jsonschema
        schema = json.loads((ROOT / 'context/input-schema.json').read_text())['properties']['author_request']['properties']['revision']
        receipt = {'schema': 'openteams/cog-revision [0.1]', 'accepted_contract_sha256': 'a'*64,
                   'candidate_sha256': 'b'*64, 'review_request': {}, 'review_envelope': {},
                   'review_sha256': 'c'*64, 'allowed_change_scope': {'paths': ['src/task_logic.py'], 'criterion_ids': ['criterion']}}
        jsonschema.validate(receipt, schema)
        bundle=json.loads((ROOT/'examples/sample-bundle.json').read_text())
        bundle['author_request']['operation']='revise'
        bundle['author_request']['revision']=receipt
        self.assertEqual(cog_core.validate_input(bundle),[])
        receipt['candidate_sha256'] = 'bad'
        self.assertTrue(cog_core.validate_input(bundle))
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(receipt, schema)

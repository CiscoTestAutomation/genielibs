import unittest
from unittest.mock import MagicMock

from genie.libs.clean.stages.iosxe.sdwan.stages import Connect
from genie.metaparser.util.exceptions import SchemaError
from genie.metaparser.util.schemaengine import Schema
from pyats.aetest.steps import Steps
from pyats.results import Passed


class TestConnect(unittest.TestCase):

    def setUp(self):
        self.stage = Connect()
        self.device = MagicMock()
        self.device.name = 'PE1'
        self.device.connect.return_value = ''

    def test_schema_accepts_logout_false(self):
        validated = Schema(self.stage.schema).validate({'logout': False})

        self.assertFalse(validated['logout'])

    def test_schema_allows_logout_to_be_omitted(self):
        validated = Schema(self.stage.schema).validate({'timeout': 200})

        self.assertNotIn('logout', validated)
        self.assertFalse(self.stage.LOGOUT)

    def test_schema_rejects_non_boolean_logout(self):
        with self.assertRaises(SchemaError):
            Schema(self.stage.schema).validate({'logout': 'false'})

    def test_logout_true_is_rejected(self):
        steps = Steps()

        with self.assertRaisesRegex(
                ValueError, "'logout: true' is not supported"):
            self.stage.connect(
                steps=steps,
                device=self.device,
                logout=True,
            )

        self.device.connect.assert_not_called()

    def test_logout_false_preserves_connection(self):
        steps = Steps()

        self.stage.connect(
            steps=steps,
            device=self.device,
            logout=False,
        )

        self.assertEqual(Passed, steps.details[0].result)
        self.device.destroy_all.assert_not_called()
        self.device.logout.assert_not_called()

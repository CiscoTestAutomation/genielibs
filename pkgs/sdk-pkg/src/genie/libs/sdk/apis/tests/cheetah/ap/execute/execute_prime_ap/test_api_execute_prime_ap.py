import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from pyats.topology import loader
from unicon.eal.dialogs import Dialog
from genie.libs.sdk.apis.cheetah.ap.execute import execute_prime_ap


class TestExecutePrimeAp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          AP188B.4500.5EE8:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os cheetah --mock_data_dir mock_data --state connect
                protocol: unknown
            os: cheetah
            platform: ap
            type: AP
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['AP188B.4500.5EE8']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_prime_ap(self):
        result = execute_prime_ap(self.device, '9.4.62.51', 'vidya-ewlc-5')
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_execute_prime_ap_adds_confirmation_dialog(self):
        device = SimpleNamespace(
            name="AP",
            execute=Mock(),
        )

        result = execute_prime_ap(device, '192.0.2.1', 'controller')

        self.assertTrue(result)
        restart_call = device.execute.call_args_list[-1]
        self.assertEqual(restart_call.args, ('test capwap restart',))
        restart_dialog = restart_call.kwargs['reply']
        self.assertIsInstance(restart_dialog, Dialog)
        self.assertTrue(any(
            r'\[confirm\]' in pattern
            for pattern in restart_dialog.get_pattern_list()
        ))

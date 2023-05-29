import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.execute import execute_clear_ip_nat_translation


class TestExecuteClearIpNatTranslation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_clear_ip_nat_translation(self):
        result = execute_clear_ip_nat_translation(self.device, False, False, False, '1.1.1.1', '2.2.2.2', None, None, None, None, None, None)
        expected_output = '%Translation not found'
        self.assertEqual(result, expected_output)

    def test_execute_clear_ip_nat_translation_1(self):
        result = execute_clear_ip_nat_translation(self.device, False, False, True, None, None, None, None, None, None, None, None)
        expected_output = ''
        self.assertEqual(result, expected_output)

    def test_execute_clear_ip_nat_translation_2(self):
        result = execute_clear_ip_nat_translation(self.device, False, False, True, '1.1.1.1', '2.2.2.2', None, None, None, None, None, None)
        expected_output = '%Translation not found'
        self.assertEqual(result, expected_output)

    def test_execute_clear_ip_nat_translation_3(self):
        result = execute_clear_ip_nat_translation(self.device, False, False, False, '1.1.1.1', '2.2.2.2', None, None, '3.3.3.3', '5.5.5.5', None, None)
        expected_output = '%Translation not found'
        self.assertEqual(result, expected_output)

    def test_execute_clear_ip_nat_translation_4(self):
        result = execute_clear_ip_nat_translation(self.device, False, True, False, '1.1.1.1', '2.2.2.2', 456, 789, '3.3.3.3', '5.5.5.5', 345, 987)
        expected_output = '%Translation not found'
        self.assertEqual(result, expected_output)

    def test_execute_clear_ip_nat_translation_5(self):
        result = execute_clear_ip_nat_translation(self.device, True, False, False, '1.1.1.1', '2.2.2.2', 456, 789, None, None, None, None)
        expected_output = '%Translation not found'
        self.assertEqual(result, expected_output)

    def test_execute_clear_ip_nat_translation_6(self):
        result = execute_clear_ip_nat_translation(self.device, False, True, False, '1.1.1.1', '2.2.2.2', 456, 789, None, None, None, None)
        expected_output = '%Translation not found'
        self.assertEqual(result, expected_output)

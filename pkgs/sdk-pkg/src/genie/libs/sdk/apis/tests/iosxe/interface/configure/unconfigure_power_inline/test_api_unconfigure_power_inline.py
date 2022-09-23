import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_power_inline


class TestUnconfigurePowerInline(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          screwball:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['screwball']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_power_inline(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'auto', '', '', '')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_power_inline_1(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'auto', '', '', '')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_power_inline_2(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'police', '', '', '')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_power_inline_3(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'never', '', '', '')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_power_inline_4(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'police', '', 'log', '')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_power_inline_5(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'police', '', 'errdisable', '')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_power_inline_6(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'consumption', 4000, '', '')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_power_inline_7(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'port', '', '', 'perpetual-poe-ha')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_power_inline_8(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'port', '', '', '1-event')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_power_inline_9(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'static', 4000, '', '')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_power_inline_10(self):
        result = unconfigure_power_inline(self.device, 'Gi1/0/1', 'auto', 4000, '', '')
        expected_output = None
        self.assertEqual(result, expected_output)

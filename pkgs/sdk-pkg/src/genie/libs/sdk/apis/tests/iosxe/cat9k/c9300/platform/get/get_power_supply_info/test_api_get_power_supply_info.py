import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.c9300.platform.get import get_power_supply_info


class TestGetPowerSupplyInfo(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_power_supply_info(self):
        result = get_power_supply_info(self.device)
        expected_output = {'PowerSupply1/B': {'input_current': 'PtgQYg==',
                    'input_power': 'QpgAAA==',
                    'input_voltage': 'Q09AAA==',
                    'output_current': 'P5j1ww==',
                    'output_power': 'QoUAAA==',
                    'output_voltage': 'Ql+n8A==',
                    'ps_capacity': 'Q68AAA==',
                    'ps_enabled': 'true'}}
        self.assertEqual(result, expected_output)

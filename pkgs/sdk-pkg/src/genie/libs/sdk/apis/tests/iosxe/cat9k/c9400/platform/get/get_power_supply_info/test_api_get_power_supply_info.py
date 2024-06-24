import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.c9400.platform.get import get_power_supply_info


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
            model: c9400
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
        expected_output = {'PowerSupplyModule1': {'input_current': 'QCZmZg==',
                        'input_power': 'RAFAAA==',
                        'input_voltage': 'Q08AAA==',
                        'output_current': 'QQzMzQ==',
                        'output_power': 'Q++AAA==',
                        'output_voltage': 'QlwAAA==',
                        'ps_capacity': 'RUgAAA==',
                        'ps_enabled': 'True'}}
        self.assertEqual(result, expected_output)

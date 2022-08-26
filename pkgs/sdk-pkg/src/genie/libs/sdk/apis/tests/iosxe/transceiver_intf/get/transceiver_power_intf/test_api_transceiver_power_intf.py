import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.transceiver_intf.get import transceiver_power_intf


class TestTransceiverPowerIntf(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          nyquist3-sjc24:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
            custom:
              abstraction:
                order: [os, type]
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['nyquist3-sjc24']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_transceiver_power_intf(self):
        result = transceiver_power_intf(self.device)
        expected_output = {'current': [[5.7, 7.7]],
 'input_power': [[-41.0, -39.0]],
 'output_power': [[-3.2, -1.2000000000000002]],
 'transceiver': ['TenGigabitEthernet1/1/6']}
        self.assertEqual(result, expected_output)

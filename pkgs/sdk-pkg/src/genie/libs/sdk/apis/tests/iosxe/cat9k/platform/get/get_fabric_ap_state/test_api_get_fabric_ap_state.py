import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.platform.get import get_fabric_ap_state


class TestGetFabricApState(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          CTLR_1_1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            custom:
                abstraction:
                    order: [os, platform]
            type: wlc
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CTLR_1_1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_fabric_ap_state(self):
        result = get_fabric_ap_state(self.device, 'AP00B0.E19A.3F60')
        expected_output = 'Registered'
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.verify import verify_dual_port_interface_config_media_type


class TestVerifyDualPortInterfaceConfigMediaType(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          1783-HMS4EG8CGR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ie3300
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['1783-HMS4EG8CGR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_dual_port_interface_config_media_type(self):
        result = verify_dual_port_interface_config_media_type(self.device, 'GigabitEthernet1/4', 'sfp', 60, 10, True)
        expected_output = True
        self.assertEqual(result, expected_output)

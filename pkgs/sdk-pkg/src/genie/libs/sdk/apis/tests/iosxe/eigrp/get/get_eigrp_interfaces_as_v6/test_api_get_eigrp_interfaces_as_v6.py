import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eigrp.get import get_eigrp_interfaces_as_v6


class TestGetEigrpInterfacesAsV6(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_eigrp_interfaces_as_v6(self):
        result = get_eigrp_interfaces_as_v6(self.device, 'default')
        expected_output = {'3': ['FastEthernet0/0'], '4': ['FastEthernet1/0']}
        self.assertEqual(result, expected_output)

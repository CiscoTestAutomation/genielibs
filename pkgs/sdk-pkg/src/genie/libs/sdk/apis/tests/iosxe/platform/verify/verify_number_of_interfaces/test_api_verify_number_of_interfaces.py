import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.verify import verify_number_of_interfaces


class TestVerifyNumberOfInterfaces(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          1783-CMS20DN:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: s5k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['1783-CMS20DN']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_number_of_interfaces(self):
        result = verify_number_of_interfaces(self.device, None, '20', None, None, None, '2', 15, 5)
        expected_output = True
        self.assertEqual(result, expected_output)

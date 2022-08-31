import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.platform.get import get_platform_software_dict


class TestGetPlatformSoftwareDict(unittest.TestCase):

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

    def test_get_platform_software_dict(self):
        result = get_platform_software_dict(self.device, 'wncd')
        expected_output = {'pid': {'9155': {'cmd': 'wncd_0',
                  'cpu': '0.0',
                  'mem': '3.6',
                  'ni': '0',
                  'pr': '20',
                  'res': '282628',
                  's': 'S',
                  'shr': '241632',
                  'time': '2:45.20',
                  'user': 'root',
                  'virt': '570676'}}}
        self.assertEqual(result, expected_output)

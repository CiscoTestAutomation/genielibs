import os
import unittest
from unittest.mock import Mock
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_ssh


class TestConfigureManagementSsh(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          vmtb-isr4451:
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
        self.device = self.testbed.devices['vmtb-isr4451']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_management_ssh(self):
        self.device.api.configure_management_vty_lines = Mock()
        result = configure_management_ssh(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

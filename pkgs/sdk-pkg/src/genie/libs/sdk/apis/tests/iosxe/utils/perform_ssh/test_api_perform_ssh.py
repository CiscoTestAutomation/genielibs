import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import perform_ssh


class TestPerformSsh(unittest.TestCase):

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
            platform: c9200
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_perform_ssh(self):
        result = perform_ssh(self.device, 'Switch', '1.1.1.1', 'test-user', 'cisco@123', None, 'cisco@123', 60, 22, None, None)
        expected_output = True
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.avb.configure import configure_avb


class TestConfigureAvb(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Ram_Gry_CR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Ram_Gry_CR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_avb(self):
        result = configure_avb(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_service_policy


class TestConfigureServicePolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          VCR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['VCR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_service_policy(self):
        result = configure_service_policy(self.device, 'PMAP_DefaultWiredDot1xClosedAuth_1X_MAB')
        expected_output = None
        self.assertEqual(result, expected_output)

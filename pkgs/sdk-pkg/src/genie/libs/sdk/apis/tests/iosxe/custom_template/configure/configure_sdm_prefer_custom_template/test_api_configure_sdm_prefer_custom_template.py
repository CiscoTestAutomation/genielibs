import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.custom_template.configure import configure_sdm_prefer_custom_template


class TestConfigureSdmPreferCustomTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          C9500h-2-DUT:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['C9500h-2-DUT']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_sdm_prefer_custom_template(self):
        result = configure_sdm_prefer_custom_template(self.device, 'acl', 'pbr', 27, 1)
        expected_output = None
        self.assertEqual(result, expected_output)

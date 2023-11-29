import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pki.configure import configure_trustpoint


class TestConfigureTrustpoint(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SVL_9500_40X:
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
        self.device = self.testbed.devices['SVL_9500_40X']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_trustpoint(self):
        result = configure_trustpoint(self.device, 'None', 'Self', 2048, False, None, False, None, None, None, None, None, None, None, False, None, None, None, False, False, None, False, False, False, None, None, None, False, 'selfsigned', None, False, False, False, None, None, None, None, None, None, None, None, None, False, False, None, None, False, False, None, None, None, False, None, None, None, None, None, 'cn=Self', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

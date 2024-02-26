import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_http_client_secure_trustpoint


class TestConfigureIpHttpClientSecureTrustpoint(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          MSFT_9410:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9410
            type: c9410
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['MSFT_9410']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_http_client_secure_trustpoint(self):
        result = configure_ip_http_client_secure_trustpoint(self.device, 'SLA-TrustPoint')
        expected_output = None
        self.assertEqual(result, expected_output)

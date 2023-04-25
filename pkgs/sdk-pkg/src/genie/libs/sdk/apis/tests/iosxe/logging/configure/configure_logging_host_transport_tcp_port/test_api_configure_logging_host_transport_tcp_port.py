import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.logging.configure import configure_logging_host_transport_tcp_port


class TestConfigureLoggingHostTransportTcpPort(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch-9300:
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
        self.device = self.testbed.devices['Switch-9300']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_logging_host_transport_tcp_port(self):
        result = configure_logging_host_transport_tcp_port(self.device, '1.1.1.1', '1')
        expected_output = None
        self.assertEqual(result, expected_output)

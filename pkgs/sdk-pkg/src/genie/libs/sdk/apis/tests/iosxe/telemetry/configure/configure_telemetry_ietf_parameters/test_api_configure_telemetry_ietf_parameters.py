import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.telemetry.configure import configure_telemetry_ietf_parameters


class TestConfigureTelemetryIetfParameters(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ott-isr4k-32:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: isr4k
            type: isr4k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ott-isr4k-32']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_telemetry_ietf_parameters(self):
        result = configure_telemetry_ietf_parameters(self.device, 501, 'yang-push', '192.168.0.11', 56789, 'grpc-tcp', '/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds', 'encode-kvgpb', 'periodic', 500, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

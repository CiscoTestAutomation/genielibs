import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import stop_packet_capture


class TestStopPacketCapture(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: CSR1000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_stop_packet_capture(self):
        result = stop_packet_capture(device=self.device, capture_name='cap1')
        expected_output = None
        self.assertEqual(result, expected_output)

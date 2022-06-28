import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.verify import verify_interface_status


class TestVerifyInterfaceStatus(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          MS2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['MS2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_interface_status(self):
        result = verify_interface_status(self.device, 'TwentyFiveGigE1/0/1', 'connected', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

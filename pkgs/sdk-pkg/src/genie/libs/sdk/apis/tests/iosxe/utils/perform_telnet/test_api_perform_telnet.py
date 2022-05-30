import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import perform_telnet


class TestPerformTelnet(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch-9500:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch-9500']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_perform_telnet(self):
        result = perform_telnet(self.device, 'Switch-9500', '10.106.26.227', 'lab', 'lab', 'Mgmt-vrf', 'lab', 60)
        expected_output = True
        self.assertEqual(result, expected_output)

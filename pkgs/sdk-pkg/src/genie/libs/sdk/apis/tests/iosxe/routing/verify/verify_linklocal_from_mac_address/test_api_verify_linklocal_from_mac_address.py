import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.verify import verify_linklocal_from_mac_address


class TestVerifyLinklocalFromMacAddress(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          uut:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iol
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['uut']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_linklocal_from_mac_address(self):
        result = verify_linklocal_from_mac_address(self.device, 'Ethernet0/0', 'Ethernet0/0')
        expected_output = True
        self.assertEqual(result, expected_output)

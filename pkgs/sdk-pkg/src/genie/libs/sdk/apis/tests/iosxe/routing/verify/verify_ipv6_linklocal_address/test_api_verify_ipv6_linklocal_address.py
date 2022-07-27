import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.verify import verify_ipv6_linklocal_address


class TestVerifyIpv6LinklocalAddress(unittest.TestCase):

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

    def test_verify_ipv6_linklocal_address(self):
        result = verify_ipv6_linklocal_address(self.device, 'Ethernet0/0', 'FE80::A8BB:CCFF:FE01:F400')
        expected_output = True
        self.assertEqual(result, expected_output)

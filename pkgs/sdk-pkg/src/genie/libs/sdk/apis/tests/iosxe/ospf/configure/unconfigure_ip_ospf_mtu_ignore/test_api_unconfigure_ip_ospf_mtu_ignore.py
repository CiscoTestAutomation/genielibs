import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ospf.configure import unconfigure_ip_ospf_mtu_ignore


class TestUnconfigureIpOspfMtuIgnore(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: switch
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_ospf_mtu_ignore(self):
        result = unconfigure_ip_ospf_mtu_ignore(self.device, 'Vlan1001')
        expected_output = None
        self.assertEqual(result, expected_output)

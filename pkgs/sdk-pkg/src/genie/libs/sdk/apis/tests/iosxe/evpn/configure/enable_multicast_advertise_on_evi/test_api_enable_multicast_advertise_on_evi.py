import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.evpn.configure import enable_multicast_advertise_on_evi


class TestEnableMulticastAdvertiseOnEvi(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9300-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_enable_multicast_advertise_on_evi(self):
        result = enable_multicast_advertise_on_evi(self.device, 10, 'vlan-based')
        expected_output = None
        self.assertEqual(result, expected_output)

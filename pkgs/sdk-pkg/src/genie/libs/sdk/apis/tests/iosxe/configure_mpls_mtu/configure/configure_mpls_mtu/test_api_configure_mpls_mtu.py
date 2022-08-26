import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.configure_mpls_mtu.configure import configure_mpls_mtu


class TestConfigureMplsMtu(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          gry24-l2-san:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: '9500'
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['gry24-l2-san']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_mpls_mtu(self):
        result = configure_mpls_mtu(self.device, 'HundredGigE1/0/26', '1400')
        expected_output = None
        self.assertEqual(result, expected_output)

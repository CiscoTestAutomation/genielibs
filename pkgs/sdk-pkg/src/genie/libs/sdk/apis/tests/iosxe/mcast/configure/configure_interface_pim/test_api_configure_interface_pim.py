import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mcast.configure import configure_interface_pim


class TestConfigureInterfacePim(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          VTEP1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500h
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['VTEP1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_pim(self):
        result = configure_interface_pim(device=self.device, interface='loopback1', pim_mode='sparse-mode')
        expected_output = None
        self.assertEqual(result, expected_output)

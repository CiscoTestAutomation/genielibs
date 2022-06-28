import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_vrf_rd_value

# Unicon
from unicon.core.errors import SubCommandFailure


class TestConfigureVrfRdValue(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          gry48-l2-san:
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
        self.device = self.testbed.devices['gry48-l2-san']
        try:
            self.device.connect(
                learn_hostname=True,
                init_config_commands=[],
                init_exec_commands=[]
            )
        except SubCommandFailure:
            raise SubCommandFailure("Could not configure VRF & RD Value")

    def test_configure_vrf_rd_value(self):
        result = configure_vrf_rd_value(
            self.device, 'red', '2:100', 'ipv4', 'export', '2:10', 'stitching'
        )
        expected_output = None
        self.assertEqual(result, expected_output)

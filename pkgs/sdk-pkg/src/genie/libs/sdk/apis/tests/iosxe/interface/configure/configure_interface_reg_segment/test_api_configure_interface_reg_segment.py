import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_reg_segment


class TestConfigureInterfaceRegSegment(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          fr1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['fr1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_reg_segment(self):
        result = configure_interface_reg_segment(self.device, 'Gi1/0/3', 55, True, True)
        expected_output = None
        self.assertEqual(result, expected_output)

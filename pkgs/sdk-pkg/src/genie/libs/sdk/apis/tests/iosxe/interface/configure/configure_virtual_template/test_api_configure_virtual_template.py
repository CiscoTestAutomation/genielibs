import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_virtual_template


class TestConfigureVirtualTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          ASR_2hx:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ASR_2hx']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_virtual_template(self):
        result = configure_virtual_template(self.device, '1', 'Loopback1', 'pap', '')
        expected_output = None
        self.assertEqual(result, expected_output)

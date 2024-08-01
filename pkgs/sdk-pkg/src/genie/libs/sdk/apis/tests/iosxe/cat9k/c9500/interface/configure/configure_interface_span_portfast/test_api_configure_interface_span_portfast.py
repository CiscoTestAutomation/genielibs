import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.c9500.interface.configure import configure_interface_span_portfast


class TestConfigureInterfaceSpanPortfast(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          m4a:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['m4a']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_span_portfast(self):
        result = configure_interface_span_portfast(device=self.device, interface='ten1/1/0/5')
        expected_output = None
        self.assertEqual(result, expected_output)

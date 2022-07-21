import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_igmp_version


class TestConfigureIgmpVersion(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          P1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['P1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_igmp_version(self):
        result = configure_igmp_version(self.device, 'loopback3001', '3')
        expected_output = None
        self.assertEqual(result, expected_output)

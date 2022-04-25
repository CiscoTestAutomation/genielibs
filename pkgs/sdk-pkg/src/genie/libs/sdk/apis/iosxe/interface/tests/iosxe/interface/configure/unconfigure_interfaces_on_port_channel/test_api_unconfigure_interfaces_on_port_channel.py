import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interfaces_on_port_channel


class TestUnconfigureInterfacesOnPortChannel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          startrek-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300X
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['startrek-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_interfaces_on_port_channel(self):
        result = unconfigure_interfaces_on_port_channel(self.device, ['HundredGigE1/0/34'], 'desirable', 1, None, False)
        expected_output = None
        self.assertEqual(result, expected_output)

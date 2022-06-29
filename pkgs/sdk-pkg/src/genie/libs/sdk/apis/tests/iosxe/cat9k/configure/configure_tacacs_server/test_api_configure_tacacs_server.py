import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.configure import configure_tacacs_server


class TestConfigureTacacsServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch-9300:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch-9300']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_tacacs_server(self):
        result = configure_tacacs_server(self.device, {'host': 'abc', 'key': 'cisco', 'server': '10.1.2.3'})
        expected_output = ['tacacs server abc', 'address ipv4 10.1.2.3', 'key cisco']
        self.assertEqual(result, expected_output)

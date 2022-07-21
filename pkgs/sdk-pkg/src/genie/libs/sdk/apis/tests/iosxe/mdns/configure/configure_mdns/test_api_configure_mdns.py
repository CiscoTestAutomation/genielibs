import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mdns.configure import configure_mdns


class TestConfigureMdns(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          C9500H_Sathya:
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
        self.device = self.testbed.devices['C9500H_Sathya']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_mdns(self):
        result = configure_mdns(self.device, 'custom22', ['policie31', 'policie32', 'policie33', 'policie34'], ['IN', 'OUT', 'OUT', 'IN'], {'Policy41': ['policie31', 'IN'],
 'Policy42': ['policie32', 'OUT', 'policie33', 'OUT', 'policie34', 'IN']}, 'policie55', 'IN', 'query', 'policie66', 'OUT', 'filter8', {'Policy43': ['policie55', 'IN', 'policie66', 'OUT']})
        expected_output = None
        self.assertEqual(result, expected_output)

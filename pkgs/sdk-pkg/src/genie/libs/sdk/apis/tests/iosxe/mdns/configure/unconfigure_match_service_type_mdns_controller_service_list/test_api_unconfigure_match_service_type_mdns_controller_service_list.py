import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mdns.configure import unconfigure_match_service_type_mdns_controller_service_list


class TestUnconfigureMatchServiceTypeMdnsControllerServiceList(unittest.TestCase):

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

    def test_unconfigure_match_service_type_mdns_controller_service_list(self):
        result = unconfigure_match_service_type_mdns_controller_service_list(self.device, 'cntrl-list77', ['apple-tv'])
        expected_output = None
        self.assertEqual(result, expected_output)

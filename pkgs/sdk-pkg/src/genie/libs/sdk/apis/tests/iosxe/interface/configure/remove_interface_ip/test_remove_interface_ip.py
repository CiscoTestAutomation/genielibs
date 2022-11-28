import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import remove_interface_ip


class TestRemoveInterfaceIp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Intrepid-P1C-PK:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-P1C-PK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_remove_interface_ip(self):
        result = remove_interface_ip(self.device, interface='Vlan100')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_remove_interface_ip_secondary(self):
        result = remove_interface_ip(self.device, interface='Vlan100', ip_address='101.101.101.101', mask='255.255.0.0', secondary=True)
        expected_output = None
        self.assertEqual(result, expected_output)

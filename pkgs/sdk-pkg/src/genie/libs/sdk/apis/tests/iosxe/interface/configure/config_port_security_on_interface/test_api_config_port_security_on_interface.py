import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import config_port_security_on_interface


class TestConfigPortSecurityOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          VCR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['VCR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_port_security_on_interface(self):
        result = config_port_security_on_interface(self.device, 'GigabitEthernet2/0/13', 3, 5, 'inactivity', 'restrict')
        expected_output = None
        self.assertEqual(result, expected_output)

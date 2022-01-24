import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import clear_port_security


class TestClearPortSecurity(unittest.TestCase):

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

    def test_clear_port_security(self):
        result = clear_port_security(self.device, 'GigabitEthernet2/0/13')
        expected_output = ''
        self.assertEqual(result, expected_output)

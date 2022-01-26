import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.udld.configure import configure_udld_alert_mode


class TestConfigureUdldAlertMode(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
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
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_udld_alert_mode(self):
        result = configure_udld_alert_mode(self.device, 'GigabitEthernet3/0/1')
        expected_output = 'interface GigabitEthernet3/0/1\r\ninterface GigabitEthernet3/0/1\r\nudld port alert\r\nudld port alert\r\n'
        self.assertEqual(result, expected_output)

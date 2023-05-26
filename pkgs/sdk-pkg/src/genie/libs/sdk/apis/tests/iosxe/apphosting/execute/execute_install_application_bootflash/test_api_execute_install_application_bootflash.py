import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.execute import execute_install_application_bootflash


class TestExecuteInstallApplicationBootflash(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          dut1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_install_application_bootflash(self):
        result = execute_install_application_bootflash(self.device, '1keyes', 'thousandeyes-enterprise-agent-4.3.0.cisco.tar', 60, 10)
        expected_output = None
        self.assertEqual(result, expected_output)

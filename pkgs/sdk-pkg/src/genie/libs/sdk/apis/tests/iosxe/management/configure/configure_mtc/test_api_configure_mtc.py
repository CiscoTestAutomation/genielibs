import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.management.configure import configure_mtc


class TestConfigureMtc(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SKYFOX-DUT3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C9500
            type: C9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SKYFOX-DUT3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_mtc(self):
        result = configure_mtc(self.device, 'ipv4', 'HundredGigE1/0/4', ['http', 'ssh', 'snmp'], '4.4.4.4')
        expected_output = None
        self.assertEqual(result, expected_output)

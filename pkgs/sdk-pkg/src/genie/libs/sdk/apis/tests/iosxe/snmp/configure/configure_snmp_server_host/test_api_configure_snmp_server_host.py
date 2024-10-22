import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.snmp.configure import configure_snmp_server_host


class TestConfigureSnmpServerHost(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Router:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            type: cat8k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Router']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_snmp_server_host(self):
        result = configure_snmp_server_host(self.device, '5.5.5.5', 6, '[QggBEaZ^MSMV`ATHVFB]Pcd^Z`O`\\')
        expected_output = None
        self.assertEqual(result, expected_output)

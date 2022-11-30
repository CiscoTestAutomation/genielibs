import unittest
import os
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.platform.get import get_platform_core

class TestPlatformCore(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        testbed:
            servers:
                scp:
                    address: 10.10.10.10
                    credentials:
                        default:
                            username: rcpuser
                            password: cisco123
        devices:
          R3_nx:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: nxos
            platform: n9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R3_nx']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_platform_core(self):
        result = get_platform_core(self.device, remote_device='scp', vrf='management')
        expected_output = ['1/18436/1']
        self.assertEqual(result, expected_output)
        result = self.device.execute("show file")
        self.assertEqual(result, '1654498218_0x1b01_sysmgr_log.18436.tar.gz')

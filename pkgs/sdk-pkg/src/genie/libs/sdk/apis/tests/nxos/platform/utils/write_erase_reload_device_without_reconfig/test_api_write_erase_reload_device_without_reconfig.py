import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.platform.utils import write_erase_reload_device_without_reconfig


class TestWriteEraseReloadDeviceWithoutReconfig(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          N93_4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir mock_data --state connect
                protocol: unknown
                ip: 127.1.1.1
                port: 25
            os: nxos
            platform: n9k
            type: n9k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['N93_4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_write_erase_reload_device_without_reconfig(self):
        result = write_erase_reload_device_without_reconfig(self.device, 'a', 300, None, None, None, 'Router', 15)
        expected_output = None
        self.assertEqual(result, expected_output)

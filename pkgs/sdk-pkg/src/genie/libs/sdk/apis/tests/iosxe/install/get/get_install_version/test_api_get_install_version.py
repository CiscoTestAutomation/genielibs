import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.get import get_install_version


class TestGetInstallVersion(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CAT9400_HA_IOX:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CAT9400_HA_IOX']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_install_version(self):
        result = get_install_version(device=self.device, install_type='IMG', install_state='C')
        expected_output = '17.10.01.0.161496'
        self.assertEqual(result, expected_output)

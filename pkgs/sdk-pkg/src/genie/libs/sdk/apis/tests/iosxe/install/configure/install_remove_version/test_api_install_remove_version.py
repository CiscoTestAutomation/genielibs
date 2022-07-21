import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.configure import install_remove_version


class TestInstallRemoveVersion(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          isr-cl2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: isr4k
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['isr-cl2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_install_remove_version(self):
        result = install_remove_version(self.device, '17.10.01.0.162943', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

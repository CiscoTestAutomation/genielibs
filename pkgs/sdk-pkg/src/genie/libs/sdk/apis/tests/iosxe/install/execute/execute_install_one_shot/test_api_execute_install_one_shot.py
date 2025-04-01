import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_one_shot


class TestExecuteInstallOneShot(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          AMZ-Acc-4:
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
        self.device = self.testbed.devices['AMZ-Acc-4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )
        self.device.settings.POST_RELOAD_WAIT = 1

    def test_execute_install_one_shot(self):
        result = execute_install_one_shot(self.device, 'tftp://172.27.18.5/auto/iconatest/users/byodis/images/cat9k_iosxe.17.10.01.SPA.bin',
                                          True, False, False, 5, 10, False, 'True', None, None)
        expected_output = False
        self.assertEqual(result, expected_output)

    def test_execute_install_one_shot1(self):
        result = execute_install_one_shot(self.device, 'tftp://172.27.18.5/auto/iconatest/users/byodis/images/cat9k_iosxe.17.10.01.SPA.bin',
                                          True, False, False, 5, 10, False, 'True', 10, [])
        expected_output = False
        self.assertEqual(result, expected_output)


class TestExecuteInstallOneShot1(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          AMZ-Acc-4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect1
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['AMZ-Acc-4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )
        self.device.settings.POST_RELOAD_WAIT = 1

    def test_execute_install_one_shot(self):
        result = execute_install_one_shot(self.device, 'bootflash:c8500x_COMPUTE_ASR1K.image.BLD_LUX_DEV_LATEST_20241029_211620.SSA.bin',
                                          False, False, False, 5, 10, False, False, 10, [])
        self.assertIn('install add file bootflash:c8500x_COMPUTE_ASR1K.image.BLD_LUX_DEV_LATEST_20241029_211620.SSA.bin activate commit prompt-level none',
                      result)

    def test_execute_install_one_shot1(self):
        result = execute_install_one_shot(self.device, 'bootflash:c8500x_COMPUTE_ASR1K.image.BLD_LUX_DEV_LATEST_20241029_211620.SSA.bin',
                                          False, False, False, 5, 10, False, False, None, None)
        self.assertIn('install add file bootflash:c8500x_COMPUTE_ASR1K.image.BLD_LUX_DEV_LATEST_20241029_211620.SSA.bin activate commit prompt-level none',
                      result)

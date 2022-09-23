import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_one_shot


class TestExecuteInstallOneShot(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PI-9300x-100:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9400
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PI-9300x-100']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_install_one_shot(self):
        result = execute_install_one_shot(self.device, 'flash:/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.bin', True, False, False, 900, 10)
        expected_output = ('install_add_activate_commit: START Mon Aug 29 03:12:44 UTC 2022\r\n'
 'install_add: START Mon Aug 29 03:12:44 UTC 2022\r\n'
 'install_add: Adding IMG\r\n'
 '--- Starting initial file syncing ---\r\n'
 'Copying flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.bin '
 'from Switch 1 to Switch 1\r\n'
 'Info: Finished copying to the selected Switch\r\n'
 'Finished initial file syncing\r\n'
 '\r\n'
 '--- Starting Add ---\r\n'
 'Performing Add on all members\r\n'
 ' [1] Finished Add package(s) on Switch 1\r\n'
 'Checking status of Add on [1]\r\n'
 'Add: Passed on [1]\r\n'
 'Finished Add\r\n'
 '\r\n'
 'Image added. Version: 17.10.01.0.164921\r\n'
 '\r\n'
 'install_activate: START Mon Aug 29 03:12:55 UTC 2022\r\n'
 'install_activate: Activating IMG\r\n'
 'Following packages shall be activated:\r\n'
 '/flash/cat9k-cc_srdriver.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '/flash/cat9k-espbase.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '/flash/cat9k-guestshell.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '/flash/cat9k-lni.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '/flash/cat9k-rpbase.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '/flash/cat9k-sipbase.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '/flash/cat9k-sipspa.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '/flash/cat9k-srdriver.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '/flash/cat9k-webui.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '/flash/cat9k-wlc.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '/flash/cat9k-rpboot.BLD_POLARIS_DEV_LATEST_20220813_143800.SSA.pkg\r\n'
 '\r\n'
 'This operation may require a reload of the system. Do you want to proceed? '
 '[y/n]y\r\n'
 '\r\n'
 '\r\n'
 '--- Starting Activate ---\r\n'
 'Performing Activate on all members\r\n'
 ' [1] Activate package(s) on Switch 1\r\n'
 ' [1] Finished Activate on Switch 1\r\n'
 'Checking status of Activate on [1]\r\n'
 'Activate: Passed on [1]\r\n'
 'Finished Activate\r\n'
 '\r\n'
 '--- Starting Commit ---\r\n'
 'Performing Commit on all members\r\n'
 ' [1] Commit package(s) on Switch 1\r\n'
 ' [1] Finished Commit on Switch 1\r\n'
 'Checking status of Commit on [1]\r\n'
 'Commit: Passed on [1]\r\n'
 'Finished Commit operation\r\n'
 '\r\n'
 'SUCCESS: install_add_activate_commit Mon Aug 29 03:15:11 UTC 2022')
        self.assertEqual(result, expected_output)

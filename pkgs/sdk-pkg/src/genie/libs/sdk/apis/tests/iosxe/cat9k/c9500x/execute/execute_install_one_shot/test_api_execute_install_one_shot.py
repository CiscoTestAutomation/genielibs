import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.c9500x.execute import execute_install_one_shot


class TestExecuteInstallOneShot(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Q9-9500X-2003:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9500
            submodel: c9500x
            chassis_type: 'stackwise_virtual'
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices["Q9-9500X-2003"]
        self.device.connect(
            learn_hostname=True, init_config_commands=[], init_exec_commands=[]
        )
        self.device.settings.POST_RELOAD_WAIT = 1

    def test_execute_install_one_shot(self):
        result = execute_install_one_shot(
            self.device,
            "bootflash:c9500x_BLD_LUX_DEV_LATEST_20250613_000857.SSA.bin",
            True,
            False,
            False,
            timeout=150,
            connect_timeout=10,
            xfsu=False,
            reloadfast=False,
            post_reload_wait_time=30,
            error_pattern=None,
        )

        self.assertIn(
            "install add file bootflash:c9500x_BLD_LUX_DEV_LATEST_20250613_000857.SSA.bin activate commit",
            result,
        )

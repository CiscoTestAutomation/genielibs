from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9400.execute import execute_install_one_shot

class TestExecuteInstallOneShot(TestCase):

    def test_execute_install_one_shot(self):
        self.device = Mock()

        results_map = {
            'write memory': 'Building configuration...\n[OK]',
            'install add file flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin activate commit':
                'install_add_activate_commit: START Thu Mar 27 06:52:57 UTC 2025\r\n'
                'install_add: START Thu Mar 27 06:52:57 UTC 2025\r\n'
                'install_add: Adding IMG\r\n'
                ' [1]  R0 Add succeed with reason: Same Image File-No Change  \r\n'
                ' [1]  R1 Add succeed with reason: Same Image File-No Change  \r\n'
                'SUCCESS: install_add_activate_commit '
                '/flash1/user/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin Thu '
                'Mar 27 06:52:57 UTC 2'
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg, "")

        self.device.execute.side_effect = results_side_effect

        self.device.api.execute_write_memory = Mock()

        result = execute_install_one_shot(
            self.device, 'flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin', 
            True, False, False, 900, 10, False, False
        )

        expected_output = (
            'install_add_activate_commit: START Thu Mar 27 06:52:57 UTC 2025\r\n'
            'install_add: START Thu Mar 27 06:52:57 UTC 2025\r\n'
            'install_add: Adding IMG\r\n'
            ' [1]  R0 Add succeed with reason: Same Image File-No Change  \r\n'
            ' [1]  R1 Add succeed with reason: Same Image File-No Change  \r\n'
            'SUCCESS: install_add_activate_commit '
            '/flash1/user/cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20250209_002120.SSA.bin Thu '
            'Mar 27 06:52:57 UTC 2'
        )

        self.assertEqual(result.strip(), expected_output.strip())


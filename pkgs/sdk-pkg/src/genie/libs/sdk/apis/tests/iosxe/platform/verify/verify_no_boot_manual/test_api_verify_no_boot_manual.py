import unittest
from unittest.mock import Mock

from genie.utils import Dq

from genie.libs.sdk.apis.iosxe.platform.verify import verify_no_boot_manual


class TestVerifyNoBootManual(unittest.TestCase):

    def test_verify_no_boot_manual_false(self):
        device = Mock()
        device.api.configure_boot_manual = Mock()
        out = '''
        ---------------------------
        Switch 1
        ---------------------------
        Current Boot Variables:
        BOOT variable = flash:/packages.conf;
        Boot Variables on next reload:
        BOOT variable = flash:/packages.conf;
        Manual Boot = no
        Enable Break = yes
        Boot Mode = DEVICE
        iPXE Timeout = 0
        ott-c9300-27#
        '''
        manual_boot_str_present = 'Manual Boot = no' in out
        self.assertTrue(manual_boot_str_present)

        manual_boot = False
        device.parse.return_value = type('Obj', (), {'q': Dq({'manual_boot': manual_boot})})()
        
        result = verify_no_boot_manual(device)

        self.assertTrue(result)
        device.parse.assert_called_once_with('show boot')
        device.api.configure_boot_manual.assert_called_once_with()

    def test_verify_no_boot_manual_true(self):
        device = Mock()
        device.api.configure_boot_manual = Mock()
        out = '''
        ---------------------------
        Switch 1
        ---------------------------
        Current Boot Variables:
        BOOT variable = flash:/packages.conf;
        Boot Variables on next reload:
        BOOT variable = flash:/packages.conf;
        Manual Boot = yes
        Enable Break = yes
        Boot Mode = DEVICE
        iPXE Timeout = 0
        ott-c9300-27#
        '''
        manual_boot_str_present = 'Manual Boot = yes' in out
        self.assertTrue(manual_boot_str_present)

        manual_boot = True
        device.parse.return_value = type('Obj', (), {'q': Dq({'manual_boot': manual_boot})})()
        
        result = verify_no_boot_manual(device)
        self.assertTrue(result)
        device.parse.assert_called_once_with('show boot')
        device.api.configure_boot_manual.assert_not_called()

if __name__ == "__main__":
    unittest.main()

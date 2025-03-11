from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import set_platform_software_selinux
from unittest.mock import Mock




class TestSetPlatformSoftwareSelinux(TestCase):

    def test_set_platform_software_selinux(self):
        self.device = Mock()
        results_map = {
            'set platform software selinux permissive': '''===================================
Setting SELinux mode on chassis 1 route-processor 0
-----------------------------------
===================================
Setting SELinux mode on chassis 2 route-processor 0
-----------------------------------
===================================
Setting SELinux mode on chassis 3 route-processor 0
-----------------------------------

(unlicensed)'''
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg, "")

        self.device.execute.side_effect = results_side_effect

        result = set_platform_software_selinux(self.device, 'permissive')

        # Normalize line endings for consistent comparison
        expected_output = '''===================================
Setting SELinux mode on chassis 1 route-processor 0
-----------------------------------
===================================
Setting SELinux mode on chassis 2 route-processor 0
-----------------------------------
===================================
Setting SELinux mode on chassis 3 route-processor 0
-----------------------------------

(unlicensed)'''

        self.assertEqual(result.strip(), expected_output.strip())  # Strip extra spaces if any

        # Ensure the command was called correctly
        self.device.execute.assert_called_with('set platform software selinux permissive')


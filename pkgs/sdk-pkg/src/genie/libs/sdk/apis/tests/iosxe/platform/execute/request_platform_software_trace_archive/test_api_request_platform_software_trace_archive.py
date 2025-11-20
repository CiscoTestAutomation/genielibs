
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.execute import request_platform_software_trace_archive


class TestRequestPlatformSoftwareTraceArchive(TestCase):

    def test_request_platform_software_trace_archive(self):
        device = Mock()
        device.name = "Device1"
        
        # Simulate command execution output (not used in actual function)
        device.execute.return_value = (
            "executing cmd on chassis 1 ...\n"
            "sending cmd to chassis  2 ...\n"
            "sending cmd to chassis  3 ...\n"
            "Creating archive file [flash:stack-stratmix1_1_RP_0_trace_archive-20250720-123745.tar.gz]\n"
            "Done with creation of the archive file: [flash:stack-stratmix1_1_RP_0_trace_archive-20250720-123745.tar.gz]"
        )

        result = request_platform_software_trace_archive(device, 300)

        # Check that the correct command was executed
        device.execute.assert_called_once_with("request platform software trace archive", timeout=300)

        # Since the function returns None, assert that
        self.assertIsNone(result)


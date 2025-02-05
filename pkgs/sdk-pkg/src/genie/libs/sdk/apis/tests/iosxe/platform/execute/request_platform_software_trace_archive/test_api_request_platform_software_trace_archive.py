from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import request_platform_software_trace_archive
from unittest.mock import Mock


class TestRequestPlatformSoftwareTraceArchive(TestCase):

    def test_request_platform_software_trace_archive(self):
        self.device = Mock()
        results_map = {
    'request platform software trace archive': 'Creating archive file [flash:SA-C9350-24P_1_RP_0_trace_archive-20241212-030058.tar.gz]' +
                                               '\nDone with creation of the archive file: [flash:SA-C9350-24P_1_RP_0_trace_archive-20241212-030058.tar.gz]',
}

        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = request_platform_software_trace_archive(self.device)
        self.assertIn(
            'request platform software trace archive',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)

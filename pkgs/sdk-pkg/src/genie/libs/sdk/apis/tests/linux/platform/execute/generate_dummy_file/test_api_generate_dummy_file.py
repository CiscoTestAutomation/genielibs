from unittest import TestCase
from genie.libs.sdk.apis.linux.platform.execute import generate_dummy_file
from unittest.mock import Mock


class TestGenerateDummyFile(TestCase):

    def test_generate_dummy_file(self):
        self.device = Mock()
        results_map = {
            'dd if=/dev/zero of=/auto/iottest/aarthi/dummyfile/newfile1 bs=1M count=1': '''1+0 records in
1+0 records out
1048576 bytes (1.0 MB, 1.0 MiB) copied, 0.0193207 s, 54.3 MB/s''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = generate_dummy_file(self.device, '/auto/iottest/aarthi/dummyfile', 'newfile1', '1M', 1)
        self.assertIn(
            'dd if=/dev/zero of=/auto/iottest/aarthi/dummyfile/newfile1 bs=1M count=1',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)

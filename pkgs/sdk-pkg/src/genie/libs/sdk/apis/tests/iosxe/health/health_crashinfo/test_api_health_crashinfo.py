import unittest
from unittest.mock import MagicMock, patch, Mock
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.health.health import health_crashinfo


def _make_device(name='R1'):
    device = Mock()
    device.name = name
    device.hostname = name
    device.os = 'iosxe'
    device.is_ha = False
    device.chassis_type = None
    device.api = MagicMock()
    return device


def _parsed_with_files(*filenames):
    """Return a mock parse result containing the given filenames."""
    mock_parsed = MagicMock()
    mock_parsed.q.get_values.return_value = list(filenames)
    return mock_parsed


class TestHealthCrashinfoPass(unittest.TestCase):
    """Pass case: crashinfo file found → copied, deleted, and reported."""

    @patch('genie.libs.sdk.apis.iosxe.health.health.os')
    @patch('genie.libs.sdk.apis.iosxe.health.health.runtime')
    def test_pass(self, mock_runtime, mock_os):
        mock_runtime.health_data = {}
        mock_runtime.synchro.dict.return_value = {}
        mock_runtime.directory = '/tmp/runinfo'
        mock_os.path.join.return_value = '/tmp/runinfo/crashinfo'
        mock_os.makedirs = MagicMock()
        mock_os.chmod = MagicMock()

        device = _make_device()
        filename = 'ott-c9300-01_crashinfo_1_RP_00_00_20260424-120000-UTC'
        device.parse = MagicMock(return_value=_parsed_with_files(filename))
        device.api.copy_from_device = MagicMock()
        device.execute = MagicMock()

        result = health_crashinfo(device, delete_files=True)

        self.assertEqual(result['health_data']['num_of_crashfiles'], 1)
        self.assertIn(filename, result['health_data']['crashfiles'][0]['filename'])
        device.api.copy_from_device.assert_called_once()
        device.execute.assert_called_once_with(
            f'delete /force crashinfo:{filename}')


class TestHealthCrashinfoFail(unittest.TestCase):
    """Fail case: copy_from_device raises → delete must NOT be called."""

    @patch('genie.libs.sdk.apis.iosxe.health.health.os')
    @patch('genie.libs.sdk.apis.iosxe.health.health.runtime')
    def test_fail(self, mock_runtime, mock_os):
        mock_runtime.health_data = {}
        mock_runtime.synchro.dict.return_value = {}
        mock_runtime.directory = '/tmp/runinfo'
        mock_os.path.join.return_value = '/tmp/runinfo/crashinfo'
        mock_os.makedirs = MagicMock()
        mock_os.chmod = MagicMock()

        device = _make_device()
        filename = 'ott-c9300-01_crashinfo_1_RP_00_00_20260424-120000-UTC'
        device.parse = MagicMock(return_value=_parsed_with_files(filename))
        device.api.copy_from_device = MagicMock(
            side_effect=Exception('SCP failed'))
        device.execute = MagicMock()

        # Must not raise — copy failure is handled gracefully
        result = health_crashinfo(device, delete_files=True)

        device.execute.assert_not_called()
        self.assertEqual(result['health_data']['num_of_crashfiles'], 1)


class TestHealthCrashinfoNegative(unittest.TestCase):
    """Negative case: parser returns no files → num_of_crashfiles == 0,
    no copy or delete attempted. Also verifies runtime.health_data=None
    does not raise TypeError."""

    @patch('genie.libs.sdk.apis.iosxe.health.health.runtime')
    def test_negative(self, mock_runtime):
        mock_runtime.health_data = None
        mock_runtime.directory = '/tmp/runinfo'

        device = _make_device()
        device.parse = MagicMock(side_effect=SchemaEmptyParserError('empty'))

        result = health_crashinfo(device)

        self.assertEqual(result['health_data']['num_of_crashfiles'], 0)
        self.assertEqual(result['health_data']['crashfiles'], [])
        device.api.copy_from_device.assert_not_called()
        device.execute.assert_not_called()


class TestHealthCrashinfoHA(unittest.TestCase):
    """HA case: both crashinfo: and stby-crashinfo: are inspected."""

    @patch('genie.libs.sdk.apis.iosxe.health.health.os')
    @patch('genie.libs.sdk.apis.iosxe.health.health.runtime')
    def test_ha(self, mock_runtime, mock_os):
        mock_runtime.health_data = {}
        mock_runtime.synchro.dict.return_value = {}
        mock_runtime.directory = '/tmp/runinfo'
        mock_os.path.join.return_value = '/tmp/runinfo/crashinfo'
        mock_os.makedirs = MagicMock()
        mock_os.chmod = MagicMock()

        device = _make_device()
        device.is_ha = True
        active_file = 'crashinfo_RP_00_00_20260424-120000-UTC.tar.gz'
        standby_file = 'crashinfo_RP_01_00_20260424-120001-UTC.tar.gz'

        # first call → active dir, second call → standby dir
        device.parse = MagicMock(side_effect=[
            _parsed_with_files(active_file),
            _parsed_with_files(standby_file),
        ])
        device.api.copy_from_device = MagicMock()
        device.execute = MagicMock()

        result = health_crashinfo(device, delete_files=False)

        # dir must have been called for both filesystems
        parse_calls = [str(c) for c in device.parse.call_args_list]
        self.assertTrue(any('dir crashinfo:' in c for c in parse_calls),
                        'Expected dir crashinfo: call')
        self.assertTrue(any('dir stby-crashinfo:' in c for c in parse_calls),
                        'Expected dir stby-crashinfo: call')

        self.assertEqual(result['health_data']['num_of_crashfiles'], 2)
        filenames = [f['filename'] for f in result['health_data']['crashfiles']]
        self.assertTrue(any(active_file in f for f in filenames))
        self.assertTrue(any(standby_file in f for f in filenames))


class TestHealthCrashinfoStack(unittest.TestCase):
    """Stack case: crashinfo-{id}: checked per member via show switch."""

    @patch('genie.libs.sdk.apis.iosxe.health.health.os')
    @patch('genie.libs.sdk.apis.iosxe.health.health.runtime')
    def test_stack(self, mock_runtime, mock_os):
        mock_runtime.health_data = {}
        mock_runtime.synchro.dict.return_value = {}
        mock_runtime.directory = '/tmp/runinfo'
        mock_os.path.join.return_value = '/tmp/runinfo/crashinfo'
        mock_os.makedirs = MagicMock()
        mock_os.chmod = MagicMock()

        device = _make_device()
        device.chassis_type = 'stack'
        device.is_ha = False

        # show switch returns members 1 and 2
        show_switch_parsed = {'switch': {'stack': {1: {}, 2: {}}}}
        member1_file = 'crashinfo_1_RP_00_00_20260424-120000-UTC.tar.gz'
        member2_file = 'crashinfo_2_RP_00_00_20260424-120001-UTC.tar.gz'

        device.parse = MagicMock(side_effect=[
            show_switch_parsed,               # show switch
            _parsed_with_files(member1_file), # dir crashinfo-1:
            _parsed_with_files(member2_file), # dir crashinfo-2:
        ])
        device.api.copy_from_device = MagicMock()
        device.execute = MagicMock()

        result = health_crashinfo(device, delete_files=False)

        parse_calls = [str(c) for c in device.parse.call_args_list]
        self.assertTrue(any('dir crashinfo-1:' in c for c in parse_calls),
                        'Expected dir crashinfo-1: call')
        self.assertTrue(any('dir crashinfo-2:' in c for c in parse_calls),
                        'Expected dir crashinfo-2: call')

        self.assertEqual(result['health_data']['num_of_crashfiles'], 2)
        filenames = [f['filename'] for f in result['health_data']['crashfiles']]
        self.assertTrue(any(member1_file in f for f in filenames))
        self.assertTrue(any(member2_file in f for f in filenames))


class TestHealthCrashinfoDuplicateSuppression(unittest.TestCase):
    """Duplicate suppression: file already in runtime.health_data is not
    re-reported on a second call (simulates second testcase post-processor)."""

    @patch('genie.libs.sdk.apis.iosxe.health.health.os')
    @patch('genie.libs.sdk.apis.iosxe.health.health.runtime')
    def test_duplicate_suppression(self, mock_runtime, mock_os):
        mock_os.path.join.return_value = '/tmp/runinfo/crashinfo'
        mock_os.makedirs = MagicMock()
        mock_os.chmod = MagicMock()

        device = _make_device()
        filename = 'crashinfo_RP_00_00_20260424-120000-UTC.tar.gz'

        # Pre-populate runtime.health_data as if the file was seen in TC1
        already_seen = {'filename': f'crashinfo:{filename}'}
        mock_runtime.directory = '/tmp/runinfo'
        mock_runtime.health_data = {
            device.name: {
                'crashinfo': {
                    'crashfiles': [already_seen]
                }
            }
        }
        mock_runtime.synchro.dict.return_value = \
            mock_runtime.health_data[device.name]

        # TC2: same file still present on device
        device.parse = MagicMock(return_value=_parsed_with_files(filename))
        device.api.copy_from_device = MagicMock()
        device.execute = MagicMock()

        result = health_crashinfo(device, delete_files=False)

        # file already tracked → must NOT be counted again
        self.assertEqual(result['health_data']['num_of_crashfiles'], 0)
        self.assertEqual(result['health_data']['crashfiles'], [])


class TestHealthCrashinfoBaselineCapture(unittest.TestCase):
    """Baseline capture mode (copy_files=False, delete_files=False):
    records existing files and returns 0 without copying or deleting."""

    @patch('genie.libs.sdk.apis.iosxe.health.health.runtime')
    def test_baseline_records_and_returns_zero(self, mock_runtime):
        device = _make_device()
        existing_file = 'ott-c9300-01_crashinfo_1_RP_00_00_20260424-120000-UTC'

        runtime_crashinfo = {}
        mock_runtime.health_data = {device.name: {'crashinfo': runtime_crashinfo}}
        mock_runtime.synchro.dict.return_value = {}
        mock_runtime.directory = '/tmp/runinfo'

        device.parse = MagicMock(return_value=_parsed_with_files(existing_file))
        device.api.copy_from_device = MagicMock()
        device.execute = MagicMock()

        result = health_crashinfo(device, copy_files=False, delete_files=False)

        # No copy, no delete
        device.api.copy_from_device.assert_not_called()
        device.execute.assert_not_called()
        # Returns 0 crashfiles — baseline files are not actionable
        self.assertEqual(result['health_data']['num_of_crashfiles'], 0)
        self.assertEqual(result['health_data']['crashfiles'], [])
        # Baseline is stored in runtime.health_data
        stored = mock_runtime.health_data[device.name]['crashinfo']
        self.assertIn(f'crashinfo:{existing_file}',
                      stored.get('baseline_files', []))


class TestHealthCrashinfoBaselineExclusion(unittest.TestCase):
    """TestCase mode with baseline: pre-existing files are skipped,
    only new files are copied/deleted/reported."""

    @patch('genie.libs.sdk.apis.iosxe.health.health.os')
    @patch('genie.libs.sdk.apis.iosxe.health.health.runtime')
    def test_baseline_files_excluded(self, mock_runtime, mock_os):
        mock_os.path.join.return_value = '/tmp/runinfo/crashinfo'
        mock_os.makedirs = MagicMock()
        mock_os.chmod = MagicMock()

        device = _make_device()
        old_file = 'ott-c9300-01_crashinfo_1_RP_00_00_20260424-120000-UTC'
        new_file = 'ott-c9300-01_crashinfo_1_RP_00_00_20260505-150000-UTC'

        # Baseline was previously captured with the old file
        mock_runtime.directory = '/tmp/runinfo'
        mock_runtime.health_data = {
            device.name: {
                'crashinfo': {
                    'baseline_files': [f'crashinfo:{old_file}'],
                    'crashfiles': []
                }
            }
        }
        mock_runtime.synchro.dict.return_value = \
            mock_runtime.health_data[device.name]

        # Device now has both old and new files
        device.parse = MagicMock(
            return_value=_parsed_with_files(old_file, new_file))
        device.api.copy_from_device = MagicMock()
        device.execute = MagicMock()

        result = health_crashinfo(device, delete_files=True)

        # Only new file should be reported
        self.assertEqual(result['health_data']['num_of_crashfiles'], 1)
        self.assertIn(new_file,
                      result['health_data']['crashfiles'][0]['filename'])
        # Only new file should be copied and deleted
        device.api.copy_from_device.assert_called_once()
        device.execute.assert_called_once_with(
            f'delete /force crashinfo:{new_file}')


if __name__ == '__main__':
    unittest.main()


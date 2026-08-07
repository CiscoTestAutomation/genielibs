from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import verify_cloud_mgmt_migration_status
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCloudMgmtMigrationStatus(TestCase):
    """Tests for verify_cloud_mgmt_migration_status.

    Parser: ShowCloudMgmtMigration (show cloud-mgmt migration)
    Schema: {'cloud_mgmt_mode_migration_status': {'migration_in_progress': str, ...}}
    """

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def _make_parsed_output(self, migration_in_progress):
        """Return a Dq-compatible parsed dict matching the real ShowCloudMgmtMigration schema."""
        from genie.utils import Dq
        parsed = {
            'cloud_mgmt_mode_migration_status': {
                'current_booted_mode': 'IE35xx-M',
                'migration_in_progress': migration_in_progress,
            }
        }
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.parse.return_value = mock_output

    def test_migration_status_not_in_progress(self):
        """Test successful verification when migration is not in progress (NO)"""
        self._make_parsed_output('NO')
        result = verify_cloud_mgmt_migration_status(
            self.device,
            expected_migration_in_progress='NO',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_migration_status_in_progress(self):
        """Test successful verification when migration is in progress (YES)"""
        self._make_parsed_output('YES')
        result = verify_cloud_mgmt_migration_status(
            self.device,
            expected_migration_in_progress='YES',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_migration_status_mismatch(self):
        """Test failure when actual value does not match expected"""
        self._make_parsed_output('YES')
        result = verify_cloud_mgmt_migration_status(
            self.device,
            expected_migration_in_progress='NO',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_migration_status_not_found(self):
        """Test failure when migration_in_progress key is absent"""
        from genie.utils import Dq
        parsed = {'cloud_mgmt_mode_migration_status': {'current_booted_mode': 'IE35xx-M'}}
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.parse.return_value = mock_output
        result = verify_cloud_mgmt_migration_status(
            self.device,
            expected_migration_in_progress='NO',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_parser_empty_output(self):
        """Test failure when parser raises SchemaEmptyParserError"""
        self.device.parse.side_effect = SchemaEmptyParserError(None)
        result = verify_cloud_mgmt_migration_status(
            self.device,
            expected_migration_in_progress='NO',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

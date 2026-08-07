from unittest import TestCase
from unittest.mock import Mock, MagicMock
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import verify_cloud_id
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCloudId(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def _make_output(self, meraki_sn):
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_output.get.return_value = {}
        mock_q.get_values.return_value = meraki_sn
        self.device.parse.return_value = mock_output

    def test_cloud_id_success(self):
        """Test successful cloud ID verification"""
        self._make_output('Q4NS-HCWU-CZR2')
        result = verify_cloud_id(self.device, expected_cloud_id='Q4NS-HCWU-CZR2', max_time=1, check_interval=1)
        self.assertTrue(result)

    def test_cloud_id_mismatch(self):
        """Test cloud ID mismatch"""
        self._make_output('WRONG-ID')
        result = verify_cloud_id(self.device, expected_cloud_id='Q4NS-HCWU-CZR2', max_time=1, check_interval=1)
        self.assertFalse(result)

    def test_cloud_id_not_found(self):
        """Test cloud ID not found"""
        self._make_output(None)
        result = verify_cloud_id(self.device, expected_cloud_id='Q4NS-HCWU-CZR2', max_time=1, check_interval=1)
        self.assertFalse(result)

    def test_parser_empty_output(self):
        """Test handling of empty parser output"""
        self.device.parse.side_effect = SchemaEmptyParserError(None)
        result = verify_cloud_id(self.device, expected_cloud_id='Q4NS-HCWU-CZR2', max_time=1, check_interval=1)
        self.assertFalse(result)

    def test_cloud_id_switch_number_success(self):
        """Test cloud ID verification with explicit switch_number using real parser schema"""
        mock_output = MagicMock()
        mock_output.get.side_effect = lambda k, d=None: {
            'meraki': {'switch': {'1': {'meraki_sn': 'Q4NS-HCWU-CZR2'}}}
        }.get(k, d if d is not None else {})
        mock_output.q = MagicMock()
        self.device.parse.return_value = mock_output
        result = verify_cloud_id(self.device, expected_cloud_id='Q4NS-HCWU-CZR2', switch_number=1, max_time=1, check_interval=1)
        self.assertTrue(result)

    def test_cloud_id_switch_number_not_found(self):
        """Test cloud ID with switch_number that does not exist in real parser schema"""
        mock_output = MagicMock()
        mock_output.get.side_effect = lambda k, d=None: {
            'meraki': {'switch': {'1': {'meraki_sn': 'Q4NS-HCWU-CZR2'}}}
        }.get(k, d if d is not None else {})
        mock_output.q = MagicMock()
        self.device.parse.return_value = mock_output
        result = verify_cloud_id(self.device, expected_cloud_id='Q4NS-HCWU-CZR2', switch_number=99, max_time=1, check_interval=1)
        self.assertFalse(result)

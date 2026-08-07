import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.span.configure import (
    configure_local_span_and_verify_output)


class TestConfigureLocalSpanAndVerifyOutput(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def _set_source_output(self, output):
        self.device.api.configure_local_span_source_and_get_output\
            .return_value = output

    def _set_destination_output(self, output):
        self.device.api.configure_local_span_destination_and_get_output\
            .return_value = output

    def test_source_validation_pass(self):
        self._set_source_output('')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4',
            int_type='interface', direction='rx',
            role='source', validation_code=0))
        (self.device.api.configure_local_span_source_and_get_output
         .assert_called_once())

    def test_destination_validation_pass(self):
        self._set_destination_output('')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/5',
            role='destination', validation_code=0))

    def test_invalid_role(self):
        self.assertFalse(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='unknown'))

    def test_max_source_port(self):
        self._set_source_output(
            '% Exceed the maximum source port number per session\n'
            'SPAN Session Validation failed.')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='source',
            validation_code=1))

    def test_only_one_dst_port(self):
        self._set_source_output(
            '% Only one Dst port is supported\n'
            'SPAN Session Validation failed.')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='source',
            validation_code=2))

    def test_already_configured_as_monitor_sources(self):
        self._set_source_output(
            '% Interface(s) Gi0/1/5 already configured '
            'as monitor sources')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='source',
            validation_code=3))

    def test_already_configured_as_monitor_destinations(self):
        self._set_source_output(
            '% Interface(s) Gi0/1/5 already configured '
            'as monitor destinations')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='source',
            validation_code=4))

    def test_src_port_already_used(self):
        self._set_source_output(
            '% Src port is already be used in session\n'
            'SPAN Session Validation failed.')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='source',
            validation_code=5))

    def test_dst_port_already_used(self):
        self._set_source_output(
            '% Dst port is already be used in session\n'
            'SPAN Session Validation failed.')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='source',
            validation_code=6))

    def test_max_session_number(self):
        self._set_source_output(
            '% Exceed the maximum SPAN session number\n'
            'SPAN Session Validation failed.')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='source',
            validation_code=7))

    def test_only_ngio_supported(self):
        self._set_source_output(
            'Only NGIO switch is supported for Local SPAN.\n'
            'SPAN Session Validation failed.')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='source',
            validation_code=8))

    def test_unknown_reason(self):
        self._set_source_output(
            '% Some unrecognized error\n'
            'SPAN Session Validation failed.')
        self.assertTrue(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='source',
            validation_code=-1))

    def test_validation_code_mismatch(self):
        self._set_source_output('')
        self.assertFalse(configure_local_span_and_verify_output(
            self.device, 1, 'Gi0/1/4', role='source',
            validation_code=3))


if __name__ == '__main__':
    unittest.main()

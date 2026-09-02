from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.telemetry.configure import (
    configure_telemetry_ietf_parameters,
)


class TestConfigureTelemetryIetfParameters(TestCase):

    def test_configure_telemetry_ietf_parameters(self):
        device = Mock()

        result = configure_telemetry_ietf_parameters(
            device,
            sub_id=501,
            stream='yang-push',
            receiver_ip='192.168.0.11',
            receiver_port=56789,
            protocol='grpc-tcp',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'telemetry ietf subscription 501',
                'receiver ip address 192.168.0.11 56789 protocol grpc-tcp',
                'stream yang-push',
                'filter xpath /process-cpu-ios-xe-oper:cpu-usage/'
                'cpu-utilization/five-seconds',
                'encoding encode-kvgpb',
                'update-policy periodic 500',
            ]
        )

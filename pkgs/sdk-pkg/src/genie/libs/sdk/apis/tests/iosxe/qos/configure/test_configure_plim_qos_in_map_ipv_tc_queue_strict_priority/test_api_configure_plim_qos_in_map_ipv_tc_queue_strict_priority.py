from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import configure_plim_qos_in_map_ipv_tc_queue_strict_priority


class TestConfigurePlimQosInMapIpvTcQueueStrictPriority(TestCase):

    def test_configure_plim_qos_in_map_ipv_tc_queue_strict_priority(self):
        self.device = Mock()
        configure_plim_qos_in_map_ipv_tc_queue_strict_priority(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['plim qos in map ipv tc 0 queue strict-priority'],)
        )

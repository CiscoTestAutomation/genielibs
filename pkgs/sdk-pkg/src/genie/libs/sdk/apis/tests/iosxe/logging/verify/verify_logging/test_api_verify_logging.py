from unittest import TestCase
from unittest.mock import Mock, patch
from genie.libs.sdk.apis.iosxe.logging.verify import verify_logging


LOGGING_OUTPUT = [
    '*Jul  7 09:42:00.485: %SYS-4-LOG_CLEARED: Logging buffer was cleared by user Unknown',
    '*Jul  7 09:42:08.982: %PLATFORM-5-LOWSPACERECOVER:  bootflash : low space alarm deassert',
    '*Jul  7 09:42:17.849: %SYS-5-CONFIG_I: Configured from console by console',
    '*Jul  7 09:42:39.692: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1/0, changed state to down',
    '*Jul  7 09:42:41.330: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan100, changed state to down',
    '*Jul  7 09:42:42.672: %SYS-5-CONFIG_I: Configured from console by console',
    '*Jul  7 09:42:48.981: %LINK-3-UPDOWN: Interface GigabitEthernet0/1/0, changed state to up',
    '*Jul  7 09:42:49.982: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1/0, changed state to up',
    '*Jul  7 09:42:49.986: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan100, changed state to up',
]


class OneAttemptTimeout:
    def __init__(self, max_time, interval_time):
        self.iterations = 0

    def iterate(self):
        self.iterations += 1
        return self.iterations == 1

    def sleep(self):
        return None


class TestVerifyLogging(TestCase):
    def test_verify_logging(self):
        device = Mock()
        device.api.get_platform_logging.return_value = LOGGING_OUTPUT

        with patch('genie.libs.sdk.apis.iosxe.logging.verify.Timeout',
                   OneAttemptTimeout):
            result = verify_logging(device, 'changed state to down',
                                    20, 2, False, True, True)
            self.assertTrue(result)

            result = verify_logging(device, 'changed state to up',
                                    20, 2, False, True, True)
            self.assertTrue(result)

            result = verify_logging(device, ['changed state to down',
                                             'changed state to up'],
                                    20, 2, False, True, True)
            self.assertTrue(result)

            result = verify_logging(device,
                                    [['changed state to up',
                                      'changed state to ?'],
                                     'changed state to down'],
                                    20, 2, False, True, True)
            self.assertTrue(result)

            result = verify_logging(device,
                                    [['changed state to @',
                                      'changed state to ?'],
                                     'changed state to down'],
                                    1, 1, False, True, True)
            self.assertFalse(result)

            result = verify_logging(device, ['changed state to down',
                                             'changed state to ?'],
                                    1, 1, False, True, True)
            self.assertFalse(result)

            result = verify_logging(device, 'changed state to down',
                                    1, 1, True, True, True)
            self.assertFalse(result)

            result = verify_logging(device, 'changed state to down',
                                    1, 1, False, True, False)
            self.assertFalse(result)

        device.api.get_platform_logging.assert_called_with(
            command='show logging')
        self.assertEqual(device.api.clear_logging.call_count, 4)

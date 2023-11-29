import logging
from abc import ABC
from datetime import datetime
from threading import Event, Thread
from typing import List
import traceback
from pyats.log.utils import banner

log = logging.getLogger(__name__)


class Subscription(ABC, Thread):
    """Base Subscription class for all notifications."""
    def __init__(self, device=None, **request):
        Thread.__init__(self)
        self.delay = 0
        self._stop_event = Event()
        self.log = request.get('log')
        if self.log is None:
            self.log = logging.getLogger(__name__)
            self.log.setLevel(logging.DEBUG)
        self.request = request
        self.verifier = request.get('verifier')
        self.namespace = request.get('namespace')
        self.sub_mode = request.get('sub_mode')
        self.encoding = request.get('encoding')
        self.transaction_time = request.get('transaction_time', 0)
        self._result = True
        self.errors: List[Exception] = []
        self.negative_test = request.get('negative_test', False)
        self.ntp_server = ""
        if device is not None:
            if self.transaction_time:
                self.ntp_server = device.device.testbed.servers.get(
                    'ntp', {}).get('server', {})
        self.stream_max = request.get('stream_max', 60)
        self.sample_poll = request.get(
            'sample_interval',  request.get('sample_poll', 5))
        if self.stream_max:
            self.log.info('Notification MAX timeout {0} seconds.'.format(
                str(self.stream_max)))
        # For transaction_time subscribtion NTP servers must be configured
        if self.transaction_time and not self.ntp_server:
            self._result = False
            self.log.error(
                banner('For transaction_time to work with Subscribtions, NTP servers must be configured.'))  # noqa
            raise self.NoNtpConfigured('NTP servers not configured')

    class NoNtpConfigured(Exception):
        pass

    class DevieOutOfSyncWithNtp(Exception):
        def __init__(self, response_timestamp: int, arrive_timestamp: int, ntp_server: str, *args: object) -> None:
            super().__init__(*args)
            self.response_dt = datetime.fromtimestamp(
                response_timestamp)
            self.ntp_dt = datetime.fromtimestamp(arrive_timestamp)
            self.ntp_server = ntp_server
            log.error(banner(
                f"""Device is out of sync with NTP server {self.ntp_server}
                Device time: {self.ntp_dt.strftime('%m/%d/%Y %H:%M:%S.%f')}
                NTP time: {self.response_dt.strftime('%m/%d/%Y %H:%M:%S.%f')}"""))

    class TransactionTimeExceeded(Exception):
        def __init__(self, delta_time: float, transaction_time: float, *args: object) -> None:
            super().__init__(*args)
            self.delta_time = delta_time
            log.error(banner(
                f'Response time: {delta_time} seconds exceeded transaction_time {transaction_time}',
            ))

    @property
    def result(self):
        return self.negative_test != self._result

    @result.setter
    def result(self, value):
        self._result = value

    def stop(self):
        self.log.info("Stopping notification stream")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
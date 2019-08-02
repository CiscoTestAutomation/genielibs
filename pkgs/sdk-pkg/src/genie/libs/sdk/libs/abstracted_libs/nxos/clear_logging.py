# python
import logging

log = logging.getLogger(__name__)


class ClearLogging(object):

    def clear_logging(self, device):
        try:
            device.execute('clear logging logfile')
        except Exception as e:
            self.failed('Failed to clear logging', from_exception=e)

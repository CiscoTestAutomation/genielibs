# python
import logging

log = logging.getLogger(__name__)


class ClearLogging(object):

    def clear_logging(self, device):
        try:
            device.execute('clear log messages')
        except Exception as e:
            self.failed('Failed to clear log messages', from_exception=e)
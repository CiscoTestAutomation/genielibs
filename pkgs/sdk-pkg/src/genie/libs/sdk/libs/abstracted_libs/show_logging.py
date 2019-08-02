# python
import logging

log = logging.getLogger(__name__)


class ShowLogging(object):

    def show_logging(self, device):
        try:
            return device.execute('show logging')
        except Exception as e:
            self.failed('Failed to show logging', from_exception=e)

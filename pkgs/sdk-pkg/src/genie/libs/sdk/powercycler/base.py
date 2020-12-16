import re
import logging
import time

from .snmp_client import SNMPClient

# Unicon
from unicon.eal.dialogs import Statement, Dialog

log = logging.getLogger(__name__)


class PowerCyclerMeta(type):

    def __new__(cls, name, bases, attrs):

        obj = super().__new__(cls, name, bases, attrs)

        if not re.match(r'Base.*|PowerCycler', name):
            if 'type' not in attrs or 'connection_type' not in attrs:
                raise Exception(
                    'type and connection type are mandatory attributes')

            type_ = attrs['type']
            connection_type = attrs['connection_type']
            PowerCycler._SUPPORTED_PC_TYPES[type_] = {connection_type: obj}

        return obj


class PowerCycler(metaclass=PowerCyclerMeta):

    _SUPPORTED_PC_TYPES = {}

    def __new__(cls, *, type, connection_type='snmp', **kwargs):

        supported_pc_types = PowerCycler._SUPPORTED_PC_TYPES
        if cls is PowerCycler:
            if type not in supported_pc_types or connection_type not in \
                    supported_pc_types[type]:
                raise Exception('UnSupported power cycler type')

            cls = supported_pc_types[type][connection_type]

        return super().__new__(cls)

    def __init__(self, host, type, connection_type, pc_delay=0.5,
                 log=log, *args, **kwargs):

        self.host = host
        self.type = type
        self.connection_type = connection_type
        self.pc_delay = pc_delay
        self.log = log

    def connect(self):
        raise NotImplementedError

    def on(self, *outlets):
        raise NotImplementedError

    def off(self, *outlets):
        raise NotImplementedError

    def get_state(self, *outlets):
        raise NotImplementedError


class BaseSNMPPowerCycler(PowerCycler):

    def __init__(self,
                 write_community='private',
                 read_community='public',
                 snmp_version='2c',
                 snmp_port=161,
                 **kwargs):

        super().__init__(**kwargs)
        self.write_community = write_community
        self.read_community = read_community
        self.version = snmp_version
        self.port = snmp_port
        self.snmp_client = None
        self.connect()

    def connect(self):
        """ Connect not required for PC
        """
        self.snmp_client = SNMPClient(host=self.host,
                                      read_community=self.read_community,
                                      write_community=self.write_community,
                                      port=self.port,
                                      version=self.version,
                                      log=self.log)

    def on(self, *outlets, after=None):

        ret = []
        if after and not isinstance(after, int):
            raise TypeError('"after" should be an int')

        if after:
            time.sleep(after)

        for outlet in outlets:
            outlet_id = '.'.join([self.oid, str(outlet)])
            result = self.snmp_client.snmp_set(oid=outlet_id,
                                               value=self.on_state,
                                               type='Integer')
            ret.extend(result)
        return ret

    def off(self, *outlets, after=None):

        ret = []
        if isinstance(after, int):
            raise TypeError('"after" should be an int')

        if after:
            time.sleep(after)

        for outlet in outlets:
            outlet_id = '.'.join([self.oid, str(outlet)])
            result = self.snmp_client.snmp_set(oid=outlet_id,
                                               value=self.off_state,
                                               type='Integer')
            ret.extend(result)
        return ret

    def get_state(self, *outlets):

        outlet_ids = []
        for outlet in outlets:
            outlet_ids.append('.'.join([self.oid, str(outlet)]))
        return self.snmp_client.snmp_get(*outlet_ids)


class BaseCyberSwitchingPowerCycler(PowerCycler):

    def __init__(self, testbed, **kwargs):
        super().__init__(**kwargs)
        self.testbed = testbed
        self.connect()

    def connect(self):
        if self.host not in self.testbed.devices:
            raise Exception("The device '{}' does not exist in the testbed"
                            .format(self.host))

        self.host = self.testbed.devices[self.host]

        self.host.connect(learn_hostname=True)

    def off(self, *outlets, after=None):
        if isinstance(after, int):
            raise TypeError('"after" should be an int')

        if after:
            time.sleep(after)

        clear_line_dialog = Dialog([
            Statement(pattern='.*\[confirm\]',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False)])

        for outlet in outlets:
            try:
                self.host.execute('clear line {}'.format(outlet),
                                  reply=clear_line_dialog)

                self.host.configure(['line {}'.format(outlet),
                                     'modem dtr-active'])
            except Exception as e:
                raise Exception("Turning off outlet '{}' on the powercycler "
                                "failed. Error: {}".format(outlet, str(e)))

    def on(self, *outlets):
        for outlet in outlets:
            try:
                self.host.configure(['line {}'.format(outlet),
                                     'no modem dtr-active'])
            except Exception as e:
                raise Exception("Turning on outlet '{}' on the powercycler "
                                "failed. Error: {}".format(outlet, str(e)))

class BaseEsxiPowerCycler(PowerCycler):

    def __init__(self, testbed, **kwargs):
        super().__init__(**kwargs)
        self.testbed=testbed
        self.connect()

    def connect(self):
        if self.host not in self.testbed.devices:
            raise Exception("The device '{}' does not exist in the testbed"
                            .format(self.host))

        self.host = self.testbed.devices[self.host]

        self.host.connect(learn_hostname=True)

    def off(self, *outlets, after=None):
        if isinstance(after, int):
            raise TypeError('"after" should be an int')

        if after:
            time.sleep(after)

        for outlet in outlets:
            try:
                self.host.api.switch_vm_power(vm_id=outlet, state='off')
            except Exception as e:
                raise Exception("Turning off outlet '{}' on the powercycler "
                                "failed. Error: {}".format(outlet, str(e)))

    def on(self, *outlets):
        for outlet in outlets:
            try:
                self.host.api.switch_vm_power(vm_id=outlet, state='on')
            except Exception as e:
                raise Exception("Turning off outlet '{}' on the powercycler "
                                "failed. Error: {}".format(outlet, str(e)))
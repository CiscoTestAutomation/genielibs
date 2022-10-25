import re
import logging
import time

from .snmp_client import SNMPClient, SNMPv3Client
try:
    import pysnmp
    from pysnmp.proto.rfc1905 import NoSuchInstance, NoSuchObject
    from pysnmp.hlapi import  UsmUserData, usmHMACMD5AuthProtocol, usmHMACSHAAuthProtocol, usmHMAC128SHA224AuthProtocol,\
     usmHMAC192SHA256AuthProtocol, usmHMAC256SHA384AuthProtocol, usmHMAC384SHA512AuthProtocol, usmNoAuthProtocol,\
     usmDESPrivProtocol, usm3DESEDEPrivProtocol, usmAesCfb128Protocol, usmAesCfb192Protocol,\
     usmAesCfb256Protocol, usmNoPrivProtocol
    pysnmp_installed = True
except ImportError:
    pysnmp_installed = False

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


class BaseSNMPv3PowerCycler(PowerCycler):

    def __init__(self,
                 snmp_port=161,
                 **kwargs):

        super().__init__(**kwargs)
        self.port = snmp_port
        self.snmp_client = None
        self.connect(**kwargs)

    def get_usm_user_data(self, **kwargs):
        """
        To collect the user data for snmpv3

        Snmpv3 supports three security levels
            1. AuthPriv (Authentication and privacy)
            2. AuthNoPriv (Authentication)
            3. NoAuthNoPriv (None)

        List of supported Authentication protocols:
            usmNoAuthProtocol (default is authKey not given)
            usmHMACMD5AuthProtocol
            usmHMACSHAAuthProtocol
            usmHMAC128SHA224AuthProtocol
            usmHMAC192SHA256AuthProtocol
            usmHMAC256SHA384AuthProtocol
            usmHMAC384SHA512AuthProtocol

        List of supported Private protocols:
            usmNoPrivProtocol (default is privKey not given)
            usmDESPrivProtocol
            usm3DESEDEPrivProtocol
            usmAesCfb128Protocol
            usmAesCfb192Protocol
            usmAesCfb256Protocol

        To learn more about snmpv3 USMUserData refer the following docs
        https://pysnmp.readthedocs.io/en/latest/docs/api-reference.html#user-based
        """

        # Snmpv3 authentication protocols
        snmp_auth_protocol = {
            'md5': usmHMACMD5AuthProtocol,
            'sha': usmHMACSHAAuthProtocol,
            'sha224': usmHMAC128SHA224AuthProtocol,
            'sha256': usmHMAC192SHA256AuthProtocol,
            'sha384': usmHMAC256SHA384AuthProtocol,
            'sha512': usmHMAC384SHA512AuthProtocol,
        }
        # Snmpv3 private protocols
        snmp_priv_protocol = {
            'des': usmDESPrivProtocol,
            '3des': usm3DESEDEPrivProtocol,
            'aes128': usmAesCfb128Protocol,
            'aes192': usmAesCfb192Protocol,
            'aes256': usmAesCfb256Protocol,
        }

        auth_protocol=None
        priv_protocol=None

        # Get the username and security level
        username = kwargs.get('username')

        # Security level defaults to NoAuthNoPriv if its not provided
        security_level = kwargs.get('security_level', 'noauthnopriv')

        # To handle Authentication protocol and key
        if security_level in ['authpriv', 'authnopriv']:
            try:
                auth_protocol = snmp_auth_protocol[kwargs.get('auth_protocol')]
            except Exception as e:
                auth_protocol = None

        if not auth_protocol:
            log.info("No authentication protocol is provided.")
            auth_protocol = usmNoAuthProtocol

        auth_key = kwargs.get('auth_key')
        if auth_protocol != usmNoAuthProtocol:
            if not auth_key:
                raise Exception("The authentication key does not exist in the testbed")

        # To handle private protocol and key
        if security_level in ['authpriv']:
            priv_protocol = kwargs.get('priv_protocol')
            try:
                priv_protocol = snmp_priv_protocol[kwargs.get('priv_protocol')]
            except Exception as e:
                auth_protocol = None

        if not priv_protocol:
            log.info("No private protocol is provided.")
            priv_protocol = usmNoPrivProtocol

        priv_key = kwargs.get('priv_key')
        if priv_protocol != usmNoPrivProtocol:
            if not priv_key:
                raise Exception("The private key does not exist in the testbed")

        # build USMuserdata
        auth = UsmUserData(
            userName=username,
            authKey=auth_key,
            authProtocol=auth_protocol,
            privKey=priv_key,
            privProtocol=priv_protocol
        )

        return auth

    def connect(self, **kwargs):
        """ To connect the snmpv3 client
        """

        # To get the usm user data for authentication
        self.auth = self.get_usm_user_data(**kwargs)

        self.snmp_client = SNMPv3Client(host=self.host,
                                        port=self.port,
                                        auth=self.auth,
                                        log=self.log)

    def on(self, *outlets, after=None):
        """ To turn on the powercycler
        """

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
        """ To turn off the powercycler
        """

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
        """ To get the powercycler state
        """

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
                                
class BaseRaritanPowerCycler(PowerCycler):

    def __init__(self, testbed, **kwargs):
        super().__init__(**kwargs)
        self.testbed = testbed
        self.connect()

    def connect(self):
        if self.host not in self.testbed.devices:
            raise Exception("The device '{}' does not exist in the testbed"
                            .format(self.host))
        log.info('Assigning the host')
        self.host = self.testbed.devices[self.host]
        
        self.host.connect(learn_hostname=True,mit=True, allow_state_change=True)
        
        log.info('Device is connected')
        
        #self.con = con

    def off(self, *outlets, after=None):
        if isinstance(after, int):
            raise TypeError('"after" should be an int')

        if after:
            time.sleep(after)

        clear_line_dialog = Dialog([
            Statement(pattern='.*\?\s*\[y\/n\]',
                      action='sendline(y)',
                      loop_continue=True,
                      continue_timer=False)])
        #time.sleep(40)
        for outlet in outlets:
            time.sleep(10)
            log.info('INSIDE OFF')
            log.info('{0}'.format(outlet))
            try:
                self.host.execute('power outlets {} off'.format(outlet),
                                  reply=clear_line_dialog)               
            except Exception as e:
                raise Exception("Turning off outlet '{}' on the powercycler "
                                "failed. Error: {}".format(outlet, str(e)))

    def on(self, *outlets):
        time.sleep(40)
        for outlet in outlets:
            time.sleep(10)
            log.info('INSIDE ON')
            log.info('{0}'.format(outlet))
            try:
                clear_line_dialog = Dialog([
                    Statement(pattern='.*\?\s*\[y\/n\]',
                      action='sendline(y)',
                      loop_continue=True,
                      continue_timer=False)])
                self.host.execute('power outlets {} on'.format(outlet),
                                 reply=clear_line_dialog)                                 
                       
            except Exception as e:
                raise Exception("Turning on outlet '{}' on the powercycler "
                                "failed. Error: {}".format(outlet, str(e)))
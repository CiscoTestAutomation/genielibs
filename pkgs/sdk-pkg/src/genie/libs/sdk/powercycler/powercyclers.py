from .base import (BaseSNMPPowerCycler,
                   BaseCyberSwitchingPowerCycler)


class RaritanSnmpPX(BaseSNMPPowerCycler):
    type = 'raritan-px'
    connection_type = 'snmp'
    oid = '1.3.6.1.4.1.13742.4.1.2.2.1.3'
    on_state = 1
    off_state = 0


class RaritanSnmpPX2(BaseSNMPPowerCycler):
    type = 'raritan-px2'
    connection_type = 'snmp'
    oid = '1.3.6.1.4.1.13742.6.4.1.2.1.2.1'
    on_state = 1
    off_state = 0


class ApcSnmpPDU(BaseSNMPPowerCycler):
    type = 'apc'
    connection_type = 'snmp'
    oid = '1.3.6.1.4.1.318.1.1.4.4.2.1.3'
    on_state = 1
    off_state = 2


class ApcSnmpRPDU(BaseSNMPPowerCycler):
    type = 'apc-rpdu'
    connection_type = 'snmp'
    oid = '1.3.6.1.4.1.318.1.1.12.3.3.1.1.4'
    on_state = 1
    off_state = 2


class DualCommSnmpPDU(BaseSNMPPowerCycler):
    type = 'dualcomm'
    connection_type = 'snmp'
    oid = '1.3.6.1.4.1.14300.1.2.1.2.1.3'
    on_state = 2
    off_state = 1


class CyberSwitching(BaseCyberSwitchingPowerCycler):
    type = 'cyberswitching'
    connection_type = 'telnet'

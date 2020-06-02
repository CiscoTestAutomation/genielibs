import logging
log = logging.getLogger(__name__)
try:
    from pysnmp.hlapi import *
    import pysnmp
    from pysnmp.proto.rfc1905 import NoSuchInstance, NoSuchObject
    pysnmp_installed = True
except ImportError:
    pysnmp_installed = False

class SNMPClient(object):

    """Implements SNMP client using pysnmp package
    provides two API's snmpget and snmpset

    Usage:
            cl = SNMPClient(host='10.104.233.42', port=161)
        cl = SNMPClient(host='10.104.233.42',
                            read_community='public',
                            write_community='private',
                            version='2c',
                            port=161,
                            log=logging.getLogger(__name__))

        # Get value
        cl.snmp_get(oid='1.3.6.1.4.1.13742.6.4.1.2.1.2.1.16')

        # Set value
        cl.snmp_set(oid='1.3.6.1.4.1.13742.6.4.1.2.1.2.1.15',
                   value=1, type='Integer')

    """

    def __init__(self, host,
                 read_community='public',
                 write_community='private',
                 version='2c',
                 port=161,
                 log=log):

        """ Instantiates snmp client
        """
        if not pysnmp_installed:
            raise Exception(
                "pysnmp is not installed. Please run 'pip install pysnmp' to use this feature")

        self.host = host
        self.port = port

        # Read/Write communities of v1/v2c
        self.read_community = read_community
        self.write_community = write_community

        # pysnmp maps version to mp_model as mentioned below
        # version =
        #        0 for SNMPv1
        #        1 for SNMPv2c.
        #        ?? for SNMPv3
        # defaults to v2c
        # refer for more info:
        # http://pysnmp.sourceforge.net/docs/pysnmp-hlapi-tutorial.html#making-snmp-query

        if version == '1' or version == 1:
            self.mp_model = 0
        else:
            self.mp_model = 1

        self.log = log

    def snmp_get(self, oid, *more_oids):

        """ Performs a SNMP get operation

        Usage:
            cl.snmp_get(oid='1.3.6.1.4.1.13742.6.4.1.2.1.2.1.16')

            cl.snmp_get(oid='1.3.6.1.4.1.13742.6.4.1.2.1.2.1.16',
                        '1.3.6.1.4.1.13742.6.4.1.2.1.2.1.15')
        """

        # Create ObjectIdentifier for each oid's in the more list
        more_oid_obj = [ObjectType(ObjectIdentity(obj)) for obj in more_oids]

        # Create command generator
        cmd_generator = \
            getCmd(SnmpEngine(),
                   CommunityData(self.read_community,
                                 mpModel=self.mp_model), \
                   UdpTransportTarget((self.host, self.port)),
                   ContextData(),
                   ObjectType(
                       ObjectIdentity(oid)),
                   *more_oid_obj
                   )

        # Fetch the values
        error_indication, error_status, error_index, var_binds =\
            next(cmd_generator)

        # Predefine our results list
        results = []

        # Check for errors and print out results
        if error_indication:
            self.log.info(error_indication)
            raise Exception(str(error_indication))
        elif error_status:
            msg = '%s at %s' % (error_status.prettyPrint(),
                                   error_index and var_binds[int(error_index) - 1][
                                       0] or '?')
            log.info(msg)
            raise Exception(msg)
        else:
            for name, value in var_binds:
                msg = ' = '.join([name.prettyPrint(), value.prettyPrint()])
                self.log.info(msg)
                if isinstance(value, (NoSuchObject, NoSuchInstance)):
                    raise ValueError('Invalid object ' + str(msg))
                results.append(value.prettyPrint())
        return results

    def snmp_set(self, oid, value, type='Integer'):

        """ Performs a SNMP set operation

        Takes three arguments,
            OID = snmp object Identifier,
            value = value to be se
            type = Type can be any of SNMP supported types
                    like Integer, Integer32

        Usage:
            cl.snmp_set(oid='1.3.6.1.4.1.13742.6.4.1.2.1.2.1.16', value=1,
                        type='Integer')

        """

        # Get the pysnmp class for oid
        value_class = getattr(pysnmp.hlapi, type, None)
        if not value_class:
            raise TypeError('Invalid Type provided: %s' % (type,))

        # Create command generator
        cmd_generator = \
            setCmd(SnmpEngine(),
                   CommunityData(self.write_community,
                                 mpModel=self.mp_model), \
                   UdpTransportTarget((self.host, self.port)),
                   ContextData(),
                   ObjectType(
                       ObjectIdentity(oid), value_class(value)
                    )
                   )

        # Fetch the values
        error_indication, error_status, error_index, var_binds =\
            next(cmd_generator)

        # Predefine our results list
        results = []

        # Check for errors and print out results
        if error_indication:
            log.info(error_indication)
            raise Exception(str(error_indication))
        elif error_status:
            msg = '%s at %s' % (error_status.prettyPrint(),
                                   error_index and var_binds[int(error_index) - 1][
                                       0] or '?')
            log.info(msg)
            raise Exception(msg)
        else:
            for name, value in var_binds:
                msg = ' = '.join([name.prettyPrint(), value.prettyPrint()])
                self.log.info(msg)
                if isinstance(value, (NoSuchObject, NoSuchInstance)):
                    raise ValueError('Invalid object ' + str(msg))
                results.append(value)
        return results

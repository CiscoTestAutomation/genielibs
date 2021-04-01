'''
    Common base Device classes for all OSes.
'''

__all__ = (
    'Device',
    'EmulatedDevice',
)

import importlib
import warnings
import abc
from enum import Enum

from genie.decorator import managedattribute
import genie.conf.base.device
from genie.conf.base import Interface
from genie.conf.base.link import EmulatedLink
from genie.conf.base.attributes import AttributesHelper, AttributesHelper2
from genie.conf.base.cli import CliConfigBuilder

from genie.libs.conf.address_family import AddressFamily


class UnsupportedDeviceOsWarning(UserWarning):
    pass


class Device(genie.conf.base.device.Device):

    def __new__(cls, name, *args, **kwargs):
        kwargs['name'] = name

        factory_cls = cls
        if factory_cls is Device:
            # need to load the correct Device for the right os.
            device_os = kwargs.get('os', None)
            if device_os is None:
                device = kwargs.get('device', None)
                if device is not None:
                    device_os = getattr(device, 'os', None)
            if device_os is None:
                warnings.warn(
                    'Device {dev} OS is unknown;'
                    ' Extended Device functionality will not be available:'
                    ' mandatory field \'os\' was not given in the yaml'
                    ' file'.format(
                        dev=name, os=device_os),
                    UnsupportedDeviceOsWarning)

            else:
                # Get the location where it will be loaded to
                mod = 'genie.libs.conf.device.{os}'.\
                    format(os=device_os)

                try:
                    # import it
                    OsDeviceModule = importlib.import_module(mod)
                    factory_cls = OsDeviceModule.Device
                except (ImportError, AttributeError) as e:
                    # it does not exist, then just use the default one.
                    # At this time, this is expected, so don't warn at all.
                    pass

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    custom_config_cli = managedattribute(
        name='custom_config_cli',
        finit=str,
        type=managedattribute.test_istype(str))

    custom_unconfig_cli = managedattribute(
        name='custom_unconfig_cli',
        finit=str,
        type=managedattribute.test_istype(str))

    # nodename
    nodename = managedattribute(
        name='nodename',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Hostname of the device")

    def learn_interface_mac_addresses(self):
        return NotImplemented  # Not an error; Just not supported.

    def build_config(self, apply=True, attributes=None):
        """method to build the configuration of the device

        Api to build the configuration of a device object. This configuration
        depends of the configurable attributes of this object.

        Args:
            apply (`bool`): Apply the configuration on the device, unless
                            it is set to False, then return the configuration,
                            without applying it.
        Return:
            None if it was applied on the device

            `str` if apply was set to False

        Examples:
            >>> from genie.base.device import Device

            Create a Device obj

            >>> device = Device(name='PE1')

            assign configurable attributes to device obj

            >>> device.username = 'lab'
            >>> device.password = 'lab'

            build configuration and apply it on the device

            >>> device.build_config()

            build configuration and only return it

            >>> configuration = device.build_config(apply=False)
        """
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder()

        # check added features and add to configurations
        if self.features:
            for feature in self.features:
                # check if feature in attributes
                feature_name = feature.__class__.__name__.lower()
                if isinstance(attributes.attributes, dict):
                    if feature_name in attributes.attributes:
                        attr = AttributesHelper2(feature, attributes.attributes[feature_name])
                        for _, sub, attributes2 in attr.mapping_items(
                            'device_attr',
                            keys=set([self]), sort=True):
                            configurations.append_block(sub.build_config(apply=False, attributes=attributes2.attributes))
                else:
                    attr = AttributesHelper2(feature, attributes)
                    for _, sub, attributes2 in attr.mapping_items(
                        'device_attr',
                        keys=set([self]), sort=True):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2))

        configurations.append_block(
            attributes.format('{custom_config_cli}'))

        if apply:
            if configurations:
                self.configure(str(configurations), fail_invalid=True)
        else:
            # Return configuration
            return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        """method to build the unconfiguration of the device object

        Api to build the unconfiguration of a device object. This
        unconfiguration depends of the configurable attributes of this object.

        Args:
            apply (`bool`): Apply the configuration on the device, unless
                            it is set to False, then return the configuration,
                            without applying it.
        Return:
            None if it was applied on the device

            `str` if apply was set to False

        Examples:
            >>> from genie.base.device import Device

            Create a Device obj

            >>> device = Device(name='PE1')

            build configuration and apply it on the device

            >>> device.build_unconfig()

            build configuration and only return it

            >>> configuration = device.build_unconfig(apply=False)
        """
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=True)

        # check added features and add to configurations
        if self.features:
            for feature in self.features:
                # check if feature in attributes
                feature_name = feature.__class__.__name__.lower()
                if isinstance(attributes.attributes, dict):
                    if feature_name in attributes.attributes:
                        attr = AttributesHelper2(feature, attributes.attributes[feature_name])
                        for _, sub, attributes2 in attr.mapping_items(
                            'device_attr',
                            keys=set([self]), sort=True):
                            configurations.append_block(sub.build_unconfig(apply=False, attributes=attributes2.attributes))
                else:
                    attr = AttributesHelper2(feature, attributes)
                    for _, sub, attributes2 in attr.mapping_items(
                        'device_attr',
                        keys=set([self]), sort=True):
                        configurations.append_block(sub.build_unconfig(apply=False, attributes=attributes2))

        configurations.append_block(
            attributes.format('{custom_unconfig_cli}'))

        if apply:
            if configurations:
                self.configure(str(configurations), fail_invalid=True)
        else:
            # Return configuration
            return str(configurations)

    #@abc.abstractmethod
    def __init__(self, *args, **kwargs):
        '''Base initialization for all Device subclasses.

        This is not an abstract class since it may be used to instantiate
        generic unsupported devices.
        '''

        super().__init__(*args, **kwargs)

    def get_os_specific_Interface_class(self):
        from genie.libs.conf.interface import Interface as xbuInterface
        return xbuInterface._get_os_specific_Interface_class(self.os)

    def clean_interface_name(self, interface_name):
        osInterface = self.get_os_specific_Interface_class()
        return osInterface.clean_interface_name(interface_name)

    def short_interface_name(self, interface_name):
        osInterface = self.get_os_specific_Interface_class()
        return osInterface.short_interface_name(interface_name)


class EmulatedDevice(Device):

    tgen_interface = managedattribute(
        name='tgen_interface',
        type=managedattribute.test_auto_ref(
            managedattribute.test_isinstance(Interface)),
        gettype=managedattribute.auto_unref)

    @property
    def tgen_device(self):
        return self.tgen_interface.device

    tgen_handle = managedattribute(
        name='tgen_handle',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='''The emulated device handle, as understood by HLTAPI/low-level vendor APIs.''')

    emulated_loopback = managedattribute(
        name='emulated_loopback',
        default=None,
        #type=(None, managedattribute.test_isinstance(EmulatedLoopbackInterface)),
    )

    emulated_interface = managedattribute(
        name='emulated_interface',
        default=None,
        #type=(None, managedattribute.test_isinstance(EmulatedInterface)),
    )

    emulated_link = managedattribute(
        name='emulated_link',
        default=None,
        type=(None, managedattribute.test_isinstance(EmulatedLink)),
    )

    @property
    def tgen_port_handle(self):
        return self.tgen_interface.tgen_port_handle

    @property
    def os(self):
        return self.tgen_device.os

    @property
    def context(self):
        return self.tgen_device.context

    @property
    def type(self):
        return self.tgen_device.type

    gateway_interface = managedattribute(
        name='gateway_interface',
        type=(None, managedattribute.test_isinstance(Interface)))

    @gateway_interface.defaulter
    def gateway_interface(self):
        return self.tgen_interface.gateway_interface

    @property
    def gateway_ipv4(self):
        gateway_interface = self.gateway_interface
        ipv4 = gateway_interface and gateway_interface.ipv4
        return ipv4 and ipv4.ip

    @property
    def gateway_ipv6(self):
        gateway_interface = self.gateway_interface
        ipv6 = gateway_interface and gateway_interface.ipv6
        return ipv6 and ipv6.ip

    def __new__(cls, name, *args, **kwargs):
        kwargs['name'] = name

        factory_cls = cls
        if factory_cls is EmulatedDevice:
            try:
                tgen_interface = kwargs['tgen_interface']
            except KeyError:
                raise TypeError('Missing tgen_interface keyword argument')
            # need to load the correct Device for the right os.
            os = tgen_interface.device.os
            # Get the location where it will be loaded to
            mod = 'genie.libs.conf.device.{os}'.\
                format(os=os)

            # import it
            OsDeviceModule = importlib.import_module(mod)
            factory_cls = OsDeviceModule.EmulatedDevice

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    @abc.abstractmethod
    def __init__(self, name, *args, tgen_interface,
                 create_loopback=True,
                 create_interface=True,
                 create_link=True,
                 address_families={AddressFamily.ipv4},
                 lo_ipv4=None, lo_ipv6=None,
                 ipv4=None, ipv6=None,
                 mac_address=None,
                 **kwargs):
        self.tgen_interface = tgen_interface  # A lot may depend on this

        super().__init__(*args, name=name, **kwargs)

        tgen_device = self.tgen_device

        if create_loopback or create_interface:
            from genie.libs.conf.interface import EmulatedInterface
            from genie.libs.conf.interface import _get_descendent_subclass
            emul_os_interface_class = EmulatedInterface._get_os_specific_EmulatedInterface_class(self.os)

        if create_loopback:

            if self.os == 'pagent':

                # Pagent requires router IDs to have lower values than interfaces;
                # Promise an address in a class A network.
                # Always need IPv4 loopback
                if lo_ipv4 is None and AddressFamily.ipv4 in address_families:
                    lo_ipv4 = self.testbed.ipv4_cache.reserve(type='A', prefixlen=32)[0]
                if lo_ipv6 is None and AddressFamily.ipv6 in address_families:
                    pass  # lo_ipv6 = self.testbed.ipv6_cache.reserve(TODO)[0]

            else:

                # Always need IPv4 loopback
                if lo_ipv4 is None and AddressFamily.ipv4 in address_families:
                    lo_ipv4 = self.testbed.ipv4_cache.reserve(prefixlen=32)[0]
                if lo_ipv6 is None and AddressFamily.ipv6 in address_families:
                    lo_ipv6 = self.testbed.ipv6_cache.reserve(prefixlen=128)[0]

            from genie.libs.conf.interface import LoopbackInterface
            emul_lo_interface_class = _get_descendent_subclass(emul_os_interface_class, LoopbackInterface)

            self.emulated_loopback = emul_lo_interface_class(
                device=self,
                name='Loopback0',
                ipv4=lo_ipv4, lo_ipv6=lo_ipv6,
            )

        if create_interface:

            router_interface = self.gateway_interface

            from genie.libs.conf.interface import EthernetInterface
            emul_phy_interface_class = _get_descendent_subclass(emul_os_interface_class, EthernetInterface)
            # TODO support other interface base classes

            #### set vRtrIntf [lindex [enaTbGetInterfacePeer $vTgenIntf -linktype {iflink ifmesh}] 0]
            if self.os == 'pagent':

                # XXXJST TODO -- Pagent can use multiple emulations (OSPF) but they overwrite the main port's IP
                if ipv4 is None and AddressFamily.ipv4 in address_families:
                    ipv4 = self.tgen_interface.ipv4
                if ipv6 is None and AddressFamily.ipv6 in address_families:
                    ipv6 = self.tgen_interface.ipv6
                if mac_address is None:
                    mac_address = self.tgen_interface.mac_address

                self.emulated_interface = emul_phy_interface_class(
                    device=self,
                    name=self.tgen_interface.name,
                    mac_address=mac_address,
                    ipv4=ipv4, ipv6=ipv6,
                )

            else:

                if ipv4 is None and AddressFamily.ipv4 in address_families:
                    base_ipv4 = self.tgen_interface.ipv4
                    assert base_ipv4
                    broadcast_address = base_ipv4.network.broadcast_address
                    for n in itertools.count(1):
                        ipv4_ip = base_ipv4.ip + n
                        if ipv4_ip == broadcast_address:
                            raise RuntimeError('No ipv4 addresses left in %r\'s network' % (base_ipv4,))
                        ipv4 = IPv4Interface((ipv4_ip, base_ipv4.network.prefixlen))
                        if not self.testbed.find_interfaces(ipv4=ipv4):
                            break

                if ipv6 is None and AddressFamily.ipv6 in address_families:
                    base_ipv6 = self.tgen_interface.ipv6
                    assert base_ipv6
                    broadcast_address = base_ipv6.network.broadcast_address
                    for n in itertools.count(1):
                        ipv6_ip = base_ipv6.ip + n
                        if ipv6_ip == broadcast_address:
                            raise RuntimeError('No ipv6 addresses left in %r\'s network' % (base_ipv6,))
                        ipv6 = IPv6Interface((ipv6_ip, base_ipv6.network.prefixlen))
                        if not self.testbed.find_interfaces(ipv6=ipv6):
                            break

                if mac_address is None:
                    mac_address = self.testbed.mac_cache.reserve(count=1)[0]

                self.emulated_interface = emul_phy_interface_class(
                    device=self,
                    name='Ethernet0',
                    ipv4=ipv4, ipv6=ipv6,
                    mac_address=mac_address,
                )

            if create_link:
                self.emulated_link = EmulatedLink(
                    name='{}-emulated_link'.format(name),
                    interfaces=[self.emulated_interface, router_interface])

    def __repr__(self):
        try:
            name = self.name
            tgen_interface = self.tgen_interface
            assert tgen_interface
            tgen_device = tgen_interface.device
            assert tgen_device
        except:
            return super().__repr__()
        else:
            return '<%s object %r on %s %s at 0x%x>' % (
                self.__class__.__name__,
                name,
                tgen_device.name,
                tgen_interface.name,
                id(self))

    @abc.abstractmethod
    def build_config(self, *args, **kwargs):
        return ''

    @abc.abstractmethod
    def build_unconfig(self, *args, **kwargs):
        return ''


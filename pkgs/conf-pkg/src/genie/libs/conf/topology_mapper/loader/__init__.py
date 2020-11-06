import os
import sys
import logging

from pyats.utils.yaml import Loader

from .markup import TopologyMarkupProcessor

from ..schema import production_schema
from ..link import Link
from ..interface import Interface
from ..device import Device
from .. import TopologyMapper
from ..exceptions import MissingDeviceError

logger = logging.getLogger(__name__)


class TopologyFileLoader(Loader):
    '''TopologyFileLoader class

    Provides APIs & functionality to load YAML topology files into
    corresponding topology objects.

    Note
    ----
        this class is in effect a singleton.
    '''

    def __init__(self):
        '''__init__ (built-in)

        instantiate parent Loader class by using custom schema, markup
        processor and post-processor. This allows loading topology context info
        directly into topology objects.
        '''

        # load and store the schema file internally
        super().__init__(schema=production_schema,
                         markupprocessor=TopologyMarkupProcessor(),
                         postprocessor=self.create_topology)

    def load(self, obj, in_place=None, locations=None):
        self.in_place = in_place
        try:
            return super().load(obj, locations=locations)
        finally:
            self.in_place = None

    def load_arbitrary(self, loadable, locations=None):
        # call generic YAML loader
        # ------------------------
        config = super().load_arbitrary(loadable, locations=locations)

        # apply defaults
        # --------------
        # force {} - yaml loads into None if there's no info
        config['subsets'] = config.get('subsets', None) or {}
        config['devices'] = config.get('devices', None) or {}
        config['topology'] = config.get('topology', None) or {}

        # apply default topology file
        # --------------------------
        filename=None
        if isinstance(loadable, str) and os.path.isfile(loadable):
            filename = os.path.basename(loadable)
            config['topology_file'] = loadable
        else:
            try:
                # If loadable is a file-like object, then it has a
                # .name attribute.
                filename = os.path.basename(loadable.name)
                config['topology_file'] = loadable.name
            except AttributeError:
                logger.debug("Loadable {} does not have .name attribute.".\
                    format(loadable))

        # apply default topology name
        # --------------------------
        try:
            name = config['name']
        except (KeyError, TypeError):
            logger.debug("Deriving topology name ...")
            if filename:
                if filename.startswith('CONFIG.'):
                    # name in the format of CONFIG.<tbname> (or other)
                    # assume last word is tb name
                    name = filename.split('.')[1]
                else:
                    # name in the format of <tbname>.yaml (or other)
                    # assume first word is testbed name
                    name = filename.split('.')[0]
            else:
                # no name provided
                name = ''
        finally:
            config['name'] = name

        return config

    def create_topology(self, config):
        # convert config into TopologyMapper objects
        # -----------------------------------
        # create TopologyMapper object from topology configs
        if self.in_place:
            topology = self.in_place
        else:
            topology = TopologyMapper(
                # TODO name=config['name'],
            )
        constraints = topology.constraints
        topology.topology_file=config.get('topology_file', None)

        # create Device objects from device section, add to topology
        for name, device in config['devices'].items():
            # expand device as kwargs
            device['match_name'] = device.pop('name', None)
            constraints.add_device(Device(name=name, **device))

        # parse topology block
        #   1. find the link fields and replace the with actual link objects
        #   2. create interfaces and add them to links
        #   3. add interfaces to each device object.

        # track all the unique links in this topology
        links = {}

        # process if there's extended link information section
        if 'links' in config['topology']:
            # make sure to pop the links section so that it doesn't get
            # treated as a device
            for name, linkinfo in config['topology'].pop('links').items():
                linkinfo['match_name'] = linkinfo.pop('name', None)
                links[name] = Link(name=name, **linkinfo)

        # process devices in topology section
        for device in config['topology']:
            if device not in constraints.devices:
                raise MissingDeviceError(device)

            interfaces = config['topology'][device]['interfaces']

            for name, intf in interfaces.items():
                if 'link' in intf:
                    # interface contains a link
                    linkname = intf['link']

                    if linkname not in links:
                        # discovered a new link in str format
                        links[linkname] = Link(name=linkname)

                    # make a copy of intf dict,
                    # replace the topology dict information with link objects
                    intf = intf.copy()
                    intf.update(link=links[linkname])

                # create the interface & add to device
                intf['match_name'] = intf.pop('name', None)
                constraints.devices[device].add_interface(
                        Interface(
                            name=device + name,  # I# -> R#I#
                            **intf))

        # process subsets section
        device_names = constraints.device_names
        link_names = constraints.link_names
        interface_names = constraints.interface_names
        for subset_name, subset_required_objects in config['subsets'].items():
            subset_required_objects = set(subset_required_objects)
            for object_name in set(subset_required_objects):
                if object_name in device_names:
                    pass
                elif object_name in link_names:
                    subset_required_objects.update(constraints.link_interface_names(object_name))
                    pass
                elif object_name in interface_names:
                    pass
                else:
                    raise ValueError(object_name)
            constraints.subsets[subset_name] = subset_required_objects

        return topology


# module = obj instance
sys.modules[__name__] = TopologyFileLoader()

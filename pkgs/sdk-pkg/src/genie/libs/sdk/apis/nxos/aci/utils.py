"""Base functions (get/post/delete) for ACI APIC"""

# Python
import logging

from genie.libs.sdk.apis.utils import copy_to_device as generic_copy_to_device

from pyats.utils.fileutils import FileUtils

log = logging.getLogger(__name__)


def apic_rest_get(device,
                  dn,
                  connection_alias='',
                  query_target='self',
                  rsp_subtree='no',
                  query_target_filter='',
                  rsp_prop_include='all',
                  rsp_subtree_include='',
                  rsp_subtree_class='',
                  expected_status_code=200,
                  timeout=30):
    """GET REST Command to retrieve information from the device

        Args:
            device (`obj`): Device object
            dn (`string`): Unique distinguished name that describes the object
                         and its place in the tree.
            connection_alias (`str`): Connection alias
            query_target {self|children|subtree}: 
                                'self': (default) MO itself
                                'children': just the MO's child objects
                                'subtree': MO and its child objects
            rsp_subtree {no|children|full}: Specifies child object level 
                                            included in the response
                                            'no': (default) the response
                                                   does not include any children
                                            'children': return only the child 
                                                        objects
                                            'full': includes the full tree 
                                                    structure
            rsp_prop_include {all|naming-only|config-only}:
                                'all': all properties of the objects
                                'naming-only': only the naming properties
                                'config-only': only configurable properties
            rsp_subtree_include (`string`): specify additional contained objects 
                                          or options to be included
            rsp_subtree_class (`string`) : specify classes
            query_target_filter (`string`): filter expression
            expected_status_code (`int`): Expected result

        Returns:
            Output from REST API
        
        Raise:
            None
    """

    if connection_alias:
        try:
                device = getattr(device, connection_alias)
        except AttributeError as e:
            raise Exception("'{dev}' does not have a connection with the "
                            "alias '{alias}'".format(
                                dev=device.name, alias=connection_alias)) from e

    output = ''
    try:
        output = device.get(dn, query_target, rsp_subtree, query_target_filter,
                            rsp_prop_include, rsp_subtree_include,
                            rsp_subtree_class, expected_status_code, timeout)
    except Exception as e:
        log.info("Failed to get: {}".format(e))

    return output


def apic_rest_post(device,
                   dn,
                   payload,
                   connection_alias='',
                   expected_status_code=200,
                   timeout=30):
    '''POST REST Command to configure information from the device

        Args:
            device (`obj`): Device object
            dn (`string`): Unique distinguished name that describes the object
                         and its place in the tree.
            payload (`dict`): Dictionary containing the information to send via
                            the post
            connection_alias (`str`): Connection alias
            expected_status_code (`int`): Expected result
            timeout (`int`): Maximum time

        Returns:
            Output from REST API
        
        Raise:
            None
    '''

    if connection_alias:
        try:
            device = getattr(device, connection_alias)
        except AttributeError as e:
            raise Exception("'{dev}' does not have a connection with the "
                            "alias '{alias}'".format(
                                dev=device.name, alias=connection_alias)) from e

    output = ''
    try:
        output = device.post(dn, payload, expected_status_code, timeout)
    except Exception as e:
        log.info("Failed to post: {}".format(e))

    return output


def apic_rest_delete(device,
                     dn,
                     connection_alias='',
                     expected_status_code=200,
                     timeout=30):
    '''DELETE REST Command to delete information from the device

        Args:
            dn (`string`): Unique distinguished name that describes the object
                         and its place in the tree.
            connection_alias (`str`): Connection alias
            expected_status_code (`int`): Expected result
            timeout (`int`): Maximum time

        Returns:
            Output from REST API
        
        Raise:
            None
    '''

    if connection_alias:
        try:
            device = getattr(device, connection_alias)
        except AttributeError as e:
            raise Exception("'{dev}' does not have a connection with the "
                            "alias '{alias}'".format(
                                dev=device.name, alias=connection_alias)) from e

    output = ''
    try:
        output = device.delete(dn, expected_status_code, timeout)
    except Exception as e:
        log.info("Failed to post: {}".format(e))

    return output

def copy_to_device(device,
                   remote_path,
                   local_path,
                   server,
                   protocol,
                   vrf=None,
                   timeout=300,
                   compact=False,
                   use_kstack=False,
                   username=None,
                   password=None,
                   **kwargs):
    """
    Copy file from linux server to device
        Args:
            device ('Device'): Device object
            remote_path ('str'): remote file path on the server
            local_path ('str'): local file path to copy to on the device
            server ('str'): hostname or address of the server
            protocol('str'): file transfer protocol to be used
            vrf ('str'): vrf to use (optional)
            timeout('int'): timeout value in seconds, default 300
            compact('bool'): compress image option for n9k, defaults False
            username('str'): Username to be used during copy operation
            password('str'): Password to be used during copy operation
            use_kstack('bool'): Use faster version of copy, defaults False
                                Not supported with a file transfer protocol
                                prompting for a username and password
        Returns:
            None
    """
    # aci uses the linux implementation and fileutils doesnt support
    # os/platform abstraction
    setattr(device, 'os', 'linux')
    fu = FileUtils.from_device(device)
    setattr(device, 'os', 'nxos')

    generic_copy_to_device(device=device,
                           remote_path=remote_path,
                           local_path=local_path,
                           server=server,
                           protocol=protocol,
                           vrf=vrf,
                           timeout=timeout,
                           compact=compact,
                           use_kstack=use_kstack,
                           username=username,
                           password=password,
                           fu=fu,
                           **kwargs)
"""Base functions (get/post/delete) for APIC"""

# Python
import re
import logging

from genie.libs.sdk.apis.nxos.aci.utils import (copy_to_device as
                                                aci_copy_to_device,
                                                copy_from_device as
                                                aci_copy_from_device)

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
                  target_subtree_class='',
                  order_by='',
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
            target_subtree_class (string): specify subtree classes
            query_target_filter (`string`): filter expression
            order_by (`string`): sort the query response by one or
                                 more properties of a class
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
            raise Exception(
                "'{dev}' does not have a connection with the "
                "alias '{alias}'".format(dev=device.name,
                                         alias=connection_alias)) from e

    output = ''
    try:
        output = device.get(dn=dn,
                            query_target=query_target,
                            rsp_subtree=rsp_subtree,
                            query_target_filter=query_target_filter,
                            rsp_prop_include=rsp_prop_include,
                            rsp_subtree_include=rsp_subtree_include,
                            rsp_subtree_class=rsp_subtree_class,
                            target_subtree_class=target_subtree_class,
                            order_by=order_by,
                            expected_status_code=expected_status_code,
                            timeout=timeout)
    except Exception as e:
        log.info("Failed to get: {}".format(e))

    return output


def apic_rest_post(device,
                   dn,
                   payload,
                   xml_payload=False,
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
            xml_payload (bool): Set to True if payload is in XML format
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
            raise Exception(
                "'{dev}' does not have a connection with the "
                "alias '{alias}'".format(dev=device.name,
                                         alias=connection_alias)) from e

    output = ''
    try:
        output = device.post(dn=dn,
                             payload=payload,
                             xml_payload=xml_payload,
                             expected_status_code=expected_status_code,
                             timeout=timeout)
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
            raise Exception(
                "'{dev}' does not have a connection with the "
                "alias '{alias}'".format(dev=device.name,
                                         alias=connection_alias)) from e

    output = ''
    try:
        output = device.delete(dn, expected_status_code, timeout)
    except Exception as e:
        log.info("Failed to post: {}".format(e))

    return output


def copy_to_device(device,
                   remote_path,
                   local_path=None,
                   server=None,
                   protocol='scp',
                   vrf=None,
                   timeout=300,
                   compact=False,
                   use_kstack=False,
                   fu=None,
                   http_auth=True,
                   **kwargs):
    """
    Copy file from linux server to the device.

    Args:
        device (Device): Device object
        remote_path (str): remote file path on the server
        local_path (str): local file to copy to on the device (default: None)
        server (str): hostname or address of the server (default: None)
        protocol(str): file transfer protocol to be used (default: scp)
        vrf (str): vrf to use (optional)
        timeout(int): timeout value in seconds, default 300
        compact(bool): compress image option for n9k, defaults False
        fu(obj): FileUtils object to use instead of creating one. Defaults to None.
        use_kstack(bool): Use faster version of copy, defaults False
                            Not supported with a file transfer protocol
                            prompting for a username and password
        http_auth (bool): Use http authentication (default: True)

    Returns:
        None

    If the server is not specified, a HTTP server will be spawned
    on the local system and serve the directory of the file
    specified via remote_path and the copy operation will use http.

    If the device is connected via CLI proxy (unix jump host) and the proxy has
    'socat' installed, the transfer will be done via the proxy automatically.
    """
    return aci_copy_to_device(device=device,
                              remote_path=remote_path,
                              local_path=local_path,
                              server=server,
                              protocol=protocol,
                              vrf=vrf,
                              timeout=timeout,
                              compact=compact,
                              use_kstack=use_kstack,
                              fu=fu,
                              http_auth=http_auth,
                              **kwargs)


def copy_from_device(device,
                     local_path,
                     remote_path=None,
                     server=None,
                     protocol='http',
                     vrf=None,
                     timeout=300,
                     timestamp=False,
                     http_auth=True,
                     **kwargs):
    """
    Copy a file from the device to the server or local system (where the script is running).
    Local system copy uses HTTP and is only supported via SSH sessions.

    Args:
        device (Device): device object
        local_path (str): local path from the device (path including filename)
        remote_path (str): Path on the server (default: .)
        server (str): Server to copy file to (optional)
        protocol (str): Protocol to use to copy (default: http)
        vrf (str): VRF to use for copying (default: None)
        timeout('int'): timeout value in seconds, default 300
        timestamp (bool): include timestamp in filename (default: False)
        http_auth (bool): Use http authentication (default: True)

    Returns:
        (boolean): True if successful, False if not

    If the server is not specified, below logic applies.

    If no filename is specified, the filename will be based on the device hostname
    and slugified name of the file determined from the local_path.

    The local IP adddress will be determined from the spawned telnet or ssh session.
    A temporary http server will be created and the show tech file will be sent
    to the host where the script is running.

    If the device is connected via proxy (unix jump host) and the proxy has
    'socat' installed, the upload will be done via the proxy automatically.

    Note: if the file already exists, it will be overwritten.
    """
    return aci_copy_from_device(device,
                                local_path=local_path,
                                remote_path=remote_path,
                                server=server,
                                protocol=protocol,
                                vrf=vrf,
                                timeout=timeout,
                                timestamp=timestamp,
                                http_auth=http_auth,
                                **kwargs)


def get_mgmt_src_ip_addresses(device):
    """ Get the source IP addresses connected via SSH or telnet to the device.

    Returns:
        List of IP addresses or []
    """
    mgmt_ip = device.api.get_mgmt_ip()

    netstat_output = device.execute('netstat -an | grep {}:22'.format(mgmt_ip))
    # tcp        0      0 172.1.1.2:22        10.1.1.1:59905     ESTABLISHED -
    mgmt_src_ip_addresses = re.findall(r'\d+ +\S+:\d+ +(\S+):\d+ +ESTAB',
                                       netstat_output)
    if not mgmt_src_ip_addresses:
        log.error(
            'Unable to find management session, cannot determine management IP addresses'
        )
        return []

    return mgmt_src_ip_addresses


def get_mgmt_ip(device):
    """ Get the management IP address of the device.

    Returns:
        IP address string or None
    """
    output = device.execute('show oob-mgmt')

    # Type             Node ID     Ip Address            Gateway               OOB-EPG               Oper State
    # ---------------  ----------  --------------------  --------------------  --------------------  ----------
    # msl-             1           172.1.1.2/24          172.1.1.1             default               up
    m = re.search(r'\S+\s+\d+\s+(\S+)/\d+\s+', output)
    if m:
        mgmt_ip = m.group(1)
    else:
        log.error(
            'Unable to find management session, cannot determine IP address')
        return None

    return mgmt_ip

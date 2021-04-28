"""Base functions (get/post/delete) for APIC"""

# Python
import re
import logging

from genie.libs.filetransferutils import FileServer

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


def copy_to_script_host(device,
                 filename,
                 local_path=None,
                 timeout=300):
    """
    Copy a file from the device to the local system where the script is running.
    Uses HTTP. Only supported via telnet or SSH sessions.

    Args:
        device (Device): device object
        filename (str): filename to copy
        local_path (str): local path to copy the file to, defaults to '.'
        timeout('int'): timeout value in seconds, default 300

    Returns:
        (boolean): True if successful, False if not

    The local IP adddress will be determined from the spawned telnet or ssh session.
    A temporary http server will be created and the show tech file will be sent
    to the host where the script is running.

    If the device is connected via proxy (unix jump host) and the proxy has
    'socat' installed, the upload will be done via the proxy automatically.
    """

    local_path = local_path or '.'

    output = device.execute('show oob-mgmt')

    # Type             Node ID     Ip Address            Gateway               OOB-EPG               Oper State
    # ---------------  ----------  --------------------  --------------------  --------------------  ----------
    # msl-             1           172.1.1.2/24          172.1.1.1             default               up
    m = re.search(r'\S+\s+\d+\s+(\S+)/\d+\s+', output)
    if m:
        mgmt_ip = m.group(1)

    netstat_output = device.execute('netstat -an | grep {}:22'.format(mgmt_ip))
    # tcp        0      0 172.1.1.2:22        10.1.1.1:59905     ESTABLISHED -
    mgmt_src_ip_addresses = re.findall(r'\d+ +\S+:\d+ +(\S+):\d+ +ESTAB', netstat_output)

    # try figure out local IP address
    local_ip = device.api.get_local_ip()

    if local_ip in mgmt_src_ip_addresses:
        mgmt_src_ip = local_ip
    else:
        mgmt_src_ip = None

    with FileServer(protocol='http',
                    address=local_ip,
                    path=local_path) as fs:

        local_port = fs.get('port')

        proxy_port = None
        # Check if we are connected via proxy device
        proxy = device.connections[device.via].get('proxy')
        if proxy and isinstance(proxy, str):
            log.info('Setting up port relay via proxy')
            proxy_dev = device.testbed.devices[proxy]
            proxy_dev.connect()
            proxy_port = proxy_dev.api.socat_relay(remote_ip=local_ip, remote_port=local_port)

            ifconfig_output = proxy_dev.execute('ifconfig')
            proxy_ip_addresses = re.findall(r'inet (?:addr:)?(\S+)', ifconfig_output)
            mgmt_src_ip = None
            for proxy_ip in proxy_ip_addresses:
                if proxy_ip in mgmt_src_ip_addresses:
                    mgmt_src_ip = proxy_ip
                    break

        try:
            if mgmt_src_ip and proxy_port:
                device.execute('curl --upload-file {} http://{}:{}'.format(
                               filename, mgmt_src_ip, proxy_port),
                               timeout=timeout, append_error_pattern=[r'%Error'])
            elif mgmt_src_ip:
                device.execute('curl --upload-file {} http://{}:{}'.format(
                               filename, mgmt_src_ip, local_port),
                               timeout=timeout, append_error_pattern=[r'%Error'])
            else:
                log.error('Unable to determine management IP address to use to upload file')
                return False

        except Exception:
            log.error('Failed to transfer file', exc_info=True)
            return False

    return True

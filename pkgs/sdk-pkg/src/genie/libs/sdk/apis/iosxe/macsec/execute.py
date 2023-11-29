# Python
import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)

def execute_crypto_pki_server(device, certificate_req, server_name, 
                              copy_certificate, sleep_time=5):
    """ Config execute crypto pki server
        Args:
            device ('obj'): device object
            certificate_req ('str'): certificate request options like <authenticate,benchmark,import,export ...>
            server_name('str'):  CA Server Name
            copy_certificate(str): CA certificate copy 
            sleep_time(int) : sleep time
        Return:
            None
        Raises:
            SubCommandFailure: Failed execute device
    """

    def send_certificate(spawn):
        time.sleep(sleep_time)
        spawn.sendline(f'{copy_certificate}')
        spawn.sendline()

    dialog = Dialog([
        Statement(pattern=r'.*End with a blank line or the word \"quit\" on a line by itself.*',
                  action=send_certificate,
                  loop_continue=True,
                  continue_timer=False)])

    cmd = f"crypto pki {certificate_req} {server_name}"

    try:
        if certificate_req == 'authenticate':
            device.execute(cmd, reply=dialog)
        else:
            device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute crypto pki action server. Error:\n{e}")

def execute_test_opssl_nonblockingsession_client(device, version, host_ip_addr, port_number,
                                                    num_connections,num_messages, pre_key,
                                                    identity_check, identity_label,verfiy_label):
    """
        Execute test opssl nonblockingsession client
        Args:
            device ('obj'): device object
            version('int'): server versions
            host_ip_addr('int'): peer's IP address
            port_number('int'):  port number for connect or accept <1-10000> 
            num_connections('int'): Number of connections <1-50> 
            num_messages('int'): number of messages before sending close notification <1-100>  
            pre_key('int'): Pre-shared key <16-134217727>
            identity_check('int'): Disable/Enable Server Identity Check <0-1> 
            identity_label('int'): Identity TrustPoint label 
            verfiy_label('str'):  Verification TrustPoint label
        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    cmd=f"test opssl nonblockingsession client {version} {host_ip_addr} {port_number} {num_connections} {num_messages} {pre_key} {identity_check} {identity_label} {verfiy_label}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure test opssl nonblockingsession client. Error:\n{e}")


def execute_test_opssl_nonblockingsession_server_stop(device, session_mode, version, test_server):
    """ Execute opssl nonblockingsession server stop
        Args:
            device ('obj'): device object
            session_mode ('str'): Session modes <client/server>
            version('str'): server versions
            test_server('str'): OPSSL test-server <start/stop>
        Return:
            None
        Raises:
            SubCommandFailure: Failed execute device
    """
    cmd = f"test opssl nonblockingsession {session_mode} {version} {test_server}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute test opssl nonblockingsession. Error:\n{e}")

def execute_test_opssl_nonblockingsession_server_start(device, version, test_server,
                                                       host_ip_addr, port_number,pre_key, 
                                                       identity_check,identity_label, verfiy_label):
    """ Execute opssl nonblockingsession server tls1.2 start
        Args:
            device ('obj'): device object
            version('str'): server versions
            test_server('str'): OPSSL test-server <start/stop>
            host_ip_addr(int):  host IP address
            port_number('int'): port number for connect or accept  <1-10000>  
            pre_key('int'): Pre-shared key  <16-134217727>  
            identity_check('int'): Disable/Enable Server Identity Check <0-1> 
            identity_label('str'):  Identity TrustPoint label
            verfiy_label ('str'): Verification TrustPoint label
        Return:
            None
        Raises:
            SubCommandFailure: Failed execute device
   """
    cmd = f"test opssl nonblockingsession server {version} {test_server} {host_ip_addr} {port_number} {pre_key} {identity_check} {identity_label} {verfiy_label}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute test opssl nonblockingsession server tls1.2 start. Error:\n{e}")

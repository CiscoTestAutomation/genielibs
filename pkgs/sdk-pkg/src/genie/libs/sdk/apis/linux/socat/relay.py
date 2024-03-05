
import re
import logging
from time import sleep

from unicon.eal.dialogs import Dialog


log = logging.getLogger(__name__)

def socat_relay(device, remote_ip, remote_port, protocol='TCP4'):
    """ Setup UDP/TCP relay using 'socat' command.

    Args:
        device (obj): Device object (optional)
        remote_ip (str): remote IP address
        remote_port (str): remote port
        protocol (str): portocol (default: TCP4)

    Returns:
        proxy_port (int): Proxy port number or False if not able to setup relay
    """
    proxy_port, _ = start_socat_relay(device, remote_ip, remote_port, protocol)
    return proxy_port


def start_socat_relay(device, remote_ip, remote_port, protocol='TCP4'):
    """ Setup UDP/TCP relay using 'socat' command.

    Args:
        device (obj): Device object (optional)
        remote_ip (str): remote IP address
        remote_port (str): remote port
        protocol (str): portocol (default: TCP4)

    Returns:
        proxy_port (int): Proxy port number or False if not able to setup relay
        socat_pid (int): Process ID for the socat process
    """
    try:
        socat_output = device.execute(f'socat {protocol}-LISTEN:0,reuseaddr,fork {protocol}:{remote_ip}:{remote_port} &',
                                      error_pattern=['command not found'])
    except Exception:
        log.error('Could not setup port relay via proxy', exc_info=True)
        return

    for _ in range(3):
        sleep(1)  # wait 1 second before checking the netstat output

        proxy_port = None

        # socat TCP4-LISTEN:0 TCP4:1.1.1.15:64196 &
        # [1] 10113
        m = re.search(r'\[\d+\] (\d+)', socat_output)
        if m:
            socat_pid = m.group(1)
            netstat_output = device.execute(r'netstat -anp | grep {}/socat'.format(socat_pid))

            # netstat -anp | grep 11614
            # (Not all processes could be identified, non-owned process info
            # will not be shown, you would have to be root to see it all.)
            # tcp        0      0 0.0.0.0:43758               0.0.0.0:*                   LISTEN      11614/socat
            m = re.search(r'\S+:(\d+)', netstat_output)
            if m:
                proxy_port = m.group(1)
                break

    if not proxy_port:
        log.error('Could not setup port relay via proxy')
        return

    return proxy_port, socat_pid


def stop_socat_relay(device, socat_pid):
    """  Stop the relay process by killing the PID

    Args:
        socat_pid (int): Process ID for socat process
    """
    dialog = Dialog([
        [r'.*?\[\d+].\s+Exit.*', 'sendline()', None, True, False]
    ])
    device.execute(f'kill {socat_pid}', reply=dialog)

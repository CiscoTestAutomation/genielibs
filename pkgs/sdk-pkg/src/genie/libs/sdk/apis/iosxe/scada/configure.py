"""Common configure functions for Scada """
import logging
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement
log = logging.getLogger(__name__)

def configure_scada_dnp3_serial_channel(device, dnp3_serial_channel_name,
                                         dnp3_serial_source_addr,
                                         dnp3_serial_request_timeout,
                                         dnp3_channel_interface):
    """ Configure DNP3 Serial Channel.

        Args:
            device (`obj`): Router on which async line is to be configured.
            dnp3_serial_channel_name (`str`): Name of the DNP3 serial channel.
            dnp3_serial_source_addr ('int'): Source address of DNP3 channel.
            dnp3_serial_request_timeout('int'): Timeout for the DNP3 channel.
            dnp3_channel_interface ('str'): Interface to bind the DNP3 channel.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure DNP3 serial channel")
    cmd =[f"scada-gw protocol dnp3-serial",
          f"channel {dnp3_serial_channel_name}",
          f"link-addr source {dnp3_serial_source_addr}",
          f"request-timeout {dnp3_serial_request_timeout}",
          f"bind-to-interface {dnp3_channel_interface}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure DNP3 serial chaneel, Error:\n{e}")
    
def unconfigure_scada_dnp3_serial_channel(device, dnp3_serial_channel_name):
    """ Unconfigure DNP3 Serial Channel.

        Args:
            device (`obj`): Router on which async line is to be configured.
            dnp3_serial_channel_name (`str`): Name of the DNP3 serial channel.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure DNP3 serial channel")
    cmd =[f"scada-gw protocol dnp3-serial",
          f"no channel {dnp3_serial_channel_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure DNP3 serial channel, Error:\n{e}")
    
def configure_scada_dnp3_serial_session(device, 
                                        dnp3_serial_session_name, 
                                        dnp3_serial_channel_name, 
                                        dnp3_serial_session_addr):
    """ Configure DNP3 Serial session.

        Args:
            device (`obj`): Router on which async line is to be configured.
            dnp3_serial_session_name (`str`): Name of the DNP3 serial session.
            dnp3_serial_channel_name ('str'): Name of the DNP3 serial channel.
            dnp3_serial_session_addr('int'): Session address of session.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure DNP3 serial session")
    cmd =[f"scada-gw protocol dnp3-serial",
          f"session {dnp3_serial_session_name}",
          f"attach-to-channel {dnp3_serial_channel_name}",
          f"link-addr dest {dnp3_serial_session_addr}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure DNP3 serial session, Error:\n{e}")
    
def unconfigure_scada_dnp3_serial_session(device, dnp3_serial_session_name):
    """ Configure DNP3 Serial session.

        Args:
            device (`obj`): Router on which async line is to be configured.
            dnp3_serial_session_name (`str`): Name of the DNP3 serial session.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure DNP3 serial session")
    cmd =[f"scada-gw protocol dnp3-serial",
          f"no session {dnp3_serial_session_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure DNP3 serial session, Error:\n{e}")

def configure_scada_dnp3_ip_channel(device, 
                                    dnp3_ip_channel_name,
                                    dnp3_ip_dest_address, 
                                    dnp3_ip_port,
                                    dnp3_ip_remote_address):
    """ Configure DNP3 IP Channel.

        Args:
            device (`obj`): Router on which async line is to be configured.
            dnp3_ip_channel_name (`str`): Name of DNP3 IP channel.
            dnp3_ip_dest_address ('int'): Destination address of DNP3 channel.
            dnp3_ip_port('int'): Port for the DNP3 IP channel.
            dnp3_ip_remote_address ('str'): Remote address of DNP3 IP channel.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure DNP3 IP channel")
    cmd =[f"scada-gw protocol dnp3-ip",
          f"channel { dnp3_ip_channel_name }",
          f"link-addr dest { dnp3_ip_dest_address }",
          f"tcp-connection local-port { dnp3_ip_port }\
            remote-ip { dnp3_ip_remote_address }"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure DNP3 IP chaneel, Error:\n{e}")
    
def unconfigure_scada_dnp3_ip_channel(device, dnp3_ip_channel_name):
    """ unonfigure DNP3 IP Channel.

        Args:
            device (`obj`): Router on which async line is to be configured.
            dnp3_ip_channel_name (`str`): Name of DNP3 IP channel.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("unonfigure DNP3 IP channel")
    cmd =[f"scada-gw protocol dnp3-ip",
          f"no channel { dnp3_ip_channel_name }"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure DNP3 IP chaneel, Error:\n{e}")

def configure_scada_dnp3_ip_session(device, 
                                    dnp3_ip_session_name, 
                                    dnp3_ip_channel_name, 
                                    dnp3_ip_source_session_addr,
                                    dnp3_serial_session_name):
    """ Configure DNP3 IP session.

        Args:
            device (`obj`): Router on which async line is to be configured.
            dnp3_ip_session_name (`str`): Name of DNP3 IP session.
            dnp3_ip_channel_name ('str'): Name of DNP3 IP channel.
            dnp3_ip_source_session_addr('int'): Source address of DNP3 session.
            dnp3_serial_session_name ('str'): Serial session to map DNP3 IP.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure DNP3 IP channel")
    cmd =[f"scada-gw protocol dnp3-ip",
          f"session {dnp3_ip_session_name}",
          f"attach-to-channel {dnp3_ip_channel_name}",
          f"link-addr source {dnp3_ip_source_session_addr}",
          f"map-to-session {dnp3_serial_session_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure DNP3 IP session, Error:\n{e}")
    
def unconfigure_scada_dnp3_ip_session(device, dnp3_ip_session_name):
    """ unconfigure DNP3 IP session.

        Args:
            device (`obj`): Router on which async line is to be configured.
            dnp3_ip_session_name (`str`): Name of DNP3 IP session.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure DNP3 IP channel")
    cmd =[f"scada-gw protocol dnp3-ip",f"no session {dnp3_ip_session_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure DNP3 IP session, Error:\n{e}")

def configure_scada_enable(device):
    """ Enable Scada Gateway.

        Args:
            device (`obj`): Router on which async line is to be configured.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure Scada Gateway")
    cmd =[f"scada-gw enable"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to enable scada Gateway, Error:\n{e}")

def unconfigure_scada_enable(device):
    """ Disable Scada Gateway.

        Args:
            device (`obj`): Router on which async line is to be configured.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("unconfigure Scada Gateway")
    cmd =[f"no scada-gw enable"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to disable scada Gateway, Error:\n{e}")
    
def configure_scada_t101_serial_channel(device, 
                                        t101_serial_channel_name, 
                                        t101_channel_interface, 
                                        t101_link_mode, 
                                        t101_link_addr_size):
    """ Configure T101 Serial Channel.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t101_serial_channel_name (`str`): Name of T101 serial channel.
            t101_channel_interface ('str'): Source address of serial channel.
            t101_link_mode('str'): Link Mode for the T101 serial channel.
            t101_link_addr_size ('str'): Link Address Size for the T101.                
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure T101 serial channel")
    cmd =[f"scada-gw protocol t101",
          f"channel {t101_serial_channel_name}",
          f"bind-to-interface {t101_channel_interface}",
          f"link-mode {t101_link_mode}",
          f"link-addr-size {t101_link_addr_size}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure T101 serial chaneel, Error:\n{e}")

def unconfigure_scada_t101_serial_channel(device, t101_serial_channel_name):
    """ unconfigure T101 Serial Channel.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t101_serial_channel_name (`str`): Name of the T101 serial channel.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure T101 serial channel")
    cmd =[f"scada-gw protocol t101",
          f"no channel {t101_serial_channel_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure T101 serial chaneel, Error:\n{e}")
    
def configure_scada_t101_serial_session(device, 
                                        t101_serial_session_name, 
                                        t101_serial_channel_name, 
                                        t101_serial_session_addrsize, 
                                        t101_serial_session_cotsize, 
                                        t101_serial_session_objsize,
                                        t101_serial_session_linkaddr):
    """ Configure T101 Serial Session.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t101_serial_session_name (`str`): Name of the T101 serial session.
            t101_serial_channel_name ('str'): Name of the T101 serial channel.
            t101_serial_session_addrsize ('str'): T101 session address size.
            t101_serial_session_cotsize ('str'): T101 session cot size.
            t101_serial_session_objsize ('str'): T101 session object address size.
            t101_serial_session_linkaddr ('int'): T101 session link address.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure T101 serial session")
    cmd =[f"scada-gw protocol t101",
          f"session {t101_serial_session_name}",
          f"attach-to-channel {t101_serial_channel_name}",
          f"common-addr-size {t101_serial_session_addrsize}",
          f"cot-size {t101_serial_session_cotsize}",
          f"info-obj-addr-size {t101_serial_session_objsize}",
          f"link-addr {t101_serial_session_linkaddr}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure T101 serial session, Error:\n{e}")

def unconfigure_scada_t101_serial_session(device, t101_serial_session_name):
    """ unconfigure T101 Serial Session.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t101_serial_session_name (`str`): Name of the T101 serial session.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("unonfigure T101 serial session")
    cmd =[f"scada-gw protocol t101",
          f"no session {t101_serial_session_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure T101 serial session, Error:\n{e}")

def configure_scada_t101_serial_sector(device, 
                                       t101_serial_sector_name, 
                                       t101_serial_session_name, 
                                       t101_serial_sector_asdu):
    """ Configure T101 Serial Sector.
        Args:
            device (`obj`): Router on which serial async line is to be configured.
            t101_serial_sector_name (`str`): Name of the T101 serial sector.
            t101_serial_session_name ('str'): Name of the T101 serial session.
            t101_serial_sector_asdu ('int'): T101 serial sector asdu address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure T101 serial sector")
    cmd =[f"scada-gw protocol t101",
          f"sector {t101_serial_sector_name}",
          f"attach-to-session {t101_serial_session_name}",
          f"asdu-addr {t101_serial_sector_asdu}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure T101 serial sector, Error:\n{e}")

def unconfigure_scada_t101_serial_sector(device, t101_serial_sector_name):
    """ unconfigure T101 Serial Sector.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t101_serial_sector_name (`str`): Name of the T101 serial sector.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure T101 serial sector")
    cmd =[f"scada-gw protocol t101",
          f"no sector {t101_serial_sector_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure T101 serial sector, Error:\n{e}")

def configure_scada_t104_ip_channel(device,
                                    t104_ip_channel_name,
                                    t104_ip_channel_kvalue,
                                    t104_ip_channel_wvalue,
                                    t104_ip_channel_t0timeout,
                                    t104_ip_channel_t1timeout,
                                    t104_ip_channel_t2timeout,
                                    t104_ip_channel_t3timeout,
                                    t104_ip_connection,
                                    t104_local_port,
                                    t104_remote_ip):
    """ Configure T104 IP Channel.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t104_ip_channel_name (`str`): Name of the T104 IP channel.
            t104_ip_channel_kvalue ('int'): K value for the T104 IP channel.
            t104_ip_channel_wvalue ('int'): W value for the T104 IP channel.
            t104_ip_channel_t0timeout ('int'): T0 timeout for T104 IP channel.
            t104_ip_channel_t1timeout ('int'): T1 timeout for T104 IP channel.
            t104_ip_channel_t2timeout ('int'): T2 timeout for T104 IP channel.
            t104_ip_channel_t3timeout ('int'): T3 timeout for T104 IP channel.
            t104_ip_connection ('int'): Connection type for T104 IP channel.
            t104_local_port ('int'): Local port for the T104 IP channel.
            t104_remote_ip ('str'): Remote IP for the T104 IP channel.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure T104 IP channel")
    cmd =[f"scada-gw protocol t104",
          f"channel {t104_ip_channel_name}",
          f"k-value {t104_ip_channel_kvalue}",
          f"w-value {t104_ip_channel_wvalue}",
          f"t0-timeout {t104_ip_channel_t0timeout}",
          f"t1-timeout {t104_ip_channel_t1timeout}",
          f"t2-timeout {t104_ip_channel_t2timeout}",
          f"t3-timeout {t104_ip_channel_t3timeout}",
          f"tcp-connection {t104_ip_connection}\
          local-port {t104_local_port}\
          remote-ip {t104_remote_ip}"]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure T104 IP chaneel, Error:\n{e}")

def unconfigure_scada_t104_ip_channel(device,t104_ip_channel_name):
    """ unconfigure T104 IP Channel.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t104_ip_channel_name (`str`): Name of the T104 IP channel.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("unconfigure T104 IP channel")
    cmd =[f"scada-gw protocol t104",
          f"no channel {t104_ip_channel_name}"]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure T104 IP channel, Error:\n{e}")
    
def configure_scada_t104_ip_session(device,
                                    t104_ip_session_name,
                                    t104_ip_channel_name):
    """ Configure T104 IP session.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t104_ip_session_name (`str`): Name of the T104 IP session.
            t104_ip_channel_name ('str'): Name of the T104 IP channel.

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure T104 IP session")
    cmd =[f"scada-gw protocol t104",
          f"session {t104_ip_session_name}",
          f"attach-to-channel {t104_ip_channel_name}"]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure T104 IP session, Error:\n{e}")
    
def unconfigure_scada_t104_ip_session(device,t104_ip_session_name):
    """ unconfigure T104 IP session.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t104_ip_session_name (`str`): Name of the T104 IP session.

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("unconfigure T104 IP session")
    cmd =[f"scada-gw protocol t104",
          f"no session {t104_ip_session_name}"]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure T104 IP session, Error:\n{e}")

def configure_scada_t104_ip_sector(device,
                                   t104_ip_sector_name,
                                   t104_ip_session_name,
                                   t104_ip_sector_asdu,
                                   t101_serial_sector_name):
    """ Configure T104 IP sector.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t104_ip_sector_name (`str`): Name of the T104 IP sector.
            t104_ip_session_name ('str'): Name of the T104 IP session.
            t104_ip_sector_asdu ('int'): ASDU address for the T104 IP sector.
            t101_serial_sector_name ('str'): T101 serial sector to be maped.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure T104 IP sector")
    cmd =[f"scada-gw protocol t104",
          f"sector {t104_ip_sector_name}",
          f"attach-to-session {t104_ip_session_name}",
          f"asdu-addr {t104_ip_sector_asdu}",
          f"map-to-sector {t101_serial_sector_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure T104 IP sector, Error:\n{e}")
    
def unconfigure_scada_t104_ip_sector(device,t104_ip_sector_name):
    """ unconfigure T104 IP sector.
        Args:
            device (`obj`): Router on which async line is to be configured.
            t104_ip_sector_name (`str`): Name of the T104 IP sector.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("unconfigure T104 IP sector")
    cmd =[f"scada-gw protocol t104",
          f"no sector {t104_ip_sector_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure T104 IP sector, Error:\n{e}")

"""Common configure functions for flow exporter"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def config_flow_exporter(device, exporter_name, monitor_name, dest_ip, udp_port):
    """ Config Flow Exporter on Device

        Args:
            device (`obj`): Device object
            exporter_name (`str`): Flow exporter name
            monitor_name (`str`): Flow monitor name
            dest_ip (`str`): Destination IP
            udp_port (`str`): UDP port
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure([
                          "et-analytics",
                          "ip flow-export destination {dest_ip} {udp_port}".format(dest_ip=dest_ip,udp_port=udp_port),
                          "flow exporter {exporter_name}".format(exporter_name=exporter_name),
                          "destination {dest_ip}".format(dest_ip=dest_ip),
                          "transport udp {udp_port}".format(udp_port=udp_port),
                          "flow exporter {monitor_name}".format(monitor_name=monitor_name),
                          "flow monitor {exporter_name}".format(exporter_name=exporter_name),
                          "exporter {exporter_name}".format(exporter_name=exporter_name),
                          "record netflow ipv4 app-client-server-stats",
                          "flow monitor {monitor_name}".format(monitor_name=monitor_name),
                          "exporter {monitor_name}".format(monitor_name=monitor_name),
                          "record {monitor_name}".format(monitor_name=monitor_name)
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure flow exporter {exporter_name}'.format(exporter_name=exporter_name)
        )

def unconfig_flow_exporter(device, exporter_name, monitor_name):
    """ Unconfigures Flow Exporter on Device

        Args:
            device (`obj`): Device object
            exporter_name (`str`): Flow exporter name
            monitor_name (`str`): Flow monitor name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure(["no flow monitor {monitor_name}".format(monitor_name=monitor_name),
                          "no flow monitor {exporter_name}".format(exporter_name=exporter_name),
                          "no flow exporter {exporter_name}".format(exporter_name=exporter_name),
                          "no et-analytics"])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure flow exporter {exporter_name} and flow monitor {monitor_name}'.format(exporter_name=exporter_name,monitor_name=monitor_name)
        )


def config_flow_monitor_on_interface(device, interface, exporter_name):
    """ Config Flow Monitor on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
            exporter_name (`str`): Flow exporter name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure([
                          "interface {interface}".format(interface=interface),
                          "et-analytics enable",
                          "ip flow monitor {exporter_name} input".format(exporter_name=exporter_name),
                          "ip flow monitor {exporter_name} output".format(exporter_name=exporter_name)])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure flow monitor {exporter_name} on interface {interface}'.format(exporter_name=exporter_name,
                 interface=interface)
        )


def clear_flow_monitor_statistics(device, monitor_name, switch=''):
    """ Clears Flow Monitor statistics on device
        Args:
            device ('obj'): Device object
            monitor_name ('str'): Specific monitor name
            switch ('str', optional): Switch (Compatible to 9300)
        Return:
            None
        Raise:
            SubCommandFailure: Failed clearing flow monitor
    """

    try:
        device.execute([f"clear flow monitor {monitor_name} cache",
                        f"clear flow monitor {monitor_name} statistics",
                        f"show platform software fed {switch} active fnf clear-et-analytics-stats"])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not clear flow monitor statistics'
        )

def configure_fnf_exporter(device, exporter_name, dest_ip, udp_port, source_int=None,
                           timeout=None):

    """ Config Flow Exporter on Device
        Args:
            device (`obj`): Device object
            exporter_name (`str`): Flow exporter name
            dest_ip (`str`): Destination IP
            source_int('str', Optional): Interface
            udp_port (`str`): UDP port
            timeout ('int', Optional): Timeout

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring fnf exporter
    """
    if source_int and timeout is not None:
        try:
            device.configure([
                          f"flow exporter {exporter_name}",
                          f"destination {dest_ip}",
                          f"source {source_int}",
                          f"transport udp {udp_port}",
                          f"template data timeout {timeout}",
                          f"option vrf-table timeout {timeout}",
                          f"option sampler-table timeout {timeout}"
                          ])

        except SubCommandFailure:
            raise SubCommandFailure(
                'Could not configure fnf exporter {exporter_name}'.
                format(exporter_name=exporter_name)
            )
    else:
        try:
            device.configure([
                          f"flow exporter {exporter_name}",
                          f"destination {dest_ip}",
                          f"transport udp {udp_port}"
                          ])
        except SubCommandFailure:
            raise SubCommandFailure(
                'Could not configure fnf exporter {exporter_name}'.
                format(exporter_name=exporter_name)
            )


def unconfigure_flow_exporter_monitor_record(device, exporter_name, monitor_name,
                                          record_name):

    """ Unconfigures Flow Exporter,Monitor and Record on Device
        Args:
            device (`obj`): Device object
            exporter_name (`str`): Flow exporter name
            monitor_name (`str`): Flow monitor name
            record_name (`str`): Flow record name

        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring Flow Exporter,monitor,record
    """

    try:
        device.configure(["no flow monitor {monitor_name}".
                           format(monitor_name=monitor_name),
                          "no flow exporter {exporter_name}".
                           format(exporter_name=exporter_name),
                          "no flow record {record_name}".
                           format(record_name=record_name)
                        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure flow exporter {exporter_name} and flow'
            'monitor {monitor_name} and flow record {record_name}'.
            format(exporter_name=exporter_name, monitor_name=monitor_name,
                   record_name=record_name)
        )

def configure_fnf_monitor_on_interface(device, interface, monitor_name, direction):

    """ Config Fnf Monitor on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
            monitor_name (`str`): Flow monitor name
            direction ('str'): Direction of monitor (input/output)

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring interface with flow monitor
    """

    try:
        device.configure([
                          "interface {interface}".format(interface=interface),
                          "ip flow monitor {monitor_name} {direction}".
                          format(monitor_name=monitor_name, direction=direction)])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure fnf monitor {monitor_name} on'
            'interface {interface}'.format(monitor_name=monitor_name,
                                          interface=interface)
        )


def unconfigure_fnf_monitor_on_interface(device, interface, monitor_name, sampler_name=None, direction='input'):
    """ Unconfig Flow Monitor on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be unconfigured
            monitor_name (`str`): Flow monitor name
            sampler_name ('str', Optional): Sampler name
            direction ('str'): Direction to be unconfigured

        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring interface with flow monitor
    """
    if sampler_name:
        cmd = [f"interface {interface}",
           f"no ip flow monitor {monitor_name} sampler {sampler_name} {direction}"]
    else:
        cmd = [f"interface {interface}",
           f"no ip flow monitor {monitor_name} {direction}" ]
    try:
        device.configure(cmd)

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure flow monitor {monitor_name} on'
            'interface {interface}'.format(monitor_name=monitor_name,
                                          interface=interface)
        )

def clear_flow_monitor(device, name, option=''):
    """ clear flow monitor data
        Args:
            device (`obj`):           Device object
            name ('str'):             Name of the flow (eg: created[ipv4_input] or user defined[monitor_ipv4_out])
            option ('str', optional): Which data to clear. Default will clear all flow monitor info or
                                      can give perticular option to clear eg:cache/statistics
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Clear flow monitor data on {device}".format(device=device))

    try:
        device.execute('clear flow monitor {name} {option}'.format(name=name,option=option))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear flow monitor data on {device}. Error:\n{error}".format(device=device, error=e)
        )


def configure_sampler(device, sampler_name, mode, num_packet, select_packet):

    """ Config Sampler
        Args:
            device (`obj`): Device object
            sampler_name (`str`): Name of sampler
            mode (`str`): Mode to be configured
            num_packet ('int'): number of packets to select per window
            select_packet ('int'): Select M packets out of an N packet window

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring Sampler
    """

    try:
        device.configure([
                          f"sampler {sampler_name}",
                          f"mode {mode} {num_packet} out-of {select_packet}"
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            f'Could not configure sampler {sampler_name}'
            )


def unconfigure_sampler(device, sampler_name):

    """ Unconfig Sampler
        Args:
            device (`obj`): Device object
            sampler_name (`str`): Name of sampler

        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring Sampler
    """

    try:
        device.configure([
                          f"no sampler {sampler_name}",
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            f'Could not unconfigure sampler {sampler_name}'
            )


def configure_fnf_monitor_sampler_interface(device, interface, monitor_name, sampler_name, direction):

    """ Config Fnf Monitor on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
            monitor_name (`str`): Flow monitor name
            sampler_name ('str'): Sampler name
            direction ('str'): Direction of monitor (input/output)

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring interface flow monitor with sampler
    """

    try:
        device.configure([
                          f"interface {interface}",
                          f"ip flow monitor {monitor_name} sampler {sampler_name} {direction}"
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            f'Could not configure fnf monitor {monitor_name} with sampler {sampler_name} on'
            'interface {interface}'
        )


def configure_fnf_monitor_datalink_interface(device, interface, monitor_name, sampler_name, direction):

    """ Config Datalink Fnf Monitor on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
            monitor_name (`str`): Flow monitor name
            sampler_name ('str'): Sampler name
            direction ('str'): Direction of monitor (input/output)

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring interface datalink flow monitor with sampler
    """

    try:
        device.configure([
                          f"interface {interface}",
                          f"datalink flow monitor {monitor_name} sampler {sampler_name} {direction}"
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            f'Could not configure datalink fnf monitor {monitor_name} with sampler {sampler_name} on'
            'interface {interface}'
        )


def unconfigure_fnf_monitor_datalink_interface(device, interface, monitor_name, sampler_name=None, direction=None):

    """ Unconfig Datalink Fnf Monitor on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
            monitor_name (`str`): Flow monitor name
            sampler_name ('str'): Sampler name
            direction ('str'): Direction of monitor (input/output)

        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring interface datalink flow monitor with sampler
    """
    if sampler_name and direction:
        cmd = [f"interface {interface}",
               f"no datalink flow monitor {monitor_name} sampler {sampler_name} {direction}"]
    else:
        cmd = [f"interface {interface}",
               f"no datalink flow monitor {monitor_name}"]
    try:
        device.configure(cmd)

    except SubCommandFailure:
        raise SubCommandFailure(
            f'Could not unconfigure datalink fnf monitor {monitor_name} on'
            'interface {interface}'
        )


def configure_flow_monitor_cache_entry(device, monitor_name, record_name,
                        timeout, cache_entries=None, exporter_name=None):
    """ Config Flow Monitor with cache entry on Device
        Args:
            device (`obj`): Device object
            monitor_name (`str`): Flow Monitor name
            record_name (`str`): Flow record name
            timeout ('int'): Timeout
            cache_entries ('int', optional): Number of cache entries
            exporter_name ('str', optional): Flow exporter name
        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring flow monitor with cache entry
    """
    cmd = [
        f"flow monitor {monitor_name}",
        f"cache timeout inactive {timeout}",
        f"cache timeout active {timeout}",
        f"record {record_name}",
    ]
    if cache_entries:
        cmd.append(f"cache entries {cache_entries}")
    if exporter_name:
        cmd.append(f"exporter {exporter_name}")

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure flow monitor {monitor_name} with cache entry. Error:\n{e}')


def unconfigure_flow_monitor(device, monitor_name):
    """ Unconfig Flow Monitor on Device
        Args:
            device (`obj`): Device object
            monitor_name (`str`): Flow Monitor name

        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring flow monitor
    """

    try:
            device.configure([
                          f"no flow monitor {monitor_name}",
                            ])

    except SubCommandFailure:
            raise SubCommandFailure(
               f'Could not unconfigure flow monitor {monitor_name}'
            )


def configure_fnf_record(
    device,
    record_name,
    match_ipv4_field_1,
    match_flow_field=None,
    match_int_field=None,
    match_ipv4_field_2=None,
    match_transport_field_1='destination-port',
    match_transport_field_2='source-port',
    collect_counter_bytes=True,
    collect_counter_packets=True,
    collect_int_field=None,
    datalink=False,
    collect_routing=True,
    datalink_type_1=None,
    datalink_type_2=None,
    datalink_subtype_1=None,
    datalink_subtype_2=None,
    address_type=None,
    collect_timestamp=False
    ):

    """ Config Flow Record on Device
        Args:
            device (`obj`): Device object
            record_name (`str`): Flow record name
            match_ipv4_field_1 ('str'): First IPv4 field to be configured
            match_flow_field ('str'): Flow field to be configured
            match_int_field ('str'): Interface field to be configured
            match_ipv4_field_2 ('str'): Second IPv4 field to be configured
            match_transport_field_1 ('str'): First transport field to be configured
            match_transport_field_2 ('str'): Second transport field to be configured
            collect_counter_bytes ('bool'): Enable counter field bytes
            collect_counter_packets ('bool'): Enable counter field packets
            collect_int_field ('str'): Collect interface field to be configured
            datalink ('bool') : Configure datalink fields
            collect_routing ('bool'): Configure routing attributes
            datalink_type_1 ('str'): First Datalink Type to be configured
            datalink_type_2 ('str'): Second datalink Type to be configure
            datalink_subtype_1 ('str'): First datalink subtype to be configured
            datalink_subtype_2 ('str'): Second datalink subtype to be configured
            address_type ('str'): Address type to be configured
            collect_timestamp ('bool'): Configure timestamp fields

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring Flow Record on Device
    """

    configs = [f'flow record {record_name}']
    if datalink :
        configs.extend([f'match datalink {datalink_type_1} {datalink_subtype_1} address {address_type}',
                        f'match datalink {datalink_type_1} {datalink_subtype_2} address {address_type}',
                        f'match datalink {datalink_type_2}'])

    if match_flow_field is not None:
                    configs.extend([f'match flow {match_flow_field}'])
    if match_int_field is not None:
                    configs.extend([f'match interface {match_int_field}'])
    if match_ipv4_field_2 is not None:
                    configs.extend([f'match ipv4 {match_ipv4_field_2}'])
    if collect_int_field is not None:
                    configs.extend([f'collect interface {collect_int_field}'])
    if collect_routing :
                    configs.extend(['collect routing source as peer 4-octet',
                                  'collect routing destination as peer 4-octet'])
    if collect_counter_bytes:
                    configs.extend(['collect counter bytes long'])
    if collect_counter_packets:
                    configs.extend(['collect counter packets long'])
    if collect_timestamp :
                    configs.extend(['collect timestamp sys-uptime first',
                                   'collect timestamp sys-uptime last'])

    try:
        device.configure(configs)
        device.configure([f'flow record {record_name}',
                'match ipv4 destination address',
                f'match ipv4 {match_ipv4_field_1}',
                'match ipv4 source address',
                'match routing vrf input',
                f'match transport {match_transport_field_1}',
                f'match transport {match_transport_field_2}',
                'collect transport tcp flags',
                ])

    except SubCommandFailure:
        raise SubCommandFailure('Could not configure flow record {record_name}'.format(record_name=record_name))


def unconfigure_flow_record(device, record_name):
    """ Unconfig Flow Monitor on Device
        Args:
            device (`obj`): Device object
            record_name (`str`): Flow Record name

        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring flow record
    """

    try:
        device.configure([
                      f"no flow record {record_name}",
                        ])

    except SubCommandFailure:
        raise SubCommandFailure(
           f'Could not unconfigure flow record {record_name}')


def configure_active_timer_under_et_analytics(device, timer):

    """ Configure active timer under  et-analytics

        Args:
            device ('obj'): device to use
            timer ('int'): timer value in seconds

        Return:
            None

        Raise:
            SubCommandFailure
    """
    log.debug("Configuring active timer under et-analytics")


    cmd = ["et-analytics",  f"active-timeout {timer}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure active timer. Error:\n{error}".format(error=e)
        )

def unconfigure_active_timer_under_et_analytics(device, timer):

    """ unconfiguring active timer under  et-analytics

        Args:
            device ('obj'): device to use
            timer ('int'): timer value in seconds

        Return:
            None

        Raise:
            SubCommandFailure
    """
    log.debug("Unconfiguring active timer under et-analytics")

    cmd = ["et-analytics",  f"no active-timeout {timer}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure active timer. Error:\n{error}".format(error=e)
        )


def clear_flow_exporter_statistics(device, exporter_name='eta-exp'):
    """ Clear Flow exporter statistics on device

        Args:
            device ('obj'): device to use
            exporter_name ('str', optional): exporter name, default value is 'eta-exp'

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring interface
    """
    cmd = f"clear flow exporter {exporter_name} statistics"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not clear flow exporter statistics. Error:\n{e}')


def configure_et_analytics(device, dest_ip, udp_port):
    """ Configure et-analytics

        Args:
            device ('obj'): Device object
            dest_ip ('str'): Destination IP
            udp_port ('str'): UDP port

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring et-analytics
    """
    cmd = ["et-analytics",  f"ip flow-export destination {dest_ip} {udp_port}"]
    try:
        device.configure(cmd)
    except SubCommandFailure:
        raise SubCommandFailure('Could not configure et_analytics')


def disable_et_analytics(device, interface):
    """ disable et-analytics
        Args:
            device ('obj'): Device object
            interface ('str'): interface name to disable et-analytics

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.debug("disabling et-analytics under {interface}".format(interface=interface))
    cmd = [f"interface {interface}",  "no et-analytics enable"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to disable et-analytics under {interface}. Error:\n{error}".format(interface=interface, error=e)
        )


def enable_et_analytics(device, interface):
    """ Enable et-analytics
        Args:
            device ('obj'): Device object
            interface ('str'): interface name to enable et-analytics

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.debug("enabling et-analytics under {interface}".format(interface=interface))
    cmd = [f"interface {interface}", "et-analytics enable"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to enable et-analytics under {interface}. Error:\n{error}".format(interface=interface, error=e)
        )


def clear_flow_monitor_statistics_for_et_analytics(device):
    """ Clears Flow Monitor statistics on device

        Args:
            device ('obj'): Device object

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.execute(["clear flow monitor eta-mon cache",
                        "clear flow monitor eta-mon statistics",
                        "show platform software fed active fnf clear-et-analytics-stats"])
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear flow monitor statistics for et-analytics. Error:\n{e}")

def configure_monitor_capture(
    device, 
    capture_name,
    match_type,
    direction,
    interface,
    file_location=None,
    file_size=None,
    buffer_size=None,
    duration=None,
    packets=None,
    packet_len=None,
    capture_frequency=None,
    pps=None
    ):
    """ Configure Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Name of the Capture
            match_type(`str`): Match type of monitor (any/ipv4/ipv6/mac)
            direction ('str'): Direction of monitor (input/output/both)
            interface('str'): Interface
            file_location ('str'): Location of the pcap file
            file_size ('int'): Total size of file(s) in MB <1-100>
            buffer_size ('int'): Buffer size in MB  : Min 1 : Max 100
            duration ('int'): Limit total duration of capture in Seconds : Min 1 - Max 1000000
            packets ('int'): Number of Packet  : Min 1 - Max 100000 
            packet_len ('int'): packet length(in bytes) : Min 64 : Max 9500
            capture_frequency('int'): Fraction of Packets to capture (every Nth)  : Min 2 - Max 100000
            pps ('int'): Maximum number of packets per second <1-1000000>
        Return:
            None
        Raise:
            SubCommandFailure: Failed to Configure Monitor Capture
    """
    cmd = f"monitor capture {capture_name} match {match_type} interface {interface} {direction}"
    if file_location:
        cmd += f" file location {file_location}"
    if file_size:
        cmd += f" size {file_size}"
    if buffer_size:
        cmd += f" buffer-size {buffer_size}"
    if duration:
        cmd += f" limit duration {duration}"
    if packets:
        cmd += f" packets {packets}"
    if packet_len:
        cmd += f" packet-len {packet_len}"
    if capture_frequency:
        cmd += f" every {capture_frequency}"
    if pps:
        cmd += f" pps {pps}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'monitor capture {capture_name} match start. Error:\n{e}')

def start_monitor_capture(device, capture_name):
    """ Start Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Monitor capture name

        Return:
            None
        Raise:
            SubCommandFailure: Failed to Start Monitor Capture
    """
    cmd = "monitor capture {capture_name} start".format(capture_name=capture_name)
    try:
        device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f'monitor capture {capture_name} match start. Error:\n{e}')

def delete_monitor_capture(device, capture_name):
    """ delete Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Monitor capture name

        Return:
            None
        Raise:
            SubCommandFailure: Failed to delete Monitor Capture
    """
    cmd = "no monitor capture {capture_name}".format(capture_name=capture_name)
    try:
        device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f'no monitor capture {capture_name}. Error:\n{e}')

def stop_monitor_capture(device, capture_name):
    """ Stop Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Monitor capture name

        Return:
            None
        Raise:
            SubCommandFailure: Failed to Stop Monitor Capture
    """
    cmd = "monitor capture {capture_name} stop".format(capture_name=capture_name)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'monitor capture {capture_name} match stop. Error:\n{e}')

def configure_monitor_capture_without_match(device, capture_name, direction, interface):
    """ Configure Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Monitor capture name
            direction ('str'): Direction of monitor (input/output/both)
            interface('str'): Interface
        Return:
            None
        Raise:
            SubCommandFailure: Failed to Configure Monitor Capture
    """
    cmd = "monitor capture {capture_name} interface {interface} {direction}".format(
            capture_name=capture_name, interface=interface, direction=direction)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure monitor capture {capture_name} on interface {interface} Error:\n{error}".format(
                capture_name=capture_name, interface=interface, error=e,
            )
        )

def configure_monitor_capture_buffer_size(device, capture_name, size):
    """ Configure Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Monitor capture name
            size ('str'): butffer size number
        Return:
            None
        Raise:
            SubCommandFailure: Failed to Configure Monitor Capture Buffer Size
    """
    cmd = "monitor capture {capture_name} buffer size {size}".format(
            capture_name=capture_name, size=size)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure monitor capture {capture_name} buffer size {size} Error:\n{error}".format(
                capture_name=capture_name, size=size, error=e,
            )
        )

def configure_monitor_capture_limit_packet_len(device, capture_name, length, pps):
    """ Configure Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Monitor capture name
            length ('str'): Limit packet-len
            pps ('str'): pps value
        Return:
            None
        Raise:
            SubCommandFailure: Failed to Configure Monitor Capture Buffer Size
    """
    cmd = "monitor capture {capture_name} limit packet-len {length} pps {pps}".format(
            capture_name=capture_name, length=length, pps=pps)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure monitor capture {capture_name} limit packet-len {length} Error:\n{error}".format(
                capture_name=capture_name, length=length, error=e,
            )
        )

def unconfigure_monitor_capture_without_match(device, capture_name, direction, interface):
    """ Unconfigure Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Monitor capture name
            direction ('str'): Direction of monitor (input/output/both)
            interface('str'): Interface
        Return:
            None
        Raise:
            SubCommandFailure: Failed To Unconfigure Monitor Capture
    """
    cmd = "no monitor capture {capture_name} interface {interface} {direction}".format(
            capture_name=capture_name, interface=interface, direction=direction)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure monitor capture {capture_name} on interface {interface} Error:\n{error}".format(
                capture_name=capture_name, interface=interface, error=e,
            )
        )

def unconfigure_monitor_capture_buffer_size(device, capture_name):
    """ Unconfigure Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Monitor capture name
        Return:
            None
        Raise:
            SubCommandFailure: Failed to Unconfigure Monitor Capture Buffer Size
    """
    cmd = "no monitor capture {capture_name} buffer size".format(
            capture_name=capture_name)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure monitor capture {capture_name} buffer size Error:\n{error}".format(
                capture_name=capture_name, error=e,
            )
        )

def unconfigure_monitor_capture_limit_packet_len(device, capture_name):
    """ Unconfigure Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Monitor capture name
        Return:
            None
        Raise:
            SubCommandFailure: Failed to Unconfigure Monitor Capture Buffer Size
    """
    cmd = "no monitor capture {capture_name} limit packet-len".format(
            capture_name=capture_name)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure monitor capture {capture_name} limit packet-len Error:\n{error}".format(
                capture_name=capture_name, error=e,
            )
        )

def configure_monitor_capture_match(
    device,
    capture_name,
    type,
    host=None,
    src_ip=None,
    dst_ip=None):
    """ Configure Monitor Capture on Device
        Args:
            device (`obj`): Device object
            capture_name (`str`): Monitor capture name
            type ('str'): Address type (ipv4/ipv6)
            src_ip ('str', optional): source start ip, default value is None
            dst_ip ('str', optional): destination start ip, default value is None
            host ('str', optional): A single source/destination host, default value is None
        Return:
            None
        Raise:
            SubCommandFailure: Failed to Configure Monitor Capture
    """
    if host is None:
        cmd = "monitor capture {capture_name} match {type} any any".format(
            capture_name=capture_name,
            type=type)
    elif host is not None and src_ip is not None and dst_ip is None:
        cmd = "monitor capture {capture_name} match {type} host {src_ip} any".format(
            capture_name=capture_name,
            type=type,
            src_ip=src_ip)
    elif host is not None and src_ip is None and dst_ip is not None:
        cmd = "monitor capture {capture_name} match {type} any host {dst_ip}".format(
            capture_name=capture_name,
            type=type,
            dst_ip=dst_ip)
    elif host and src_ip and dst_ip is not None:
        cmd = "monitor capture {capture_name} match {type} host {src_ip} host {dst_ip}".format(
            capture_name=capture_name,
            type=type,
            src_ip=src_ip,
            dst_ip=dst_ip)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure monitor capture {capture_name} Error:\n{error}".format(
                capture_name=capture_name, error=e,
            )
        )


def unconfigure_interface_datalink_flow_monitor(device, interface, protocol, flow_monitor, direction):
    """ unconfigure_flow_monitor
        Args:
            device ('obj'): Device object
            interface ('str'): Interface Name
            protocol ('str'): Protocol to unconfigure. Ex: ip, ipv6, datalink
            flow_monitor ('str'): Flow monitor name.
            direction ('str'): Direction to apply Flow Monitor on traffic
        Return:
            None
        Raise:
            SubCommandFailure: Failed to Configure Monitor Capture
    """

    cmd = [f'interface {interface}', f'no {protocol} flow monitor {flow_monitor} {direction}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure flow monitor . Error:\n{error}"
                .format(device=device, error=e))

def configure_flow_monitor_on_vlan_configuration(device, vlan_id, monitor_name, direction, sampler_name='', type='datalink'):
    """ Configure Flow Monitor on vlan configuration
        Args:
            device ('obj'): Device object
            vlan_id ('str'): Vlan id list (eg. 1-10,15)
            type ('str'): Type of flow monitor (eg. datalink,ip,ipv6)
            monitor_name ('str'): Flow monitor name
            sampler_name ('str', Optional): Sampler name
            direction ('str'): Direction of monitor (input/output)
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring interface with flow monitor
    """
    if sampler_name:
        cmd = [f"vlan configuration {vlan_id}",
            f"{type} flow monitor {monitor_name} sampler {sampler_name} {direction}"]
    else:
        cmd = [f"vlan configuration {vlan_id}",
            f"{type} flow monitor {monitor_name} {direction}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure {type} flow monitor {monitor_name} on valn configuration {vlan_id}. Error:\n{e}'
        )

def unconfigure_flow_monitor_on_vlan_configuration(device, vlan_id, monitor_name, direction, sampler_name='', type='datalink'):
    """ Unconfigure Flow Monitor on vlan configuration
        Args:
            device ('obj'): Device object
            vlan_id ('str'): Vlan id list (eg. 1-10,15)
            type ('str'): Type of flow monitor (eg. datalink,ip,ipv6)
            monitor_name ('str'): Flow monitor name
            sampler_name ('str', Optional): Sampler name
            direction ('str'): Direction of monitor (input/output)
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring interface with flow monitor
    """
    if sampler_name:
        cmd = [f"vlan configuration {vlan_id}",
            f"no {type} flow monitor {monitor_name} sampler {sampler_name} {direction}"]
    else:
        cmd = [f"vlan configuration {vlan_id}",
            f"no {type} flow monitor {monitor_name} {direction}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure {type} flow monitor {monitor_name} on valn configuration {vlan_id}. Error:\n{e}'
        )


def configure_flow_record_match_ip(device, record_name, ip_version, field_type, address=False):
    """ Config Flow Record with match parameters on Device
        Args:
            device ('obj'): Device object
            record_name ('str'): Flow record name
            ip_version ('str'): ipv4 or ipv6 version.
            field_type ('str'): Field type. Ex: source, protocol etc.
            address ('bool', optional): address to configure. Default is False.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring Flow Record Match IP on Device
    """

    config = [f'flow record {record_name}', f'match {ip_version} {field_type}{" address" if address else ""}']

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure flow record {record_name} match ip. Error: {e}')


def configure_flow_record_match_collect_interface(device, record_name, direction, match=True, collect=True):
    """ Config Flow Record interface parameters on Device
        Args:
            device ('obj'): Device object
            record_name ('str'): Flow record name
            direction ('str'): ipv4 or ipv6 version.
            match ('bool', optional): configure match interface. Default is True.
            collect ('bool', optional): configure collect interface. Default is True.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring Flow Record interface on Device
    """

    config = [f'flow record {record_name}']
    if match:
        config.append(f'match interface {direction}')
    if collect:
        config.append(f'collect interface {direction}')

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure flow record {record_name} interface. Error: {e}')


def configure_flow_record_match_datalink(device, record_name, field_type, mac_type=None, direction=None):
    """ Config Flow Record with match parameters on Device
        Args:
            device ('obj'): Device object
            record_name ('str'): Flow record name
            field_type ('str'): Field type. Ex: source, protocol etc.
            mac_type ('str', optional): source or destination mac type. Default is None.
            direction ('str', optional): input or output direction. Default is None.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring Flow Record Match datalink on Device
    """

    config = [f'flow record {record_name}']

    if mac_type and direction:
        config.append(f'match datalink {field_type} {mac_type} address {direction}')
    elif direction is None and mac_type is None:
        config.append(f'match datalink {field_type}')
    elif direction is not None and mac_type is None:
        config.append(f'match datalink {field_type} {direction}')
    elif direction:
        config.append(f'match datalink {field_type} {mac_type} {direction}')

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure flow record {record_name} match datalink. Error: {e}')


def configure_flow_record_collect_timestamp(device, record_name, packet_time):
    """ Config Flow Record collect timestamp parameters on Device
        Args:
            device ('obj'): Device object
            record_name ('str'): Flow record name
            packet_time ('str'): First or Last packet.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring Flow Record collect timestamp on Device
    """

    config = [f'flow record {record_name}', f'collect timestamp absolute {packet_time}']

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure flow record {record_name} collect timestamp. Error: {e}')


def configure_flow_record_collect_counter(device, record_name, counter_type, layer2=False):
    """ Config Flow Record collect counter parameters on Device
        Args:
            device ('obj'): Device object
            record_name ('str'): Flow record name
            counter_type ('str'): bytes or packets counter type.
            layer2 ('bool', optional): Configures layer2 if True. Default is False
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring Flow Record collect counter on Device
    """

    config = [f'flow record {record_name}', f'collect counter {counter_type}{" layer2" if layer2 else ""} long']

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure flow record {record_name} collect counter. Error: {e}')

def configure_ipv6_flow_monitor(device, interface, monitor_name,direction):
    """ configure ipv6 flow monitor
        Args:
            device (`obj`): Device object
            interface ('str'): interface name to ipv6
            monitor_name ('str'): monitor name
            direction('str'):input or output
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"interface {interface}".format(interface=interface),
           f"ipv6 flow monitor {monitor_name} {direction}".format(monitor_name=monitor_name,direction=direction)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ipv6 flow monitor. Error:\n{error}".format(
                device=device, interface=interface, error=e
            )
        )

def unconfigure_ipv6_flow_monitor(device, interface, monitor_name,direction):
    """ unconfigure ipv6 flow monitor
        Args:
            device (`obj`): Device object
            interface ('str'): interface name to ipv6
            monitor_name ('str'): monitor name
            direction('str'):input or output
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"interface {interface}".format(interface=interface),
           f"no ipv6 flow monitor {monitor_name} {direction}".format(monitor_name=monitor_name,direction=direction)]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ipv6 flow monitor. Error:\n{error}".format(
                device=device, interface=interface, error=e
            )
        )

def configure_flow_exporter(device, exporter_name, dest_ip=None, udp_port=None, dscp=None,
    ttl=None, data_timeout=None, table_type=None, table_timeout=None, source_int=None, export_proto=None):
    """ Configure Flow Exporter on Device
        Args:
            device ('obj'): Device object
            exporter_name ('str'): Flow exporter name
            dest_ip ('str', optional): Destination IP. Default is None
            udp_port ('str', optional): UDP port. Default is None
            dscp ('str', optional): dscp value. Default is None
            ttl ('str', optional): ttl value. Default is None
            data_timeout ('str', optional): template data timeout value. Default is None
            table_type ('str', optional): option table type. Default is None
            table_timeout ('str', optional): option table timeout value. Default is None
            source_int ('str', optional): Source interface. Default int None
            export_proto ('str', optional): export-protocol. Default is None
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring flow exporter
    """

    config = [f'flow exporter {exporter_name}']
    if dest_ip:
        config.append(f'destination {dest_ip}')
    if udp_port:
        config.append(f'transport udp {udp_port}')
    if dscp:
        config.append(f'dscp {dscp}')
    if ttl:
        config.append(f'ttl {ttl}')
    if data_timeout:
        config.append(f'template data timeout {data_timeout}')
    if table_type:
        config.append(f'option {table_type}{f" timeout {table_timeout}" if table_timeout else ""}')
    if source_int:
        config.append(f'source {source_int}')
    if export_proto:
        config.append(f'export-protocol {export_proto}')

    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure flow exporter {exporter_name}. Error\n{e}')

def configure_monitor_capture_export_location(device, capture_name, filepath):
    """ Configure Monitor capture export location
        Args:
            device ('obj'): device to use
            capture_name ('str'): Capture name
            filepath ('str'): file path ex:flash:/mypcap.pcap
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'monitor capture {capture_name} export location {filepath}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure Monitor capture export location file. Error:\n{e}')

def configure_monitor_capture_export_status(device, capture_name):
    """ Configure Monitor capture export status
        Args:
            device ('obj'): device to use
            capture_name ('str'): Capture name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'monitor capture {capture_name} export status'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure Monitor capture export status. Error:\n{e}')

def configure_fnf_flow_record(
    device,
    record_name,
    datalink = False,
    datalink_type_1 = None,
    datalink_subtype_1 = None,
    address_type = None,
    match_int_field = None,
    match_ipv4_field = None,
    collect_counter_bytes = False,
    collect_counter_packets = False,
    match_transport_field = None,
    address_mode = None,
    tcp_field = False,
    collect_event = False,
    application_name = False,
    connection_type = None,
    connection_address_type = None,
    observation_point = False,
    collect_timestamp = None,
    flow_direction = False,
    initiator = False,
    new_connections = False,
    connection_counter = None,
    collect_type_mask = None,
    collect_length = None,
    collect_ipv4_ttl = None,
    collect_udp_ports = None
    ):

    """ Config Flow Record on Device
        Args:
            device (`obj`): Device object
            record_name (`str`): Flow record name
            datalink ('bool') : Configure datalink fields
            datalink_type_1 ('str', optional): First Datalink Type to be configured
            datalink_subtype_1 ('str', optional): First datalink subtype to be configured
            match_int_field ('str', optional): Interface field to be configured
            match_ipv4_field ('str', optional): First IPv4 field to be configured
            collect_counter_bytes ('bool'): Enable counter field bytes
            collect_counter_packets ('bool'): Enable counter field packets
            match_transport_field ('str', optional): First transport field to be configured
            address_mode('str', optional): Address mode to be configured
            tcp_field('bool'): Configure collect transport tcp flags
            collect_event('bool'): Configure collect policy firewall event
            application_name('bool'): Configure application name
            connection_type('str', optional): connection type to be configured
            connection_address_type('str', optional): connection address type to be configured
            observation_point('bool'): Configure observation point
            collect_timestamp('str', optional): timestamp to be configured
            flow_direction('bool'): Configure flow direction
            initiator('bool'): Configure initiator
            new_connections('bool'): Configure new connections
            connection_counter('str', optional): connection bytes to be configured, default value is None
            collect_type_mask('str', optional): ipv4 source or destination to be configured, default value is None
            collect_length('str', optional): configure ipv4 length total or header, default value is None
            collect_ipv4_ttl('str', optional): ttl value minimum or maximum to be configured, default value is None
            collect_udp_ports('str', optional): udp source-port or destination port to be configured, default value is None
        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring Flow Record on Device
    """

    configs = [f'flow record {record_name}']
    if datalink:
        if datalink_type_1 and datalink_subtype_1 and address_type:
            configs.extend([f'match datalink {datalink_type_1} {datalink_subtype_1} address {address_type}'])
    if match_int_field:
        configs.extend([f'match interface {match_int_field}'])
    if match_ipv4_field:
        configs.extend([f'match ipv4 {match_ipv4_field}'])
    if collect_counter_bytes:
        configs.extend(['collect counter bytes long'])
    if collect_counter_packets:
        configs.extend(['collect counter packets long'])
    if match_transport_field:
        configs.extend([f'match transport {match_transport_field}'])
    if address_mode:
        configs.extend([f'match ipv4 {address_mode} address'])
    if tcp_field:
        configs.extend([f'collect transport tcp flags'])
    if collect_event:
        configs.extend([f'collect policy firewall event'])
    if application_name:
        configs.extend(['match application name'])
    if connection_type and connection_address_type:
        configs.extend([f'match connection {connection_type} {connection_address_type} address'])
    if connection_type:
        configs.extend([f'match connection {connection_type} transport port'])
    if observation_point:
        configs.extend(['match flow observation point'])
    if collect_timestamp:
        configs.extend([f'collect timestamp absolute {collect_timestamp}'])
    if flow_direction:
        configs.extend(['collect flow direction'])
    if initiator:
        configs.extend(['collect connection initiator'])
    if new_connections:
        configs.extend(['collect connection new-connections'])
    if connection_type and connection_counter:
        configs.extend([f'collect connection {connection_type} counter {connection_counter} long'])
    if collect_type_mask:
        configs.extend([f'collect ipv4 {collect_type_mask} mask'])
    if collect_length:
        configs.extend([f'collect ipv4 length {collect_length}'])
    if collect_ipv4_ttl:
        configs.extend([f'collect ipv4 ttl {collect_ipv4_ttl}'])
    if collect_udp_ports:
        configs.extend([f'collect transport udp {collect_udp_ports}'])

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure flow record. Error:\n{e}')

def unconfigure_record_configs_from_flow_monitor(
    device,
    monitor_name,
    record_name=None,
    active_timeout=None,
    inactive_timeout=None,
    cache_entries=None,
    exporter_name=None
    ):
    """ Unconfig Flow Monitor with cache entry on Device
        Args:
            device ('obj'): Device object
            monitor_name ('str'): Flow Monitor name
            record_name ('str', optional): Flow record name, default value is None
            active_timeout ('int', optional): Active timeout, default value is None
            inactive_timeout ('int', optional): Inactive timeout, default value is None
            cache_entries ('int', optional): Number of cache entries, default value is None
            exporter_name ('str', optional): Flow exporter name, default value is None
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring flow monitor with cache entry
    """
    cmd = ["flow monitor {monitor_name}".format(monitor_name=monitor_name)]
    if active_timeout:
        cmd.append("no cache timeout active {active_timeout}".format(active_timeout=active_timeout))
    if inactive_timeout:
        cmd.append("no cache timeout inactive {inactive_timeout}".format(inactive_timeout=inactive_timeout))
    if record_name:
        cmd.append("no record {record_name}".format(record_name=record_name))
    if cache_entries:
        cmd.append("no cache entries {cache_entries}".format(cache_entries=cache_entries))
    if exporter_name:
        cmd.append("no exporter {exporter_name}".format(exporter_name=exporter_name))

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure flow monitor {monitor_name} with cache entries. Error:\n{e}')

def unconfigure_flow_exporter(device, exporter_name, dest_ip=None, udp_port=None, dscp=None,
    ttl=None, data_timeout=None, source_int=None, export_proto=None):
    """ Unconfigure Flow Exporter on Device
        Args:
            device ('obj'): Device object
            exporter_name ('str'): Flow exporter name
            dest_ip ('str', optional): Destination IP. Default is None
            udp_port ('str', optional): UDP port. Default is None
            dscp ('str', optional): dscp value. Default is None
            ttl ('str', optional): ttl value. Default is None
            data_timeout ('str', optional): template data timeout value. Default is None
            source_int ('str', optional): Source interface. Default int None
            export_proto ('str', optional): export-protocol. Default is None
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring flow exporter
    """

    config = ['flow exporter {exporter_name}'.format(exporter_name=exporter_name)]
    if dest_ip:
        config.append('no destination {dest_ip}'.format(dest_ip=dest_ip))
    if udp_port:
        config.append('no transport udp {udp_port}'.format(udp_port=udp_port))
    if dscp:
        config.append('no dscp {dscp}'.format(dscp=dscp))
    if ttl:
        config.append('no ttl {ttl}'.format(ttl=ttl))
    if data_timeout:
        config.append('no template data timeout {data_timeout}'.format(data_timeout=data_timeout))
    if source_int:
        config.append('no source {source_int}'.format(source_int=source_int))
    if export_proto:
        config.append('no export-protocol {export_proto}'.format(export_proto=export_proto))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Unconfigure flow exporter {exporter_name}. Error\n{e}')


def configure_flow_monitor(device, monitor_name, exporter_name, record_name,
                        timeout):
    """ Config Flow Monitor on Device
        Args:
            device (`obj`): Device object
            monitor_name (`str`): Flow Monitor name
            exporter_name (`str`): Flow exporter name
            record_name (`str`): Flow record name
            timeout ('int'): Timeout

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring flow monitor
    """

    try:
        device.configure([
                          f"flow monitor {monitor_name}",
                          f"exporter {exporter_name}",
                          f"cache timeout inactive {timeout}",
                          f"cache timeout active {timeout}",
                          f"record {record_name}"
                          ])
    except SubCommandFailure:
            raise SubCommandFailure(
               f'Could not configure flow monitor {monitor_name}'
            )

def  configure_datalink_flow_monitor(device, interface, flow_name, direction):
    """ Config datalink flow monitor on Device
        Args:
            device ('obj'): Device object
            interface ('str'): interface
            flow_name ('str'): different flow names.
            direction ('str'): Input or Output direction.
            ex:)
                input    Apply Flow Monitor on input traffic
                output   Apply Flow Monitor on output traffic
                sampler  Optional Sampler to apply to this Flow Monitor
        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring datalink flow monitor
    """

    config = [f'interface {interface}', f'datalink flow monitor {flow_name} {direction}']

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure datalink flow monitor m4out device {device.name}. Error:\n{e}")


def  unconfigure_datalink_flow_monitor(device, interface, flow_name, direction):
    """ Unconfigure datalink flow monitor on Device
        Args:
            device ('obj'): Device object
            interface('str'): interface
            flow_name ('str'): different flow names.
            direction ('str'): Input or Output direction.
            ex:)
                input    Apply Flow Monitor on input traffic
                output   Apply Flow Monitor on output traffic
                sampler  Optional Sampler to apply to this Flow Monitor
        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring datalink flow monitor
    """
    config=[f'interface {interface}', f'no datalink flow monitor {flow_name} {direction}']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure datalink flow monitor device {device.name}. Error:\n{e}")


def configure_fnf_flow_record_match_flow(device, record_name, flow_name, cts_type=None):

    """ Configure Flow Record match flow on Device
        Args:
            device ('obj'): Device object
            record_name ('str'): Flow record name
            flow_name ('str'): cts or direction or observation
            cts_type ('str', optional): source or destination. Default is None

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring Flow Record on Device
    """

    config = [f'flow record {record_name}']
    if flow_name == 'observation':
        config.append(f'match flow observation point')
    elif flow_name == 'cts' and cts_type:
        config.append(f'match flow cts {cts_type} group-tag')
    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(f'Could not configure flow record {record_name}')

def clear_monitor_capture(device, capture_name):
    """
        Execute monitor capture <capture_name> clear
        Example: monitor capture test clear
        Args:
            device ('obj'): Device Object
            capture_name ('str'): Name of Capture
    """
    cmd = f"monitor capture {capture_name} clear"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not execute monitor capture {capture_name} clear. \nError: {e}")

def unconfigure_exporter(device, exporter_name):
    """ Unconfigure Flow Exporter on Device

        Args:
            device (`obj`): Device object
            exporter_name (`str`): Flow exporter name

        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring flow exporter
    """
    log.debug(f"Unconfiguring flow exporter {exporter_name} on device {device.name}")
    cmd = [f"no flow exporter {exporter_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure flow exporter {exporter_name}. Error:\n{e}')


def configure_vlan_and_no_shutdown(device, vlan_id):
    """ Configure VLAN and No Shutdown
        Args:
            device (`obj`): Device object
            vlan_id (`str`): VLAN ID
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring VLAN and no shutdown
    """
    cmd = [
        f"interface vlan {vlan_id}",
        "no shutdown",
        f"vlan {vlan_id}",
        "no shutdown"
    ]
    log.debug(f"Configuring VLAN {vlan_id} with commands: {cmd}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to configure VLAN {vlan_id} and no shutdown. Error: {e}")
        raise SubCommandFailure(f'Could not configure VLAN {vlan_id} and no shutdown. Error:\n{e}'
        )
        
def unconfigure_device_sampler(device, sampler_name):
    """ Unconfigure Sampler on Device
        Args:
            device (`obj`): Device object
            sampler_name (`str`): Sampler name
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring sampler
    """
    log.debug(f"Unconfiguring sampler {sampler_name} on device {device.name}")
    cmd = [f"no sampler {sampler_name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure sampler {sampler_name} on device {device.name}. Error: {e}")
        raise SubCommandFailure(f'Could not unconfigure sampler {sampler_name}. Error:\n{e}')
    


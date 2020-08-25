"""start functions for flamegraph"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)


def start_perf(device, service='', sleep=10):
    """ start perf in shell mode
        # CISCO INTERNAL

        Args:
            device (`obj`): Device object
            service (`str`): service to set for Perf
            sleep (`int`, optional): sleep for shell command. Defaults to 10 seconds
        Returns:
            ret_dict (`dict`): Dictionary
            
        example:
        ret_dict = {
            `service_pid`: '8086',
            `perf_pid`: '15026',
        }
    """
    # get service pid
    try:
        out = device.parse(
            'show system internal sysmgr service name {service}'.format(
                service=service))
    except SchemaEmptyParserError:
        return {}
    if out:
        service_pid = str(out.q.contains(service).get_values('pid', 0))

        # get perf pid
        with device.bash_console() as bash:
            bash.execute(
                'sudo perf record -F 99 -a -g -p {service_pid} & sleep {sleep}'.format(
                    service_pid=service_pid, sleep=sleep))
            perf_pid = bash.execute('echo $!')

        if service_pid and perf_pid:
            return {'service_pid': service_pid, 'perf_pid': perf_pid}
        else:
            raise Exception("Couldn't get both service_pid and perf_pid")


def stop_perf_and_generate_svg(device,
                               perf_pid,
                               perf_filename,
                               vrf,
                               perf_save_remote_server,
                               svg_filename,
                               remote_flamegraph_location,
                               svg_archive_location='',
                               perf_save_local_bash='/bootflash/home/admin',
                               perf_save_local_nxos='bootflash:home/admin',
                               perf_save_remote_user='',
                               perf_save_remote_pass='',
                               perf_save_remote_via='',
                               sleep=10):
    """ stop perf in shell mode and then copy to remote and generate svg file
        # CISCO INTERNAL

        Args:
            device (`obj`): Device object
            perf_pid (`str`): Perf process id
            perf_filename (`str`): Perf filename
            perf_save_local_bash (`str`): Location to save perf file in shell
            perf_save_local_nxos (`str`): Location to save perf file in NXOS
            vrf: VRF for copying file to remote server
            perf_save_remote_user (`str`): userid on remote server
            perf_save_remote_pass (`str`): password of userid on remote server
            perf_save_remote_server (`str`): remote server name in testbed yaml
            perf_save_remote_via (`via`): specify connection to get ip
                                          if not specified, use active connection one
            svg_filename (`str`): svg filename
            svg_archive_location (`str`): svg archive location
            remote_flamegraph_location (`str`): flamegraph location on remote server
            sleep (`int`, optional): sleep for shell command. Defaults to 10 seconds

        Returns:
            svg_location (`str`): location of svg file

    """
    # check remote server in testbed yaml
    if perf_save_remote_server in device.testbed.devices:
        remote_srv = device.testbed.devices[perf_save_remote_server]
        # check if username/password for remote server
        if not perf_save_remote_user or not perf_save_remote_pass:
            perf_save_remote_user, perf_save_remote_pass = remote_srv.api.get_username_password(
            )
        # find ip for remote server from testbed yaml
        if perf_save_remote_via:
            perf_save_remote_server_ip = str(
                remote_srv.connections[perf_save_remote_via]['ip'])
        else:
            perf_save_remote_server_ip = str(
                remote_srv.connections[remote_srv.via]['ip'])
    else:
        raise Exception('{device} is not in testbed yaml'.format(
            device=perf_save_remote_server))

    # stop perf
    with device.bash_console() as bash:
        out = bash.execute(
            'sudo kill -2 {perf_pid} && sleep {sleep}'.format(perf_pid=perf_pid, sleep=sleep))
        if 'No such process' in out:
            raise Exception('No such process')

        # remove file in advance
        bash.execute(
            'rm -f {perf_filename}'.format(perf_filename=perf_filename))
        bash.execute('rm -f {perf_save_local_bash}/{perf_filename}'.format(
            perf_save_local_bash=perf_save_local_bash,
            perf_filename=perf_filename))

        # copy to bootflash
        bash.execute('sudo perf script > {perf_filename}'.format(
            perf_filename=perf_filename))
        bash.execute('sudo cp {perf_filename} {perf_save_local_bash}'.format(
            perf_filename=perf_filename,
            perf_save_local_bash=perf_save_local_bash))

    dialog = Dialog([
        Statement(pattern=r".*password",
                  action="sendline({remote_pass})".format(
                      remote_pass=perf_save_remote_pass),
                  args=None,
                  loop_continue=True,
                  continue_timer=False)
    ])
    out = device.execute(
        "copy {local_nxos}/{perf_filename} scp://{remote_user}@{remote_server}/{flamegraph_location}/{perf_filename} vrf {vrf}"
        .format(local_nxos=perf_save_local_nxos,
                perf_filename=perf_filename,
                remote_user=perf_save_remote_user,
                remote_server=perf_save_remote_server_ip,
                flamegraph_location=remote_flamegraph_location,
                vrf=vrf),
        reply=dialog)
    # generate svg file
    out = remote_srv.execute([
        "rm -f {flamegraph_location}/{perf_filename}-folded".format(
            flamegraph_location=remote_flamegraph_location,
            perf_filename=perf_filename),
        "cd {flamegraph_location} && cat {perf_filename} | .stackcollapse-perf.pl > {perf_filename}-folded"
        .format(flamegraph_location=remote_flamegraph_location,
                perf_filename=perf_filename),
        "./flamegraph.pl {perf_filename}-folded > {svg_filename}".format(
            perf_filename=perf_filename, svg_filename=svg_filename), "ls"
    ])
    if svg_filename not in out['ls']:
        raise Exception(
            "Couldn't generate svg file '{file}'".format(file=svg_filename))

    # move svg file to archive location
    if svg_archive_location:
        remote_srv.execute('mv {file} {archive_location}/{file}'.format(
            file=svg_filename, archive_location=svg_archive_location))
        return "{archive_location}/{file}".format(archive_location=svg_archive_location, file=svg_filename)
    else:
        return "{flamegraph_location}/{file}".format(
            flamegraph_location=remote_flamegraph_location, file=svg_filename)

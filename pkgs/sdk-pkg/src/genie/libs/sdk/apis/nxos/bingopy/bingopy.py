"""functions for BingoPy"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)


def analyze_core_by_bingopy(
        device,
        service,
        remote_server,
        remote_location,
        vrf='management',
        private_image_tree='',
        private_image_process_path='',
        clear_cores=True,
        max_time=360,
        check_interval=10,
        remote_user='',
        remote_pass='',
        remote_via='',
        bloggered=True,
        source_location='/auto/andatc/independent/shellrc-files/current/rc/.bashrc.build',
        bingopy_location='/ws/xianqin-sjc/bingo/blogger_core.pl',
        timeout=600):
    """ analyze core by BingoPy
        # CISCO INTERNAL

        Args:
            device (`obj`): Device object
            clear_cores (`bool`): To clear cores before generating core. Default to True
            service (`str`): service to generate core
            remote_server (`str`): remote server name in testbed yaml
            remote_user (`str`, optional): userid on remote server
            remote_pass (`str`, optional): password of userid on remote server
            remote_location (`str`): Location of saving core file
            remote_via: (`str`, optional): specify connection to get ip
                                 if not specified, use active connection one
            vrf (`str`): VRF for copying file to remote server
                         Defaults to management
            private_image_tree (`str`, optional): Tree location for private image
            private_image_process_path (`str`, optional): Process path for private image
            sleep (`int`, optional): sleep for shell command. Defaults to 10 seconds
            clear_cores (`Bool`, optional): clear cores if TRUE. Defaults to True
            max_time (`int`, optional): Maximum time to wait. 
                                        Defaults to 360 seconds
            check_interval (`int`, optional): Time interval while checking.
                                              Defaults to 10 seconds
            bloggered (`bool`, optional): if use bloggered command
                                          if False, use kill -6 command instead
                                          Defaults to True
            source_location (`str`, optional): source file location for BingoPy
                                               Defaults to /auto/andatc/independent/shellrc-files/current/rc/.bashrc.build
            bingopy_location (`str`, optional): bingopy location
                                                Defaults to /ws/xianqin-sjc/bingo/blogger_core.pl

        Returns:
            out (`str`): Output of BingoPy
    """

    # check remote server in testbed yaml
    if remote_server in device.testbed.devices:
        remote_srv = device.testbed.devices[remote_server]
        # check if username/password for remote server
        if not remote_user or not remote_pass:
            remote_user, remote_pass = remote_srv.api.get_username_password()
        # find ip for remote server from testbed yaml
        if remote_via:
            remote_server_ip = str(remote_srv.connections[remote_via]['ip'])
        else:
            remote_server_ip = str(
                remote_srv.connections[remote_srv.via]['ip'])
    else:
        raise Exception(
            '{device} is not in testbed yaml'.format(device=remote_server))

    # clear cores
    if clear_cores:
        device.execute("clear cores")

    # get sap_id
    try:
        out = device.parse(
            "show system internal sysmgr service name {service}".format(
                service=service))
        # example:
        # {
        #     "instance": {
        #         "bgp": {
        #             "tag": {
        #                 "65000": {
        #                     "internal_id": 87,
        #                     "last_restart_date": "Thu Aug 20 05:49:00 2020",
        #                     "last_terminate_reason": "SYSMGR_DEATH_REASON_FAILURE_SIGNAL",
        #                     "pid": 19262,
        #                     "plugin_id": "1",
        #                     "previous_pid": 18234,
        #                     "process_name": "bgp",
        #                     "restart_count": 12,
        #                     "sap": 308,
        #                     "state": "SRV_STATE_HANDSHAKED",
        #                     "state_start_date": "Thu Aug 20 05:49:00 2020",
        #                     "uuid": "0x11B"
        #                 }
        #             }
        #         }
        #     }
        # }
        sap_id = out.q.contains(service).get_values('sap', 0)
        pid = out.q.contains(service).get_values('pid', 0)
        if not sap_id:
            raise Exception("Couldn't get sap id")
    except SchemaEmptyParserError:
        return ''

    # generate core
    dialog = Dialog([
        Statement(pattern=r".*Want to proceed",
                  action="sendline(yes)",
                  args=None,
                  loop_continue=True,
                  continue_timer=False)
    ])
    if bloggered:
        out = device.execute(
            "bloggerd live-process-core sap {sap_id}".format(sap_id=sap_id),
            reply=dialog)
        if 'Successfully Saved' not in out:
            raise Exception("Core couldn't be generated by bloggerd command.")
    else:
        with device.bash_console() as bash:
            out = bash.execute(["sudo kill -6 {pid}".format(pid=pid)])

    # check cores
    out = ''
    tmout = Timeout(max_time=max_time, interval=check_interval)
    while tmout.iterate():
        try:
            out = device.parse("show cores")
            # example:
            # {
            #     "date": {
            #         "2020-08-20 05:49:09": {
            #             "pid": {
            #                 18234: {
            #                     "instance": 1,
            #                     "module": 1,
            #                     "process_name": "bgp-65000",
            #                     "vdc": 1
            #                 }
            #             }
            #         }
            #     }
            # }
            if out.q.contains(int(pid)):
                module_num = out.q.contains(pid).get_values('module', 0)
                break
        except SchemaEmptyParserError:
            pass
        tmout.sleep()

    if out:
        # check core filename
        with device.bash_console() as bash:
            out = bash.execute(["cd /logflash/core", "ls -rt | tail -n 1"])
            core_filename = out["ls -rt | tail -n 1"]

        # copy core to remote
        dialog = Dialog([
            Statement(pattern=r".*password",
                      action="sendline({remote_pass})".format(
                          remote_pass=remote_pass),
                      args=None,
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r".*Are you sure you want to",
                      action="sendline(yes)",
                      args=None,
                      loop_continue=True,
                      continue_timer=False)
        ])
        out = device.execute(
            "copy core://{module_num}/{pid} scp://{remote_user}@{remote_server}{remote_location} vrf {vrf} use-kstack"
            .format(module_num=module_num,
                    pid=pid,
                    remote_user=remote_user,
                    remote_server=remote_server_ip,
                    remote_location=remote_location,
                    vrf=vrf),
            reply=dialog)
        if 'No route to host' in out:
            raise Exception('No route to host {remote_server}'.format(
                remote_server=remote_server_ip))

        # run BingoPy
        if private_image_process_path or private_image_tree:
            out = remote_srv.execute(
                "cd {remote_location} && source {source_location} && "\
                "mkdir {dir} && {bingopy_location} -t ./{core_filename} "\
                "-M {remote_location}/{dir} -L {private_image_tree} "\
                "-p {private_image_process_path}"
                .format(source_location=source_location,
                        bingopy_location=bingopy_location,
                        remote_location=remote_location,
                        core_filename=core_filename,
                        dir=core_filename.replace('.tar.gz', ''),
                        private_image_tree=private_image_tree,
                        private_image_process_path=private_image_process_path),
                timeout=timeout)
        else:
            out = remote_srv.execute(
                "cd {remote_location} && {source_location} && mkdir {dir} "\
                "&& {bingopy_location} -t ./{core_filename} "\
                "-M {remote_location}/{dir}"
                .format(source_location=source_location,
                        bingopy_location=bingopy_location,
                        remote_location=remote_location,
                        core_filename=core_filename,
                        dir=core_filename.replace('.tar.gz', '')),
                timeout=timeout)
        # return output from BingoPy
        return out
    else:
        raise Exception("Core was not confirmed.")

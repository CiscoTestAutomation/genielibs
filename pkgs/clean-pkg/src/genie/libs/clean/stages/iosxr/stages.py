'''
IOSXR specific clean stages
'''

# Python
import os
import time
import logging

# pyATS
from pyats import aetest
from pyats.log.utils import banner

# Genie
from genie.libs.clean.utils import clean_schema

# MetaParser
from genie.metaparser.util.schemaengine import Optional

# Logger
log = logging.getLogger()


#===============================================================================
#                       stage: load_pies
#===============================================================================

@clean_schema({
    'files': list,
    Optional('server'): str,
    Optional('prompt_level'): str,
    Optional('synchronous'): bool,
    Optional('install_timeout'): int,
    Optional('max_time'): int,
    Optional('check_interval'): int,
})
@aetest.test
def load_pies(section, steps, device, files, server=None, prompt_level='none',
    synchronous=True, install_timeout=600, max_time=300, check_interval=60):

    '''
    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
        load_pies:
          files ('list'): List of XR pies to install
          server('str'): Hostname or IP address of server to use for install command
                         Default None (testbed YAML reverse lookup for TFTP server)
          prompt_level('str'): Prompt-level argument for install command
                               Default 'none' (Optional)
          synchronous ('bool'): Synchronous option for install command
                                Default True (Optional)
          install_timeout ('int'): Maximum time required for install command execution to complete
                                   Default 600 seconds (Optional)
          max_time ('int'): Maximum time to wait while checking for pies installed
                            Default 300 seconds (Optional)
          check_interval ('int'): Time interval while checking for pies installed
                                  Default 30 seconds (Optional)

    Example:
    --------
    devices:
      PE1:
        load_pies:
          files:
            - /auto/path/to/image/asr9k-mcast-px.pie-7.3.1.08I
            - /auto/path/to/image/asr9k-mgbl-px.pie-7.3.1.08I
            - /auto/path/to/image/asr9k-mpls-px.pie-7.3.1.08I
          server: 10.1.6.244
          prompt_level: 'all'
          synchronous: True
          timeout: 150
          max_time: 300
          check_interval: 20

    Flow:
    -----
    before:
      apply_configuration (Optional, user wants to boot device without PIE or SMU files)
    after:
      tftp_boot (Optional, user wants to boot device without PIE or SMU files)
    '''

    log.info("Section steps:\n1- Install and activate pie files provided"
             "\n2- Verify installed pie files are activated")

    # Init
    installed_packages = []

    with steps.start("Install and activate pie files on device {}".\
                    format(device.name)) as step:

        # Install pie files on device
        for file in files:

            # Install and activate pie
            log.info(banner("Install and activate pie: {}".format(file)))
            
            try:
                device.api.execute_install_pie(
                    image_dir=os.path.dirname(file),
                    image=os.path.basename(file),
                    server=server,
                    prompt_level=prompt_level,
                    synchronous=synchronous,
                    install_timeout=install_timeout)
            except Exception as e:
                log.error(str(e))
                section.failed("Unable to install or activate pie file {} on "
                               "device {}".format(file, device.name),
                               goto=['exit'])
            else:
                installed_packages.append(os.path.basename(file).split(".pie")[0])
                log.info("Installed and activated file {} on device {}".\
                        format(file, device.name))

        step.passed("Succesfully installed and activated all the pie files provided")


    with steps.start("Verify installed pie files are activated on device {}".\
                    format(device.name)) as step:

        # Verify pie file is successfully installed
        if not device.api.verify_installed_pies(
                    installed_packages=installed_packages,
                    check_interval=check_interval,
                    max_time=max_time):
            section.failed("Unable to activate pie files on device {}".\
                            format(device.name), goto=['exit'])
        else:
            section.passed("Successfully activated pie files on device {}".\
                            format(device.name))


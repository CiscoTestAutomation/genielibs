'''
Processors for Genie Triggers
'''

# Python
import time
import logging

# ATS
from pyats.aetest import Testcase
from pyats.aetest import reporter
from pyats.log.utils import banner
from pyats.log import managed_handlers
from pyats.results import TestResult, Passed, Failed, Skipped, Passx, Aborted, Errored
from pyats.aetest.base import TestableId
from pyats.datastructures import AttrDict
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

# Genie
from genie.libs import sdk
from genie.abstract import Lookup
from genie.harness.utils import connect_device
from genie.harness.exceptions import GenieTgnError
from genie.harness.libs.prepostprocessor.processors import report
from genie.utils.profile import pickle_traffic, unpickle_traffic, unpickle_stream_data
import re
import sys 
import time
import csv
import os
import shutil
import pdb
# Logger
log = logging.getLogger(__name__)

name_mapping = {}

def _get_connection_class(section):

    conn_class_name = None
    for dev in section.parameters['testbed'].find_devices(type='tgn'):
        for con in dev.connections:
            try:
                conn_class_name = dev.connections[con]['class'].__name__
            except:
                continue
    return conn_class_name

# ==============================================================================
# processor: send_arp
# ==============================================================================

@report
def send_arp(section, arp_wait_time=30):

    '''Trigger Processor:
        * Send ARP on traffic generator device
    '''

    # Init

    log.info(banner("processor: 'send_arp'"))

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        try:
            dev.connect(via='tgn')
        except GenieTgnError as e:
            log.error(e)
            log.error("Unable to connect to traffic generator device '{}'".\
                      format(dev.name))
            send_arp.result = Failed
            section.result += send_arp.result

        else:
            log.info("Connected to traffic generator device '{}'".\
                     format(dev.name))
            send_arp.result = Passed
            section.result += send_arp.result

        # Stop traffic on TGN
        try:
            dev.send_arp(wait_time=arp_wait_time)
        except GenieTgnError as e:
            log.error(e)
            log.error("Unable to send ARP  on '{}'".format(dev.name))
            send_arp.result = Failed
        else:
            log.info("Send ARP on '{}'".format(dev.name))
            send_arp.result = Passed


# ==============================================================================
# processor: send_ns
# ==============================================================================

@report
def send_ns(section, ns_wait_time=30):

    '''Trigger Processor:
        * Send NS on traffic generator device
    '''

    # Init

    log.info(banner("processor: 'send_ns'"))

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        try:
            dev.connect(via='tgn')
        except GenieTgnError as e:
            log.error(e)
            log.error("Unable to connect to traffic generator device '{}'".\
                      format(dev.name))
            send_ns.result = Failed
            section.result += send_ns.result

        else:
            log.info("Connected to traffic generator device '{}'".\
                     format(dev.name))
            send_ns.result = Passed
            section.result += send_ns.result

        # Stop traffic on TGN
        try:
            dev.send_ns(wait_time=ns_wait_time)
        except GenieTgnError as e:
            log.error(e)
            log.error("Unable to send NS  on '{}'".format(dev.name))
            send_ns.result = Failed
        else:
            log.info("Send NS on '{}'".format(dev.name))
            send_ns.result = Passed


# ==============================================================================
# processor: apply_traffic
# ==============================================================================

@report
def apply_traffic(section, apply_wait_time=30):

    '''Trigger Processor:
        * Applying traffic on traffic generator device
    '''

    # Init

    log.info(banner("processor: 'apply_traffic'"))

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        try:
            dev.connect(via='tgn')
        except GenieTgnError as e:
            log.error(e)
            log.error("Unable to connect to traffic generator device '{}'".\
                      format(dev.name))
            apply_traffic.result = Failed
            section.result += apply_traffic.result

        else:
            log.info("Connected to traffic generator device '{}'".\
                     format(dev.name))
            apply_traffic.result = Passed
            section.result += apply_traffic.result

        # Stop traffic on TGN
        try:
            dev.apply_traffic(wait_time=apply_wait_time)
        except GenieTgnError as e:
            log.error(e)
            log.error("Unable to apply traffic on '{}'".format(dev.name))
            apply_traffic.result = Failed
        else:
            log.info("Applying traffic on '{}'".format(dev.name))
            apply_traffic.result = Passed


# ==============================================================================
# processor: create_genie_statistics_view
# ==============================================================================

@report
def create_genie_statistics_view(section, view_create_interval=30, view_create_iteration=5, disable_tracking=False, disable_port_pair=False):

    '''Trigger Processor:
        * Creates GENIE traffic statistics view on traffic generator device
        * This processor is useful if we want to check compare traffic profile
          after we do stop_traffic and apply_traffic in a trigger. 
          apply_traffic will delete the existing GENIE statistic view. 
    '''

    # Init

    log.info(banner("processor: 'create_genie_statistics_view'"))

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info("Traffic generator devices not specified in --devices")
            return

        # Connect to TGN
        try:
            dev.connect(via='tgn')
        except GenieTgnError as e:
            log.error(e)
            log.error("Unable to connect to traffic generator device '{}'".\
                      format(dev.name))
            create_genie_statistics_view.result = Failed
            section.result += create_genie_statistics_view.result

        else:
            log.info("Connected to traffic generator device '{}'".\
                     format(dev.name))
            create_genie_statistics_view.result = Passed
            section.result += create_genie_statistics_view.result

        # Creating GENIE traffic view on TGN
        try:
            dev.create_genie_statistics_view(view_create_interval=view_create_interval, \
                    view_create_iteration=view_create_iteration, \
                    disable_tracking=disable_tracking, \
                    disable_port_pair=disable_port_pair)
        except GenieTgnError as e:
            log.error(e)
            log.error("Unable to create GENIE traffic statistics view on '{}'".format(dev.name))
            create_genie_statistics_view.result = Failed
        else:
            log.info("Creating GENIE traffic statistic view on '{}'".format(dev.name))
            create_genie_statistics_view.result = Passed


######################################################################################################################################################

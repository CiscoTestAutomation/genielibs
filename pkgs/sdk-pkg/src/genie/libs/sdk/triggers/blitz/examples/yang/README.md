Examples
========

This directory contains working examples run against Cisco devices.

The testbed file has an XE Cat9K, and a Nexus 9k setup (Fake IP addresses).
The mapping file allows you to filter out the device you want to test.
The test_trigger_extended "data" file contains various xpath, namespace, and values that extends the test_trigger.
The test_trigger file contains the actual definitions of the test and extends the data file.
The job file is an example of how to choose exactly which test you wish to run.

Main points to get your test running.

- Testbed file device name must match the configured "host" name of the device.
- TLS certificates will be needed if you are testing secure connections (see testbed file).
- TLS certificate host override setting, if added to certificate, must be added to host file or DNS.
- Mapping file must match the device name or alias you want to test in the testbed file.
- Data file may need device name/connection of mapping file and the protocol used in test.
- Job file, uncomment tests you want to run, comment out tests you don't want to run.

Tests in test file:

- device_cleanup - Not called in job file but there as an example.
- native_oper_interface_statistics_get - An XE NETCONF get of interface statistics with returned values verified.
- openconfig_gnmi_fan_statistics_subscribe - An XE gNMI SAMPLE subscription which receives fan speed every 5 seconds and verifies value.
- native_netconf_cpu_statistics_subscribe - An XE NETCONF SAMPLE subscription which receives CPU five-minute statistic every 5 seconds and verifies value.
- nexus_openconfig_gnmi_fan_statistics_subscribe - An NX gNMI SAMPLE subscription which receives fan speed every 5 seconds and verifies value.
- nexus_netconf_interface_state_subscribe - An NX NETCONF ON_CHANGE subscription which verifies interface state when change on device.

Command:

pyats run job job_native_test.py -t testbed_native_test.yaml --no-mail --pdb

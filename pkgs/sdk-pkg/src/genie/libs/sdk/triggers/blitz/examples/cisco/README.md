Examples
========

This directory contains working examples run against Cisco devices (OS agnostic).

The testbed file has a CSR1K, Cat9K, and Nexus 9k setups.
The mapping file allows you to filter out the device you want to test.
The data file contains various xpath, namespace, and values that you are interested in.
The native_test file contains the actual definitions of the test and extends the data file.
The job file is an example of how to choose exactly which test you wish to run.

Main points to get your test running.

- Testbed file device name must match the configured "host" name of the device.
- Mapping file must match the device name you want to test in the testbed file.
- Data file must have device name/connection of mapping file and the protocol you want to test.
- Job file, uncomment tests you want to run, comment out tests you don't want to run.

Command:

pyats run job job_native_test.py -t testbed_native_test.yaml --no-mail --pdb

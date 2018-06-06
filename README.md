# Genie libs

This library package contains the open source implementations for:
 
- Genie Ops: objects modelling the operational state of devices
- Genie Conf: objects modelling the configuration of devices
- Genie Robot: robot library layer, enabling Genie libs to be used in Robot Framework
- Genie SDK: triggers and verifications (reuseable testcases) implemented using
             Genie infrastructure.

## About

Genie is both a library framework and a test harness that facilitates rapid
development, encourage re-usable and simplify writing test automation. Genie
bundled with the modular architecture of pyATS framework accelerates and
simplifies test automation leveraging all the perks of the Python programming
language in an object-orienting fashion.

pyATS is an end-to-end testing ecosystem, specializing in data-driven and
reusable testing, and engineered to be suitable for Agile, rapid development
iterations. Extensible by design, pyATS enables developers to start with small,
simple and linear test cases, and scale towards large, complex and asynchronous
test suites.

Genie was initially developed internally in Cisco, and is now available to the
general public starting early 2018 through [Cisco DevNet].

[Cisco Devnet]: https://developer.cisco.com/


# Installation

This package is automatically installed when Genie gets installed.

```bash
bash$ pip install genie
```

Detailed installation guide can be found on [our website].

[our website]: https://developer.cisco.com/site/pyats/


# Development

To develop this package, assuming you have Genie already installed in your
environment, follow the commands below:

```bash
# remove the packages
bash$ pip uninstall -y genie.libs.conf genie.libs.ops genie.libs.sdk genie.libs.robot

# clone this repo
bash$ git clone https://github.com/CiscoTestAutomation/genielibs.git

# put all packages in dev mode
bash$ cd genielibs
bash$ make develop
```

Now you should be able to develop the files and see it reflected in your runs.

# ChangeLog

* [conf](pkgs/conf-pkg/changelog/CHANGELOG.md)
* [sdk](pkgs/sdk-pkg/changelog/CHANGELOG.md)
* [ops](pkgs/ops-pkg/changelog/CHANGELOG.md)
* [robot](pkgs/robot-pkg/changelog/CHANGELOG.md)

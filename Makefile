################################################################################
#                                                                              #
#                      Cisco Systems Proprietary Software                      #
#        Not to be distributed without consent from Test Technology            #
#                               Cisco Systems, Inc.                            #
#                                                                              #
################################################################################
#                           Genie Libs Makefile
#
# Author:
#   Siming Yuan        (siyuan@cisco.com)    - CSG
#   Jean-Benoit Aubin  (jeaubin@cisco.com)   - CSG
#
# Support:
#    python-core@cisco.com
#
# Version:
#   v2.1
#
# Date:
#   April 2018
#
# About This File:
#   This script will build individual Genie libs modules into Python PyPI packages.
#    Make sure all requirements are met before adding new package names to
#    PACKAGES variable.
#
# Requirements:
#    1. Module name is the same as package name.
#    2. setup.py file is stored within the module folder
################################################################################

# Variables
PKG_NAME      = genie.libs
BUILD_DIR     = $(shell pwd)/__build__
DIST_DIR      = $(BUILD_DIR)/dist
BUILD_CMD     = python setup.py bdist_wheel --dist-dir=$(DIST_DIR)
PROD_USER     = pyadm@pyats-ci
PROD_PKGS     = /auto/pyats/packages
PROD_SCRIPTS  = /auto/pyats/bin
TESTCMD       = runAll
WATCHERS      = asg-genie-dev@cisco.com
HEADER        = [Watchdog]
PYPIREPO      = pypitest
PYTHON		  = python
PYLINT_CMD	  = pylintAll
CYTHON_CMD	  = compileAll

# Development pkg requirements
RELATED_PKGS = genie.libs.health genie.libs.clean genie.libs.conf genie.libs.ops genie.libs.robot genie.libs.sdk
RELATED_PKGS += genie.libs.filetransferutils
DEPENDENCIES = restview psutil Sphinx wheel asynctest pysnmp
DEPENDENCIES += setproctitle  sphinx-rtd-theme pyftpdlib tftpy
DEPENDENCIES += Cython requests ruamel.yaml

# Internal variables.
# (note - build examples & templates last because it will fail uploading to pypi
#  due to duplicates, and we'll for now accept that error)
PYPI_PKGS      = health-pkg clean-pkg conf-pkg ops-pkg robot-pkg sdk-pkg filetransferutils-pkg

ALL_PKGS       = $(PYPI_PKGS)

.PHONY: help docs distribute_docs clean check devnet\
	develop undevelop distribute test install_build_deps
	uninstall_build_deps $(ALL_PKGS)

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "     --- common actions ---"
	@echo ""
	@echo " check                 check setup.py content"
	@echo " clean                 remove the build directory ($(BUILD_DIR))"
	@echo " help                  display this help"
	@echo " test                  run all unittests in an efficient manner"
	@echo " develop               set all package to development mode"
	@echo " undevelop             unset the above development mode"
	@echo " devnet                Build DevNet package."
	@echo " install_build_deps    install pyats-distutils"
	@echo " uninstall_build_deps  remove pyats-distutils"
	@echo " compile               Compile all python modules to c"
	@echo " coverage_all          Run code coverage on all test files"
	@echo " pylint_all            Run python linter on all python modules"
	@echo " json					 Build json files"
	@echo " changelogs			 Build compiled changelog file"
	@echo ""
	@echo "     --- build all targets ---"
	@echo ""
	@echo " all                  make all available pyATS packages"
	@echo ""
	@echo "     --- build specific targets ---"
	@echo ""
	@echo " health-pkg            	build genie.libs.health package"
	@echo " clean-pkg            	build genie.libs.clean package"
	@echo " conf-pkg             	build genie.libs.conf package"
	@echo " ops-pkg              	build genie.libs.ops package"
	@echo " sdk-pkg              	build genie.libs.sdk package"
	@echo " robot                	build genie.libs.robot package"
	@echo " filetransferutils-pkg   build genie.libs.filetransferutils package"
	@echo ""
	@echo "     --- distributions to production environment ---"
	@echo ""
	@echo " distribute           distribute built pkgs to production server"
	@echo ""
	@echo "     --- redirects ---"
	@echo " docs             create all documentation locally. This the same as"
	@echo "                  running 'make docs' in ./docs/"
	@echo " distribute_docs  release local documentation to website. This is"
	@echo "                  the same as running 'make distribute' in ./docs/"
	@echo ""
	@echo "     --- build arguments ---"
	@echo " DEVNET=true              build for devnet style (cythonized, no ut)"
	@echo " INCLUDE_TESTS=true       build include unittests in cythonized pkgs"

compile:
	@echo ""
	@echo "Compiling to C code"
	@echo --------------------------
	@$(CYTHON_CMD) --exclude *iosxe/ip_precedence/verify.py *iosxe/udp/get.py
	@echo "Done Compiling"
	@echo ""
	@echo "Done."
	@echo ""

coverage_all:
	@echo ""
	@echo "Running code coverage on all unittests"
	@echo ---------------------------------------
	@$(TESTCMD) --path tests/ --coverage --no-refresh
	@echo ""
	@echo "Done."
	@echo ""

pylint_all:
	@echo ""
	@echo "Running Pylint on all modules"
	@echo "-----------------------------"
	@$(PYLINT_CMD)
	@echo "Done linting"
	@echo ""
	@echo "Done."
	@echo ""

devnet: all
	@echo "Completed building DevNet packages"
	@echo ""

install_build_deps:
	@pip install --upgrade pip setuptools wheel

uninstall_build_deps:
	@echo "nothing to do"

docs:
	@echo "No documentation to build for genie.libs"

clean:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Removing make directory: $(BUILD_DIR)"
	@rm -rf $(BUILD_DIR)
	@$(foreach dir,$(ALL_PKGS),(cd pkgs/$(dir) && python setup.py clean) &&) :
	@echo "Removing *.pyc *.c and __pycache__/ files"
	@find . -type f -name "*.pyc" | xargs rm -vrf
	@find . -type f -name "*.c" | xargs rm -vrf
	@find . -type d -name "__pycache__" | xargs rm -vrf
	@find . -type d -name "build" | xargs rm -vrf
	@echo ""
	@echo "Done."
	@echo ""

develop:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Installing development dependencies"
	@pip uninstall -y $(RELATED_PKGS) || true
	@pip install $(DEPENDENCIES)
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Setting up development environment"
	@$(foreach dir,$(ALL_PKGS),(cd pkgs/$(dir) && python setup.py develop --no-deps -q) &&) :
	@echo ""
	@echo "Done."
	@echo ""

undevelop:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Removing development environment"
	@$(foreach dir,$(ALL_PKGS),(cd pkgs/$(dir) && python setup.py develop -q --no-deps --uninstall) &&) :
	@echo ""
	@echo "Done."
	@echo ""

distribute:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Copying all distributable to $(PROD_PKGS)"
	@test -d $(DIST_DIR) || { echo "Nothing to distribute! Exiting..."; exit 1; }
	@ssh -q $(PROD_USER) 'test -e $(PROD_PKGS)/$(PKG_NAME) || mkdir $(PROD_PKGS)/$(PKG_NAME)'
	@scp $(DIST_DIR)/* $(PROD_USER):$(PROD_PKGS)/$(PKG_NAME)/
	@echo ""
	@echo "Done."
	@echo ""

all: $(ALL_PKGS)
	@echo ""
	@echo "Done."
	@echo ""

package: $(ALL_PKGS)
	@echo ""
	@echo "Done."
	@echo ""

$(ALL_PKGS):
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Building pyATS distributable: $@"
	@echo ""

	cd pkgs/$@/; $(BUILD_CMD)

	@echo "Completed building: $@"
	@echo ""
	@echo "Done."
	@echo ""

test:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Running all unit tests..."
	@echo ""

	@$(TESTCMD) --path tests/

	@echo "Completed unit testing"
	@echo ""
	@echo "Done."
	@echo ""

check:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Checking setup.py consistency..."
	@echo ""

	@$(foreach dir,$(ALL_PKGS),(cd pkgs/$(dir) && python setup.py check) &&) :

	@echo "Done."
	@echo ""

json:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Generating libs json file"
	@echo ""
	@python -c "from genie.json.make_json import make_genielibs; make_genielibs()"
	@echo ""
	@echo "Done."
	@echo ""

changelogs:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Generating changelog file"
	@echo ""
	@python "./tools/changelog_script.py" "./pkgs/clean-pkg/changelog/undistributed" --output "./pkgs/clean-pkg/changelog/undistributed.rst"
	@echo "clean-pkg changelog done..."
	@python "./tools/changelog_script.py" "./pkgs/health-pkg/changelog/undistributed" --output "./pkgs/health-pkg/changelog/undistributed.rst"
	@echo "health-pkg changelog done..."
	@python "./tools/changelog_script.py" "./pkgs/conf-pkg/changelog/undistributed" --output "./pkgs/conf-pkg/changelog/undistributed.rst"
	@echo "conf-pkg changelog done..."
	@python "./tools/changelog_script.py" "./pkgs/filetransferutils-pkg/changelog/undistributed" --output "./pkgs/filetransferutils-pkg/changelog/undistributed.rst"
	@echo "filetransferutils-pkg changelog done..."
	@python "./tools/changelog_script.py" "./pkgs/ops-pkg/changelog/undistributed" --output "./pkgs/ops-pkg/changelog/undistributed.rst"
	@echo "ops-pkg changelog done..."
	@python "./tools/changelog_script.py" "./pkgs/robot-pkg/changelog/undistributed" --output "./pkgs/robot-pkg/changelog/undistributed.rst"
	@echo "robot-pkg changelog done..."
	@python "./tools/changelog_script.py" "./pkgs/sdk-pkg/changelog/undistributed" --output "./pkgs/sdk-pkg/changelog/undistributed.rst"
	@echo "sdk-pkg changelog done..."
	@echo ""
	@echo "Done."
	@echo ""

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
#    pyats-core@cisco.com
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
BUILD_DIR     = $(shell pwd)/__build__
DIST_DIR      = $(BUILD_DIR)/dist
BUILD_CMD     = python3 setup.py bdist_wheel --dist-dir=$(DIST_DIR)
TESTCMD       = runAll
WATCHERS      = asg-genie-dev@cisco.com
HEADER        = [Watchdog]
PYPIREPO      = pypitest
PYTHON		  = python3
PYLINT_CMD	  = pylintAll
CYTHON_CMD	  = compileAll

# Development pkg requirements
RELATED_PKGS = genie.libs.health genie.libs.clean genie.libs.conf genie.libs.ops genie.libs.robot genie.libs.sdk
RELATED_PKGS += genie.libs.filetransferutils
# Adding pyasyncore pkg to fix pysnmp scripts for python 3.12
DEPENDENCIES = restview psutil Sphinx wheel asynctest 'pysnmp>=6.1.4,<6.2' pyasn1==0.6.0
DEPENDENCIES += sphinx-rtd-theme==1.1.0 pyftpdlib tftpy\<0.8.1 robotframework
DEPENDENCIES += Cython requests ruamel.yaml grpcio protobuf jinja2 pyVmomi
# Internal variables.
# (note - build examples & templates last because it will fail uploading to pypi
#  due to duplicates, and we'll for now accept that error)
DEV_PKGS       =   develop-health   develop-clean   develop-conf   develop-ops   develop-robot   develop-sdk   develop-filetransferutils
UNDEV_PKGS     = undevelop-health undevelop-clean undevelop-conf undevelop-ops undevelop-robot undevelop-sdk undevelop-filetransferutils
PYPI_PKGS      = health-pkg clean-pkg conf-pkg ops-pkg robot-pkg sdk-pkg filetransferutils-pkg
ALL_PKGS       = $(PYPI_PKGS)


.PHONY: help docs distribute_docs clean check devnet\
	develop undevelop distribute distribute_staging distribute_staging_external\
	test install_build_deps uninstall_build_deps $(ALL_PKGS) $(DEV_PKGS)
	test install_build_deps uninstall_build_deps $(ALL_PKGS) $(DEV_PKGS)
	$(UNDEV_PKGS)

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
	@echo " distribute                    distribute built pkgs to production"
	@echo "                               server"
	@echo " distribute_staging            distribute build pkgs to staging area"
	@echo " distribute_staging_external   distribute build pkgs to external"
	@echo "                               staging area"
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
	@pip install cisco-distutils --upgrade || true
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

dependencies:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Installing development dependencies"
	@pip install $(DEPENDENCIES)
	@echo "Done."
	@echo ""

docs:
	@echo "No documentation to build for genie.libs"

clean:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Removing make directory: $(BUILD_DIR)"
	@rm -rf $(BUILD_DIR)
	@$(foreach dir,$(ALL_PKGS),(cd pkgs/$(dir) && python3 setup.py clean) &&) :
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
	# workaround for Polaris SDK
	@if [ $BINOS_ATESTS ]; \
	 then pip install $(DEPENDENCIES) --ignore-installed docutils; \
	 else pip install $(DEPENDENCIES); \
	fi
	@pip uninstall -y $(RELATED_PKGS) || true
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Setting up development environment"
	@$(foreach dir,$(ALL_PKGS),(cd pkgs/$(dir) && python3 setup.py develop --no-deps -q) &&) :
	@echo ""
	@echo "Done."
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Development environment has been setup."
	@echo -e "\e[1;33mWarning: Do make json to generate json files to acccess the genie features!!!\e[0m"
	@echo "--------------------------------------------------------------------"


undevelop:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Removing development environment"
	@$(foreach dir,$(ALL_PKGS),(cd pkgs/$(dir) && python3 setup.py develop -q --no-deps --uninstall) &&) :
	@echo ""
	@echo "Done."
	@echo ""

$(DEV_PKGS):
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Setting up development environment"
	@pip uninstall -y $(subst develop-,,genie.libs.$@) || true
	@cd $(subst develop-,,pkgs/$@-pkg) && python setup.py develop -q --no-deps
	@echo ""
	@echo "Done."
	@echo ""

$(UNDEV_PKGS):
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Removing development environment"
	@cd $(subst undevelop-,,pkgs/$@-pkg) && python setup.py develop -q --no-deps --uninstall
	@echo ""
	@echo "Done."
	@echo ""

distribute:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Copying all distributable to $(PROD_PKGS)"
	@test -d $(DIST_DIR) || { echo "Nothing to distribute! Exiting..."; exit 1; }
	@echo "Organizing distributable into folders"
	@organize_dist --dist $(DIST_DIR)
	@rsync -rtlpv --progress $(DIST_DIR)/* $(PROD_USER):$(PROD_PKGS)
	@echo ""
	@echo "Done."
	@echo ""

distribute_staging:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Copying all distributable to $(STAGING_PKGS)"
	@test -d $(DIST_DIR) || { echo "Nothing to distribute! Exiting..."; exit 1; }
	@echo "Organizing distributable into folders"
	@organize_dist --dist $(DIST_DIR)
	@rsync -rtlpv --progress $(DIST_DIR)/* $(PROD_USER):$(STAGING_PKGS)
	@echo ""
	@echo "Done."
	@echo ""

distribute_staging_external:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Copying all distributable to $(STAGING_EXT_PKGS)"
	@test -d $(DIST_DIR) || { echo "Nothing to distribute! Exiting..."; exit 1; }
	@echo "Organizing distributable into folders"
	@organize_dist --dist $(DIST_DIR)
	@rsync -rtlv --progress $(DIST_DIR)/* $(PROD_USER):$(STAGING_EXT_PKGS)
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

	@$(foreach dir,$(ALL_PKGS),(cd pkgs/$(dir) && python3 setup.py check) &&) :

	@echo "Done."
	@echo ""

json:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Generating libs json file"
	@echo ""
	@python3 -c "from genie.json.make_json import make_genielibs; make_genielibs()"
	@echo ""
	@echo "Done."
	@echo ""

json_apis:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Generating Genie API json file"
	@echo ""
	@python3 -c "from genie.json.make_json import make_apis; make_apis()"
	@echo ""
	@echo "Done."
	@echo ""

json_ops:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Generating Genie OPS json file"
	@echo ""
	@python3 -c "from genie.json.make_json import make_ops; make_ops()"
	@echo ""
	@echo "Done."
	@echo ""

json_clean:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Generating Genie OPS json file"
	@echo ""
	@python3 -c "from genie.json.make_json import make_clean; make_clean()"
	@echo ""
	@echo "Done."
	@echo ""

json_models:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Generating Genie OPS json file"
	@echo ""
	@python3 -c "from genie.json.make_json import make_models; make_models()"
	@echo ""
	@echo "Done."
	@echo ""

json_triggers:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Generating Genie OPS json file"
	@echo ""
	@python3 -c "from genie.json.make_json import make_triggers; make_triggers()"
	@echo ""
	@echo "Done."
	@echo ""

json_verifications:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Generating Genie OPS json file"
	@echo ""
	@python3 -c "from genie.json.make_json import make_verifications; make_verifications()"
	@echo ""
	@echo "Done."
	@echo ""

changelogs:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Generating changelog file"
	@echo ""
	@python3 -c "from ciscodistutils.make_changelog import main; main('./pkgs/clean-pkg/changelog/undistributed', './pkgs/clean-pkg/changelog/undistributed.rst')"
	@echo "clean-pkg changelog done..."
	@python3 -c "from ciscodistutils.make_changelog import main; main('./pkgs/health-pkg/changelog/undistributed', './pkgs/health-pkg/changelog/undistributed.rst')"
	@echo "health-pkg changelog done..."
	@python3 -c "from ciscodistutils.make_changelog import main; main('./pkgs/conf-pkg/changelog/undistributed', './pkgs/conf-pkg/changelog/undistributed.rst')"
	@echo "conf-pkg changelog done..."
	@python3 -c "from ciscodistutils.make_changelog import main; main('./pkgs/filetransferutils-pkg/changelog/undistributed', './pkgs/filetransferutils-pkg/changelog/undistributed.rst')"
	@echo "filetransferutils-pkg changelog done..."
	@python3 -c "from ciscodistutils.make_changelog import main; main('./pkgs/ops-pkg/changelog/undistributed', './pkgs/ops-pkg/changelog/undistributed.rst')"
	@echo "ops-pkg changelog done..."
	@python3 -c "from ciscodistutils.make_changelog import main; main('./pkgs/robot-pkg/changelog/undistributed', './pkgs/robot-pkg/changelog/undistributed.rst')"
	@echo "robot-pkg changelog done..."
	@python3 -c "from ciscodistutils.make_changelog import main; main('./pkgs/sdk-pkg/changelog/undistributed', './pkgs/sdk-pkg/changelog/undistributed.rst')"
	@echo "sdk-pkg changelog done..."
	@echo ""
	@echo "Done."
	@echo ""

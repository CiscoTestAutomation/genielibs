# Variables
BUILD_ROOT    = $(shell pwd)/__build__
OUTPUT_DIR    = $(BUILD_ROOT)/dist
BUILD_CMD     = python setup.py bdist_wheel --dist-dir=$(OUTPUT_DIR)
TESTCMD       = ./tests/runAll --path tests/

# Development pkg requirements
DEPENDENCIES  = restview psutil Sphinx wheel asynctest
DEPENDENCIES += setproctitle sphinxcontrib-napoleon sphinx-rtd-theme httplib2 
DEPENDENCIES += pip-tools Cython requests

PKGS      = conf ops robot sdk 


.PHONY: help clean check develop undevelop test all $(PKGS)

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "     --- common actions ---"
	@echo ""
	@echo "	check                check setup.py content"
	@echo " clean                remove the build directory ($(BUILD_ROOT))"
	@echo " help                 display this help"
	@echo " test                 run all unittests in an efficient manner"
	@echo " develop              set all package to development mode"
	@echo " undevelop            unset the above development mode"
	@echo ""
	@echo "     --- build all targets ---"
	@echo ""
	@echo " all                  make all available pyATS packages"
	@echo ""
	@echo "     --- build specific targets ---"
	@echo ""
	@echo " conf                 build genie.libs.conf package"
	@echo " ops                  build genie.libs.ops package"
	@echo " sdk                  build genie.libs.sdk package"
	@echo " robot                build genie.libs.robot package"
	@echo ""


clean:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Removing make directory: $(BUILD_ROOT)"
	@rm -rf $(BUILD_ROOT)
	@$(foreach dir,$(PKGS),(cd pkgs/$(dir)-pkg && python setup.py clean) &&) :
	@echo "Removing *.pyc *.c and __pycache__/ files"
	@find . -type f -name "*.pyc" | xargs rm -vrf
	@find . -type f -name "*.c" | xargs rm -vrf
	@find . -type d -name "__pycache__" | xargs rm -vrf
	@echo ""
	@echo "Done."
	@echo ""

develop:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Installing development dependencies"
	@pip install $(DEPENDENCIES)
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Setting up development environment"
	@$(foreach dir,$(PKGS),(cd pkgs/$(dir)-pkg && python setup.py develop --no-deps -q) &&) :
	@echo ""
	@echo "Done."
	@echo ""

undevelop:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Removing development environment"
	@$(foreach dir,$(PKGS),(cd pkgs/$(dir)-pkg && python setup.py develop -q --no-deps --uninstall) &&) :
	@echo ""
	@echo "Done."
	@echo ""

all: $(PKGS)
	@echo ""
	@echo "Done."
	@echo ""

$(PKGS):
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Building pyATS distributable: $@"
	@echo ""

	mkdir -p $(OUTPUT_DIR)/
	cd pkgs/$@-pkg/; $(BUILD_CMD)
	
	@echo "Completed building: $@"
	@echo ""

test:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Running all unit tests..."
	@echo ""

	@$(TESTCMD) 

	@echo "Completed unit testing"
	@echo ""

check:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Checking setup.py consistency..."
	@echo ""

	@$(foreach dir,$(PKGS),(cd pkgs/$(dir)-pkg && python setup.py check) &&) :

	@echo "Done"
	@echo ""

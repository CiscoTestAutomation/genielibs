from pyats.topology.exceptions import *

class AllSubsetsRejectedError(ValueError):

    def __init__(self, topology):
        self.topology = topology
        super().__init__('All topology subsets were rejected')

class FailedToResolveException(Exception):

    def __init__(self, topology):
        self.topology = topology
        super().__init__('Failed to resolve topology')

# vim: ft=python ts=8 sw=4 et

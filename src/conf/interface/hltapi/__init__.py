from .interface import *
try:
    from genie import abstract
    abstract.declare_token(__name__)
except Exception as e:
    import warnings
    warnings.warn('Could not declare abstraction token: ' + str(e))

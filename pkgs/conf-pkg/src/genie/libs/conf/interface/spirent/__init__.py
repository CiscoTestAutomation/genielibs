from .interface import *
try:
    from genie import abstract
    # ODD ABSTRACT
    abstract.declare_token(os='spirent')
except Exception as e:
    import warnings
    warnings.warn('Could not declare abstraction token: ' + str(e))

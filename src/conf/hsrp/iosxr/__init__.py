# Enable abstraction using this directory name as the abstraction token
try:
    from genie import abstract
    abstract.declare_token(__name__)
except Exception as e:
    warnings.warn('Could not declare abstraction token: ' + str(e))

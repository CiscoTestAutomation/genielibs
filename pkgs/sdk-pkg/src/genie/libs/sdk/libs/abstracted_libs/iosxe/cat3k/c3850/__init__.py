# Enable abstraction using this directory name as the abstraction token
try:
    from genie import abstract
    abstract.declare_token(model='c3850')
except Exception as e:
    import warnings
    warnings.warn('Could not declare abstraction token: ' + str(e))

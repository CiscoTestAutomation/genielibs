# Enable abstraction using this directory name as the abstraction token
try:
    from genie import abstract
    # ODD ABSTRACT
    abstract.declare_token(platform='rest')
except Exception as e:
    import warnings
    warnings.warn('Could not declare abstraction token: ' + str(e))

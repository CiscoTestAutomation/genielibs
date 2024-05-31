try:
    from genie import abstract
    abstract.declare_token(platform='ap')
except Exception as e:
    import warnings
    warnings.warn('Could not declare abstraction token: ' + str(e))

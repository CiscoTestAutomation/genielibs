try:
    from genie import abstract
    abstract.declare_token(platform='cat8k', model='c8200')
except Exception as e:
    import warnings
    warnings.warn('Could not declare abstraction token: ' + str(e))

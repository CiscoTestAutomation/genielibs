try:
    from genie import abstract
    abstract.declare_token(platform='cat9k', model='c9500')
except Exception as e:
    import warnings
    warnings.warn('Could not declare abstraction token: ' + str(e))

try:
    from genie import abstract
    abstract.declare_token(os='iosxe')
except Exception as e:
    import warnings
    warnings.warn('Could not declare abstraction token: ' + str(e))

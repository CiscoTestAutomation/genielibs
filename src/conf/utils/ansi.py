'''ANSI constants'''

re_CSIesc = r'(?:\x1B\[)'  # Control Sequence Initiator (ANSI X3.64)
re_CSIiso = r'(?:\x9B)'    # Control Sequence Introducer (ISO 8859)
re_CSI = r'(?:' + re_CSIesc + r'|' + re_CSIiso + r')'
re_arg = r'(?:\d*|"[^"]*")'
re_generic = r'(?:' + re_CSI + re_arg + r'(?:;' + re_arg + r')*[A-Za-z])'


"""PasswordType type implementation
"""

__all__ = (
        'PasswordType',
        )

from enum import Enum


class PasswordType(Enum):
    clear = 'clear'
    encrypted = proprietary = 'encrypted'
    md5 = 'md5'


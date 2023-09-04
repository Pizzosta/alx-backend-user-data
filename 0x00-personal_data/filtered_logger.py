#!/usr/bin/env python3
'''Regex-ing Module'''

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''
    Returns the log message obfuscated

    Args:
        fields (list[str]): A list of strings representing fields to obfuscate.
        redaction (str): the value by which the fields will be obfuscated.
        message (str): A str representing the log message.
        separator (str): the character that separates fields in the log msg.
    '''
    return re.sub(fr'(?<=^{separator}|{separator})({"|".join(fields)})\
                  (?={separator}|$)', redaction, message)

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
        redaction (str): A string representing the value by which the fields will be obfuscated.
        message (str): A string representing the log message.
        separator (str): A string representing the character that separates fields in the log message.
    '''
    return re.sub(fr'(?<=^{separator}|{separator})({"|".join(fields)})\
                  (?={separator}|$)', redaction, message)

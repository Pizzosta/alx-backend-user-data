#!/usr/bin/env python3
"""Definition of filter_datum function that
returns an obfuscated log message
"""

import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message obfuscated

    Args:
        fields (list[str]): A list of strings representing fields to obfuscate.
        redaction (str): the value by which the fields will be obfuscated.
        message (str): A str representing the log message.
        separator (str): the character that separates fields in the log msg.
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Redact the message of LogRecord instance

        Args:
            record (logging.LogRecord): LogRecord instance containing message
        """
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """Return a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to a database securely"""
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )
    return connection


def main():
    db_connection = get_db()
    logger = get_logger()
    cursor = db_connection.cursor()

    cursor.execute("SELECT * FROM users;")

    filtered_fields = cursor.column_names

    for row in cursor.fetchall():
        log_message = "".join("{}={}; ".format(k, v)
                              for k, v in zip(filtered_fields, row))
        logger.info(log_message.strip())

    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()

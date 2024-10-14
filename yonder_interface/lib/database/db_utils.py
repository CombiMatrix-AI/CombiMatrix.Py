from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict
import logging

logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

def get_connection(credentials: Dict):
    connection_string = (
        f"mysql+mysqlconnector://{credentials['username']}:{quote_plus(credentials['password'])}@{credentials['host']}:{credentials['port']}/{credentials['database']}"
    )
    return create_engine(connection_string)

def is_valid_connection(con) -> bool:
    try:
        con.connect()
        logging.info("Valid connection")
        return True
    except SQLAlchemyError as e:
        logging.warning("Invalid connection due to error: %s", e.__cause__)
        return False
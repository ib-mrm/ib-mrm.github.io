"""
General functions for database connections
"""

import psycopg2
import pandas as pd

from sqlalchemy import create_engine
from .context import config


def get_connection(db):
    """
    Setup a connection to a postgres database
    """
    if db == 'dbprod':
        dbhost = config.dbprod_host
        dbname = config.dbprod_name
        dbuser = config.dbprod_user
        dbpassword = config.dbprod_password
        dbport = config.dbprod_port
    else:
        dbhost = config.dbdev_host
        dbname = config.dbdev_name
        dbuser = config.dbdev_user
        dbpassword = config.dbdev_password
        dbport = config.dbdev_port

    conn = psycopg2.connect(
        dbname=dbname,
        user=dbuser,
        password=dbpassword,
        host=dbhost,
        port=dbport)

    return conn


def get_engine(db):
    """Create engine through SQL Alchemy.
    Args:
        db (str): Defines the environment that should be run. "dbprod" if we are using the production environment. "dbdev" otherwise.
    Returns:
        engine (???): Engine object.
    """
    if db == 'dbprod':
        dbhost = config.dbprod_host
        dbname = config.dbprod_name
        dbuser = config.dbprod_user
        dbpassword = config.dbprod_password
        dbport = config.dbprod_port
    else:
        dbhost = config.dbdev_host
        dbname = config.dbdev_name
        dbuser = config.dbdev_user
        dbpassword = config.dbdev_password
        dbport = config.dbdev_port

    engine = create_engine(
        f'postgresql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}')

    return engine


def read_table_to_df(engine, table_name):
    """Reads a table into a dataframe with a 'select *' query
    Input:
        connection: the database connection
        table_name: the name of the table in the database
    Returns:
        df (pandas Dataframe)
    """
    query = f"select * from {table_name};"

    with engine.begin() as connection:
        df = pd.read_sql_query(query, con=connection)

    return df


def write_df_to_table(df, engine, table_name, index=False):
    """Example function with types documented in the docstring.
    Long description.
    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.
    Returns:
        bool: The return value. True for success, False otherwise.
    """
    with engine.begin() as connection:
        df.to_sql(table_name, con=connection, if_exists="append", index=index)
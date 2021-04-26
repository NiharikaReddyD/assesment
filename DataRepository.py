import logging

from pandas import DataFrame
from sqlalchemy import create_engine


def insert_data(data: DataFrame, table_name: str, chunk_size: int):
    logging.info("Started inserting data into %s", table_name)
    logging.info("total data count %s", data.shape[0])
    engine = create_engine(
        "postgresql+psycopg2://postgres:password@kaleo.c8mvgqgndkqv.us-east-2.rds.amazonaws.com/interview")
    data.to_sql(table_name, engine, if_exists="append", index=False, chunksize=chunk_size)
    logging.info("Successfully inserted data into %s", table_name)

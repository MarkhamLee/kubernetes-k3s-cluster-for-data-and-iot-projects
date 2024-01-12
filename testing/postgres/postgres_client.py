# Markham Lee (C) 2023
# productivity-music-stocks-weather-IoT-dashboard
# https://github.com/MarkhamLee/productivity-music-stocks-weather-IoT-dashboard
# utilities for writing data to PostgreSQL

import psycopg2
from io import StringIO
from logging_util import logger


class PostgresUtilities():

    def __init__(self) -> None:
        pass

    @staticmethod
    def postgres_client(params: dict) -> object:

        # connect to DB
        try:
            conn = psycopg2.connect(**params)
            logger.info('PostgreSQL connection successful')

        except (Exception, psycopg2.DatabaseError) as error:
            logger.debug(f'connection to Postgres failed with error: {error}')
            return error

        return conn

    # strict enforcement of what columns are used ensures data quality
    # avoids issues where tab delimiting can create erroneous empty columns
    # in the data frame
    @staticmethod
    def prepare_payload(payload: object, columns: list) -> object:

        buffer = StringIO()

        # explicit column definitions + tab as the delimiter allow us to ingest
        # text data with punctuation  without having situations where a comma
        # in a sentence is treated as new column or causes a blank column to be
        # created.
        payload.to_csv(buffer, index=False, sep='\t', columns=columns,
                       header=False)
        buffer.seek(0)

        return buffer

    @staticmethod
    def clear_table(connection: object, table: str):

        try:
            # clear out table - for things like lists or alerts where we only
            # want the newest data
            delete_string = (f'DELETE FROM {table}')
            cursor = connection.cursor()

            cursor.execute(delete_string)
            connection.commit()
            return 0

        except (Exception, psycopg2.DatabaseError) as error:
            return error

    @staticmethod
    def write_data(connection: object, buffer: object, table: str):

        cursor = connection.cursor()

        try:
            cursor.copy_from(buffer, table, sep="\t")
            connection.commit()
            cursor.close()
            logger.info('Postgres write successful')
            return 0

        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            cursor.close()
            logger.debug(f'Postgres write unsucessful with error: {error}')
            return error

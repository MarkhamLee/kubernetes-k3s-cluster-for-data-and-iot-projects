# Markham Lee (C) 2023
# productivity-music-stocks-weather-IoT-dashboard
# https://github.com/MarkhamLee/productivity-music-stocks-weather-IoT-dashboard
# A test script that retrieves 5 cat facts from the cat facts API and then
# writes them to PostgreSQL, and then goes to sleep and then repeats
# the process 40 times to ensure there aren't any issues writing to Postgres.
# Just an easy way to test a a simple ETL pipeline + writing to Postgres
# without having to worry about rate limits and such.

import requests
import os
import time
import pandas as pd
from postgres_client import PostgresUtilities  # noqa: E402
from logging_util import logger


def get_cat_data():

    fact_list = []
    count = 0

    while count < 5:
        url = 'https://catfact.ninja/fact'
        headers = {}

        data = requests.get(url=url, headers=headers)
        data = data.json()

        fact = data['fact']

        fact_list.append(fact)

        count += 1

    return fact_list


def create_dataframe(data: list) -> object:

    # create blank dataframe
    df = pd.DataFrame(columns=['cat_fact'])
    df['cat_fact'] = data

    return df


def write_data(data: object):

    # Postgres DB connection data
    POSTGRES_TABLE = os.environ.get('CAT_TABLE')

    # instantiate Postgres writing class
    postgres_utilities = PostgresUtilities()

    param_dict = {
        "host": os.environ.get('DB_HOST'),
        "database": os.environ.get('DATABASE'),
        "port": int(os.environ.get('POSTGRES_PORT')),
        "user": os.environ.get('POSTGRES_USER'),
        "password": os.environ.get('POSTGRES_PASSWORD')

    }

    # get dataframe columns for managing data quality
    columns = list(data.columns)

    # get connection client
    connection = postgres_utilities.postgres_client(param_dict)

    # prepare payload
    buffer = postgres_utilities.prepare_payload(data, columns)

    # write data
    response = postgres_utilities.write_data(connection, buffer,
                                             POSTGRES_TABLE)

    return response


def main():

    # grab five cat facts every 15 minutes and then write them to the database

    count = 0

    while count < 40:

        logger.info('getting fact facts')

        # get data
        cat_data = get_cat_data()

        # get data frame
        df = create_dataframe(cat_data)

        # write data to Postgres
        response = write_data(df)  # noqa: F841

        count += 1

        if response == 0:
            logger.info('cat fact loop complete, sleeping...')

        else:
            logger.debug(f'Postgres write failed due to error: {response},\
                         halting tests')
            exit()

        time.sleep(900)

    logger.info('Postgres w/ Cat Facts testing complete')


if __name__ == '__main__':
    main()

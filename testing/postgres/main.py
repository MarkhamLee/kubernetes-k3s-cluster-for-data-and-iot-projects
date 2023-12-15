# Markham Lee (C) 2023
# productivity-music-stocks-weather-IoT-dashboard
# https://github.com/MarkhamLee/productivity-music-stocks-weather-IoT-dashboard
# A test script that retrieves 5 cat facts from the cat facts API and then
# writes them to PostgreSQL. Just an easy way to test writing to Postgres
# without having to worry about authentication or rate limits.

import requests
import os
import logging
import time
import pandas as pd
from postgres_client import PostgresUtilities  # noqa: E402

# create logger for logging errors, exceptions and the like
logging.basicConfig(filename='cat_test.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


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
    POSTGRES_TABLE = os.environ.get('cat_table')

    # instantiate Postgres writing class
    postgres_utilities = PostgresUtilities()

    param_dict = {
        "host": os.environ.get('DB_HOST'),
        "database": os.environ.get('cat_db'),
        "port": int(os.environ.get('POSTGRES_SANDBOX_PORT')),
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

        # get data
        cat_data = get_cat_data()

        # get data frame
        df = create_dataframe(cat_data)

        # write data to Postgres
        response = write_data(df)

        if response != 0:
            error_payload = {"error_response": response}
            logging.debug(f'db write error {error_payload}')

        count += 1
        time.sleep(900)


if __name__ == '__main__':
    main()

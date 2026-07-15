# This script uses the Technitium API to quickly load
# DHCP reservations from a CSV file.
import os
import requests
import pandas as pd


# load env vars
API_KEY = os.environ['TECHNITIUM_SECRET2']
SERVER_IP = os.environ['DNS2_SERVER_IP']
SERVER_PORT = int(os.environ['DNS1_SERVER_PORT'])


def load_dhcp_reservation_data(data_file: str):

    # Load data and convert to list of dicts to be
    reservation_data = pd.read_csv(data_file,
                                   usecols=range(3)).\
                                    map(lambda x: x.strip()
                                        if isinstance(x,
                                                      str) else x).to_dict(orient='records')  # noqa: E501

    return reservation_data


def build_add_dhcp_url(data, scope_name):

    url = (f'http://{SERVER_IP}:{SERVER_PORT}/api/dhcp/scopes/addReservedLease?token={API_KEY}&name={scope_name}&hostname={data['hostname']}&hardwareAddress={data['mac']}&ipAddress={data['ip']}')  # noqa: E501

    return url


def update_dhcp_reservations(reservation_data):

    for reservation in reservation_data:

        url = build_add_dhcp_url(reservation, 'Default')
        response = requests.post(url=url)

        status = response.json()['status']

        if status == 'ok':

            outcome_message = (f'DHCP reservation for {reservation['hostname']} was added with status: {status}')  # noqa: E501

        else:
            outcome_message = (f'Failed to add DHCP reservation for {reservation['hostname']} with status: {status}')  # noqa: E501

        print(outcome_message)


def main():

    # csv containing your MAC addresses, columns:
    # mac, ip, hostname
    data_file = 'static_ip_reservations.csv'

    # load data
    reservation_data = load_dhcp_reservation_data(data_file)

    # update static leases
    update_dhcp_reservations(reservation_data)


if __name__ == '__main__':
    main()

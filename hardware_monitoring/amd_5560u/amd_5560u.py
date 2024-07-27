# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# script to retrieve CPU related data on an AMD x86 machine
# and then write to InfluxDB
import json
import psutil


class AMD5560Data():

    def __init__(self):

        # get the # of cores, as we can use that to iterate through and
        # get things like current speed for all CPU cores
        self.core_count = psutil.cpu_count(logical=False)

    def build_payload(self, inputFunction, index=0):

        temp_dict = {}

        while self.core_count > index:

            data = inputFunction[index].current
            data = round(data, 1)
            key = (f'core {index}')
            temp_dict[key] = data
            index += 1

        payload = json.dumps(temp_dict)

        return payload

    # get average clock speed for all cores
    def get_freq(self, all_cpu=False):

        all_freq = psutil.cpu_freq(percpu=all_cpu)[0]
        all_freq = round(all_freq, 1)

        return all_freq, self.core_count

    # get frequency per core
    @staticmethod
    def freq_per_core(self, all_cpu=True):

        per_core_freq = self.buildPayload(psutil.cpu_freq(percpu=all_cpu))

        return per_core_freq

    # CPU load
    @staticmethod
    def get_cpu_data():

        cpu_util = (psutil.cpu_percent(interval=1))
        cpu_util = round(cpu_util, 1)

        return cpu_util

    # get current RAM used
    @staticmethod
    def get_ram_data():

        ram_use = (psutil.virtual_memory()[3]) / 1073741824
        ram_use = round(ram_use, 2)

        return ram_use

    @staticmethod
    def amd_linux_temp_data():

        nvme_temp = psutil.sensors_temperatures()['nvme'][0].current
        cpu_temp = psutil.sensors_temperatures()['k10temp'][0].current
        amdgpu_temp = psutil.sensors_temperatures()['amdgpu'][0].current

        return nvme_temp, cpu_temp, amdgpu_temp

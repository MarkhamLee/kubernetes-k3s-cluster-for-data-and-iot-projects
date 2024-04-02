# Markham Lee (C) 2023 - 2024
# kubernetes-k3s-data-and-IoT-Platform
# https://github.com/MarkhamLee/kubernetes-k3s-data-and-IoT-Platform
# Utility methods for pulling hardware monitoring data from a
# Raspberry Pi 4B.
import psutil


class Rpi4bData():

    def __init__(self):

        # get the # of cores, as we can use that to iterate through and
        # get things like current speed for all CPU cores
        self.coreCount = psutil.cpu_count(logical=False)

    # get average clock speed for all cores
    def get_freq(self, all_cpu=False):

        allFreq = psutil.cpu_freq(percpu=all_cpu)[0]
        allFreq = round(allFreq, 1)

        return allFreq, self.coreCount

    # CPU load/utilization
    def get_cpu_data(self):

        cpuUtil = (psutil.cpu_percent(interval=1))
        cpuUtil = round(cpuUtil, 1)

        return cpuUtil

    # get current RAM used
    def get_ram_data(self):

        ramUse = (psutil.virtual_memory()[3]) / 1073741824
        ramUse = round(ramUse, 2)

        return ramUse

    # get CPU temp for Raspberry Pi 4B
    @staticmethod
    def get_rpi4b_temps():

        rpi_cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current

        return rpi_cpu_temp

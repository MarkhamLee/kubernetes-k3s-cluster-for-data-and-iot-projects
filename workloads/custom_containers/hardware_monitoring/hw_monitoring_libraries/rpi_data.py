# Markham Lee (C) 2025
# Homelab & Self Hosting Toolkit
# https://github.com/MarkhamLee/kubernetes-k3s-data-and-IoT-Platform
# Utility methods for pulling hardware monitoring data from a
# Raspberry Pi. The NVME has only been tested on a RPI5.
import psutil


class RpiData():

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

    # get load average over the last 5, 15 minutes
    def get_load_average(self):

        load_tuple = psutil.getloadavg()

        five_minute_average = round((load_tuple[1] * self.coreCount), 2)
        fifteen_minute_average = round((load_tuple[2] * self.coreCount), 2)

        return five_minute_average, fifteen_minute_average

    # get internet connection data
    def ethernet_data(self, interface_name):

        # commenting out because if connectivity is lost Prometheus
        # will pick it up and/or no data will come in.
        # status = psutil.net_if_stats()['eth0'].isup
        speed = psutil.net_if_stats()[interface_name].speed

        return speed

    def get_cpu_temps(self):

        rpi_cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current

        return rpi_cpu_temp

    # get NVME temp
    def get_nvme_temps(self):

        rpi_cpu_temp = psutil.sensors_temperatures()['nvme'][0].current

        return rpi_cpu_temp

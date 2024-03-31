# Markham Lee (C) 2023
# https://github.com/MarkhamLee/productivity-music-stocks-weather-IoT-dashboard
# methods for retrieving data from a Raspberry Pis CPU, GPU sensors, et al,
# plus utility scripts for MQTT: MQTT client and generating unique client
# IDs
import psutil


class Rpi4bData():

    def __init__(self):

        # get the # of cores, as we can use that to iterate through and
        # get things like current speed for all CPU cores
        self.coreCount = psutil.cpu_count(logical=False)

    # get average clock speed for all cores
    def getFreq(self, all_cpu=False):

        allFreq = psutil.cpu_freq(percpu=all_cpu)[0]
        allFreq = round(allFreq, 1)

        return allFreq, self.coreCount

    # CPU load/utilization
    def getCPUData(self):

        cpuUtil = (psutil.cpu_percent(interval=1))
        cpuUtil = round(cpuUtil, 1)

        return cpuUtil

    # get current RAM used
    def getRamData(self):

        ramUse = (psutil.virtual_memory()[3]) / 1073741824
        ramUse = round(ramUse, 2)

        return ramUse

    # get CPU temp for Raspberry Pi 4B
    @staticmethod
    def get_rpi4b_temps():

        rpi_cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current

        return rpi_cpu_temp

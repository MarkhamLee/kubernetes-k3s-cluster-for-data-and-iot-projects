
### Hardware Dashboard

This is used to monitor all of my "homelab" devices + power consumption of my Gaming PC. The reason for the extra monitoring is that my prometheus setup doesn't monitor temps and to give me insight into actual CPU and RAM usage vs the "potential" numbers shown via k8s monitoring.

* All 7 K3s Nodes: monitoring CPU temps for all, CPU & RAM utilization for the single board computers (E.g., Raspberry Pis)
* **Total Power Consumption for the following:** 
    * K3s Nodes
    * Beta Server (Beelink N95 Mini PC)
    * Firewall Server (N100 Mini PC)
    * All network switches: 16 port and an 8 port, both with POE
    * Primary dev box: 12th Gen Intel NUC
    * Music Server: 11th Gen Intel NUC running [Roon Optimized Core Kit](https://help.roonlabs.com/portal/en/kb/articles/roon-optimized-core-kit#So_what_is_Roon_Optimized_Core_Kit_ROCK_then), Roon's music server software that allows you to turn a Intel NUC (nearly any x86 machine, but your mileage will vary if it's not an Intel NUC) into a dedicated network appliance for music.
    * Gigabit broadband modem 
* For context: my primary gaming PC with an 12th Gen 12700k + a 3090TI pulls about 130 watts at idle, and my 11th Gen i5/3060TI desktop pulls about 145 watts at idle. Meaning: Six Intel NUC style Mini PCs + four single board computers, 7 of which are active parts of a Kubernetes cluster, only pull about 30-40 more watts than a gaming desktop.

* Cost is calculated base on average kilowatt hours X average cost of electricity in Seattle + 10%.
* My Gaming PC was "asleep" when this screenshot was taken, so just the cost to have it at idle + the tiny bit of power the PC case temperature sensors I have running on a Raspberry Pi Pico microcontroller uses. 

![HW Monitor #1](images/hw_mon1.png)



![HW Monitor #2](images/hw_mon2.png)
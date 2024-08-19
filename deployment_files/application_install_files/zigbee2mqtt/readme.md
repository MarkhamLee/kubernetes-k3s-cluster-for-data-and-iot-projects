## Instructions for deploying Zigbee2MQTT on Kubernetes 

Deploying Zigbee2MQTT on Kubernetes can be bit tricky due to the dependency on the external device, and a couple of extra steps you need to take to override the container's default settings. However, if you follow the instructions below you shouldn't run into any issues. Just keep in mind that if the service continually fails to start up, it's likely a MQTT issue or an issue with the device address.

### Quick Deployment via Argo CD

* Read through the [device configuration instructions](configuring_usb_dongle.md) to set up your Zigbee USB dongle
* Look through the values.yaml file and configure the secrets, config maps and the like per the settings on your K8s cluster. The section below has a detailed look at how to set up the values.yaml file properly.
* Update the values.yaml file with the name of the node that the USB dongle will be connected to
* Drop the values.yaml into a folder on GitHub and then point Argo CD towards it. 

### General Deployment

The values.yaml file in this folder is largely influenced by what I found [here](https://github.com/Koenkk/zigbee2mqtt/discussions/10899), but I had to make a couple of changes to get everything to work properly:  

I was having issues with values defined in the values.yaml or config map being ignored in favor of the configuration.yaml file baked into the image. E.g., putting the path to my Zigbee dongle in the values.yaml file was always ignored file in favor of the path given in the container's config: /dev/ACM0, which is fine if your device is at ACM0, but if it isn't. 

To get around this I followed the instructions on the Zigbee2mqtt web site to override those values by adding environmental variables to the values.yaml file. The best approach is to add a config map to the namespace you're deploying Zigbee2MQTT in, and then reference those values in the values.yaml file. See below for the format to override the values in configuration.yaml file via environmental variables, chances are, if this deployment is failing it's a device or config data issue.

    ~~~
    config:
        serial:
            port:
    ~~~
    becomes:
    ~~~
    ZIGBEE2MQTT_CONFIG_SERIAL_PORT
        value: <path/to/your/USB/device>
    ~~~
* I also added environmental variables for connecting to my MQTT broker and for Zigbee2MQTT's base topic. 
    * Zigbee2MQTT will send data to base topic + device name. So if your base topic is /iot and the name of a device is "garage_temp" it will send that device's data to the /iot/garage_temp MQTT topic. Keep in mind that you can't change the base topic within the app itself even though it looks editable in settings, it will always revert back to what's in the config file. So, just define it via environmental variables as part of the deployment. 
* I added a node name for the node that has the USB dongle attached. I.e., you need to explicitly   define the node, so the pod for this app doesn't get deployed on a node that the dongle isn't plugged into. 
    * You can get around this limitation by using something like ser2net to allow you to effectively stream your USB device over your network/make it available over tcp. E.g., you could plug your Zigbee dongle into a Raspberry Pi 3B or Zero, use the TCP address as the serial port path and now your Zigbee2MQTT deployment isn't tied to a specifc node. I've never tried it, but the instructions for it are [here](https://www.zigbee2mqtt.io/advanced/remote-adapter/connect_to_a_remote_adapter.html)
    * Similarly there are USB network devices that perform the same function as above only with simpler configuration steps, you plug the USB device into the network device and now other devices in your network can receive data from it. If you search usb over tcp/ip on Amazon or Newegg, you can find them for for around $50-$70.00. For the record I've never tried it, but it's on my list. 
* I added resource limits so linting doesn't scream at you + just a good practice. 

Once you have everything configured for your environment, drop the values.yaml file into a folder on GitHub, point Argo CD towards it and you should be good to go.

### Critical step once you deploy the application

The default for Zigbee2MQTT is to log EVERYTHING, meaning every single time it receives data from any of your devices it will update the log file with the values from that device. Even if you only have a dozen or so devices it won't take long before you use up your container's allocated space for logs (the mount for /data), and then the container will crash. To avoid this: go to settings --> advanced --> Log level and set it to "warn" at minimum, so the service is only logging things you need to troubleshoot or address problems. 

If your container crashes due to this issue you'll get an "out of space" error, and the path to fixing it is just manually increasing the size of persistent volume claim via Longhorn (or whatever you use for storage), once the container crashes it will be too late to fix it in the values.yaml file, because the the container won't be able to spin up and increase the size of the volume claim. 

FTR, I looked for a setting or config for deleting old logs but couldn't find anything, my plan is to keep looking and if I don't find anything either build a fix myself and/or raise it as an issue. 

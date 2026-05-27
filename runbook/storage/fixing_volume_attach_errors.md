## Storage Tips & Tricks

Kubernetes storage can be tricky, putting some notes here on how to resolve some thorny issues that can pop up from time to time. 


### Volume Attachment Errors 

When redeploying an app after making config changes, updating the version, etc., I would sometimes get an error like the following:

~~~
MountVolume.MountDevice failed for volume "cluster-app-media" : rpc error: code = Internal desc = mount failed: exit status 32 Mounting command: mount Mounting arguments: -t ext4 -o defaults /dev/longhorn/cluster-app-media /var/lib/kubelet/plugins/kubernetes.io/csi/driver.longhorn.io/<redacted UID>/globalmount Output: mount: /var/lib/kubelet/plugins/kubernetes.io/csi/driver.longhorn.io/<redacted UID>/globalmount: /dev/longhorn/cluster-app-media already mounted or mount point busy. dmesg(1) may have more information after failed mount system call.
~~~

I would just redeploy the workload a few times and the issue would resolve itself, well after a recent occurrence I decided to dig into a bit more and discovered it only occurred on two headless Ubuntu worker nodes (rest are running Desktop). The issue was related to a configuration on the node itself that was causing it to "take ownership" of the Longhorn volume, and was preventing the volume from attaching. Fixing it was simple 

Edit the config file, if you run the command below and it's empty than don't worry about it, I've only had this problem when workloads were deployed to nodes that had this config.

~~~

nano /etc/multipath.conf 

~~~

Once in that file, you'll likely see something like this:


~~~

defaults {
  user_friendly_names yes
}

blacklist {
  devnode "^sd[a-z0-9]+"
}


~~~

Update it so it looks like the below, this will ensure that the node doesn't take control of the Longhorn volume.

~~~

blacklist {
    devnode "^sd[a-z0-9]+"
    devnode "^nvme[a-z0-9]+"
    devnode "^longhorn.*"
}

~~~

Restart the multipath service

~~~

sudo systemctl restart multipathd.service

~~~

That should clear the issue up. 
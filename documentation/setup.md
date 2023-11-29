
## Basic setup with Ansible 

* Honestly, just use [Techno Tim's playbook for the basic setup](https://www.youtube.com/watch?v=CbkEWcUZ7zM&t=316s), you'll save yourself a LOT of headaches, plus learning ansible will payoff later on. 

#### A couple of tricks to make it go smoother after you've cloned Tim's repo but BEFORE you run any commands: 

##### Preparing your environment to run the playbook: 
* Make sure you have an up to date version of python installed, including pip and virtual environments. 
* Install Ansible on your machine but make sure you follow this process, as chances are your Linux distro installed an older one. This is the process I followed:
    * Check your Ansible version the instructions say at least 2.11, FWIW I had 2.16 installed on mine. If you're above 2.11, you're good, if not, follow the next step(s):
    * Remove the old version: 
        * sudo apt remove ansible 
        * sudo apt --purge autoremove 
    * sudo apt update 
    * sudo apt upgrade
    * Run the following commands to install PPA support + add teh ansible repo
        * sudo apt -y install software-properties-common
        * sudo apt-add-repository ppa:ansible/ansible
    * Install ansible: sudo apt install ansible 
* Create a python virtual environment and install Ansible directly into it:
    * python3 -m pip install ansible
* You may or may not get an netaddr error, so you go ahead and install that into your virtual environment. 
* Now install the requirements.txt file that came with the repo into your virtual environment
* **Optional Steps:**
    * You'll need some additional server arguments to get things setup to fully use monitoring, see them below. I got these from Tim's Video on setting up the graphs, using his server arguments when you first get things setup will just make things easier. Also, I didn't use his instructions and instead used the built in monitoring package in Rancher, as that worked better for me, but your mileage may vary. 
    

##### Preparing your hardware 
* Make sure you turn off swap on all your devices
* On the device you're going to run the playbook from set that one up for passwordless SSH with itself. I know it sounds goofy, but it can hang otherwise as Ansible connects to the host via SSH. FTR it will often just connect and run fine, but if it doesn't.. 

##### Other Tips 
* The playbook is solid, at least it has been for me, chances are if you run into some issues it's with your ansible installation: 
* If you get a jinja error noting a filter isn't available, you're using an older version of ansible and that's likely from your Linux distro intalling an older one - see the instructions for updating Ansible version above  
* If the script runs and won't connect, doublecheck your server arguments, I'd copy and paste the original ones from the repo and see if those work... don't ask how I know. 


#### Post Setup 
* To add a node just update your hosts file with the IP address for the new node after getting it setup, the setup process will ignore the existing nodes and just setup the new ones. I would experiment with building things up, resetting and building again, adding nodes, removing them, etc., and getting really comfortable with that before you go further. 


## Things I wish I picked up sooner    
* Your certificates are at the namespace level. So if something in namespace xyz needs a cert, you need to generate one in that namespace. 
* The above being said, your ingress has a secure cert and you're using wildcard certs so you SHOULD be okay if you just setup the ingress. This appears to be working for me, but again, mileage varies. 
* In keeping with the above, SOME apps/services you can just give it the ingress class and the email you used with cloudflare and it will do the rest (see Rancher) others, not so much. 



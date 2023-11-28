
## Basic setup with Ansible 

* Honestly, just use [Techno Tim's playbook for the basic setup](https://www.youtube.com/watch?v=CbkEWcUZ7zM&t=316s), you'll save yourself a LOT of headaches, plus learning ansible will payoff later on. 

A couple of tricks to make it go smoother:
* Make sure you turn off swap on all your devices
* On the device you're going to run the playbook from set that one up for passwordless SSH with itself. I know it sounds goofy, but it can hang otherwise as Ansible connects to the host via SSH. FTR it will often just connect and run fine, but if it doesn't.. 
* If you get a jinja error noting a filter isn't available, you're using an older version of ansible, upgrade it
* I created a virtual environment and then installed the requirements.txt file on the first set of machines I tried the playbook this wasn't an issue, but on the second, some of the python libraries got installed in weird places, creating the virtual environments removed this issue. 
* If the script runs and won't connect, doublecheck your server arguments, I'd copy and paste the original ones from the repo and see if those work... don't ask how I know. 


## Post Setup - Things I wish I picked up sooner    
* Your certificates are at the namespace level. So if something in namespace xyz needs a cert, you need to generate one in that namespace. 
* In keeping with the above, SOME apps/services you can just give it the ingress source and the email you used with cloudflare and it will do the rest (see Rancher) others, not so much. 



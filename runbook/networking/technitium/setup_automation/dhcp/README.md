## DHCP Reservation Automation

The Python script and the csv file are examples of how you could add DHCP reservations to your Technitium instance via the API. A couple of notes:

* You'll need to create an API key within the Technitium UI 
* Using this approach will over-write existing reservations, so for on-going maintenance it might be smart to only have new reservations in the file and/or create a process where you check for the existence of an existing reservation for a particular MAC address before you upload it. 



## A couple of preparation steps before getting started with encryption
* Setup a custom router, any used computer will do, but ideally you'd get something with dual NICs. I used a small form factor PC with Dual NICs (Trigkey G5 w/ Intel N100) and  it works great, but I sometimes think I should've gotten a firewall appliances with 4-6 LAN ports instead. 
* Make sure you know how to create local domains (or host overrides) on your local network 
* Create a CloudFlare account and setup a local domain if you want to go the full encryption route 



### Setting up your cluster with secure certificates

* The simple answer is to just follow [Tim's tutorial](https://www.youtube.com/watch?v=G4CmbYL9UPg&t=1344s), but with a couple of extra points that should make your life easier: 
    * When looking at the traefik dashboard, the full URL will be something like: traefik.local.example.com/dashboard/ make sure you have the /dashboard/ after your URL or you'll get a 404 message. 
    * If the above doesn't work, go back a few steps and just do them over, it's a lot of information to work through and it's easy to miss a step. 
    * 404 messages aren't actually bad, they mean you're hitting the right service, but you've made a small error in your URL somewhere 
    
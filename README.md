# bible-verse
 $env:FLASK_APP = "app/main.py"
 flask run --host=0.0.0.0      
 On Ubuntu, the easiest way to save iptables rules, so they will survive a reboot, is to use the iptables-persistent package. Install it with apt-get like this:

 
sudo apt-get install iptables-persistent
During the installation, you will asked if you want to save your current firewall rules.

If you update your firewall rules and want to save the changes, run this command:

 
sudo invoke-rc.d iptables-persistent save



gunicorn -b 0.0.0.0:8000 main:app //local testing
tail -f /var/log/nginx/access.log //log
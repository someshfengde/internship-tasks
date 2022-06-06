# create ssh connection with access point 
#%% 
from ipaddress import ip_address
import paramiko

def ssh_connection(ip_address, username, password):
    """
    create ssh connection with access point 
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)
    return ssh

ip_address = "172.31.254.125"
username = 'root'
password = "openwifi"

connect = ssh_connection(ip_address, username, password)
# %%

# # create ssh connection with access point 
# #%% 
# from ipaddress import ip_address
# import paramiko

# def ssh_connection(ip_address, username, password):
#     """
#     create ssh connection with access point 
#     """
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(ip_address, username=username, password=password)
#     return ssh

# ip_address = "172.31.254.125"
# username = 'root'
# password = "openwifi"

# connect = ssh_connection(ip_address, username, password)
# # %%


import pexpect
import sys
ch=pexpect.spawn('ssh root@172.31.254.193')
ch.logfile=sys.stdout.buffer
print('1st successful')
ch.expect('password:')
ch.sendline('openwifi')
print('2nd succesful')
ch.expect('#')
ch.sendline('ifconfig')
print('command 3 successful')
print()
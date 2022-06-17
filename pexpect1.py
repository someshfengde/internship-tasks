import pexpect
import sys
import time
import paramiko


ch = pexpect.spawn("ssh -o StrictHostKeyChecking=no root@172.31.254.231")
ch.logfile = sys.stdout.buffer
print("1st successful")
ch.expect("password:")
ch.sendline("openwifi")
print("2nd succesful")
ch.expect("#")
ch.sendline("ifconfig")
print("command 3 successful")
ch.expect("#")
ch.sendline("cd /tmp")
ch.expect("/tmp#")
ch.sendline(
    "wget https://ucentral-ap-firmware.s3.amazonaws.com/20220202-indio_um-305ac-v2.4.1-6d9d4ab-upgrade.bin"
)
ch.expect("#")
print("downloading completed")

#%%

import pssh
def print_output(output):
    for host_out in output:
        for line in host_out.stdout:
            print(line)
from pssh.clients import ParallelSSHClient
client = ParallelSSHClient(['10.0.21.1'],port=2233, user='root', password='w1f1s0ft123#')
output=client.run_command('arp -a')
print_output(output)
res=client.run_command('ls')
print_output(res)
# %%
import subprocess

# Traverse the ipconfig information
data = subprocess.check_output(['arp',' -a']).decode('utf-8').split('\n')

# Arrange the bytes data
for item in data:
    print(item.split('\r')[:-1])
# %%

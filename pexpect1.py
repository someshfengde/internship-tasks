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

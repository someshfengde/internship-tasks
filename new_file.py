#%%
from flask import has_app_context
from pssh.clients import ParallelSSHClient
import hashlib
import os
import sys
import time
import paramiko
import pexpect


def print_output(output):
    for host_out in output:
        for line in host_out.stdout:
            print(line)

    print("----------")


#%%

# write a function to calculate the message digest of a file using the SHA-256 algorithm
def calc_digest(filename):
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# write a function to verify digest using sha256 algorithm
def verify_digest(filename, digest):
    return calc_digest(filename) == digest


def command_to_aps(ip_list, user="root", password="openwifi"):
    client = ParallelSSHClient(ip_list, user=user, password=password)
    output = client.run_command("uname")
    print_output(output)
    output = client.run_command("ifconfig")
    print_output(output)
    out = client.run_command("cd /tmp")
    out = client.run_command("ls")
    print_output(out)
    dp = client.run_command(
        "cd /tmp && wget --timeout=900 https://ucentral-ap-firmware.s3.amazonaws.com/20220202-indio_um-305ac-v2.4.1-6d9d4ab-upgrade.bin"
    )
    print_output(dp)
    output = client.run_command("ls")
    print_output(output)
    hash_val = get_hash_from_server(client)
    for idx, x in enumerate(hash_val):
        if verify_digest(
            filename="/home/somesh/Downloads/20220202-indio_um-305ac-v2.4.1-6d9d4ab-upgrade.bin",
            digest=x,
        ):
            print(f"{ip_list[idx]} is authenticated")
            print("file is verified for integrity")
        else:
            client.run_command(
                "rm -rf 20220202-indio_um-305ac-v2.4.1-6d9d4ab-upgrade.bin"
            )
            # command_to_aps(ip_list,user = "root" , password ="openwifi")
            print(f"{ip_list[idx]} is not authenticated")
            print("RETRY SENDING FILE!")


def get_hash_from_server(
    client, filename="20220202-indio_um-305ac-v2.4.1-6d9d4ab-upgrade.bin"
):
    output = client.run_command("cd /tmp && sha256sum " + filename)
    # print_output(output)
    hash_values = []
    for host_out in output:
        for line in host_out.stdout:
            hash_values.append(line.split(" ")[0])
            break
    print(hash_values)
    return hash_values


# %%

# command_to_aps(ip_list,user = "root" , password ="openwifi")

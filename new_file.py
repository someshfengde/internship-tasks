#%% 
from pssh.clients import ParallelSSHClient
hosts = ["172.31.255.155", "172.31.255.125"]

client = ParallelSSHClient(hosts, user = "root" , password = "openwifi")
#%%
output = client.run_command("uname")
for host_out in output:
    for line in host_out.stdout:
        print(line)

print("----------")

# %%
op = client.run_command("ifconfig")

# %%
for host_out in op:
    for line in host_out.stdout:
        print(line)
    print("--------------------------")
# %%

dp = client.run_command("wget https://ucentral-ap-firmware.s3.amazonaws.com/20220202-indio_um-305ac-v2.4.1-6d9d4ab-upgrade.bin")

# for host_out in dp:
#     for line in host_out.stdout:
#         print(line)
#     print("--------------------------")
# %%

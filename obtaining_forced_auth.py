#%% 
from ipaddress import ip_address
import requests
import pandas as pd 
from new_file import * 


mac_ids = ["72-6D-EC-0A-27-48","72-6D-EC-0A-2E-B8"]#,,"70-6D-EC-0A-80-AC"
# we will get JSON data through API 
# search mac_ids in JSON data 
def ip_addresses_through_mac(mac_ids):
    """
        we will get JSON data through API 
    """
    response = requests.get('http://172.31.254.1/unibox/tools/getForceAuthData.php?', verify=False)
    JSON_data = response.json()
    df = pd.DataFrame(JSON_data['data'])
    ip_addresses= []
    for x in mac_ids:
        successful = False
        try:
            ip_addresses.append(df[df['mac'] == x ]['ip'].to_numpy()[0])
            successful = True
        except:
            pass
        if not successful:
            print(f"MAC {x} is not authenticated! Authenticate and try")

    return ip_addresses
ip_address = ip_addresses_through_mac(mac_ids)
# %%
print(ip_address)
#%%
command_to_aps(ip_address)
#%%

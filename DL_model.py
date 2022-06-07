#%% 
import torch 
import pandas as pd 
import numpy as np 

# reading in the data from the csv file
scan_1 = pd.read_csv("nap-scan.csv")
scan_2 = pd.read_csv("nap-scan-2.csv")
cols = ["ApId",
"NApMacAddress",
"LastCheckinTime",
"LastStatusId",         
"SSID",                 
"TSF",                  
"Frequency",            
"Rssi",                  
"PrimaryChannel",       
"SecondaryChannel",     
"ChannelWidth",         
"StaChannelWidth",      
"FirstCenterFrequency", 
"SecondCenterFrequency",
"Authentication",       
"Security"]
scan_1.columns = cols
# checking the column 
print(scan_2[r'\N'].value_counts(), len(scan_2[r'\N']))
# seems like the \N col is having only newline values dropping it 
scan_2 = scan_2.drop(r"\N", axis = 1 ) 
scan_2.columns = cols
total_scan = scan_1.append(scan_2, ignore_index=True)
#%%

class NewApproach(torch.nn.Module):
    def __init__(self):
        super(NewApproach, self).__init__()
        self.conv1 = torch.nn.Conv1d(1, 32, 3, padding=1)
        self.conv2 = torch.nn.Conv1d(32, 64, 3, padding=1)
        self.gru = torch.nn.LSTM(64, 64, num_layers=2, bidirectional=True)
        self.output = torch.nn.Linear(64, 1, )
    
    def forward(self, x):
        x = self.conv1(x)
        x = torch.nn.functional.relu(x)
        x = self.conv2(x)
        x = torch.nn.functional.relu(x)
        x = x.transpose(1, 2)
        x, _ = self.gru(x)
        x = x.transpose(1, 2)
        x = self.output(x)
        return x


# %%
# creating the dataset for loading csv files and creating the dataset
class Dataset(torch.utils.data.Dataset):
    def __init__(self, df, unique_ids):
        self.df = df
        self.unique_ids = unique_ids

    def __len__(self):
        return len(self.unique_ids)
     
    def __getitem__(self, idx):
        id = self.unique_ids[idx]
        data = self.df.query(f"ApId == {str(id)}")
        channel = data["PrimaryChannel"].to_numpy()
        data = data[["Rssi","ChannelWidth"]].to_numpy()
        if data.shape[0] < 42:
            data = np.append(data,np.zeros((42-len(data),2)),axis =2 )
            channel = np.append(channel, np.zeros((42-len(channel))))
        elif data.shape[0] > 42:
            data = data[:42]
            channel = channel[:42]
        return data , channel

ds = Dataset(total_scan, total_scan["ApId"].unique())# %%
dl = torch.utils.data.DataLoader(ds, batch_size = 32 , shuffle = True)
# %%
for idx,x in enumerate(ds):
    print(x)
    if idx == 10:
        break
# %%

# %%

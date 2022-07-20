
# Info about the repo: 
> This is repo I've created to mangae the tasks I've done in my internship at Indio Networks 

<!-- ## **Overview of the tasks:** -->

## Dash application for visualizing Mysql data
This is in progress application I'm creating this application for visualizing various columns in our organizations database. 

**Main feaatures of this application:** 

* End to End database connectivity
* Interactive graphs with plotly 
* Ability to visualize multiple tables in multiple databases 
* Customizable graphs
* URL to application can be shared with other people.


> requirements are listed in `requiremetns.txt` file.


**for installation of the required libraries** 
```
# make sure you are in same directory as this file
pip install -r requirements.txt
```
 
some more requirements for running this project:

1. mysql server installed on the machine 
2. The datatable used for this visualizations is ap_status_rf_clients under new_database 
3. the database dump file is included in the repo i.e ap_status_rfclientsdump.sql
----------------------------------------------------
## `ap_channel_allocation.py`
I've developed this script which helps to optimize the random channel allocation happening in access points. This script also  contains code for visualizing the channel allocated to different access points. For seperate code for visualization please see  `net_vis.py`
I've optimized channel for minimizing the interference between access points at the same time using as minimum channels for allocation as possible. 

-----------------------------------------------------

## SSH access with python: 
* In this task i've tried to connect access points and upgrading the access points firmwawre with help of shell commands in python 

## April 2022: 
* visualized, created models, curated data for predicting channel allocation based on RF frequency and ChannelWidth
* the folder contains files for 
    * data processsing 
    * EDA notebook 
    * Model building with Pycaret 
    * Saved model for decision trees 


import os
import time
import json
import requests
import sqlite3
import math
from decimal import Decimal
import numpy as np
import datetime
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pytz     #for getting current

#for current IST Time because of diffrent time zone VM
IST_start_time = "06:00:00"
IST_end_time = "06:00:00"
timeZone = pytz.timezone('Asia/Kolkata')
IST_now = datetime.now().astimezone(timeZone)
IST_today_date = IST_now.strftime("%Y-%m-%d")
IST_previous_date = IST_now - timedelta(days=1)
IST_previous_date = IST_previous_date.strftime("%Y-%m-%d")

#for current IST Time because of diffrent time zone VM
timeZone = pytz.timezone('Asia/Kolkata')
today_date = datetime.now().astimezone(timeZone)
today_date = today_date.strftime("%d %b %Y")
today_date

PATH = ""
sla_target = "90.00%"

P1 = "1 - Critical"
P2 = "2 - High"
P3 = "3 - Moderate"
P4 = "4 - Low"
P5 = "5 - Planning"

"""# for changing IST to GMT for API Calling"""

previous_timestamp = datetime.strptime(IST_previous_date+" "+IST_start_time, "%Y-%m-%d %H:%M:%S")
today_timestamp = datetime.strptime(IST_today_date+" "+IST_end_time, "%Y-%m-%d %H:%M:%S")
old_timezone = pytz.timezone("Asia/Kolkata")
new_timezone = pytz.timezone("Etc/GMT")

# returns previous datetime in the new timezone
previous_timestamp_in_new_timezone = old_timezone.localize(previous_timestamp).astimezone(new_timezone)
previous_timestamp_in_new_timezone = previous_timestamp_in_new_timezone.strftime(str(previous_timestamp_in_new_timezone))
previous_timestamp_in_new_timezone = previous_timestamp_in_new_timezone.split("+")[0]

# returns today's datetime in the new timezone
today_timestamp_in_new_timezone = old_timezone.localize(today_timestamp).astimezone(new_timezone)
today_timestamp_in_new_timezone = today_timestamp_in_new_timezone.strftime(str(today_timestamp_in_new_timezone))
today_timestamp_in_new_timezone = today_timestamp_in_new_timezone.split("+")[0]

api_previous_date = previous_timestamp_in_new_timezone.split(" ")[0]
api_previous_time = previous_timestamp_in_new_timezone.split(" ")[1]
api_today_date = today_timestamp_in_new_timezone.split(" ")[0]
api_today_time = today_timestamp_in_new_timezone.split(" ")[1]



"""# Calling API with dynamic sysparms including between and operator"""

USERNAME = 'username'
PASSWORD = '*************'
API_URL = """https://your-instance.service-now.com/api/now/table/incident?sysparm_display_value=all&sysparm_query=assignment_group=ca1e0ef5db510b00b90b7b6b8c961942^parent_incidentISEMPTY^stateIN7,6^u_resolution_category=Support Resolution^close_code!=Release^resolved_atBETWEENjavascript:gs.dateGenerate('"""+api_previous_date+"""','"""+api_previous_time+"""')@javascript:gs.dateGenerate('"""+api_today_date+"""','"""+api_today_time+"""')^cmdb_ci.u_service_offeringISNOTEMPTY"""
api = requests.get(API_URL, auth=(USERNAME, PASSWORD))
api = api.json()

#storing all incident in one list and onhold reason
incident_list = []
if(api['result'] != []):
    for i in range(len(api['result'])):
        incident_list.append(api['result'][i]['number']['display_value'])



"""# RESPONSE SLA TABLE FOR MAIL"""

#variable for different priority

#all priority total incidents
p1_total = 0
p2_total = 0
p3_total = 0
p4_total = 0
p5_total = 0
#for Response SLA
p1_response_sla_met_count = 0
p2_response_sla_met_count = 0
p3_response_sla_met_count = 0
p4_response_sla_met_count = 0
p5_response_sla_met_count = 0
#----------------------------------
p1_response_sla_breach_count = 0
p2_response_sla_breach_count = 0
p3_response_sla_breach_count = 0
p4_response_sla_breach_count = 0
p5_response_sla_breach_count = 0

#for Resolution SLA

p1_resolution_sla_met_count = 0
p2_resolution_sla_met_count = 0
p3_resolution_sla_met_count = 0
p4_resolution_sla_met_count = 0
p5_resolution_sla_met_count = 0
#----------------------------------------
p1_resolution_sla_breach_count = 0
p2_resolution_sla_breach_count = 0
p3_resolution_sla_breach_count = 0
p4_resolution_sla_breach_count = 0
p5_resolution_sla_breach_count = 0

if(api['result'] != []):
    
    for i in range(len(api['result'])):
        incident_priority = api['result'][i]['priority']['display_value']
        response_sla_breach = str(api['result'][i]['u_response_sla_breach']['value'])
        resolution_sla_breach = str(api['result'][i]['u_sla_breach']['value'])
        
        if(incident_priority == '1 - Critical'):
            p1_total += 1
            if(response_sla_breach == 'true'):
                p1_response_sla_breach_count += 1
            elif(response_sla_breach == 'false'):
                p1_response_sla_met_count += 1
                
            if(resolution_sla_breach == 'true'):
                p1_resolution_sla_breach_count += 1
            elif(resolution_sla_breach == 'false'):
                p1_resolution_sla_met_count += 1
        
        elif(incident_priority == '2 - High'):
            p2_total += 1
            if(response_sla_breach == 'true'):
                p2_response_sla_breach_count += 1
            elif(response_sla_breach == 'false'):
                p2_response_sla_met_count+= 1
                
            if(resolution_sla_breach == 'true'):
                p2_resolution_sla_breach_count+= 1
            elif(resolution_sla_breach == 'false'):
                p2_resolution_sla_met_count+= 1
        
        elif(incident_priority == '3 - Moderate'):
            p3_total += 1
            if(response_sla_breach == 'true'):
                p3_response_sla_breach_count+= 1
            elif(response_sla_breach == 'false'):
                p3_response_sla_met_count+= 1
                
            if(resolution_sla_breach == 'true'):
                p3_resolution_sla_breach_count+= 1
            elif(resolution_sla_breach == 'false'):
                p3_resolution_sla_met_count+= 1
        
        elif(incident_priority == '4 - Low'):
            p4_total += 1
            if(response_sla_breach == 'true'):
                p4_response_sla_breach_count+= 1
            elif(response_sla_breach == 'false'):
                p4_response_sla_met_count+= 1
                
            if(resolution_sla_breach == 'true'):
                p4_resolution_sla_breach_count+= 1
            elif(resolution_sla_breach == 'false'):
                p4_resolution_sla_met_count+= 1
        
        elif(incident_priority == '5 - Planning'):
            p5_total += 1
            if(response_sla_breach == 'true'):
                p5_response_sla_breach_count+= 1
            elif(response_sla_breach == 'false'):
                p5_response_sla_met_count+= 1
                
            if(resolution_sla_breach == 'true'):
                p5_resolution_sla_breach_count+= 1
            elif(resolution_sla_breach == 'false'):
                p5_resolution_sla_met_count+= 1





#for calculating Response SLA Met Percentage
p1_response_sla_met_percent = 100
p2_response_sla_met_percent = 100
p3_response_sla_met_percent = 100
p4_response_sla_met_percent = 100
p5_response_sla_met_percent = 100

if(p1_total != 0):
    p1_response_sla_met_percent = round(abs((p1_response_sla_met_count/p1_total)*100), 2)
    p1_response_sla_met_percent = p1_response_sla_met_percent

if(p2_total != 0):
    p2_response_sla_met_percent = round(abs((p2_response_sla_met_count/p2_total)*100), 2)
    p2_response_sla_met_percent = p2_response_sla_met_percent

if(p3_total != 0):
    p3_response_sla_met_percent = round(abs((p3_response_sla_met_count/p3_total)*100), 2)
    p3_response_sla_met_percent = p3_response_sla_met_percent

if(p4_total != 0):
    p4_response_sla_met_percent = round(abs((p4_response_sla_met_count/p4_total)*100), 2)
    p4_response_sla_met_percent = p4_response_sla_met_percent

if(p5_total != 0):
    p5_response_sla_met_percent = round(abs((p5_response_sla_met_count/p5_total)*100), 2)
    p5_response_sla_met_percent = p5_response_sla_met_percent







#for calculating Resolution SLA Met Percentage
p1_resolution_sla_met_percent = 100
p2_resolution_sla_met_percent = 100
p3_resolution_sla_met_percent = 100
p4_resolution_sla_met_percent = 100
p5_resolution_sla_met_percent = 100

if(p1_total != 0):
    p1_resolution_sla_met_percent = round(abs((p1_resolution_sla_met_count/p1_total)*100), 2)
    p1_resolution_sla_met_percent = p1_resolution_sla_met_percent

if(p2_total != 0):
    p2_resolution_sla_met_percent = round(abs((p2_resolution_sla_met_count/p2_total)*100), 2)
    p2_resolution_sla_met_percent = p2_resolution_sla_met_percent

if(p3_total != 0):
    p3_resolution_sla_met_percent = round(abs((p3_resolution_sla_met_count/p3_total)*100), 2)
    p3_resolution_sla_met_percent = p3_resolution_sla_met_percent

if(p4_total != 0):
    p4_resolution_sla_met_percent = round(abs((p4_resolution_sla_met_count/p4_total)*100), 2)
    p4_resolution_sla_met_percent = p4_resolution_sla_met_percent

if(p5_total != 0):
    p5_resolution_sla_met_percent = round(abs((p5_resolution_sla_met_count/p5_total)*100), 2)
    p5_resolution_sla_met_percent = p5_resolution_sla_met_percent


#making % symbol

"""# Creating dataframe for response first table with breached, met and total SLA incidents"""

list_to_create_response_df = [
    ["1 - Critical", p1_response_sla_met_count, p1_response_sla_breach_count, p1_total, p1_response_sla_met_percent, sla_target],
    ["2 - High", p2_response_sla_met_count, p2_response_sla_breach_count, p2_total, p2_response_sla_met_percent, sla_target],
    ["3 - Moderate", p3_response_sla_met_count, p3_response_sla_breach_count, p3_total, p3_response_sla_met_percent, sla_target],
    ["4 - Low", p4_response_sla_met_count, p4_response_sla_breach_count, p4_total, p4_response_sla_met_percent, sla_target],
    ["5 - Planning", p5_response_sla_met_count, p5_response_sla_breach_count, p5_total, p5_response_sla_met_percent, sla_target]
]

#now creating df for response SLA first table
df_response = pd.DataFrame(list_to_create_response_df, columns=["Priority","SLA Met","SLA Breached","Total Incidents","SLA Met %","SLA Target"])

#now creating df for 'Overall SLA' for Response
overall_response_sla_percent = "100.00"
if(sum(df_response['Total Incidents']) != 0):
    overall_response_sla_percent = round(float(((sum(df_response['SLA Met'])/sum(df_response['Total Incidents']))*100)), 2)

df_response

overall_response_sla_percent

"""# Creating dataframe for resolution first table with breached, met and total SLA incidents"""

list_to_create_resolution_df = [
    ["1 - Critical", p1_resolution_sla_met_count, p1_resolution_sla_breach_count, p1_total, p1_resolution_sla_met_percent, sla_target],
    ["2 - High", p2_resolution_sla_met_count, p2_resolution_sla_breach_count, p2_total, p2_resolution_sla_met_percent, sla_target],
    ["3 - Moderate", p3_resolution_sla_met_count, p3_resolution_sla_breach_count, p3_total, p3_resolution_sla_met_percent, sla_target],
    ["4 - Low", p4_resolution_sla_met_count, p4_resolution_sla_breach_count, p4_total, p4_resolution_sla_met_percent, sla_target],
    ["5 - Planning", p5_resolution_sla_met_count, p5_resolution_sla_breach_count, p5_total, p5_resolution_sla_met_percent, sla_target]
]

#now creating df for response SLA first table
df_resolution = pd.DataFrame(list_to_create_resolution_df, columns=["Priority","SLA Met","SLA Breached","Total Incidents","SLA Met %","SLA Target"])

#now creating df for 'Overall SLA' for Response
overall_resolution_sla_percent = "100.00%"
if(sum(df_resolution['Total Incidents']) != 0):
    overall_resolution_sla_percent = round(float(((sum(df_resolution['SLA Met'])/sum(df_resolution['Total Incidents']))*100)), 2)

df_resolution

overall_resolution_sla_percent



"""# Response SLA - Resource Wise"""

#creating list of resources
assigned_to_names = []
if(api['result'] != []):
    
    for i in range(len(api['result'])):
        assigned_person = api['result'][i]['assigned_to']['display_value']
        assigned_to_names.append(assigned_person)

#to get unique names in api response, need to change it to set and again to list
assigned_to_names = set(assigned_to_names)
assigned_to_names = list(assigned_to_names)

list_of_keys_for_each_assigned = ["P1","P2","P3","P4","P5","Total Breach","Total assigned Incidents"]
# creating one dictionary to hold all values like p1,p2,p3,p4,p5, total breach and assigned_to as key
response_sla_resource = dict.fromkeys(assigned_to_names)

#creating dictionary for each name (that is also dictionary key in above dictionary) with each value as 0
for i in response_sla_resource.keys():
    response_sla_resource[i] = dict.fromkeys(list_of_keys_for_each_assigned, 0)

# now checking in api response using assinged_to name and filling values in all fields of each name
if(api['result'] != []):
    
    for i in range(len(api['result'])):
        assigned_person = api['result'][i]['assigned_to']['display_value']
        response_sla_breach = str(api['result'][i]['u_response_sla_breach']['value'])
        incident_priority = api['result'][i]['priority']['display_value']
        #looping for each name in dictionary
        for i in response_sla_resource.keys():
            
            if(assigned_person == i):
                
                #increasing total assigned incidents field
                response_sla_resource[i]["Total assigned Incidents"] += 1
                #checking response sla breached or not
                if(response_sla_breach == "true"):
                    response_sla_resource[i]["Total Breach"] += 1
                    if(incident_priority == P1):
                        response_sla_resource[i]["P1"] += 1
                    
                    elif(incident_priority == P2):
                        response_sla_resource[i]["P2"] += 1
                    
                    elif(incident_priority == P3):
                        response_sla_resource[i]["P3"] += 1
                    
                    elif(incident_priority == P4):
                        response_sla_resource[i]["P4"] += 1
                    
                    elif(incident_priority == P5):
                        response_sla_resource[i]["P5"] += 1
            else:
                #print("pass")
                pass

"""# creating response sla resource table"""

#creating df for response sla resource wise
df_response_resource_wise = pd.DataFrame(response_sla_resource).T
df_response_resource_wise = df_response_resource_wise.reset_index()
df_response_resource_wise = df_response_resource_wise.rename(columns={"index": "Resource Name"})
df_response_resource_wise = df_response_resource_wise.sort_values("Total assigned Incidents", ascending=False)

#adding last row as grand Total
list_of_list = [
    ["Grand Total"],
    [sum(df_response_resource_wise["P1"])],
    [sum(df_response_resource_wise["P2"])],
    [sum(df_response_resource_wise["P3"])],
    [sum(df_response_resource_wise["P4"])],
    [sum(df_response_resource_wise["P5"])],
    [sum(df_response_resource_wise["Total Breach"])],
    [sum(df_response_resource_wise["Total assigned Incidents"])]
]

#creating new temp dataframe for appending last row as Grand total
temp_pd = pd.DataFrame(list_of_list, ["Resource Name","P1","P2","P3","P4","P5","Total Breach","Total assigned Incidents"]).T

#appending both dataframes for making whole Response SLA Resource wise table
df_response_resource_wise = df_response_resource_wise.append(temp_pd)

#adding last column in df
df_response_resource_wise["SLA Met %"] = (abs((df_response_resource_wise["Total assigned Incidents"] - df_response_resource_wise["Total Breach"]))/df_response_resource_wise["Total assigned Incidents"]) * 100
#now reseting index because it will create problem in case of access similar index value
df_response_resource_wise = df_response_resource_wise.reset_index(drop=True)

# for rounding SLA Met % values and adding % at last in percent value
ls = list(df_response_resource_wise["SLA Met %"])
for i in range(len(ls)):
    df_response_resource_wise["SLA Met %"][i] = round(float((ls[i])), 2)

df_response_resource_wise





"""# Resolution SLA - Resource Wise"""

#creating list of resources
assigned_to_names = []
if(api['result'] != []):
    
    for i in range(len(api['result'])):
        assigned_person = api['result'][i]['assigned_to']['display_value']
        assigned_to_names.append(assigned_person)

#to get unique names in api response, need to change it to set and again to list
assigned_to_names = set(assigned_to_names)
assigned_to_names = list(assigned_to_names)

list_of_keys_for_each_assigned = ["P1","P2","P3","P4","P5","Total Breach","Total assigned Incidents"]
# creating one dictionary to hold all values like p1,p2,p3,p4,p5, total breach and assigned_to as key
resolution_sla_resource = dict.fromkeys(assigned_to_names)

#creating dictionary for each name (that is also dictionary key in above dictionary) with each value as 0
for i in resolution_sla_resource.keys():
    resolution_sla_resource[i] = dict.fromkeys(list_of_keys_for_each_assigned, 0)

# now checking in api response using assinged_to name and filling values in all fields of each name
if(api['result'] != []):
    
    for i in range(len(api['result'])):
        assigned_person = api['result'][i]['assigned_to']['display_value']
        resolution_sla_breach = str(api['result'][i]['u_sla_breach']['value'])
        incident_priority = api['result'][i]['priority']['display_value']
        #looping for each name in dictionary
        for i in resolution_sla_resource.keys():
            
            if(assigned_person == i):
                
                #increasing total assigned incidents field
                resolution_sla_resource[i]["Total assigned Incidents"] += 1
                #checking response sla breached or not
                if(resolution_sla_breach == "true"):
                    resolution_sla_resource[i]["Total Breach"] += 1
                    if(incident_priority == P1):
                        resolution_sla_resource[i]["P1"] += 1
                    
                    elif(incident_priority == P2):
                        resolution_sla_resource[i]["P2"] += 1
                    
                    elif(incident_priority == P3):
                        resolution_sla_resource[i]["P3"] += 1
                    
                    elif(incident_priority == P4):
                        resolution_sla_resource[i]["P4"] += 1
                    
                    elif(incident_priority == P5):
                        resolution_sla_resource[i]["P5"] += 1
            else:
                #print("pass")
                pass

"""# creating resolution sla resource table"""

#creating df for response sla resource wise
df_resolution_resource_wise = pd.DataFrame(resolution_sla_resource).T
df_resolution_resource_wise = df_resolution_resource_wise.reset_index()
df_resolution_resource_wise = df_resolution_resource_wise.rename(columns={"index": "Resource Name"})
df_resolution_resource_wise = df_resolution_resource_wise.sort_values("Total assigned Incidents", ascending=False)

#adding last row as grand Total
list_of_list = [
    ["Grand Total"],
    [sum(df_resolution_resource_wise["P1"])],
    [sum(df_resolution_resource_wise["P2"])],
    [sum(df_resolution_resource_wise["P3"])],
    [sum(df_resolution_resource_wise["P4"])],
    [sum(df_resolution_resource_wise["P5"])],
    [sum(df_resolution_resource_wise["Total Breach"])],
    [sum(df_resolution_resource_wise["Total assigned Incidents"])]
]

#creating new temp dataframe for appending last row as Grand total
temp_pd = pd.DataFrame(list_of_list, ["Resource Name","P1","P2","P3","P4","P5","Total Breach","Total assigned Incidents"]).T

#appending both dataframes for making whole Response SLA Resource wise table
df_resolution_resource_wise = df_resolution_resource_wise.append(temp_pd)

#adding last column in df
df_resolution_resource_wise["SLA Met %"] = (abs((df_resolution_resource_wise["Total assigned Incidents"] - df_resolution_resource_wise["Total Breach"]))/df_resolution_resource_wise["Total assigned Incidents"]) * 100
#now reseting index because it will create problem in case of access similar index value
df_resolution_resource_wise = df_resolution_resource_wise.reset_index(drop=True)

# for rounding SLA Met % values and adding % at last in percent value
ls = list(df_resolution_resource_wise["SLA Met %"])
for i in range(len(ls)):
    df_resolution_resource_wise["SLA Met %"][i] = round(float((ls[i])), 2)



""" Creating table for mail body for snapshot"""

#creating for first response table
first_response_table = df_response.to_html(index=False, classes="table first_response", justify="center")

#creating for second resolution table
second_resolution_table = df_resolution.to_html(index=False, classes="table second_resolution", justify="center")

#creating third response resource-wise table
third_response_resource_wise_table = df_response_resource_wise.to_html(index=False, classes="table third_response_resource_wise", justify="center")

#creating forth resolution resource-wise table
forth_resolution_resource_wise_table = df_resolution_resource_wise.to_html(index=False, classes="table forth_resolution_resource_wise", justify="center")
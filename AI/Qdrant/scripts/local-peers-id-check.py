#This is a script to check the peer id of a node in the cluster and get the shard ids of a particular collection

# Usage: 
#       local-peers-id-check.py HOST_IP COLLECTION_NAME 

#Needed to check values passed to the script
import argparse
#Importing subprocess for curl command and json to format the curl output
import subprocess, json
from subprocess import TimeoutExpired
#Importing tabulate to create/print our pretty table
from tabulate import tabulate
#Imports needed to exit the program if failures, and manage failures on curl command
import sys, requests, signal



#Function to get the arguments passed to the script and call to validate the ip
#We check two arguments are passed to the script, first the ip, second a collection name
def check_prompt():
    parser = argparse.ArgumentParser(description="Script to get the topology of our cluster")
    parser.add_argument("IP", help="IP of the host to connect to")
    parser.add_argument("COLLECTION", help="Collection from which we want to check its shards")
    arg = parser.parse_args()

    ip_collection = list()
    ip_collection.append(arg.IP)
    ip_collection.append(arg.COLLECTION)

    return ip_collection


#Function to validate the ip
def validate_ip(ip_value):
    if ip_value == "localhost":
        return True
    else:
        octects = ip_value.split('.')
        if len(octects) != 4:
            return False
        for x in octects:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
        return True


#Curl call to get the info needed, we also check if there is a timeout, which can be caused by a collectin not existing or by some issue in the cluster
def curl_call(url):

    command = ['curl',url]
    try:
        result = subprocess.run(command, timeout=5, capture_output=True, text=True)
        return result.stdout
    #If not imported TimeoutExpired we can raise the exception by getting the subprocess: subprocess.TimeoutExpired
    except TimeoutExpired:
        print("There was a timeout while trying to reach out your cluster, it can be due to a wrong ip provided to connect to or by some issue on your cluster, please, check the ip provided and if it ok then you can try to re-execute the script to see if it was a temporary issue or if it fails again we encourage you to check the status of your cluster.")
        sys.exit(1)


#Function to print output and depending on the cluster topology/number of nodes the output must be different
def table_print(shards,table_content):
    if shards == 1:
        #Output for a cluster with one node so it is useful only peer id and number of shards as all belong to this unique node/host
        print("Your cluster is compound by only one host, which peer_id and shard info is provided below:")
        table = [['peer_id', 'shard_count'], [table_content[0],table_content[1]]]
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    else:
        #Output for a cluster with more than one node, where we also consider the shard_id of each node
        shard_ids = len(table_content)
        adding_ids = str(table_content[2])
        i = 2
        while i < shard_ids-1:
            adding_ids += "," + str(table_content[i+1])
            i += 1
        table = [['peer_id', 'shard_count', 'shard_ids'], [table_content[0],table_content[1],adding_ids]]
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))


###########################################################################################################################################
###########################################################################################################################################
########################################                           MAIN                            ########################################
###########################################################################################################################################
###########################################################################################################################################

#Variable used to check if qdrant cluster is enabled
is_cluster = 0

#Getting values from prompt
cluster_info = list()
cluster_info = check_prompt()

#Checking if a valid ip has been provided from prompt
ip_valid = validate_ip(cluster_info[0])
if ip_valid is False:
    print("The ip provided is not a valid one, please, re-execute the script by providing a valid one.")
    sys.exit(1)

#Defining the curl http endpoint and getting cluster info
res_cluster = curl_call('http://'+cluster_info[0]+':6333/cluster')

#Formatting to json
json_object = json.loads(res_cluster)
res_formatted = json.dumps(json_object, indent=2)

json_data = json.loads(res_cluster)

temp1 = json_data['result']['status']

#Checking if the qdrant cluster is enabled (it can be compound by 1 or more nodes) or not
if temp1 == "enabled":
    is_cluster = 1
else:
    is_cluster = 0

#Defining the curl http endpoint to get info about shards from peers
res_collect = curl_call('http://'+cluster_info[0]+':6333/collections/'+cluster_info[1]+'/cluster')

#Formatting to json
json_object = json.loads(res_collect)
res_formatted = json.dumps(json_object, indent=2)

json_data = json.loads(res_collect)
temp2 = json_data['status']

#If the status from the json output is not ok, then the collecton does not exist and we finish the script execution
if temp2 != "ok":
    print("The collection name you have provided does not exist, please re-execute the script by providing a valid one. Thanks and see you soon!")
    sys.exit(1)

#Creating the array for the table output with peers and shard info
peers_shard = list()

if is_cluster == 1:
    temp3=json_data['result']['peer_id']
    peers_shard.append(temp3)
    temp3=json_data['result']['shard_count']
    shard_count=temp3
    peers_shard.append(temp3)

    if shard_count > 1:
        num = 0
        while num < len(json_data['result']['local_shards']):
            temp3=json_data['result']['local_shards'][num]['shard_id']
            peers_shard.append(temp3)
            num = num + 1
    else:
        table_print(1,peers_shard)

    # Printing values in pretty way
    table_print(shard_count,peers_shard)

else:
    temp3=json_data['result']['peer_id']
    peers_shard.append(temp3)
    temp3=json_data['result']['shard_count']
    peers_shard.append(temp3)

    # Printing values in pretty way
    table_print(1,peers_shard)

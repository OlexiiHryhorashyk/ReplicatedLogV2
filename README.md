# ReplicatedLog
Link to Github: https://github.com/OlexiiHryhorashyk/ReplicatedLogV2

Replicated log V2 task for Distributed Systems course on UCU Data Engineering certification program.

Demonstration project for asynchronous distributed message replication.

For convenience, I united this files in Pycharm project, but for running this code we will be using Docker.

Each python server file will be wrapped as separate docker container inside one network which allows the containers to communicate using http requests.

For deployment of these containers created Docker compose .yml file.

Consist with 3 python files, rewritten from synchronous HTTPserver to asynchronous aiohttp, saving the core functionality and adding write concern:

server.py - Master node, which can receive message from client as http POST request. Saves the message locally, and provide tunable semi-synchronicity for message replication to secondary nodes with http POST request. If message starts with write consern value w = (1, 2, 3), waits for (0, 1, 2) ACK from secondary nodes. Also can return to the client list of saved messages using http GET request.
sub.py -  code for every secondary nodee, can receive and save the message form master node as POST request. Also return to the client list of saved messages as GET request.
client.py - simple file to simulate a client, which receives messages from terminal and send it to master node as POST requests, also can list messages from each node by making GET request to master and secondary nodes.
Also consist of 2 Dockerfile, one for master and other for every secondary container deployment. And one Docker compose file (docker-compose.yml) for running all three nodes together inside one network.

For running this project you need:

Clone this repository.
docker-compose build
docker-compose up
Run client.py in Pycharm or in command shell: python client.py
Terminal log will receive any message, and send it to master. 

By default, replication works in synchronous mode (w=3). 

If message starts with "w=", it means that write concern parameter is provided. 

if w<=1 --> w==1 --> async mode --> not waiting for response form secondary nodes. 

if w==2 --> semi-sync mode --> wait for at least one response from any of secondary nodes 

if w>2 --> w==3 --> sync mode --> wait for response from all secondary nodes

Have 3 keywords: list/list master, list1/list sub1, list2/list sub2 - makes GET request to coresponding node, to list saved messages of the node.

Logs of all three nodes can be seen in a terminal, where was executed docker-compose file. Logs of each separeted node can be viewed in Desktop or by running:

docker logs main/node1/node2.

In Docker desktop it works like this: 

   In Docker desktop it works like this:
 ![image](https://github.com/OlexiiHryhorashyk/ReplicatedLogV2/assets/58079096/3c66f876-31ad-41be-b423-e55836d907ee)

   In terminal-client.py console. We can see client blocking time difference with different write consern values. I have simulated latancy 3 sec. for secondary №1 and 1sec. for secondary node №2:
![image](https://github.com/OlexiiHryhorashyk/ReplicatedLogV2/assets/58079096/452353b4-fdfa-46c0-ac04-70b374371f9a)
![image](https://github.com/OlexiiHryhorashyk/ReplicatedLogV2/assets/58079096/d3c52933-a1b9-40fc-b1c3-3b7575aa007b)

   In nodes logs:
![image](https://github.com/OlexiiHryhorashyk/ReplicatedLogV2/assets/58079096/3f690da8-4a32-4120-aedc-8bec77a79456)
![image](https://github.com/OlexiiHryhorashyk/ReplicatedLogV2/assets/58079096/1d462f73-0fa7-45f3-813d-784de5bbadaa)

   In Docker Desktop logs for each node:
   Master:
   
![image](https://github.com/OlexiiHryhorashyk/ReplicatedLogV2/assets/58079096/648f6fa7-b11f-4100-9e4c-f1fc47a5d80e)

  Sub1:
  
 ![image](https://github.com/OlexiiHryhorashyk/ReplicatedLogV2/assets/58079096/cd3e8549-51ae-4c46-a51b-b9206ec53e3d)

And demonstration of simulated inconsistency. Set up "latency" for 10 seconds on first sub-node. Then sent message in async (w=1) mode. One by one, listed contents of master node and sub1 node. We see that last msg is not saved yet, but after few more seconds contents starts to mach again.

![image](https://github.com/OlexiiHryhorashyk/ReplicatedLogV2/assets/58079096/456f2d66-1129-4c86-aae4-f8323b1a878b)

PS: Added (preventive) message deduplication by adding an increment in master node and adding it to JSON in post to secondary. Now messages saved as a dict (not list), with the increment value as a key. If the key of a message already exist, it prevents saving the same one message more than once. 




 

import hashlib
from Nodes import Nodes


current_time = 0
end_time = 100000
time_interval = 600
contact_frequency = 600 #seconds
nodes_id = [i for i in range(20)]
nodes_list = []

for i in nodes_id:
    nodes_list.append(Nodes(i))




print(nodes_id)
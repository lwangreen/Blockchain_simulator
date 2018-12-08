import random
import os


def write_into_file(f, winning_time, node):
    f.write(str(winning_time)+" "+str(node)+"\n")


def random_select_winner(len_nodes_list):
    winners = []
    terminate_prob = 0
    ongoing_winning_time = 0
    while terminate_prob < 0.8 and len(winners) < 3:
        node = random.randint(0, len_nodes_list - 1)
        while node in winners:
            node = random.randint(0, len_nodes_list - 1)
        ongoing_winning_time += random.randint(0, 200)
        winners.append([node, ongoing_winning_time])

        terminate_prob = random.random()

    return winners


dur = 600       # Time flows by 600 secs a time
endtime = 100000
time = 0
count = 0


file_path = os.getcwd() + "\\Created_data_trace\\"
if not os.path.exists(file_path):
    os.makedirs(file_path)

f = open(file_path+"winners.txt", 'w+')
count = 0

while time < endtime:
    winners = random_select_winner(20)
    for winner in winners:
        write_into_file(f, winner[1]+time, winner[0])
    time += dur
f.close()
print(count)

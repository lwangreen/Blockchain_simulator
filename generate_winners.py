import random
import os

num_winners = 9
population_size = 20
def write_into_file(f, winning_time, node):
    f.write(str(winning_time)+" "+str(node)+"\n")


def random_select_winner(len_nodes_list):
    winners = []
    terminate_prob = 0
    ongoing_winning_time = 0
    while terminate_prob < 0.8 and len(winners) < num_winners:
        node = random.randint(0, len_nodes_list - 1)
        while node in winners:
            node = random.randint(0, len_nodes_list - 1)
        ongoing_winning_time += random.randint(0, int(600/num_winners))
        winners.append([node, ongoing_winning_time])

        terminate_prob = random.random()

    return winners


dur = 600       # Time flows by 600 secs a time
endtime = 1000000
time = 0
count = 0


file_path = os.getcwd() + "\\Created_data_trace\\"
if not os.path.exists(file_path):
    os.makedirs(file_path)

f = open(file_path+"nodes"+str(population_size)+"_winners"+str(num_winners)+"_long.txt", 'w+')
count = 0

while time < endtime:
    winners = random_select_winner(population_size)
    for winner in winners:
        write_into_file(f, winner[1]+time, winner[0])
    time += dur
f.close()
print(count)

Number of nodes: 20

Transactions:
Transaction format: [time, sender, recipient, amount]
Max transaction time: 85000 seconds
The transaction senders and recipients are selected randomly from nodes pool.
Number of transactions: 
transaction_1.txt: 2680
transaction_2.txt: 5360
transaction_3.txt: 8040

Time unit: 600s
Mining winners: the winners are randomly chosen. Only 3 winners at most within a time unit.
Winners always generate new block no matter whether the incomplete transaction list is empty.

Keywords:
RT: random transactions
RW: random winner
RC: random connection time to Internet
RSC: random start connection time to Internet for each node

Output files:
./Log:
filename format: [time]_[contact frequency]_[transaction rate]_[random transaction]_[random winner]_[random Internet connection time interval within a range]_[random start connecting to Internet time].txt
It displays all the blockchains exist in the simulator, and the owners for each blockchain.
Block difference section displays the blocks that different to other chain.

./Stats:
filename format: statistics_[random winner]_[random Internet connection time interval within a range]_[random start connecting to Internet time].csv
No keyword in the finame means the associate parameter is set to False.


How to run:
python BlockchainSimulator.py -c [CONTACT_FREQUENCY] -t [TRANSACTION_RATE] --RANDOM_TRANS [True or False] --RANDOM_WINNERS [True or False] --RANDOM_CONNECT [True or False] --RANDOM_START_CONNECT [True or False]

Or simply run any of the .bat file.
import argparse
from Bnetwork import Bnetwork
from verification import verification

parser = argparse.ArgumentParser(description='Please enter data in the format [ Examples/alarms.json  Burglary:T John_calls 1000 -mb earthquake] ')
parser.add_argument('file', metavar='File',type =str,help='JSON file name containing the Bayesian Network')
# parser.add_argument('-e',metavar='--evidence',type=json.loads,help='Evidence is to be formatted as a dictionary' )
parser.add_argument(
    'e',metavar='Evidence',
    type=lambda v: {k:str(v) for k,v in (x.split(':') for x in v.split(','))},
    help='comma-separated Node:state pairs, e.g. Burglary:T,Color:blue'
)
parser.add_argument('q',metavar='Query', type=str,help='Name of the query node')
parser.add_argument('i',metavar='iter',type= int,help='No of iterations of MCMC')
parser.add_argument('-mb',metavar='--MarkovBlanket',type=str,help='Name of node whose markov blanket is to be printed')
args = parser.parse_args()

#Create Network
network = Bnetwork(args.file,args.i)
#Verify Network
verify = verification(network)
verify.verify_data()
#Verify Evidence and Query

verify.check_parameters(network,args.e,[args.q])

#Run MCMC
answer = network.beta_mcmc(evidence=args.e, query=[args.q])
print(answer)
#If needed print Markov Blanket
if(args.mb):
    print(network.print_blanket(args.mb))



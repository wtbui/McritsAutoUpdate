from pkg.dclient.dclient import *
from pkg.farm.farm import *
from core.flags import parse_args
 
import os

def start(argv):
    #link = fetch_update(os.environ['UKEY'])
    args = parse_args(argv)

    if args.farm:
        err = run_farm()
        
        if err:
            return -1
    
    return 1
    

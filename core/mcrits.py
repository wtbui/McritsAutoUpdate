from pkg.dclient.dclient import *
from pkg.farm.farm import *
from core.flags import parse_args
from pkg.logging import setup_logging 

def start(argv):
    #link = fetch_update(os.environ['UKEY'])
    args = parse_args(argv)

    setup_logging()
    logging.info("Logging Setup")

    if args.farm:
        err = run_farm(args)
        
        if err:
            return -1
    
    return 1
    

import argparse

def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog = "Miscrits Helper Client",
        description = "Miscrits assist client",
    )
    
    parser.add_argument('-f', '--farm', action='store_true', help='Runs autofarming')

    return parser.parse_args()

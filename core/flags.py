import argparse
import sys

def parse_args(argv):
    print(argv)
    parser = argparse.ArgumentParser(
        prog = "Miscrits Helper Client",
        description = "Miscrits assist client, --help to see command options",
    )
    
    parser.add_argument(
        "-f",
        "--farm",           # or "-n"
        type=int,             # ensures the argument is converted to int
        default=0,           # (optional) default value if --number is not provided
        help="Runs autofarming, 1 - Blighted Flue, 2 - Dark Poltergust"
    )

    parser.add_argument(
        '-l',
        '--level',
        action="store_true",
        default=False,
        help="Turns on auto leveling feature"
    )

    if len(argv) == 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args()

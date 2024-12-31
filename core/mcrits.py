from pkg.dclient.dclient import *
import os

def start():
   link = fetch_update(os.environ['UKEY'])
   print(link)

import time

from datetime import datetime

def log(outstr):
    print_to_log("[MSG]: " + outstr)

def error(outstr):
    print_to_log("[ERR]: " + outstr)

def print_to_log(outstr):
    now = datetime.now()
    time = now.strftime("%d-%m-%y %H:%M:%S ")

    with open("cur.log", "a", encoding="utf8") as log:
        log.write(time + outstr)

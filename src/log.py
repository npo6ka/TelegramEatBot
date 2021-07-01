import logging

log = None

def create_log():
    global log

    logging.basicConfig(handlers=[logging.FileHandler(filename="./cur.log",
        encoding='utf-8', mode='a+')],
        format='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt='%d-%m-%y %H:%M:%S',
        level=logging.INFO)

    logging.info("Running bot logging")
    log = logging.getLogger('Bot Log')


def out(outstr, is_print = False):
    if log:
        log.info(outstr)
    if is_print:
        print(outstr)

def error(outstr):
    log.error(outstr)
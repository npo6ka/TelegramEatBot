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


def out(outstr):
    log.info(outstr)

def error(outstr):
    log.error(outstr)
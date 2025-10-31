import logging

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(
        filename="local_ai.log", 
        format='(%(asctime)s) [%(filename)s:%(funcName)s:%(levelname)s]:: %(message)s', 
        datefmt='%d/%m/%Y %I:%M:%S %p', 
        level=logging.INFO)
    logger.info("Started local_ai!")
    # Do stuff
    logger.info("Finished!")

if __name__ == '__main__':
    main()
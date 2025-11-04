import logging
import argparse
import sys, os
import toml

logger = logging.getLogger(__name__)

def main():
    logging_setup()
    logger.info("Started local_ai!")
    # Do stuff
    logger.info("Finished!\n")

def get_run_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='dev')
    args = parser.parse_args()
    return args

def logging_setup():
    # Logger should change base config depending on runtime mode. 
    # dev: Should be level "DEBUG"
    # test: Should be level "INFO" 
    # prod: Sould be level "ERROR"
    runtime_mode = get_run_mode()
    logging_level = None
    if runtime_mode.mode == "dev":
        logging_level = logging.DEBUG
    elif runtime_mode == "test":
        logging_level = logging.INFO
    elif runtime_mode == "prod":
        logging_level = logging.ERROR
    else:
        logging_level = logging.CRITICAL

    logging.basicConfig(
        filename="local_ai.log", 
        format='(%(asctime)s) [%(filename)s:%(funcName)s:%(levelname)s]:: %(message)s', 
        datefmt='%d/%m/%Y %I:%M:%S %p', 
        level=logging_level)
    logger.info("Main logger initialized.")

    log_default_run_environment()

def log_default_run_environment():
    """
    1. Python version
    2. App version
    3. Runtime args (if any)
    4. Mode: Build/test/prod
    """
    app_name = os.getenv("local_ai")
    pyproject = toml.load('pyproject.toml')
    project_version = pyproject['project']['version']

    runtime_args = get_run_mode()
    logger.debug(f"Runtime args: {runtime_args}")
    logger.info(f"MODE: {runtime_args.mode}")

    logger.info(f"Running python version: {sys.version}")
    logger.info(f"Local-Ai version: {project_version}")

if __name__ == '__main__':
    main()
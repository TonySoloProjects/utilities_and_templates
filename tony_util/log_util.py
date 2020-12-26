"""
Routines and classes to assist in logging.
Created by: Tony Held tony.held@gmail.com
Created on: 2020-12-26
Copyright © 2020 Tony Held.  All rights reserved."""

import logging
import sys
import os


class FilterDebugInfoNotset(logging.Filter):
    """Allow only DEBUG, INFO, & NOTSET records to be logged."""
    def filter(self, record):
        # print(f'{record} \n{record.levelno} \n {record.levelname}')
        if record.levelno in [logging.DEBUG, logging.INFO, logging.NOTSET]:
            return True
        else:
            return False


class FilterInfo(logging.Filter):
    """Allow only INFO records to be logged."""
    def filter(self, record):
        # print(f'{record} \n{record.levelno} \n {record.levelname}')
        if record.levelno in [logging.INFO]:
            return True
        else:
            return False


class SingletonLogger:
    """Application level logger with the following characteristics:
        1) Logger has a name and the logger with the same name is shared application-wide
        2) DEBUG or greater logs go to log file: "logs/<logger_name>.log"
        3) WARNING or greater logs go to sys.stderr
        4) INFO only logs go to sys.stdout
        """
    loggers = {}

    @classmethod
    def get_logger(cls, name='my_logger', path='logs'):
        """Get logger if it exists, otherwise create it..

            Parameters
            ----------
            name : str
                Name of logger

            path : str
                path for logger output file

            Returns
            -------
            logger : type***
                Application wide logger named 'name'
            """
        if name not in SingletonLogger.loggers:
            SingletonLogger.create_logger(name, path)
        return SingletonLogger.loggers[name]

    @classmethod
    def create_logger(cls, name='my_logger', path='logs'):
        """Get create logger named 'name' and add it to the class level dictionary

            Parameters
            ----------
            name : str
                Name of logger

            path : str
                path for logger output file

            Returns
            -------
            logger : type***
                Application wide logger named 'name'
            """
        # create path if it does not exist yet
        if os.path.isfile(path):
            raise FileExistsError(f'Attempt to create a directory that is already a regular file:\n {path}')
        elif not os.path.isdir(path):
            os.makedirs(path)

        file_name = f'{path}/{name}.log'

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(file_name)
        fh.setLevel(logging.DEBUG)

        sh_err = logging.StreamHandler(stream=sys.stderr)
        sh_err.setLevel(logging.WARNING)

        sh_out = logging.StreamHandler(stream=sys.stdout)
        sh_out.setLevel(logging.INFO)
        sh_out.addFilter(FilterInfo())

        logger.addHandler(fh)
        logger.addHandler(sh_err)
        logger.addHandler(sh_out)

        SingletonLogger.loggers[name] = logger


if __name__ == "__main__":

    log = SingletonLogger.get_logger()
    log = SingletonLogger.get_logger('bob')
    log = SingletonLogger.get_logger('alice')
    print(SingletonLogger.loggers)

    print(type(log), log)
    log.debug(f'Called with debug 10')
    log.info(f'Called with info 20')
    log.warning(f'Called with warning 30')
    log.error(f'Called with error 40')
    log.critical(f'Called with critical 50')

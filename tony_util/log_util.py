"""
Routines and classes to assist in logging.
Created by: Tony Held tony.held@gmail.com
Created on: 2020-12-26
Copyright © 2020 Tony Held.  All rights reserved.

Notes
______

Level Name, Value,  Use
----------  -----   --------------------------------------------------------------------------
NOTSET      0       When the logger is created with getLogger(), the level is set to NOTSET.
                    If the logging level is not set explicitly with setLevel(),
                    the messages are propagated to the logger parents.
DEBUG       10      Detailed information, typically of interest only when diagnosing problems.
INFO        20      Confirmation that things are working as expected.
WARNING     30      An indication that something unexpected happened,
                    or indicative of some problem in the near future (e.g. ‘disk space low’).
                    The software is still working as expected.
ERROR       40      Due to a more serious problem,
                    the software has not been able to perform some function.
CRITICAL    50      A serious error,
                    indicating that the program itself may be unable to continue running.
                    """

import logging
import sys
import os

# todo - double check new filters

class FilterOutWarningsErrors(logging.Filter):
    """Filter out logging.WARNING or greater messages.
    Primary use of this class is filter records sent to stdout so they don't
    duplicate records that will also be sent to stderr."""
    def filter(self, record):
        # print(f'{record} \n{record.levelno} \n {record.levelname}')
        if record.levelno >= logging.WARNING:
            return False
        else:
            return True


class SingletonLogger:
    """Application level logger with the following characteristics:
        1) Loggers with the same name will be shared application-wide
        2) Loggers will log to a file and to stdout and stderr
        3) WARNING or greater logs go to sys.stderr
        4) log level for sys.stdout can be set (default is INFO).
        3) The file name of the log file is: "<path>/<name>.log"
        """
    loggers = {}

    @classmethod
    def get_logger(cls,
                   name='my_logger',
                   path='logs',
                   stdout_level=logging.INFO,
                   file_level=logging.DEBUG,
                   ):
        """Get logger if it exists, otherwise create it..

            Parameters
            ----------
            name : str
                Name of logger

            path : str
                path for logger output file

            stdout_level: logging.DEBUG | logging.INFO
                logging level for stdout output.

            file_level: int
                logging level for output file.

            Returns
            -------
            logger : logging
                Application wide logger named 'name'
            """
        if name not in SingletonLogger.loggers:
            SingletonLogger.create_logger(name, path, stdout_level, file_level)
        return SingletonLogger.loggers[name]

    @classmethod
    def create_logger(cls, name='my_logger',
                      path='logs',
                      stdout_level=logging.INFO,
                      file_level=logging.DEBUG,
                      ):
        """Create logger named 'name' and add it to the class level dictionary

        Parameters
        ----------
        name : str
            Name of logger

        path : str
            path for logger output file

        stdout_level: logging.DEBUG | logging.INFO
            logging level for stdout output.

        file_level: int
            logging level for output file.
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
        fh.setLevel(file_level)

        sh_err = logging.StreamHandler(stream=sys.stderr)
        sh_err.setLevel(logging.WARNING)

        sh_out = logging.StreamHandler(stream=sys.stdout)
        sh_out.setLevel(stdout_level)
        sh_out.addFilter(FilterOutWarningsErrors())

        logger.addHandler(fh)
        logger.addHandler(sh_err)
        logger.addHandler(sh_out)

        SingletonLogger.loggers[name] = logger


if __name__ == "__main__":

    log1 = SingletonLogger.get_logger()
    log2 = SingletonLogger.get_logger('bob')
    log3 = SingletonLogger.get_logger('alice')
    print(SingletonLogger.loggers)

    print(type(log1), log1)
    print(type(log2), log2)
    print(type(log3), log3)
    log3.debug(f'Called with debug 10')
    log3.info(f'Called with info 20')
    log3.warning(f'Called with warning 30')
    log3.error(f'Called with error 40')
    log3.critical(f'Called with critical 50')

# module used to test import statements
from tony_util.log_util import SingletonLogger

log = SingletonLogger.get_logger('module_b')

log.debug(f'Module: {__name__}: Called with debug 10')
log.info(f'Module: {__name__}: Called with info 20')
log.warning(f'Module: {__name__}: Called with warning 30')
log.error(f'Module: {__name__}: Called with error 40')
log.critical(f'Module: {__name__}: Called with critical 50')


log2 = SingletonLogger.get_logger()
log2.debug(f'Module: {__name__}: Called with debug 10b')
log2.info(f'Module: {__name__}: Called with info 20b')
log2.warning(f'Module: {__name__}: Called with warning 30b')
log2.error(f'Module: {__name__}: Called with error 40b')
log2.critical(f'Module: {__name__}: Called with critical 50b')

import luigi
import logging
import os
from dotenv import load_dotenv

load_dotenv()

log_level = os.environ.get('LOG_LEVEL', 'DEBUG')
local_scheduler = os.environ.get('LOCAL_SCHEDULER', True) == 'True'

luigi.interface.InterfaceLogging.setup(
    type(
        'opts',
        (),
        {
            'background': None,
            'logdir': None,
            'logging_conf_file': None,
            'log_level': log_level
        }
    )
)

""" Report the luigi logging level by writing to the log file
    that is specified above via logging.basicConfig() """
luigi_interface_log_level = logging.getLogger('luigi-interface').level
logging.info(
    f"logging.getLogger('luigi-interface').level"
    f" = {luigi_interface_log_level} = "
    f"logging.{logging._levelToName[luigi_interface_log_level]}"
)

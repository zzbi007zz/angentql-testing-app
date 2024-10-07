import logging
from contextlib import contextmanager
from typing import Union

from agentql import trail_logger
from agentql._core._base_debug_manager import BaseDebugManager

log = logging.getLogger("agentql")


class DebugManager(BaseDebugManager):
    @classmethod
    @contextmanager
    def debug_mode(cls):
        cls.debug_mode_enabled = True
        trail_logger.init_if_needed()
        cls.create_debug_files_dir()
        try:
            yield
        except Exception as e:
            cls.save_traceback(e)
            raise
        finally:
            cls.debug_mode_enabled = False
            trail_logger.finalize()
            cls.save_logging_file()
            cls.save_last_accessibility_tree()
            cls.save_meta_data()
            log.debug(f"Debug files saved to {cls.debug_files_path}")

    @staticmethod
    def get_last_trail() -> Union[trail_logger.TrailLogger, None]:
        """
        Get the last trail recorded, if DebugManager is used in the context.
        """
        logger_store = trail_logger.TrailLoggerStore.get_loggers()
        return logger_store[-1] if logger_store else None

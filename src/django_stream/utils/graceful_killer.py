import logging
import signal
from typing import Any

logger = logging.getLogger(__name__)


class GracefulKiller:
    def __init__(self) -> None:
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self._kill_now = False

    def exit_gracefully(self, signum: Any, frame: Any) -> None:
        logger.info("Received termination signal. Exiting gracefully.")
        self._kill_now = True

    @property
    def kill_now(self) -> bool:
        logger.debug(f"Current 'kill now' status for Inbox - {self._kill_now}")
        return self._kill_now

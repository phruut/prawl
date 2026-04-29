import webbrowser
import threading
import logging
from typing import Any

logger = logging.getLogger('prawl')

class HelpCallbacks:
    interface: Any
    update: Any

    def __init__(self, gui):
        self.gui = gui
        self.interface = gui.interface
        self.update = gui.update

    def update_button(self):
        logger.info('update check requested')
        self.interface.configure('update_button', enabled=False)
        self.interface.configure('update_link', show=False)
        self.interface.set('update_status_text', 'checking for updates...')
        thread = threading.Thread(target=self.update_worker, daemon=True)
        thread.start()

    def update_worker(self):
        logger.debug('update worker started')
        self.update.check(callback=lambda results: self.update_post(None, None, results))

    def update_post(self, sender, app_data, user_data):
        message, is_update_available = user_data
        logger.info(f'update check complete | message: {message} | available: {is_update_available}')
        self.interface.set('update_status_text', message)
        if is_update_available and self.update.release_url:
            logger.info(f'update available: {self.update.latest_version}')
            self.interface.configure(
                'update_link',
                show=True,
                label=f'download {self.update.latest_version}',
                callback=lambda: webbrowser.open(self.update.release_url)
            )
        self.interface.configure('update_button', enabled=True)

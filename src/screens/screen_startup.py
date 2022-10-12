from components import screen

#------------------------------------------------------------------------------

class StartUpScreen(screen.AppScreen):

    # def get_icon(self):
    #     return 'progress-clock'

    def get_title(self):
        return 'initializing ...'

    def get_statuses(self):
        return {
            None: 'starting the main process',
            'AT_STARTUP': 'starting',
            'LOCAL': 'initializing local environment',
            'MODULES': 'starting sub-modules',
            'INSTALL': 'installing application',
            'READY': 'application is ready',
            'STOPPING': 'application is shutting down',
            'SERVICES': 'starting network services',
            'INTERFACES': 'starting application interfaces',
            'EXIT': 'application is closed',
        }

    def is_closable(self):
        return False

    def on_enter(self, *args):
        self.ids.state_panel.attach(automat_id='initializer')

    def on_leave(self, *args):
        self.ids.state_panel.release()

import time

#------------------------------------------------------------------------------

from lib import api_client

from components import screen

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

class RecoverIdentityScreen(screen.AppScreen):

    # def get_icon(self):
    #     return 'account-key'

    def get_title(self):
        return 'recover identity'

    def is_closable(self):
        return True

    def on_start_recover_identity_button_clicked(self, *args):
        self.ids.recover_identity_button.disabled = True
        self.ids.recover_identity_result_message.text = ''
        api_client.identity_recover(
            private_key_source=self.ids.private_key_input.text,
            join_network=True,
            cb=self.on_identity_recover_result,
        )

    def on_identity_recover_result(self, resp):
        if _Debug:
            print('on_identity_recover_result', resp)
        self.ids.recover_identity_button.disabled = False
        self.ids.recover_identity_result_message.from_api_response(resp)
        if not api_client.is_ok(resp):
            return
        self.main_win().state_identity_get = 0
        self.control().run()
        self.main_win().select_screen('welcome_screen')
        self.main_win().close_screen('new_identity_screen')
        self.main_win().close_screen('recover_identity_screen')
        self.main_win().screens_stack.clear()

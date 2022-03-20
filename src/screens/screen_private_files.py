from kivy.clock import mainthread
from kivy.properties import StringProperty, NumericProperty  # @UnresolvedImport

from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.list import TwoLineIconListItem

from plyer import filechooser

from lib import api_client

from components import screen

#------------------------------------------------------------------------------

_Debug = True

#------------------------------------------------------------------------------

class PrivateFileItem(TwoLineIconListItem):

    type = StringProperty()
    name = StringProperty()
    global_id = StringProperty()
    remote_path = StringProperty()
    customer = StringProperty()
    size = NumericProperty(0)

    def get_secondary_text(self):
        sec_text = ''
        if _Debug:
            print('PrivateFileItem.get_secondary_text', self.global_id, sec_text)
        return '[color=dddf]%s[/color]' % sec_text

    def on_pressed(self):
        if _Debug:
            print('PrivateFileItem.on_pressed', self)


class UploadPrivateFile(OneLineIconListItem):

    def on_pressed(self):
        if _Debug:
            print('UploadPrivateFile.on_pressed', self)


class PrivateFilesScreen(screen.AppScreen):

    def get_title(self):
        return 'private files'

    def get_icon(self):
        return 'file-lock'

    def populate(self, *args, **kwargs):
        pass

    def on_created(self):
        api_client.add_model_listener('private_file', listener_cb=self.on_private_file)
        self.populate()

    def on_destroying(self):
        api_client.remove_model_listener('private_file', listener_cb=self.on_private_file)

    def on_enter(self, *args):
        self.ids.state_panel.attach(automat_id='service_my_data')

    def on_leave(self, *args):
        self.ids.state_panel.release()

    def on_private_file(self, payload):
        if _Debug:
            print('PrivateFilesScreen.on_private_file', payload)

    # @mainthread
    def on_upload_file_button_clicked(self, *args):
        if _Debug:
            print('PrivateFilesScreen.on_upload_file_button_clicked', args)
        raw_path = filechooser.open_file(
            title="Upload new file",
            preview=True,
            show_hidden=False,
            on_selection=self.on_upload_file_selected,
        )
        if _Debug:
            print('raw_path', raw_path)

    def on_upload_file_selected(self, *args, **kwargs):
        if _Debug:
            print('PrivateFilesScreen.on_upload_file_selected', args, kwargs)

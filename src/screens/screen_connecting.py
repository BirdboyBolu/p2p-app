from kivy.metrics import dp
from kivy.clock import Clock

#------------------------------------------------------------------------------

from components import screen
from components import styles
from components import buttons

from lib import api_client
from lib import websock

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------


class NetworkServiceElement(buttons.CustomRaisedFlexButton):
    pass


class ConnectingScreen(screen.AppScreen):

    fetch_services_list_task = None
    known_services = {}
    state_panel_attached = False

    # def get_icon(self):
    #     return 'lan-pending'

    def get_title(self):
        return 'network services'

    def is_closable(self):
        return False

    def on_enter(self, *args):
        if not self.state_panel_attached:
            self.state_panel_attached = self.ids.state_panel.attach(automat_id='p2p_connector')
        Clock.schedule_once(self.schedule_nw_task)

    def on_leave(self, *args):
        self.ids.state_panel.release()
        self.state_panel_attached = False
        self.unschedule_nw_task()

    def on_services_list_result(self, resp):
        if _Debug:
            print('ConnectingScreen.on_services_list_result', len(self.known_services))
        if not websock.is_ok(resp):
            self.known_services.clear()
            self.ids.services_list.clear_widgets()
            return
        services_by_state = {}
        services_by_name = {}
        count_total = 0.0
        count_on = 0.0
        for svc in websock.response_result(resp):
            st = svc.get('state')
            if not svc.get('enabled'):
                continue
            if st not in services_by_state:
                services_by_state[st] = {}
            services_by_state[st][svc['name']] = svc
            services_by_name[svc['name']] = svc
            count_total += 1.0
            if st == 'ON':
                count_on += 1.0
        if not self.known_services:
            for st in ['ON', 'STARTING', 'DEPENDS_OFF', 'INFLUENCE', 'STOPPING', 'OFF', ]:
                for svc_name in sorted(services_by_state.get(st, {}).keys()):
                    svc = services_by_state[st][svc_name]
                    if svc.get('enabled'):
                        clr = self.get_service_color(svc.get('state'))
                    else:
                        clr = styles.app.color_btn_disabled
                    lbl = self.get_service_label(svc)
                    service_label = NetworkServiceElement(text=lbl)
                    service_label.md_bg_color = clr
                    self.ids.services_list.add_widget(service_label)
                    self.known_services[svc['name']] = service_label
        else:
            for svc_name in services_by_name.keys():
                svc = services_by_name[svc_name]
                if svc.get('enabled'):
                    clr = self.get_service_color(svc.get('state'))
                else:
                    clr = styles.app.color_btn_disabled
                service_label = self.known_services.get(svc['name'])
                if not service_label:
                    lbl = self.get_service_label(svc)
                    service_label = NetworkServiceElement(text=lbl)
                    service_label.md_bg_color = clr
                    self.ids.services_list.add_widget(service_label)
                    self.known_services[svc['name']] = service_label
                else:
                    service_label.md_bg_color = clr
        services_by_name.clear()
        services_by_state.clear()

    def schedule_nw_task(self, *a, **kw):
        if not self.fetch_services_list_task:
            Clock.schedule_once(self.populate)
            self.fetch_services_list_task = Clock.schedule_interval(self.populate, 0.5)

    def unschedule_nw_task(self, *a, **kw):
        if self.fetch_services_list_task:
            Clock.unschedule(self.fetch_services_list_task)
            self.fetch_services_list_task = None

    def populate(self, *args, **kwargs):
        if _Debug:
            print('ConnectingScreen.populate')
        if not self.state_panel_attached:
            self.state_panel_attached = self.ids.state_panel.attach(automat_id='p2p_connector')
        api_client.services_list(cb=self.on_services_list_result)

    def get_service_label(self, svc):
        txt = '[size=14sp][b]{}[/b][/size]'.format(svc['name'].replace('service_', ''))
        if svc['depends']:
            txt += '[size=10sp][color=#888888]\ndepend on:[/color]'
            for d in svc['depends']:
                txt += '\n[color=#555555] + {}[/color]'.format(d.replace('service_', ''))
            txt += '[/size]'
        return txt

    def get_service_color(self, st):
        clr = styles.app.color_btn_disabled
        if st == 'DEPENDS_OFF':
            clr = self.theme_cls.primary_light
        elif st in ['NOT_INSTALLED', 'OFF', ]:
            clr = styles.app.color_btn_disabled
        elif st in ['INFLUENCE', ]:
            clr = self.theme_cls.primary_light
        elif st in ['STARTING', 'STOPPING', ]:
            clr = styles.app.color_btn_pending_yellow_1
        else:
            clr = self.theme_cls.accent_light if st == 'ON' else self.theme_cls.primary_light
        return clr

import dearpygui.dearpygui as dpg
from .base import BaseView

class MainView(BaseView):
    def build(self):
        with dpg.group(tag='main_group', show=True):
            with dpg.group(horizontal=True):
                with dpg.group():

                    # timer slider
                    with dpg.group():
                        self.add_slider_text(
                            tag='match_time',
                            width=168, height=20,
                            min_value=1, max_value=25,
                            default_value=int(self.config.settings.get('timings', 'match_time')),
                            callback=self.callbacks.update_estimate,
                            user_data=('', ' minute', ['match_time', 'match_time_2'])
                        )
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('', tag='estimated_values')
                            self.callbacks.update_estimate(None, self.config.settings.get('timings', 'match_time'))

                    # buttons
                    dpg.add_spacer()
                    with dpg.group(horizontal=True):

                        # settings icon
                        dpg.add_button(label='P', width=36, height=28, callback=self.callbacks.show_settings_group)
                        dpg.bind_item_font(dpg.last_item(), self.icon_font)
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('settings')

                        # the loopy icon
                        dpg.add_button(label='Ó', width=36, height=28, callback=self.callbacks.oops_button)
                        dpg.bind_item_font(dpg.last_item(), self.icon_font)
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('retry dc / rc (oops)')

                        # the circle icon
                        dpg.add_button(label='O', width=36, height=28, tag='toggle_button', callback=self.callbacks.toggle_button)
                        dpg.bind_item_font(dpg.last_item(), self.icon_font)
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('hide brawlhalla window', tag='toggle_button_tooltip')

                        # the power button icon
                        dpg.add_button(label='\\', width=36, height=28, tag='launch_button', callback=self.callbacks.launch_button)
                        dpg.bind_item_font(dpg.last_item(), self.icon_font)
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('start brawlhalla', tag='launch_button_tooltip')

                    # stats
                    dpg.add_spacer()
                    with dpg.group(horizontal=True):

                        # games
                        dpg.add_button(label='0', width=20, height=20, tag='total_games')
                        dpg.bind_item_theme(dpg.last_item(), '__gameTextTheme')
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('total games')

                        # gold
                        dpg.add_button(label='0', width=66, height=20, tag='total_gold')
                        dpg.bind_item_theme(dpg.last_item(), '__goldTextTheme')
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('total gold')

                        # exp
                        dpg.add_button(label='0', width=66, height=20, tag='total_exp')
                        dpg.bind_item_theme(dpg.last_item(), '__expTextTheme')
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('total exp')

                # biiig run button
                dpg.add_button(label='â', tag='run_button', width=84, height=83, callback=self.callbacks.run_button)
                dpg.bind_item_font(dpg.last_item(), self.icon_font)
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('start', tag='run_button_tooltip')

            # status text
            dpg.add_spacer()
            dpg.add_button(label='inactive', width=260, height=24, tag='farm_status')
            dpg.bind_item_theme(dpg.last_item(), '__statusTextTheme')

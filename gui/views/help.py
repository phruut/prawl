import dearpygui.dearpygui as dpg
from .base import BaseView

class HelpView(BaseView):
    def build(self):
        with dpg.group(tag='help_group', show=False):
            with dpg.group(horizontal=True):

                # back button
                dpg.add_button(label='P', callback=self.callbacks.show_settings_group)
                dpg.bind_item_font(dpg.last_item(), self.icon_font)

            with dpg.collapsing_header(label='instructions', bullet=True):
                dpg.add_text('1. make a custom game room', indent=8)
                dpg.add_text('2. apply the settings below', indent=8)
                dpg.add_text('3. select a legend to farm', indent=8)
                dpg.add_text('4. press the start button!', indent=8)
                dpg.add_spacer()
                with dpg.tree_node(label='GAME RULE'):
                    for text in ['game mode: crew battle', 'stocks: 99', 'match time: 25 minutes', 'mapset: (tournament) 1v1', 'max players: 2']:
                        dpg.add_text(text, bullet=True)
                dpg.add_spacer()
                with dpg.tree_node(label='LOBBY'):
                    for text in ['map selection: random', 'disable friend/clan join']:
                        dpg.add_text(text, bullet=True)

            with dpg.collapsing_header(label='faq', bullet=True):
                dpg.add_spacer()
                with dpg.tree_node(label='why crew battle?'):
                    dpg.add_text('because it has 25 minute game option and the less time you spend in game menus, the more exp youre gonna get (i think lol)', wrap=0)
                    self.hyperlink('cat 05/17/2024', 'https://discord.com/channels/829496409681297409/1240709211642527824/1240710940140503170')
                    dpg.add_text('xp and gold requires active participation and different modes calculate participation differently so bot is too dumb for ffa basically, because ffa requires actually doing damage and kills', wrap=0)
                    self.hyperlink('sovamorco 10/08/2023', 'https://discord.com/channels/829496409681297409/829503904190431273/1160557662145097898')

                with dpg.tree_node(label='exp rate limit'):
                    dpg.add_text('Around 5 hours or once you earn around 13000 XP, you have to stop farming for about 45-50 minutes to reset the XP limit.', wrap=0)
                    self.hyperlink('jeffriesuave 10/16/2023', 'https://discord.com/channels/829496409681297409/829503904190431273/1163246039197831198')
                    dpg.add_text('*most people are reporting a wait time between 30 to 60 minutes', wrap=0)

            dpg.add_spacer()
            with dpg.group(horizontal=True):
                dpg.add_button(label='check for updates', tag='update_button', callback=self.callbacks.update_button)
                dpg.add_text('', tag='update_status_text')
            dpg.add_button(label='download', tag='update_link', show=False)
            dpg.bind_item_theme(dpg.last_item(), '__hyperlinkTheme')

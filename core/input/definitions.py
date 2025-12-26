
# calculate left or right based on match time
def _calc_scrolls(interface, current_val, target_val, max_items=25):
    diff = (target_val - current_val) % max_items
    if diff <= max_items // 2:
        return interface.get('key_right'), diff, target_val
    else:
        return interface.get('key_left'), max_items - diff, target_val

# returns input sequences, removed live timing updates because it just over complicated everything and i lost track
def get_definitions(interface):

    W_GAMELOAD = interface.get('game_load_delay')
    W_RESTART = interface.get('game_restart_delay')
    W_DC_DELAY = interface.get('disconnect_delay')
    W_RC_DELAY = interface.get('reconnect_delay')
    W_QU_DELAY = interface.get('queue_delay')

    C_START_SPAM = interface.get('game_start_spam')
    C_RETRY_AMOUNT = interface.get('retry_amount')

    K_LEFT = interface.get('key_left')
    K_UP = interface.get('key_up')
    K_DOWN = interface.get('key_down')
    K_THROW = interface.get('key_throw')
    K_LIGHT = interface.get('key_light')
    K_HEAVY = interface.get('key_heavy')
    K_MENU = interface.get('key_menu')

    TIME_KEY, TIME_COUNT, TIME_VALUE = _calc_scrolls(interface, 20, interface.get('match_time'))

    return {
            # this is to stop the farmer loop immidiately on special use cases like lobby setup
            'stop_farmer': [('status', 'stopped')],

            # wait before starting
            'wait_restart': [
                ('countdown', W_RESTART, 'starting game in {}...')
            ],

            # spam through results / start match
            'spam_menu': [
                ('status', 'spamming through menu!'),
                ('press', K_LIGHT, {'count': C_START_SPAM}),
            ],
            'spam_menu_net': [
                ('status', 'spamming, waiting for connection...'),
                ('retry_net', {'mode': 'connect', 'attempts': C_START_SPAM}, [
                    ('press', K_LIGHT),
                ]),
                ('countdown', W_GAMELOAD, 'stabilizing connection {}s...')
            ],

            # wait for match load (only used in online mode now )
            'wait_match': [
                ('countdown', W_GAMELOAD, 'waiting for game {}...')
            ],
            'wait_match_net': [
                ('status', 'waiting for connection...'),
                ('retry_net', {'mode': 'connect', 'attempts': W_QU_DELAY}, [
                    ('wait', 1000),
                ]),
                ('countdown', W_GAMELOAD, 'stabilizing connection {}s...')
            ],

            # open esc menu, disconnect
            'disconnect': [
                ('status', 'open esc menu'),
                ('press', K_MENU, {'count': 2}),
                ('wait', W_DC_DELAY),
                ('status', 'try disconnect'),
                ('press', K_UP),
                ('press', K_LIGHT),

                # +fix mode now default
                ('press', K_MENU),
                ('wait', W_DC_DELAY),
                ('press', K_UP),
                ('press', K_LIGHT)
            ],
            'disconnect_hold': [
                ('status', 'open esc menu'),
                ('press', K_MENU), ('press', K_MENU, {'hold': 2000}),
                ('wait', W_DC_DELAY),
                ('status', 'try disconnect'),
                ('press', K_UP),
                ('press', K_LIGHT),
            ],
            'disconnect_net': [
                ('status', 'attempting disconnect...'),
                ('press', K_MENU),
                ('retry_net', {'mode': 'disconnect', 'attempts': C_RETRY_AMOUNT}, [
                    ('press', K_MENU),
                    ('wait', W_DC_DELAY),
                    ('press', K_UP),
                    ('press', K_LIGHT),
                    ('wait', 1000)
                ]),
                ('countdown', W_RC_DELAY, 'stabilizing disconnect {}s...')
            ],
            'disconnect_net_hold': [
                ('status', 'attempting disconnect...'),
                ('retry_net', {'mode': 'disconnect', 'attempts': C_RETRY_AMOUNT}, [
                    ('press', K_MENU), ('press', K_MENU, {'hold': 2000}),
                    ('wait', W_DC_DELAY),
                    ('press', K_UP),
                    ('press', K_LIGHT),
                    ('wait', 1000)
                ]),
                ('countdown', W_RC_DELAY, 'stabilizing disconnect {}s...')
            ],

            # reconnect to match
            'reconnect': [
                ('countdown', W_RC_DELAY, 'reconnecting in {}...'),
                ('status', 'pressing...'), ('press', K_LIGHT, {'count': 2})
            ],
            'reconnect_net': [
                ('status', 'attempting reconnect...'),
                ('retry_net', {'mode': 'connect', 'attempts': C_RETRY_AMOUNT}, [
                    ('press', K_LIGHT, {'count': 2}),
                    ('wait', 1000)
                ])
            ],

            # lobby setups
            'lobby_setup_gamerule': [
                ('status', 'GAME RULES'), ('press', K_HEAVY),
                ('status', 'GAME MODE: CREW BATTLE'), ('press', K_LEFT, {'count': 6}),
                ('status', 'LIVES: 99'), ('press', K_DOWN, {'count': 3}), ('press', K_LEFT, {'count': 3}),
                ('status', f'MATCH TIME: {TIME_VALUE}'), ('press', K_DOWN), ('press', TIME_KEY, {'count': TIME_COUNT}),
                ('status', 'DAMAGE: 50%'), ('press', K_DOWN, {'count': 2}), ('press', K_LEFT, {'count': 5}),
                ('status', 'GADGET SPAWN RATE: Disabled'), ('press', K_DOWN, {'count': 2}), ('press', K_LEFT),
                ('status', 'MAP SET: Tournament 1v1'), ('press', K_DOWN, {'count': 3}), ('press', K_LEFT, {'count': 2}),
                ('status', 'MAX PLAYERS: 2'), ('press', K_DOWN), ('press', K_LEFT, {'count': 2}),
            ],
            'lobby_setup_lobby': [
                ('status', 'LOBBY'), ('press', ']'),
                ('wait', 200),
                ('status', 'PRIVACY - FRIENDS: Off'), ('press', K_DOWN, {'count': 3}), ('press', K_LEFT),
                ('status', 'PRIVACY - GUILDMATES: Off'), ('press', K_DOWN), ('press', K_LEFT),
                ('status', 'MAP CHOOSING: Random'), ('press', K_DOWN, {'count': 2}), ('press', K_LEFT, {'count': 2}),
                ('status', 'ALLOW HANDICAPS: On'), ('press', K_DOWN, {'count': 2}), ('press', K_LEFT),
            ],
            'lobby_setup_party': [
                ('wait', 500),
                ('status', 'MANAGE PARTY'), ('press', K_THROW),
                ('status', 'Add Bot'), ('press', K_LIGHT, {'count': 2, 'delay': 500}),
                ('status', 'BOT - Lives: 89'), ('press', K_DOWN), ('press', K_LEFT, {'count': 10}),
                ('status', 'BOT - Dmg Done: 50%'), ('press', K_DOWN), ('press', K_LEFT, {'count': 5}),
                ('status', 'BOT - Dmg Taken: 50%'), ('press', K_DOWN), ('press', K_LEFT, {'count': 5}),
                ('status', 'switching to P1 menu...'), ('press', K_LIGHT), ('press', K_UP), ('press', K_LIGHT),
                ('status', 'P1 - Dmg Done: 50%'), ('press', K_DOWN, {'count': 2}), ('press', K_LEFT, {'count': 5}),
                ('status', 'P1 - Dmg Taken: 50%'), ('press', K_DOWN), ('press', K_LEFT, {'count': 5}),
                ('status', 'close MANAGE PARTY'), ('press', K_THROW)
            ],
            'lobby_setup_exit': [
                ('press', K_LIGHT),
                ('wait', 200)
            ]
}

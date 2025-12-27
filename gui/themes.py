import dearpygui.dearpygui as dpg

def create_fonts(config):
    with dpg.font_registry():
        main = dpg.add_font(config.main_font, config.theme.get('fonts', 'main_size'))
        icon = dpg.add_font(config.icon_font, config.theme.get('fonts', 'icon_size'))
        return main, icon

def create_themes(config):

    def c(key):
        return config.theme.get_col('colors', key)

    # main theme
    # ---------------------------------------------------
    with dpg.theme(tag='__windowTheme'):
        with dpg.theme_component(dpg.mvAll):

            # window
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0.0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0.0)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8.0,8.0)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4.0)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, c('bg_primary'))
            dpg.add_theme_color(dpg.mvThemeCol_Border, c('bg_primary'))
            dpg.add_theme_color(dpg.mvThemeCol_Text, c('text_primary'))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, c('text_primary_disabled'))

            # components
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 2.0,2.0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4.0)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, c('hover'))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, c('active'))
            dpg.add_theme_color(dpg.mvThemeCol_Header, c('bg_primary'))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, c('hover'))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, c('active'))

            # buttons
            dpg.add_theme_color(dpg.mvThemeCol_Button, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c('hover'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c('active'))

            # sliders
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3.0)
            dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 15.0)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, c('active'))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, c('bg_secondary'))

            # checkbox
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, c('active'))

            # child window
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 8.0)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4.0)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, c('bg_primary'))

            # scrollbar
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 4.0)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 8.0)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, c('transparent'))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, c('bg_primary'))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, c('hover_extra'))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, c('active'))

        # tooltip
        with dpg.theme_component(dpg.mvTooltip):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8.0,6.0)
            dpg.add_theme_style(dpg.mvStyleVar_PopupBorderSize, 0.0)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 4.0)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, c('bg_quaternary'))

    # center text themes
    # ---------------------------------------------------
    with dpg.theme(tag='__centerTitleTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, c('transparent'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c('transparent'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c('transparent'))
            dpg.add_theme_color(dpg.mvThemeCol_Text, c('active'))

    with dpg.theme(tag='__statusTextTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_Text, c('text_secondary_disabled'))

    with dpg.theme(tag='__gameTextTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_Text, c('stats_game'))

    with dpg.theme(tag='__goldTextTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_Text, c('stats_gold'))

    with dpg.theme(tag='__expTextTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c('bg_secondary'))
            dpg.add_theme_color(dpg.mvThemeCol_Text, c('stats_exp'))

    # other themes
    # ---------------------------------------------------
    with dpg.theme(tag="__hyperlinkTheme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, c('transparent'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c('transparent'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c('hyper_hover'))
            dpg.add_theme_color(dpg.mvThemeCol_Text, c('hyper_text'))

    with dpg.theme(tag='__blankButtonTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, c('transparent'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c('transparent'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c('transparent'))

    with dpg.theme(tag='__layoutTableTheme'):
        with dpg.theme_component(dpg.mvTable):
            dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 4.0, 0.0)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0.0, 0.0)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0.0, 0.0)

    with dpg.theme(tag='__activeButtonTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, c('active'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, c('active_hover'))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, c('hover_extra'))
            dpg.add_theme_color(dpg.mvThemeCol_Text, c('text_secondary'))

    with dpg.theme(tag='__groupBackgroundTheme1'):
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 2.0, 2.0)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 2.0,0.0)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0.0)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, c('bg_secondary'))
        with dpg.theme_component(dpg.mvTooltip):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8.0,4.0)

    with dpg.theme(tag='__groupBackgroundTheme2'):
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0.0)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8.0, 8.0)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, c('bg_tertiary'))

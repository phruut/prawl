from tkinter import W
import dearpygui.dearpygui as dpg

def create_fonts(main_font, icon_font):
    with dpg.font_registry():
        main = dpg.add_font(main_font, 15)
        icon = dpg.add_font(icon_font, 16)
        return main, icon

def create_themes():

    main_col_bg_primary = [42, 42, 45]
    main_col_bg_secondary = [48, 48, 52]
    main_col_text = [182, 185, 189]
    main_col_text_pink = [250, 206, 211]
    main_col_text_pink_dim = [215, 180, 184]
    main_col_text_disabled = [155, 161, 168]
    main_col_hover = [54, 54, 58]
    main_col_hover_extra = [60, 60, 66]
    main_col_active = [255, 114, 121]
    main_col_interact = [255, 114, 121]
    hyperlink_col_text = [100, 149, 238]
    hyperlink_col_hover = [29, 151, 236, 25]

    col_transparent = [0, 0, 0, 0]

    stat_col_game = [7, 190, 171]
    stat_col_gold = [213, 189, 4]
    stat_col_exp = [17, 175, 208]

    # center text themes
    # ---------------------------------------------------
    with dpg.theme(tag='__centerTitleTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, col_transparent)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, col_transparent)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, col_transparent)
            dpg.add_theme_color(dpg.mvThemeCol_Text, main_col_active)

    with dpg.theme(tag='__statusTextTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_Text, main_col_text_pink_dim)

    with dpg.theme(tag='__gameTextTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_Text, stat_col_game)

    with dpg.theme(tag='__goldTextTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_Text, stat_col_gold)

    with dpg.theme(tag='__expTextTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_Text, stat_col_exp)

    # other themes
    # ---------------------------------------------------
    with dpg.theme(tag="__hyperlinkTheme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, col_transparent)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, col_transparent)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, hyperlink_col_hover)
            dpg.add_theme_color(dpg.mvThemeCol_Text, hyperlink_col_text)

    with dpg.theme(tag='__blankButtonTheme'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, col_transparent)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, col_transparent)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, col_transparent)

    with dpg.theme(tag='__childWindowTheme'):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6,2)

    with dpg.theme(tag='__popupTheme'):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4)

    with dpg.theme(tag='__windowTheme'):
        with dpg.theme_component(dpg.mvAll):

            # main window
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, main_col_bg_primary)
            dpg.add_theme_color(dpg.mvThemeCol_Border, main_col_bg_primary)
            dpg.add_theme_color(dpg.mvThemeCol_Text, main_col_text)
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, main_col_text_disabled)

            # components
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8,8)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 2,2)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, main_col_hover)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, main_col_active)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, main_col_hover)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, main_col_active)

            # buttons
            dpg.add_theme_color(dpg.mvThemeCol_Button, main_col_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, main_col_hover)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, main_col_active)

            # sliders
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 4)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, main_col_interact)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, main_col_bg_secondary)

            # checkbox
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, main_col_interact)

            # child window
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 4)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, main_col_bg_primary)
            dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 4,4)

            # scrollbar
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 6)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, col_transparent)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, main_col_hover)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, main_col_hover_extra)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, main_col_active)

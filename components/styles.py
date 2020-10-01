from kivy.metrics import dp, sp

_Debug = True

def init(app):
    if _Debug:
        print('dp(1.0):', dp(1.0))
        print('sp(1.0):', sp(1.0))

    #--- FONT SIZE
    app.font_size_normal_absolute = 14
    app.font_size_small_absolute = 11
    app.font_size_large_absolute = 16
    app.font_size_icon_absolute = 14

    app.font_size_normal = sp(app.font_size_normal_absolute)
    app.font_size_small = sp(app.font_size_small_absolute)
    app.font_size_large = sp(app.font_size_large_absolute)
    app.font_size_icon = sp(app.font_size_icon_absolute)

    #--- PADDING
    app.button_text_padding_x = dp(5)
    app.button_text_padding_y = dp(5)
    app.text_input_padding_y = dp(5)

    #--- SCROLL BAR
    app.scroll_bar_width = dp(15)

    #--- COLORS
    app.color_transparent = (0,0,0,0)
    app.color_black = (0,0,0,1)
    app.color_white = (1,1,1,1)

    app.color_btn_text_light = (1,1,1,1)
    app.color_btn_text_dark = (.3,.7,1,1)
    app.color_btn_normal = (.2,.5,.8,1)
    app.color_btn_pressed = (.3,.6,.9,1)
    app.color_btn_inactive = (.1,.4,.7,1)
    app.color_btn_disabled = (.8,.8,.8,1)

    #--- SCREEN FRIENDS
    app.friend_record_padding_x = dp(5)
    app.friend_record_padding_y = dp(5)
    app.friend_record_height = sp(16) + dp(12)

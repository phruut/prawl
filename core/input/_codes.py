
# set mappings
VK_CODE = {
    'enter':13, 'esc':27, 'spacebar':32,
    'left':37, 'up':38, 'right':39, 'down':40,
    '0':48, '1':49, '2':50, '3':51, '4':52, '5':53, '6':54, '7':55, '8':56, '9':57,
    'a':65, 'b':66, 'c':67, 'd':68, 'e':69, 'f':70, 'g':71, 'h':72, 'i':73, 'j':74, 'k':75, 'l':76, 'm':77,
    'n':78, 'o':79, 'p':80, 'q':81, 'r':82, 's':83, 't':84, 'u':85, 'v':86, 'w':87, 'x':88, 'y':89, 'z':90,
    'numpad_0':96, 'numpad_1':97, 'numpad_2':98, 'numpad_3':99, 'numpad_4':100, 'numpad_5':101, 'numpad_6':102, 'numpad_7':103, 'numpad_8':104, 'numpad_9':105,
    'left_shift':160, 'right_shift':161, 'left_control':162, 'right_control':163,
    '+':187, ',':188, '-':189, '.':190, '/':191, '`':192, ';':186, '[':219, '\\':220, ']':221, "'":222
}

VK_NAME = {v: k for k, v in VK_CODE.items()}

EXTENDED_KEYS = {
    VK_CODE['left'],
    VK_CODE['up'],
    VK_CODE['right'],
    VK_CODE['down']
}

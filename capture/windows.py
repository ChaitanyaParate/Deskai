# from Xlib import display, X

# try:
#     _dsp = display.Display()
# except Exception:
#     _dsp = None


# NET_ACTIVE = _dsp.intern_atom("_NET_ACTIVE_WINDOW")
# NET_NAME = _dsp.intern_atom("_NET_WM_NAME")
# UTF8 = _dsp.intern_atom("UTF8_STRING")
# NET_PID = _dsp.intern_atom("_NET_WM_PID")

# def get_active_window():

#     if _dsp is None:
#         return None

#     root = _dsp.screen().root

#     prop = root.get_full_property(NET_ACTIVE, X.AnyPropertyType)
#     if not prop:
#         return None

#     window_id = prop.value[0]
#     window = _dsp.create_resource_object("window", window_id)

#     name_prop = window.get_full_property(NET_NAME, UTF8)

#     if name_prop:
#         if isinstance(name_prop.value, bytes):
#             title = name_prop.value.decode("utf-8", errors="ignore")
#         else:
#             title = str(name_prop.value)
#     else:
#         title = ""

#     pid_prop = window.get_full_property(NET_PID, X.AnyPropertyType)
#     pid = pid_prop.value[0] if pid_prop else None

#     return {
#         "window_id": hex(window_id),
#         "title": title,
#         "pid": pid,
#     }

# def shutdown():
#     _dsp.close()

from Xlib import display, X

try:
    _dsp = display.Display()
except Exception:
    _dsp = None

NET_NAME = _dsp.intern_atom("_NET_WM_NAME")
UTF8 = _dsp.intern_atom("UTF8_STRING")
NET_PID = _dsp.intern_atom("_NET_WM_PID")

def get_window_under_cursor():
    if _dsp is None:
        return None

    screen = _dsp.screen()
    root = screen.root

    pointer = root.query_pointer()

    if not pointer.child:
        return None  # cursor is on empty root background

    window = pointer.child

    # climb until we reach a real top-level client window
    while True:
        tree = window.query_tree()
        if tree.parent == root or tree.parent is None:
            break
        window = tree.parent

    if window == root:
        return None

    window_id = window.id

    name_prop = window.get_full_property(NET_NAME, UTF8)
    title = (
        name_prop.value.decode("utf-8", errors="ignore")
        if name_prop and isinstance(name_prop.value, bytes)
        else ""
    )

    pid_prop = window.get_full_property(NET_PID, X.AnyPropertyType)
    pid = pid_prop.value[0] if pid_prop else None

    return {
        "window_id": hex(window_id),
        "title": title,
        "pid": pid,
    }

def shutdown():
    if _dsp:
        _dsp.close()

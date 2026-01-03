from Xlib import display, X

try:
    _dsp = display.Display()
except Exception:
    _dsp = None

NET_NAME = _dsp.intern_atom("_NET_WM_NAME")
UTF8 = _dsp.intern_atom("UTF8_STRING")
NET_PID = _dsp.intern_atom("_NET_WM_PID")

# ---- Geta window id title and pid of window under curser ----

def get_window_under_cursor():
    if _dsp is None:
        return None

    screen = _dsp.screen()
    root = screen.root

    pointer = root.query_pointer()

    if not pointer.child:
        return None 

    window = pointer.child

    
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

import time
import numpy as np
import cv2
from Xlib import X
from .windows import get_window_under_cursor, _dsp
from .backend import get_backend

def capture_active_window():

    env = get_backend()
    if env == "x11":
        
        info = get_window_under_cursor()
        if info is None:
            return None

        window_id = int(info["window_id"], 16)

        window = _dsp.create_resource_object("window", window_id)

        geom = window.get_geometry()
        width, height = geom.width, geom.height

        raw = window.get_image(
            0, 0,
            width, height,
            X.ZPixmap, 0xffffffff
        )

        if width <= 0 or height <= 0:
            return None


        image = np.frombuffer(raw.data, dtype=np.uint8)
        image = image.reshape((height, width, 4))
        image = image[:, :, :3]
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        return {
            "image": image,
            "window_id": info["window_id"],
            "timestamp": time.time()
        }
    return None

if __name__ == "__main__":
    data = capture_active_window()

    cv2.imshow("active window", data["image"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""A camera that renders an image only where it is on screen.

manim's cairo camera warps every image to its full on-screen size, off-screen parts included, so a
zoom that carries a picture to a hundred times the frame spends minutes per frame on pixels no one
sees. This one skips images wholly off screen and crops very large ones to the visible part first.
"""

import numpy as np
from manim import Camera, ImageMobject


class ClippingCamera(Camera):
    def display_image_mobject(self, image_mobject, pixel_array):
        if not self.is_in_frame(image_mobject):
            return
        ul, ur, dl = image_mobject.points[:3]
        w, h = ur[0] - ul[0], ul[1] - dl[1]
        fw, fh = self.frame_width, self.frame_height
        if w <= 1.5 * fw and h <= 1.5 * fh or abs(ur[1] - ul[1]) > 1e-9:  # small, or turned: draw as is
            return super().display_image_mobject(image_mobject, pixel_array)
        cx, cy = self.frame_center[:2]
        pad = 0.02 * fw
        left, right = max(ul[0], cx - fw / 2 - pad), min(ur[0], cx + fw / 2 + pad)
        top, bottom = min(ul[1], cy + fh / 2 + pad), max(dl[1], cy - fh / 2 - pad)
        arr = image_mobject.get_pixel_array()
        H, W = arr.shape[:2]
        c0, c1 = int(np.floor((left - ul[0]) / w * W)), int(np.ceil((right - ul[0]) / w * W))
        r0, r1 = int(np.floor((ul[1] - top) / h * H)), int(np.ceil((ul[1] - bottom) / h * H))
        c0, r0, c1, r1 = max(c0, 0), max(r0, 0), min(max(c1, c0 + 1), W), min(max(r1, r0 + 1), H)
        part = ImageMobject(arr[r0:r1, c0:c1])
        x0, x1 = ul[0] + c0 / W * w, ul[0] + c1 / W * w
        y0, y1 = ul[1] - r0 / H * h, ul[1] - r1 / H * h
        part.points = np.array([[x0, y0, 0], [x1, y0, 0], [x0, y1, 0], [x1, y1, 0]])
        part.resampling_algorithm = image_mobject.resampling_algorithm
        return super().display_image_mobject(part, pixel_array)

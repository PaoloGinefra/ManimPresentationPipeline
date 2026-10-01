"""Turn the recap video into the README's GIF: every few frames, scaled down, one shared palette.

    uv run python docs/recap/gif.py <video.mp4> <out.gif>
"""
import sys

import av
from PIL import Image

WIDTH, FPS = 960, 12


def main(src: str, out: str) -> None:
    stream = av.open(src)
    rate = float(stream.streams.video[0].average_rate)
    step = max(1, round(rate / FPS))
    frames = []
    for i, frame in enumerate(stream.decode(video=0)):
        if i % step == 0:
            im = frame.to_image()
            frames.append(im.resize((WIDTH, round(im.height * WIDTH / im.width)), Image.LANCZOS))
    # one palette for every frame, from the most colourful one: the deck uses few colours, so this
    # keeps them exact and the file small
    palette = max(frames, key=lambda im: len(im.getcolors(1 << 20) or [])).quantize(colors=64)
    quantized = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
    quantized[0].save(out, save_all=True, append_images=quantized[1:], duration=round(1000 / FPS), loop=0,
                      optimize=True)


if __name__ == "__main__":
    main(*sys.argv[1:3])

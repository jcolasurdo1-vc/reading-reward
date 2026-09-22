"""Generate PWA icons: navy rounded tile with the gold car from the progress track."""
from PIL import Image, ImageDraw

NAVY, GOLD, INK, GLASS, TIRE = "#1b2f57", "#ffcc33", "#5a4200", "#bfe4ff", "#222222"

def car(d, cx, cy, s):
    # s = scale factor (1 unit = s px); geometry mirrors the SVG car in index.html
    d.rounded_rectangle([cx-20*s, cy-11*s, cx+20*s, cy+4*s], radius=5*s, fill=GOLD, outline=INK, width=max(1,int(2*s)))
    d.polygon([(cx-12*s, cy-11*s), (cx-6*s, cy-21*s), (cx+8*s, cy-21*s), (cx+14*s, cy-11*s)], fill=GOLD, outline=INK)
    d.rectangle([cx-4*s, cy-19*s, cx+6*s, cy-12*s], fill=GLASS)
    for wx in (-11, 11):
        d.ellipse([cx+wx*s-5*s, cy+5*s-5*s, cx+wx*s+5*s, cy+5*s+5*s], fill=TIRE, outline=INK, width=max(1,int(1.5*s)))

def tile(size, radius_frac, pad_frac, road=True):
    im = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,size-1,size-1], radius=int(size*radius_frac), fill=NAVY)
    if road:
        y = int(size*0.62); h = int(size*0.16)
        d.rounded_rectangle([int(size*0.08), y-h//2, int(size*0.92), y+h//2], radius=h//2, fill="#3a3f4b")
        dash = int(size*0.06); gap = int(size*0.045); x = int(size*0.14)
        while x < int(size*0.86):
            d.rectangle([x, y-int(size*0.008), min(x+dash, int(size*0.86)), y+int(size*0.008)], fill="#f6e9a8"); x += dash+gap
    s = size/64.0 * (1-pad_frac)
    car(d, size*0.5, size*0.62 - 2*s, s)
    return im

for name, size, r, pad in [("icon-32",32,.2,0), ("icon-192",192,.2,0), ("icon-512",512,.2,0), ("apple-touch-icon",180,0,0)]:
    tile(size, r, pad).save(f"{name}.png")
# Maskable: full-bleed square, content inside the safe 80% circle.
m = Image.new("RGBA", (512,512), NAVY); d = ImageDraw.Draw(m)
inner = tile(512, 0, 0.25); m.alpha_composite(inner); m.save("maskable-512.png")
print("ok")

"""
Remove AI platform watermark ("图片由AI生成") from generated images.
Strategy: sample background color from surrounding area, paint over watermark region.
The sketch-notes style has uniform cream/beige background at bottom-right.
"""

from PIL import Image, ImageDraw
import os
import sys

def remove_watermark(input_path: str, output_path: str = None):
    img = Image.open(input_path).convert("RGB")
    w, h = img.size
    
    # Watermark "图片由AI生成" is in bottom-right corner, BELOW @Testkid
    # Cover generously from ~70px above bottom to ensure full coverage
    wm_margin_bottom = 0                           # flush to bottom
    wm_height = max(55, int(h * 0.072))            # ~74px tall (from bottom up)
    wm_margin_right = 0                            # flush to right
    wm_width = max(180, int(w * 0.34))             # ~261px wide
    
    wm_box = (
        w - wm_width - wm_margin_right,
        h - wm_height - wm_margin_bottom,
        w - wm_margin_right,
        h - wm_margin_bottom
    )
    
    # Sample background color: take pixels OUTSIDE watermark box but nearby
    # Sample from area just above and left of the watermark
    sample_region = (
        w - wm_width - wm_margin_right - 10,    # slightly more left
        h - wm_height - wm_margin_bottom - 25,  # above watermark + @Testkid
        w - wm_margin_right + 5,
        h - wm_height - wm_margin_bottom - 5
    )
    
    # Clamp to image bounds
    sample_region = (
        max(0, sample_region[0]),
        max(0, sample_region[1]),
        min(w, sample_region[2]),
        min(h, sample_region[3])
    )
    
    if sample_region[2] <= sample_region[0] or sample_region[3] <= sample_region[1]:
        # Fallback: use bottom-left area for sampling (should be same bg)
        sample_region = (0, h - 50, min(200, w), h)
    
    # Extract sample area and compute median color (robust against any stray marks)
    import statistics
    sample_img = img.crop(sample_region)
    pixels = list(sample_img.getdata())
    
    # Filter out outlier dark pixels (text/markings) - keep only light bg pixels
    brightness = [(r + g + b) / 3 for r, g, b in pixels]
    threshold = sum(brightness) / len(brightness) * 0.85  # keep brighter pixels
    bg_pixels = [p for p, b in zip(pixels, brightness) if b >= threshold]
    
    if len(bg_pixels) < 10:
        bg_pixels = pixels  # fallback
    
    # Median RGB for natural look
    r_median = statistics.median([p[0] for p in bg_pixels])
    g_median = statistics.median([p[1] for p in bg_pixels])
    b_median = statistics.median([p[2] for p in bg_pixels])
    
    fill_color = (int(r_median), int(g_median), int(b_median))
    
    # Paint over watermark region
    draw = ImageDraw.Draw(img)
    draw.rectangle(wm_box, fill=fill_color)
    
    # Save
    if output_path is None:
        output_path = input_path  # overwrite
    img.save(output_path, "PNG", quality=95)
    
    print(f"Done: {input_path} -> {output_path}")
    print(f"  Image size: {w}x{h}")
    print(f"  Watermark box: {wm_box}")
    print(f"  Fill color (median bg): RGB{fill_color}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_watermark.py <image_path> [output_path]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    remove_watermark(input_file, output_file)

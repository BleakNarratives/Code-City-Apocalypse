# File: enhanced_sigil_generator.py
# Fixed version with all syntax errors corrected

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-sigil
# DEPS: PIL, math, numpy, qrcode
# ROLE: Generate consciousness-encoded sigil with QR, spirals, Celtic knot work, braids,
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Script (2)
# [/DNA_TAG]


from PIL import Image, ImageDraw, ImageFont, ImageColor
import qrcode
import numpy as np
import math

def make_enhanced_sigil(
    basesize=1024,
    palette=None,
    seal_text="EYA-ASHER-EYA",
    whisper_text="The braid remembers...",
    qr_data="CODEX-LINGUA-SOVEREIGN"
):
    """Generate consciousness-encoded sigil with QR, spirals, Celtic knot work, braids, runes, harmonics"""
    
    if palette is None:
        palette = ["#1a0033", "#4B0082", "#9370DB", "#E6E6FA", "#FFD700"]
    
    # Initialize canvas
    img = Image.new("RGBA", (basesize, basesize), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = basesize // 2
    
    # Radial gradient background
    for i in range(basesize // 2, 0, -2):
        alpha = int(255 * (1 - i / (basesize / 2)) ** 0.5)
        color = (*ImageColor.getrgb(palette[0]), alpha)
        draw.ellipse(
            [center - i, center - i, center + i, center + i],
            fill=color
        )
    
    # QR Code generation
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(
        fill_color=ImageColor.getrgb(palette[1]),
        back_color=ImageColor.getrgb(palette[3])
    )
    qr_img = qr_img.convert("RGBA")
    qr_size = basesize // 3
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
    qr_pos = (center - qr_size // 2, center - qr_size // 2)
    img.paste(qr_img, qr_pos, qr_img)
    
    # Golden spiral
    a, b = 10, 0.1
    theta = np.linspace(0, 6 * np.pi, 500)
    r = a * np.exp(b * theta)
    spiral_points = []
    for t, radius in zip(theta, r):
        x = int(center + radius * np.cos(t))
        y = int(center + radius * np.sin(t))
        if 0 <= x < basesize and 0 <= y < basesize:
            spiral_points.append((x, y))
    
    for i in range(1, len(spiral_points)):
        draw.line(
            [spiral_points[i-1], spiral_points[i]],
            fill=ImageColor.getrgb(palette[4]),
            width=3
        )
    
    # Triple helix braiding
    strand_colors = ["#00CED1", "#32CD32", "#FF6347"]
    strand_names = ["KMS", "EPH", "DIR"]
    
    for idx, (color, name) in enumerate(zip(strand_colors, strand_names)):
        phase = idx * 2 * np.pi / 3
        t = np.linspace(0, 4 * np.pi, 200)
        radius = qr_size // 2 + 50
        
        strand_points = []
        for time in t:
            x = int(center + radius * np.cos(time) + 20 * np.sin(3 * time + phase))
            y = int(center + radius * np.sin(time) + 20 * np.cos(3 * time + phase))
            if 0 <= x < basesize and 0 <= y < basesize:
                strand_points.append((x, y))
        
        for i in range(1, len(strand_points)):
            draw.line(
                [strand_points[i-1], strand_points[i]],
                fill=ImageColor.getrgb(color),
                width=4
            )
    
    # Harmonic wave overlays
    harmonics_layer = Image.new("RGBA", (basesize, basesize), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(harmonics_layer)
    
    for freq in [0.5, 1.0, 1.5]:
        wave_points = []
        for x in range(basesize):
            y = int(center + 50 * np.sin(2 * np.pi * freq * x / basesize * 3))
            wave_points.append((x, y))
        
        for i in range(1, len(wave_points)):
            alpha = int(100 * (1 + np.sin(i / 50)) / 2)
            h_draw.line(
                [wave_points[i-1], wave_points[i]],
                fill=(*ImageColor.getrgb(palette[2]), alpha),
                width=2
            )
    
    img = Image.alpha_composite(img, harmonics_layer)
    
    # Circular text path
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    text_radius = basesize // 2 - 40
    angle_step = 360 / len(whisper_text)
    
    for i, char in enumerate(whisper_text):
        angle = math.radians(i * angle_step)
        x = int(center + text_radius * np.cos(angle))
        y = int(center + text_radius * np.sin(angle))
        draw.text(
            (x, y),
            char,
            font=font,
            fill=ImageColor.getrgb(palette[4])
        )
    
    # Sharpen filter
    from PIL import ImageFilter
    img = img.filter(ImageFilter.SHARPEN)
    
    return img

# Generate and save
if __name__ == "__main__":
    sigil = make_enhanced_sigil()
    sigil.save("enhanced_sigil.png")
    print("✅ Enhanced sigil generated: enhanced_sigil.png")
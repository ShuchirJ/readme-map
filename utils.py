import colorsys

def generate_shades(hex_color, num_shades):
    """
    Generate lighter and darker shades of a given hex color.

    Args:
        hex_color (str): Color in hex format, e.g. "#3498db"
        num_shades (int): Number of shades to generate

    Returns:
        List[str]: List of hex color strings
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)

    shades = []
    for i in range(num_shades):
        # Vary lightness from 0.4 to 0.8
        new_l = 0.4 + (0.4 * i / max(num_shades-1, 1))
        nr, ng, nb = colorsys.hls_to_rgb(h, new_l, s)
        shade = "#{:02x}{:02x}{:02x}".format(int(nr*255), int(ng*255), int(nb*255))
        shades.append(shade)
    return shades

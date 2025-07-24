import colorsys, requests, base64

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

def country_code_to_flag_emoji(country_code):
    """
    Convert a 2-letter country code to its emoji flag.
    Example: 'US' → '🇺🇸'
    """
    if len(country_code) != 2:
        raise ValueError("Country code must be 2 letters")
    base = 0x1F1E6  # Unicode codepoint for 'REGIONAL INDICATOR SYMBOL LETTER A'
    return ''.join(chr(base + ord(char.upper()) - ord('A')) for char in country_code)


def emoji_to_data_uri(code):
    url = f"https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/{code}.svg"
    response = requests.get(url).text
    return "data:image/svg+xml;base64," + base64.b64encode(response.encode('utf-8')).decode('utf-8')

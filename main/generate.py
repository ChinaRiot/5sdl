#!/usr/bin/env python3


import json
import re
import html
from pathlib import Path

def escape_html(text):
    return html.escape(str(text))

def parse_description(text):
    url_pattern = r'https?://[^\s<>"]+' 
    
    def replace_url(match):
        url = match.group(0)
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'
    
    return re.sub(url_pattern, replace_url, text)

def get_skillset_definitions():
    return {
        "Jack": "The difficulty of this map mainly comes from jacks.",
        "Chokepoints": "This map contains sections that are significantly more difficult than others.",
        "Technical": "This map has difficult or awkward patterning.",
        "Streams": "The difficulty of this map mainly comes from streams.",
        "Physicality": "This map has patterning that requires high jackspeed relative to it's difficulty level.",
        "Stamina": "This map requires sustained physicality, consistency, or reading over a long period of time.",
        "Gimmicky": "This map may vary in difficulty greatly between different players."
    }

def get_demon_face(tier):
    if tier >= 29:
        return "resources/ExtremeDemon.png"
    elif tier >= 27:
        return "resources/InsaneDemon.png"
    elif tier >= 25:
        return "resources/HardDemon.png"
    elif tier >= 23:
        return "resources/MediumDemon.png"
    else:
        return "resources/EasyDemon.png"

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def interpolate_color(tier):
    min_tier = 22.5
    max_tier = 30
    min_color = hex_to_rgb('fd4e72')
    max_color = hex_to_rgb('6962dc')
    
    tier = max(min_tier, min(max_tier, tier))
    
    if max_tier == min_tier:
        ratio = 0
    else:
        ratio = (tier - min_tier) / (max_tier - min_tier)
    
    r = min_color[0] + (max_color[0] - min_color[0]) * ratio
    g = min_color[1] + (max_color[1] - min_color[1]) * ratio
    b = min_color[2] + (max_color[2] - min_color[2]) * ratio
    
    return rgb_to_hex((r, g, b))

def generate_html(data):
    
    skillset_defs = get_skillset_definitions()
    demons_html = ""
    
    for demon in data["demons"]:
        tier = demon.get('tier', 22)
        color = interpolate_color(tier)
        demon_face = get_demon_face(tier)
        
        # uyyep
        escaped_name = escape_html(demon['name'])
        
        parsed_description = parse_description(escape_html(demon['description']))
        
        skillsets_html = ""
        skillsets = demon.get('skillsets', [])
        if skillsets:
            skillsets_html = '        <div class="skillsets">\n'
            for skillset in skillsets:
                definition = skillset_defs.get(skillset, "No definition available")
                skillsets_html += f'          <div class="skillset-box">\n'
                skillsets_html += f'            <span class="skillset-name">{escape_html(skillset)}</span>\n'
                skillsets_html += f'            <div class="skillset-tooltip">{escape_html(definition)}</div>\n'
                skillsets_html += '          </div>\n'
            skillsets_html += '        </div>\n'
        
        demons_html += f"""    <div class="demon-entry">
      <div class="demon-left">
        <div class="rank-badge">#{demon['rank']}</div>
        <img src="{demon_face}" alt="Demon face" class="demon-face">
      </div>
      <div class="demon-info">
        <h2 class="demon-name">{escaped_name}</h2>
        <p class="creator">Created by: {escape_html(demon['creator'])}</p>
        <p class="difficulty" style="color: {color};">Tier {tier}</p>
{skillsets_html}        <p class="description">{parsed_description}</p>
      </div>
    </div>
"""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['list_name']}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <div class="nav-container">
            <a href="index.html" class="nav-logo">5SDL</a>
            <ul class="nav-links">
                <li><a href="index.html" class="active">Demon List</a></li>
                <li><a href="info.html">Info</a></li>
            </ul>
        </div>
    </nav>
    
    <main>
    <div class="container">
        <header>
            <h1>{data['list_name']}</h1>
            <p class="description">{data['description']}</p>
        </header>
        
        <div class="list-container">
{demons_html}        </div>
        
        <footer>
            <p>Last updated: <span id="timestamp"></span></p>
            <script>
                document.getElementById('timestamp').textContent = new Date().toLocaleDateString();
            </script>
        </footer>
    </div>
    </main>
    <script src="background-loader.js"></script>
</body>
</html>
"""
    return html_content

def main():
    data_file = Path("data.json")
    
    if not data_file.exists():
        print(f"Error: {data_file} not found!")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    html = generate_html(data)
    
    index_file = Path("index.html")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated {index_file} with {len(data['demons'])} str")

if __name__ == "__main__":
    main()

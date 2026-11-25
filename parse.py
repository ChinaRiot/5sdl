#!/usr/bin/env python3


import json
import re
from pathlib import Path

def parse_list(input_text):
    demons = []
    lines = input_text.strip().split('\n')

    pattern = r'^(.+?)\s+/\s+(.+?):\s+([\d.]+)\s*\((.+?)\)\s*(.*)$'
    
    rank = 1    
    for line in lines:
        line = line.strip()
        if not line:
            # do the jiggy
            continue
        
        match = re.match(pattern, line)
        if match:
            creator, name, tier, skillsets_str, map_link = match.groups()
            
            skillsets = [s.strip().capitalize() for s in skillsets_str.split(',')]
            
            demon = {
                "rank": rank,
                "name": name.strip(),
                "creator": creator.strip(),
                "tier": float(tier),
                "skillsets": skillsets,
                "description": map_link.strip()
            }
            demons.append(demon)
            rank += 1
        else:
            print(f"Warning: Could not parse line: {line}")
    
    return demons

def main():
    input_file = Path("list.txt")
    output_file = Path("data.json")
    
    if not input_file.exists():
        print(f"Error: {input_file} not found!")
        print("Please create a list.txt file with the standardized format:")
        print("  Valedict / !!! IMPULSIVE <!!> WAVE !!!: 30.5 (streams, stamina)")
        return
    

    with open(input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()
    

    demons = parse_list(input_text)
    
    if not demons:  
        print("Error: No demons parsed from list.txt")
        return
    

    data = {
        "list_name": "5 Star Demon List",
        "description": "Community-based listing of the hardest ranked 5 star osu!mania maps.",
        "demons": demons
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Parsed {len(demons)} str from {input_file}")
    print(f"Generated {output_file}")
    print("\nNext: Run generate.py")

if __name__ == "__main__":
    main()

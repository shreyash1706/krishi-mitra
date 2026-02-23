from ingest_crop import clean_text
from pathlib import Path

fpath = Path("kb/kb_crop/agriculture_maha.md")
if fpath.exists():
    raw = fpath.read_text(encoding="utf-8", errors="replace")
    print(f"File size: {len(raw)} chars")
    
    # Check for the specific problematic snippet
    if "700</td>" in raw:
        print("Found '700</td>' in raw file.")
        
        # Run clean_text
        cleaned = clean_text(raw)
        
        if "700</td>" in cleaned:
            print("FAILED: '700</td>' still in cleaned text!")
        else:
            print("SUCCESS: '700</td>' was stripped from cleaned text.")
            
        # Check if table tags remain generally
        import re
        leftover_tags = re.findall(r'<[^>]+>', cleaned)
        if leftover_tags:
            print(f"Leftover tags found: {leftover_tags[:10]}")
        else:
            print("No HTML tags found in cleaned text.")
            
        # Preview around the cleaned area
        idx = cleaned.find("700")
        if idx != -1:
            print("\nPreview of cleaned text around '700':")
            print(cleaned[max(0, idx-100):idx+100])
    else:
        print("'700</td>' not found in raw file. Checking for '<td>'...")
        if "<td>" in raw:
            print("Found '<td>' in raw file.")
            cleaned = clean_text(raw)
            if "<td>" in cleaned:
                print("FAILED: '<td>' still in cleaned text!")
            else:
                print("SUCCESS: '<td>' was stripped.")
else:
    print(f"File not found: {fpath}")

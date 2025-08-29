#!/usr/bin/env python3
import hashlib, os, json, sys

CATALOG = "catalog.json"

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 tools/add_pcap.py <pcap_path> <tags_csv> [description]")
        sys.exit(1)

    pcap_path = sys.argv[1]
    tags_csv = sys.argv[2]
    desc = sys.argv[3] if len(sys.argv) > 3 else ""

    if not os.path.exists(pcap_path):
        print(f"Error: {pcap_path} not found")
        sys.exit(1)

    # Load catalog
    with open(CATALOG, "r") as f:
        catalog = json.load(f)

    fname = os.path.basename(pcap_path)
    size = os.path.getsize(pcap_path)
    digest = sha256sum(pcap_path)
    tags = [t.strip() for t in tags_csv.split(",") if t.strip()]

    entry = {
        "filename": fname,
        "sha256": digest,
        "size_bytes": size,
        "protocols": [],
        "tags": tags,
        "description": desc
    }

    # Prevent duplicates by sha256
    for i, it in enumerate(catalog.get("items", [])):
        if it.get("sha256") == digest:
            catalog["items"][i] = entry  # replace/update
            break
    else:
        catalog["items"].append(entry)

    with open(CATALOG, "w") as f:
        json.dump(catalog, f, indent=2)

    print(f"✔ Indexed {fname}")
    print(f"  size_bytes: {size}")
    print(f"  sha256    : {digest}")

if __name__ == "__main__":
    main()

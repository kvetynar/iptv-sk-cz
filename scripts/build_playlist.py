from urllib.request import Request, urlopen
from pathlib import Path

SOURCES = [
    "https://iptv-org.github.io/iptv/countries/sk.m3u",
    "https://iptv-org.github.io/iptv/countries/cz.m3u",
    "https://iptv-org.github.io/iptv/categories/movies.m3u",
    "https://iptv-org.github.io/iptv/categories/series.m3u",
]
out = ["#EXTM3U"]
seen = set()
for url in SOURCES:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=45) as response:
        lines = response.read().decode("utf-8-sig").splitlines()
    count = 0
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF:"):
            metadata = line
            extras = []
            i += 1
            while i < len(lines) and lines[i].strip().startswith("#") and not lines[i].strip().startswith("#EXTINF:"):
                extras.append(lines[i].strip())
                i += 1
            if i < len(lines):
                stream = lines[i].strip()
                if stream.startswith(("http://", "https://")) and stream not in seen:
                    seen.add(stream)
                    out.extend([metadata, *extras, stream])
                    count += 1
        i += 1
    if count == 0:
        raise RuntimeError(f"No channels loaded from {url}")
    print(f"{url}: {count} unique channels")
Path("sk-cz.m3u").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"Generated {len(seen)} unique streams")

#!/usr/bin/env python3
"""Mirror the approved DC TV feed without changing published episode identity."""
from pathlib import Path
from urllib.request import urlopen
from xml.etree import ElementTree as ET

SOURCE = 'https://media.leeheggan.tech/dc-tv/assets/podcast/feed.xml'
PUBLIC = 'https://leeheggan-droid.github.io/dctv-podcast/feed.xml'
ATOM = 'http://www.w3.org/2005/Atom'
for prefix, uri in [('itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd'),
                    ('atom', ATOM), ('content', 'http://purl.org/rss/1.0/modules/content/')]:
    ET.register_namespace(prefix, uri)


def mirror(previous: bytes, incoming: bytes) -> bytes:
    old, new = ET.fromstring(previous), ET.fromstring(incoming)
    current = new.findall('./channel/item')
    by_guid = {item.findtext('guid'): item for item in current}
    if not current or None in by_guid or len(by_guid) != len(current):
        raise ValueError('Empty feed or missing/duplicate episode GUID')
    for item in old.findall('./channel/item'):
        replacement = by_guid.get(item.findtext('guid'))
        if replacement is None:
            raise ValueError('Published episode disappeared or changed identity')
        if replacement.find('enclosure').attrib != item.find('enclosure').attrib:
            raise ValueError('Published audio URL, length or type changed')
        if replacement.findtext('pubDate') != item.findtext('pubDate'):
            raise ValueError('Published episode date changed')
    for item in current:
        enclosure = item.find('enclosure')
        if enclosure is None or not enclosure.get('url', '').startswith('https://') or int(enclosure.get('length', '0')) <= 0:
            raise ValueError('Invalid audio enclosure')
    if 'Lee Heggan' not in new.findtext('./channel/title', ''):
        raise ValueError('Missing Lee Heggan show branding')
    link = new.find(f'./channel/{{{ATOM}}}link')
    if link is not None:
        link.set('href', PUBLIC)
    return ET.tostring(new, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    target = Path(__file__).with_name('feed.xml')
    with urlopen(SOURCE, timeout=60) as response:
        updated = mirror(target.read_bytes(), response.read())
    staged = target.with_suffix('.xml.staged')
    staged.write_bytes(updated)
    staged.replace(target)
    print(f'Validated and mirrored {len(ET.fromstring(updated).findall("./channel/item"))} approved episodes')

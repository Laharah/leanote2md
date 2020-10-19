import json
import re
import sys
import functools
from pathlib import Path
from datetime import datetime

import lxml.etree
import base64
import hashlib

TIMEFMT = "%Y%m%dT%H%M%SZ"

resources = []


folder = Path(sys.argv[1])
def make_resource(url_match, f_name):
    path = folder / Path(f_name + "_files") / (url_match.group(1) + ".png")
    if not path.exists():
        path = folder / Path(f_name + "_files") / (url_match.group(1) + ".jpg")
    with open(path, "rb") as fin:
        data = fin.read()
    hsh = hashlib.md5(data).hexdigest()
    encoded = base64.encodebytes(data)
    resource = lxml.etree.Element("resource")
    data = lxml.etree.SubElement(resource, "data", encoding="base64")
    data.text = encoded
    mime = lxml.etree.SubElement(resource, "mime")
    mime.text = "image/png" if path.suffix == '.png' else "image/jpeg"
    width = lxml.etree.SubElement(resource, "width")
    width.text = ""
    height = lxml.etree.SubElement(resource, "height")
    height.text = ""
    duration = lxml.etree.SubElement(resource, "duration")
    duration.text = "0"
    re_attrib = lxml.etree.SubElement(resource, "resource-attributes")
    timestamp = lxml.etree.SubElement(re_attrib, "timestamp")
    timestamp.text = datetime.now().strftime(TIMEFMT)
    file_name = lxml.etree.SubElement(re_attrib, "file-name")
    file_name.text = ""
    resources.append(resource)
    return f":/{hsh}"


notes = []
files = {p.stem for p in folder.iterdir() if p.is_file()}
for f in files:
    with open(folder / f"{f}.leanote") as fin:
        j = json.load(fin)
    if j['notes'][0]['isMarkdown']:
        continue
    created = datetime.fromisoformat(j["notes"][0]["createdTime"])
    updated = datetime.fromisoformat(j["notes"][0]["updatedTime"])
    with open(folder / f"{f}.enex") as fin:
        xml = fin.read()
    xml = re.sub(
        r"<created>.*</created>",
        f"<created>{created.strftime(TIMEFMT)}</created>",
        xml,
    )
    xml = re.sub(
        r"<updated>.*</updated>",
        f"<updated>{updated.strftime(TIMEFMT)}</updated>",
        xml,
    )

    repl = functools.partial(make_resource, f_name=f)
    xml = re.sub(r"leanote://file/getImage\?fileId=([0-9a-fA-F]+)", repl, xml)
    note = re.search(r"<note>.*</note>", xml, re.MULTILINE | re.DOTALL)
    if not note:
        print(f)
        raise RuntimeError
    notes.append(note.group(0))

with open("full_notebook.enex", "w") as fout:
    fout.write(
        """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">
<en-export export-date="20201016T105124Z" application="leanote.desktop.app.darwin" version="2.6.2">\n"""
    )
    for note in notes:
        fout.write(note)
    for resource in resources:
        fout.write(lxml.etree.tostring(resource, pretty_print=True).decode())
    fout.write("</en-export>")

#!/usr/bin/env python3
"""Writes assets/favicon.svg: the logo PNG (argv[1], ~96px) clipped to a circle and embedded as a data URI."""
import base64
import pathlib
import sys

png = base64.b64encode(pathlib.Path(sys.argv[1]).read_bytes()).decode()
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
    '<clipPath id="c"><circle cx="50" cy="50" r="47"/></clipPath>'
    f'<image href="data:image/png;base64,{png}" x="-4" y="-4" width="108" height="108" clip-path="url(#c)"/>'
    "</svg>\n"
)
out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "favicon.svg"
out.write_text(svg)
print(f"wrote {out} ({len(svg)} bytes)")

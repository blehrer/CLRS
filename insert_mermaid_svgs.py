#!/usr/bin/env python
import nbformat
import os
import re
import subprocess
from pathlib import Path
import hashlib

NOTEBOOKS_GLOB = "*.ipynb"
ASSETS_DIR = "assets/mermaid"
MMDC_CMD = "mmdc"
MMDC_PUPPETEER_CONFIG = "mmdc-puppeteer-config.json"
MERMAID_BLOCK_PATTERN = r"```mermaid\s*\n([\s\S]+?)\n```"


def render_mermaid_to_svg(mermaid_code, svg_path):
    mmd_path = svg_path.with_suffix(".mmd")
    with open(mmd_path, "w") as f:
        f.write(mermaid_code)
    cmd = [
        MMDC_CMD,
        "-i",
        str(mmd_path),
        "-o",
        str(svg_path),
        "-b",
        "transparent",  # or "white"
        "-p",
        MMDC_PUPPETEER_CONFIG,
    ]
    print(f"[render] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    os.remove(mmd_path)
    print(f"[cleanup] Deleted temp file: {mmd_path}")


def get_svg_filename(mermaid_code):
    # Use a hash of the code for unique, repeatable filenames
    h = hashlib.sha256(mermaid_code.encode("utf-8")).hexdigest()[:8]
    return f"diagram-{h}.svg"


def md_img_pattern():
    p = r"("
    p += re.escape("![")
    p += r".*"
    p += re.escape(f"]({str(Path(ASSETS_DIR))}")
    p += r".*"
    p += re.escape(")")
    p += r"\s*)+"
    return re.compile(p, re.MULTILINE)


def remove_mermaid_svg_links(source):
    """
    Removes all SVG image links to assets/mermaid
    """
    pos = 0
    pieces = []
    for svg in md_img_pattern().finditer(source):
        pieces.append(source[pos : svg.start()])
        pos += svg.end()
    return "".join(pieces)


def process_notebook(nb_path: Path):
    nb = nbformat.read(nb_path, as_version=4)
    modified = False
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue

        # Find all mermaid code blocks
        matches = list(re.finditer(MERMAID_BLOCK_PATTERN, cell.source))
        if not matches:
            # Still need to remove dead links!
            new_source = cell.source
            if new_source != cell.source:
                cell.source = new_source
                modified = True
            continue

        new_source = update_md_cell(cell, nb_path)
        if new_source != cell.source:
            cell.source = new_source
            modified = True

    if modified:
        print(f"[update] Notebook updated: {nb_path}")
        nbformat.write(nb, nb_path)
    else:
        print(f"[skip] No changes needed: {nb_path}")


def update_md_cell(cell, nb_path: Path) -> str:
    nb_name = nb_path.name
    folder = ""
    if nb_name:
        folder = nb_name
        for s in nb_path.suffixes:
            folder = folder.removesuffix(s)
    new_source = ""
    last_end = 0
    cleaned_source = remove_mermaid_svg_links(cell.source)
    matches = list(re.finditer(MERMAID_BLOCK_PATTERN, cleaned_source))
    for match in matches:
        mermaid_code = match.group(1)
        svg_filename = get_svg_filename(mermaid_code)
        svg_path = Path(ASSETS_DIR) / folder / svg_filename
        # Render SVG if it doesn't exist
        if not svg_path.exists():
            svg_path.parent.mkdir(parents=True, exist_ok=True)
            render_mermaid_to_svg(mermaid_code, svg_path)
        else:
            print(f"[skip] SVG already exists: {svg_path}")
        # Insert image tag after code block
        new_source += cleaned_source[last_end : match.end()]
        new_source += f"\n\n![]({svg_path.as_posix()})\n"
        last_end = match.end()
    new_source += cleaned_source[last_end:]
    return new_source


def cleanup(dir: Path):
    if dir.exists() and dir.is_dir():
        for ext in ("*.svg", "*.mmd"):
            for file in dir.glob(ext):
                print(f"[delete] Removing old asset: {file}")
                file.unlink()
        for d in filter(lambda d: d.is_dir(), dir.iterdir()):
            cleanup(d)
    else:
        print(
            f"[info] No assets directory found at \
            {dir}, nothing to delete."
        )


def main():
    cleanup(Path(ASSETS_DIR))
    for nb_path in Path(".").glob(NOTEBOOKS_GLOB):
        print(f"[process] Checking notebook: {nb_path}")
        process_notebook(nb_path)


if __name__ == "__main__":
    main()

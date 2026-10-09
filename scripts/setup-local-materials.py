"""Restore the user-supplied PDFs into the dev-only viewer folder after a fresh clone.
Do not publish these files until redistribution rights are confirmed."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'private-materials';dest=ROOT/'public'/'materials';dest.mkdir(parents=True,exist_ok=True)
if not src.exists():raise SystemExit('Private source PDFs not found; obtain your local authorized copies before using the viewer.')
for f in src.glob('*.pdf'):shutil.copy2(f,dest/f.name)
print('Copied',len(list(src.glob('*.pdf'))),'PDFs for local development only.')

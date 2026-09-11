from pathlib import Path
import pymupdf

root = Path(__file__).resolve().parents[1]
source = root / "output" / "pdf"
target = root / "tmp" / "pdfs"
target.mkdir(parents=True, exist_ok=True)

for pdf_path in sorted(source.glob("*.pdf")):
    document = pymupdf.open(pdf_path)
    for page_number, page in enumerate(document):
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(1.7, 1.7), alpha=False)
        output = target / f"{pdf_path.stem}-page-{page_number + 1}.png"
        pixmap.save(output)
        print(output)

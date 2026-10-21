"""Render p1..p5.html to A4 pages and merge them into one PDF; report any page overflow."""
import sys, pathlib
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter

here = pathlib.Path(__file__).resolve().parent
pages = sorted(here.glob('p[0-9].html'))
out = here / (sys.argv[1] if len(sys.argv) > 1 else 'CATL_Ad-hoc_Opinion_Syz_21Oct2026.pdf')
writer = PdfWriter()
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    page = browser.new_page(viewport={'width': 794, 'height': 1123})
    for i, f in enumerate(pages, 1):
        page.goto(f.as_uri(), wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        # overflow check: last content block must end above the footer
        gap = page.evaluate("""() => {
            const pg = document.querySelector('.page'), ft = pg.querySelector('footer');
            const kids = [...pg.children].filter(e => e !== ft);
            const bottom = Math.max(...kids.map(e => e.getBoundingClientRect().bottom));
            return {gap: ft.getBoundingClientRect().top - bottom, scroll: pg.scrollHeight - pg.clientHeight};
        }""")
        print(f.name, gap)
        page.screenshot(path=str(here / f'preview_{i}.png'))
        tmp = here / f'_tmp_{i}.pdf'
        page.pdf(path=str(tmp), width='794px', height='1123px', print_background=True)
        writer.append(str(tmp))
        tmp.unlink()
    browser.close()
writer.write(str(out))
print('wrote', out)

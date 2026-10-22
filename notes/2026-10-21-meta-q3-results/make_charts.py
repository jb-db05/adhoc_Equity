"""Build the two SVG charts of the Meta Q3 2026 earnings update from the Bloomberg export."""
import datetime as dt
import statistics
import sys

import openpyxl

SPACE, BLUEBERRY, TIGER, GOLD, MINT, LINE = '#202945', '#4B5F80', '#FF6C0E', '#FFC545', '#3BAF90', '#D9D9D9'
END = dt.datetime(2026, 10, 21)
# results dates (after the US close); the reaction is the next session's close-to-close move
RESULTS = [dt.datetime(2025, 10, 29), dt.datetime(2026, 1, 28), dt.datetime(2026, 4, 29), dt.datetime(2026, 7, 29)]
MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()


def load(path):
    ws = openpyxl.load_workbook(path, data_only=True)['Sheet1']
    rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0] and r[1]]
    rows.sort(key=lambda r: r[0])
    return rows


def frame(w, h, l, r, t, b):
    return w, h, l, r, t, b, w - l - r, h - t - b


def axes(svg, W, H, L, R, T, B, PW, PH, yticks, ymap, fmt):
    for v in yticks:
        y = ymap(v)
        svg.append(f'<line x1="{L}" x2="{L + PW}" y1="{y:.1f}" y2="{y:.1f}" stroke="{LINE}" stroke-width="0.6"/>')
        svg.append(f'<text x="{L - 6}" y="{y + 3.5:.1f}" text-anchor="end" font-size="9" fill="{SPACE}">{fmt(v)}</text>')
    svg.append(f'<line x1="{L}" x2="{L}" y1="{T}" y2="{T + PH}" stroke="{SPACE}" stroke-width="1"/>')
    svg.append(f'<line x1="{L}" x2="{L + PW}" y1="{T + PH}" y2="{T + PH}" stroke="{SPACE}" stroke-width="1"/>')


def xmonths(svg, start, end, xmap, T, PH, step, with_year):
    d = dt.datetime(start.year, start.month, 1)
    i = 0
    while d <= end:
        if d >= start and i % step == 0:
            x = xmap(d)
            lab = f"{MONTHS[d.month - 1]} {str(d.year)[2:]}" if with_year or d.month == 1 else MONTHS[d.month - 1]
            svg.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{T + PH}" y2="{T + PH + 4}" stroke="{SPACE}" stroke-width="1"/>')
            svg.append(f'<text x="{x:.1f}" y="{T + PH + 15}" text-anchor="middle" font-size="9" fill="{SPACE}">{lab}</text>')
        d = dt.datetime(d.year + (d.month == 12), d.month % 12 + 1, 1)
        i += 1


def path(points, xmap, ymap):
    return 'M' + ' L'.join(f'{xmap(d):.1f},{ymap(v):.1f}' for d, v in points)


def price_chart(rows):
    start = END - dt.timedelta(days=366)
    pts = [(r[0], r[1]) for r in rows if start <= r[0] <= END]
    ma = [(r[0], r[5]) for r in rows if start <= r[0] <= END and r[5]]
    W, H, L, R, T, B, PW, PH = frame(335, 210, 38, 44, 10, 22)
    lo, hi = 480, 820
    xmap = lambda d: L + (d - start).total_seconds() / (END - start).total_seconds() * PW
    ymap = lambda v: T + (hi - v) / (hi - lo) * PH
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Nunito, Arial, sans-serif">']
    axes(svg, W, H, L, R, T, B, PW, PH, range(500, 801, 100), ymap, lambda v: f'{v:.0f}')
    xmonths(svg, start, END, xmap, T, PH, 2, False)
    svg.append(f'<path d="{path(ma, xmap, ymap)}" fill="none" stroke="{TIGER}" stroke-width="1.4"/>')
    svg.append(f'<path d="{path(pts, xmap, ymap)}" fill="none" stroke="{SPACE}" stroke-width="1.3"/>')
    px = dict(pts)
    days = sorted(px)
    for d in RESULTS:
        nxt = days[days.index(d) + 1]
        move = px[nxt] / px[d] - 1
        x, y = xmap(nxt), ymap(px[nxt])
        col = MINT if move > 0 else TIGER
        ly = y - 12 if move > 0 else y + 18
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#fff" stroke="{col}" stroke-width="1.6"/>')
        anchor = 'start' if x - L < 20 else 'middle'
        svg.append(f'<text x="{x + (4 if anchor == "start" else 0):.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="9.5" font-weight="800" fill="{col}" stroke="#fff" stroke-width="3" paint-order="stroke">{move * 100:+.0f}%</text>')
    last = pts[-1][1]
    y = ymap(last)
    svg.append(f'<rect x="{L + PW + 3}" y="{y - 8:.1f}" width="40" height="16" rx="4" fill="#fff" stroke="{SPACE}" stroke-width="1"/>')
    svg.append(f'<text x="{L + PW + 23}" y="{y + 3.5:.1f}" text-anchor="middle" font-size="9.5" font-weight="800" fill="{SPACE}">{last:.1f}</text>')
    svg.append('</svg>')
    return '\n'.join(svg)


def pe_chart(rows):
    start = END - dt.timedelta(days=365 * 3)
    pts = [(r[0], r[3]) for r in rows if start <= r[0] <= END and r[3]]
    avg = statistics.mean(v for _, v in pts)
    W, H, L, R, T, B, PW, PH = frame(335, 210, 30, 44, 10, 22)
    lo, hi = 10, 30
    xmap = lambda d: L + (d - start).total_seconds() / (END - start).total_seconds() * PW
    ymap = lambda v: T + (hi - v) / (hi - lo) * PH
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Nunito, Arial, sans-serif">']
    axes(svg, W, H, L, R, T, B, PW, PH, range(10, 31, 5), ymap, lambda v: f'{v:.0f}x')
    xmonths(svg, start, END, xmap, T, PH, 6, True)
    y = ymap(avg)
    svg.append(f'<line x1="{L}" x2="{L + PW}" y1="{y:.1f}" y2="{y:.1f}" stroke="{BLUEBERRY}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    svg.append(f'<path d="{path(pts, xmap, ymap)}" fill="none" stroke="{SPACE}" stroke-width="1.3"/>')
    last = pts[-1][1]
    y = ymap(last)
    svg.append(f'<rect x="{L + PW + 3}" y="{y - 8:.1f}" width="40" height="16" rx="4" fill="#fff" stroke="{SPACE}" stroke-width="1"/>')
    svg.append(f'<text x="{L + PW + 23}" y="{y + 3.5:.1f}" text-anchor="middle" font-size="9.5" font-weight="800" fill="{SPACE}">{last:.1f}x</text>')
    svg.append('</svg>')
    return '\n'.join(svg), avg, last


if __name__ == '__main__':
    rows = load(sys.argv[1])
    out = sys.argv[2]
    pe_svg, avg, last = pe_chart(rows)
    open(f'{out}/chart1-price.svg', 'w').write(price_chart(rows))
    open(f'{out}/chart2-pe.svg', 'w').write(pe_svg)
    print(f'P/E last {last:.1f}x, 3y average {avg:.1f}x')

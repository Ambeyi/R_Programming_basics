"""Render frequency tables as a standalone SVG without plotting dependencies."""
from html import escape

def render(bands):
    if not bands or max(b['count'] for b in bands) <= 0:
        raise ValueError('Chart requires a positive count')
    maximum = max(b['count'] for b in bands)
    height = 105 + 46*len(bands)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="{height}" viewBox="0 0 760 {height}" role="img" aria-labelledby="title desc">',
             '<title id="title">Synthetic age distribution</title>',
             '<desc id="desc">Counts in inclusive age bands. Data are simulated.</desc>',
             '<rect width="100%" height="100%" fill="#f8fafc"/>',
             '<g font-family="sans-serif" fill="#0f172a">',
             '<text x="24" y="32" font-size="22">Synthetic age distribution</text>',
             '<text x="24" y="57" font-size="13">Uniform integer sampling · counts by inclusive age band</text>']
    for i, band in enumerate(bands):
        y=80+i*46
        parts.extend([f'<text x="24" y="{y+21}">{escape(str(band["band"]))}</text>',
            f'<rect x="100" y="{y}" width="{500*band["count"]/maximum:.2f}" height="30" rx="4" fill="#2563eb"/>',
            f'<text x="620" y="{y+21}">{band["count"]}</text>'])
    return '\n'.join(parts+['</g></svg>'])+'\n'

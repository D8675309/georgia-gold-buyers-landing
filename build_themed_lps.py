#!/usr/bin/env python3
"""
Themed LP generator — Georgia Gold Buyers
Generates 8 theme×city landing pages by transforming lp-valdosta.html / lp-mcdonough.html.

Cities: valdosta, mcdonough  (preserve city-specific phones, addresses, maps, area copy)
Themes: coins, jewelry, silver, watches

Output: lp-{city}-{theme}.html (8 files)

Strategy: targeted string replacements on the source template per (city, theme).
Preserves all conversion tracking (gtag labels, POS Railway endpoint, __gads_fire).
"""

import re
import os
from pathlib import Path

REPO = Path(__file__).parent

# ----- THEME CONFIGS -----

THEMES = {
    'coins': {
        'title_short': 'Gold Coins',
        'title_kw_lower': 'gold coins',
        'h1_word': 'Gold Coins',           # replaces "Gold" in hero h1
        'meta_desc_topic': 'gold coins, bullion, US gold, silver coins & rare coin collections',
        'urgency_msg': 'Gold &amp; silver prices are near all-time highs',
        'widget_headline_topic': 'Coin Collection',
        'item_list_html': (
            'We pay top dollar for: <strong>American Gold Eagles</strong>, <strong>American Buffalo</strong>, '
            '<strong>Krugerrands</strong>, <strong>Canadian Maple Leafs</strong>, '
            '<strong>pre-1933 US gold</strong> (Saint-Gaudens, Liberty, Indian), '
            '<strong>Morgan &amp; Peace silver dollars</strong>, <strong>Mercury &amp; Roosevelt dimes</strong>, '
            '<strong>Walking Liberty halves</strong>, <strong>90% junk silver</strong>, '
            '<strong>silver bars &amp; rounds</strong>, <strong>gold bars</strong> (PAMP, Credit Suisse, Valcambi), '
            '<strong>commemorative coins</strong>, <strong>foreign gold &amp; silver coins</strong>, '
            '<strong>entire coin collections</strong>, and certified graded coins (PCGS, NGC, ANACS). '
            'Not sure what you have? Bring it in &mdash; we test and value every piece.'
        ),
        'expert_line': 'Sigma Metalytics verification + XRF analyzer for exact purity. We pay competitive premiums on bullion and numismatic coins.',
        'what_you_have': '1922 Peace dollar, 1/10oz Eagle, junk silver bag, dad\'s coin album...',
    },
    'jewelry': {
        'title_short': 'Gold Jewelry',
        'title_kw_lower': 'gold jewelry',
        'h1_word': 'Gold Jewelry',
        'meta_desc_topic': 'gold jewelry, chains, rings, bracelets, broken &amp; estate pieces',
        'urgency_msg': 'Gold prices are near all-time highs',
        'widget_headline_topic': 'Jewelry',
        'item_list_html': (
            'We buy: <strong>14k, 18k, 22k, &amp; 24k gold jewelry</strong>, <strong>broken &amp; tangled chains</strong>, '
            '<strong>diamond rings</strong>, <strong>engagement &amp; wedding bands</strong>, '
            '<strong>gold &amp; silver chains</strong> (rope, Cuban, Figaro), '
            '<strong>bracelets, earrings, pendants</strong>, '
            '<strong>class rings</strong>, <strong>dental gold</strong>, '
            '<strong>estate jewelry collections</strong>, <strong>sterling silver jewelry</strong>, '
            '<strong>platinum jewelry</strong>, <strong>signed pieces</strong> (Tiffany, Cartier, David Yurman), '
            '<strong>mismatched earrings</strong>, and <strong>any condition</strong> &mdash; tangled, broken, or kinked, '
            'we don\'t care. The gold is still gold.'
        ),
        'expert_line': 'XRF analyzer gives exact karat purity to 0.01%. We pay on live spot price, updated daily. No deductions for broken chains.',
        'what_you_have': '14k chain, broken earrings, grandma\'s ring, dental crowns...',
    },
    'silver': {
        'title_short': 'Silver',
        'title_kw_lower': 'silver',
        'h1_word': 'Silver',
        'meta_desc_topic': 'sterling silver, silver coins, flatware, tea sets & 90% junk silver',
        'urgency_msg': 'Silver prices are near multi-year highs',
        'widget_headline_topic': 'Silver Collection',
        'item_list_html': (
            'We buy: <strong>sterling silver flatware</strong> (Reed &amp; Barton, Gorham, Towle, Wallace), '
            '<strong>silver tea &amp; coffee sets</strong>, <strong>candelabras &amp; trays</strong>, '
            '<strong>90% junk silver</strong> (pre-1965 dimes, quarters, halves), '
            '<strong>Morgan &amp; Peace silver dollars</strong>, '
            '<strong>silver bars &amp; rounds</strong> (Engelhard, JM, Sunshine), '
            '<strong>American Silver Eagles</strong>, <strong>Canadian Silver Maples</strong>, '
            '<strong>sterling jewelry</strong>, <strong>silver bullion</strong>, '
            '<strong>Mexican &amp; foreign silver</strong>, '
            '<strong>antique silver pieces</strong>, and full estate collections. '
            'Even tarnished or damaged silver still has weight value &mdash; bring it in.'
        ),
        'expert_line': 'Sigma Metalytics confirms authenticity instantly. Precision scales calibrated daily. We pay weight + bullion premium on coins and bars.',
        'what_you_have': 'Sterling flatware set, junk silver roll, silver bars, tea service...',
    },
    'watches': {
        'title_short': 'Luxury Watches',
        'title_kw_lower': 'luxury watches',
        'h1_word': 'Luxury Watches',
        'meta_desc_topic': 'Rolex, Omega, Cartier, Breitling, Patek &amp; other luxury timepieces',
        'urgency_msg': 'Luxury watch demand is at record highs',
        'widget_headline_topic': 'Watch',
        'item_list_html': (
            'We buy: <strong>Rolex</strong> (Submariner, Daytona, Datejust, GMT, Explorer), '
            '<strong>Omega</strong> (Speedmaster, Seamaster, Constellation), '
            '<strong>Cartier</strong> (Tank, Santos, Pasha), '
            '<strong>Breitling</strong>, <strong>TAG Heuer</strong>, '
            '<strong>Patek Philippe</strong>, <strong>Audemars Piguet</strong>, '
            '<strong>Panerai</strong>, <strong>IWC</strong>, <strong>Tudor</strong>, '
            '<strong>vintage &amp; pre-owned luxury watches</strong>, '
            '<strong>gold &amp; two-tone pieces</strong>, '
            '<strong>watches with original box &amp; papers</strong> (premium offers), '
            '<strong>watches without papers</strong>, '
            '<strong>broken or non-running luxury watches</strong>, '
            'and estate watch collections. Not sure of authenticity? We verify every piece on-site.'
        ),
        'expert_line': 'Expert on-site authentication. Premium offers on pieces with box, papers, and service history. Discrete, professional consultation.',
        'what_you_have': 'Rolex Submariner, vintage Omega, dad\'s old Tag Heuer, broken Cartier...',
    },
}

# ----- CITY CONFIGS (for sanity / reference) -----
CITIES = {
    'valdosta': {
        'phone_display': '(229) 375-0015',
        'phone_tel': '+12293750015',
        'address': '3996 N Valdosta Rd, Valdosta, GA 31602',
        'map_short': 'https://maps.app.goo.gl/vQGRfVUG9vskyoNFA',
        'area_intro': 'South Georgia',
        'city_pretty': 'Valdosta',
        'location_name': 'Georgia Gold &amp; Silver Buyers &mdash; Valdosta',
    },
    'mcdonough': {
        'phone_display': '(678) 919-9265',
        'phone_tel': '+16789199265',
        'address': '120 S Point Blvd, McDonough, GA 30253',
        'map_short': 'https://maps.app.goo.gl/MDE1pakZBBCEd5v56',
        'area_intro': "Henry County",
        'city_pretty': 'McDonough',
        'location_name': 'Georgia Gold Buyers &mdash; McDonough',
    },
}


def transform(src_html: str, city: str, theme: str) -> str:
    """Transform city base template into themed LP via targeted replacements."""
    t = THEMES[theme]
    c = CITIES[city]
    city_pretty = c['city_pretty']

    html = src_html

    # ===== TITLE =====
    # Original: "Sell Your Gold in Valdosta | Georgia Gold Buyers"
    html = re.sub(
        r'<title>Sell Your Gold in ' + city_pretty + r' \| Georgia Gold Buyers</title>',
        f'<title>Sell {t["title_short"]} in {city_pretty} | Georgia Gold Buyers</title>',
        html
    )

    # ===== META DESCRIPTION =====
    # Original Valdosta: 'Sell gold, silver, jewelry &amp; coins in Valdosta, GA. Free appraisals, instant cash. Family-owned since 2012.'
    # Original McDonough: 'Sell gold, silver, jewelry &amp; coins in McDonough, GA...'
    html = re.sub(
        r'<meta name="description" content="Sell gold, silver, jewelry &amp; coins in [^"]*">',
        f'<meta name="description" content="Sell {t["meta_desc_topic"]} in {city_pretty}, GA. Free appraisals, instant cash. Family-owned since 2012.">',
        html
    )

    # ===== OG TITLE =====
    html = re.sub(
        r'<meta property="og:title" content="Sell Your Gold for Top Dollar in ' + city_pretty + r' \| Georgia Gold Buyers">',
        f'<meta property="og:title" content="Sell {t["title_short"]} for Top Dollar in {city_pretty} | Georgia Gold Buyers">',
        html
    )

    # ===== HERO H1 =====
    # Original: <h1>Sell Your Gold for <span>Top Dollar</span> in Valdosta</h1>
    html = re.sub(
        r'<h1>Sell Your Gold for <span>Top Dollar</span> in ' + city_pretty + r'</h1>',
        f'<h1>Sell {t["h1_word"]} for <span>Top Dollar</span> in {city_pretty}</h1>',
        html
    )

    # ===== HERO SUBLINE =====
    # Valdosta: "South Georgia's #1 rated gold buyer..."
    # McDonough: "Henry County's highest-rated gold buyer..."
    # Make them theme-specific
    if city == 'valdosta':
        html = html.replace(
            "South Georgia's #1 rated gold buyer &mdash; 5.0 stars, 84+ reviews. Free expert appraisal, instant cash, guaranteed best offer.",
            f"South Georgia's #1 rated buyer for {t['title_kw_lower']} &mdash; 5.0 stars, 84+ reviews. Free expert appraisal, instant cash, guaranteed best offer."
        )
    else:  # mcdonough
        html = html.replace(
            "Henry County's highest-rated gold buyer. Free expert appraisal, instant cash, guaranteed best offer.",
            f"Henry County's highest-rated buyer for {t['title_kw_lower']}. Free expert appraisal, instant cash, guaranteed best offer."
        )

    # ===== URGENCY BANNER =====
    html = html.replace(
        '<strong>Gold prices are near all-time highs</strong> &mdash; lock in today\'s price. Get your free appraisal now.',
        f'<strong>{t["urgency_msg"]}</strong> &mdash; lock in today\'s price. Get your free appraisal now.'
    )

    # ===== WIDGET HEADLINE =====
    html = html.replace(
        '<h2 class="widget-headline">Get Your Custom Quote Now</h2>',
        f'<h2 class="widget-headline">Get Your {t["widget_headline_topic"]} Quote Now</h2>'
    )

    # ===== WIDGET FIRST QUESTION =====
    # Default is "What would you like to sell?" — keep generic since widget options stay the same
    # but pre-select the matching theme option (cosmetic) — handled below if needed

    # ===== WIDGET DETAILS PLACEHOLDER =====
    html = re.sub(
        r'placeholder="e\.g\., 14k gold necklace, class ring, Rolex, silver flatware\.\.\."',
        f'placeholder="e.g., {t["what_you_have"]}"',
        html
    )

    # ===== "WHAT WE BUY" SECTION =====
    # Replace the generic items list with theme-specific list
    original_what_we_buy = (
        'We buy: <strong>gold jewelry</strong> (all karats), <strong>broken &amp; tangled chains</strong>, '
        '<strong>gold coins</strong>, <strong>silver flatware</strong>, <strong>sterling silver</strong>, '
        '<strong>diamond rings</strong>, <strong>luxury watches</strong> (Rolex, Omega, Cartier), '
        '<strong>designer handbags</strong> (Chanel, LV, Gucci), <strong>platinum</strong>, '
        '<strong>palladium</strong>, <strong>dental gold</strong>, <strong>estate collections</strong>, '
        '<strong>class rings</strong>, and more. Not sure? Bring it in &mdash; we\'ll tell you if it has value.'
    )
    if original_what_we_buy in html:
        html = html.replace(original_what_we_buy, t['item_list_html'])
    else:
        # Fall back: a slightly different variant (some files differ in whitespace/wording)
        # Just attempt without the trailing sentence; will be no-op if no match
        loose_pattern = re.compile(
            r'We buy: <strong>gold jewelry</strong>.*?Not sure\? Bring it in &mdash; we\'ll tell you if it has value\.',
            re.DOTALL
        )
        html = loose_pattern.sub(t['item_list_html'], html)

    # ===== WHAT WE BUY HEADING (add theme context) =====
    html = html.replace(
        '<h3 style="font-size:18px; font-weight:700; margin-bottom:12px; color:#1a1a1a;">What We Buy</h3>',
        f'<h3 style="font-size:18px; font-weight:700; margin-bottom:12px; color:#1a1a1a;">What {t["title_short"]} We Buy</h3>'
    )

    # ===== EXPERT TESTING LINE (in HIW or comparison area) =====
    # Replace the "XRF analyzer, precision scales..." line with theme-specific expertise
    html = html.replace(
        'XRF analyzer, precision scales, transparent process. You see everything.',
        t['expert_line'] + ' Transparent process &mdash; you see everything.'
    )

    return html


def build_one(city: str, theme: str) -> tuple[str, int]:
    """Generate one LP file. Returns (path, byte_count)."""
    src_path = REPO / f'lp-{city}.html'
    src_html = src_path.read_text(encoding='utf-8')

    out_html = transform(src_html, city, theme)

    out_path = REPO / f'lp-{city}-{theme}.html'
    out_path.write_text(out_html, encoding='utf-8')
    return (str(out_path), len(out_html))


def main():
    print('Building themed landing pages...\n')
    results = []
    for city in ['valdosta', 'mcdonough']:
        for theme in ['coins', 'jewelry', 'silver', 'watches']:
            path, size = build_one(city, theme)
            print(f'  ✓ {os.path.basename(path)}  ({size:,} bytes)')
            results.append((path, size))
    print(f'\nTotal: {len(results)} files generated.')

    # Sanity checks
    print('\nVerifying conversion tracking on all 8 pages...')
    required_labels = [
        'AW-16941991771/xH6vCLTht88aENuOyY4_',  # email
        'AW-16941991771/FJz9CITzxM8aENuOyY4_',  # phone
        'AW-16941991771/dHuGCN-Sxc8aENuOyY4_',  # maps
        'AW-16941991771/zCH5CJP9xs8aENuOyY4_',  # lead form
    ]
    all_ok = True
    for path, _ in results:
        content = Path(path).read_text(encoding='utf-8')
        missing = [lbl for lbl in required_labels if lbl not in content]
        if missing:
            print(f'  ✗ {os.path.basename(path)}: MISSING labels: {missing}')
            all_ok = False
        else:
            print(f'  ✓ {os.path.basename(path)}: all 4 conversion labels present')

    if all_ok:
        print('\n✅ All 8 pages have full conversion tracking.')
    else:
        print('\n⚠️  Some pages are missing labels — DO NOT DEPLOY.')

    return all_ok


if __name__ == '__main__':
    ok = main()
    exit(0 if ok else 1)

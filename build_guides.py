#!/usr/bin/env python3
"""Build answer-first guide pages from testing.html's shell (header, footer, form, scripts).
Re-run after editing GUIDES below:  python3 build_guides.py"""
import re, json, html

SRC = open('testing.html', encoding='utf-8').read()
TODAY = '2026-09-30'
TODAY_H = 'September 30, 2026'
BASE = 'https://georgiagoldbuying.com/'

GUIDE_CSS = """
<style id="guide-css">
.guide-wrap { max-width: 780px; margin: 0 auto; padding: 0 20px; }
.guide-meta { font-size: 13px; color: #888; margin: 0 0 20px; }
.answer-box { background: #FBF6E9; border: 1px solid #E8D9AE; border-left: 4px solid #C5961A; border-radius: 12px; padding: 20px 22px; margin: 0 0 32px; }
.answer-box h2 { font-size: 15px; letter-spacing: .06em; text-transform: uppercase; color: #8A6A12; margin: 0 0 8px; }
.answer-box p { margin: 0; font-size: 17px; line-height: 1.6; color: #1a1a1a; }
.guide-body h2 { font-size: 26px; line-height: 1.25; margin: 40px 0 14px; color: #1a1a1a; }
.guide-body h3 { font-size: 19px; margin: 24px 0 10px; color: #1a1a1a; }
.guide-body p, .guide-body li { font-size: 16.5px; line-height: 1.7; color: #333; }
.guide-body p { margin: 0 0 16px; }
.guide-body ul, .guide-body ol { margin: 0 0 18px; padding-left: 22px; }
.guide-body ul { list-style: disc; }
.guide-body ol { list-style: decimal; }
.guide-body li::marker { color: #C5961A; font-weight: 700; }
.guide-cards { list-style: none; }
.guide-body li { margin-bottom: 8px; }
.guide-body a { color: #8A6A12; text-decoration: underline; text-underline-offset: 2px; }
.table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 0 20px; border: 1px solid #E6E1D6; border-radius: 12px; }
.guide-body table { width: 100%; border-collapse: collapse; font-size: 15px; min-width: 480px; }
.guide-body th, .guide-body td { padding: 12px 14px; text-align: left; border-bottom: 1px solid #EEE9DD; }
.guide-body th { background: #F7F3EA; font-weight: 700; color: #1a1a1a; }
.guide-body tr:last-child td { border-bottom: 0; }
.guide-body td.num { font-variant-numeric: tabular-nums; white-space: nowrap; }
.formula { background: #1a1a1a; color: #fff; border-radius: 12px; padding: 18px 20px; font-size: 16px; line-height: 1.6; margin: 0 0 20px; }
.formula strong { color: #E2B94A; }
.note { font-size: 14px; color: #777; }
.guide-cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin: 8px 0 32px; }
.guide-card { display: block; background: #fff; border: 1px solid #E6E1D6; border-radius: 14px; padding: 22px; text-decoration: none !important; color: #1a1a1a !important; transition: border-color .2s, transform .2s; }
.guide-card:hover { border-color: #C5961A; transform: translateY(-2px); }
.guide-card h3 { margin: 0 0 8px; font-size: 18px; }
.guide-card p { margin: 0; font-size: 15px; color: #555; line-height: 1.55; }
.related { border-top: 1px solid #E6E1D6; margin-top: 40px; padding-top: 24px; }
@media (max-width: 640px) {
  .guide-body h2 { font-size: 22px; }
  .answer-box p { font-size: 16px; }
  .guide-cards { grid-template-columns: 1fr; }
  .guide-body table { min-width: 0; font-size: 14px; }
  .guide-body th, .guide-body td { padding: 10px 10px; }
  .guide-body table.wide { font-size: 13.5px; }
  .guide-body table.wide td:first-child { font-weight: 600; width: 26%; }
}
</style>
"""

def faq_html(faqs):
    out = []
    for q, a in faqs:
        out.append(f'''      <div class="faq-item reveal">
        <button class="faq-question" aria-expanded="false">
          {html.escape(q)}
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="faq-answer">
          <div class="faq-answer-inner">{a}</div>
        </div>
      </div>
''')
    return '\n'.join(out)

def strip(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()

LABELS = {
 'en': dict(by='By Georgia Gold Buyers &middot; ', updated='Updated', date=TODAY_H, quick='Quick answer', faq='Frequently Asked Questions', cta='Get Your Free Quote'),
 'es': dict(by='Por Georgia Gold Buyers &middot; ', updated='Actualizado el', date='30 de septiembre de 2026', quick='Respuesta rápida', faq='Preguntas frecuentes', cta='Obtenga su cotización gratis'),
}

def build(g):
    t = SRC
    es = g.get('lang') == 'es'
    L = LABELS['es' if es else 'en']
    url = BASE + g['slug']
    if es:
        t = t.replace('<html lang="en">', '<html lang="es">', 1)
    if g.get('alt'):
        en_url, es_url = (BASE + g['alt'], url) if es else (url, BASE + g['alt'])
        t = t.replace('</head>', f'<link rel="alternate" hreflang="en" href="{en_url}">\n<link rel="alternate" hreflang="es" href="{es_url}">\n<link rel="alternate" hreflang="x-default" href="{en_url}">\n</head>', 1)
    # --- head meta
    t = re.sub(r'<title>.*?</title>', f"<title>{html.escape(g['title'])}</title>", t, count=1, flags=re.S)
    for name in ['description', 'twitter:description']:
        t = re.sub(rf'<meta name="{name}" content="[^"]*">', f'<meta name="{name}" content="{html.escape(g["desc"])}">', t, count=1)
    t = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(g["desc"])}">', t, count=1)
    for p in ['og:title']:
        t = re.sub(rf'<meta property="{p}" content="[^"]*">', f'<meta property="{p}" content="{html.escape(g["title"])}">', t, count=1)
    t = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{html.escape(g["title"])}">', t, count=1)
    t = re.sub(r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="article">', t, count=1)
    t = t.replace('https://georgiagoldbuying.com/testing.html', url)
    if g.get('og'):
        t = t.replace(BASE + 'og-image.jpg', BASE + g['og'])
    t = re.sub(r'<meta name="subject" content="[^"]*">', f'<meta name="subject" content="{html.escape(g["h1_plain"])}">', t, count=1)
    # --- schema: drop testing.html ld+json, insert ours
    t = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', t, flags=re.S)
    ld = [
        {"@context": "https://schema.org", "@type": g.get("ld_type", "Article"), "headline": g['h1_plain'], "inLanguage": "es" if es else "en", "description": g['desc'],
         "url": url, "mainEntityOfPage": url, "datePublished": TODAY, "dateModified": TODAY,
         "image": BASE + "og-image.jpg",
         "author": {"@type": "Organization", "name": "Georgia Gold Buyers", "url": BASE},
         "publisher": {"@id": BASE + "#business", "@type": "LocalBusiness", "name": "Georgia Gold Buyers", "url": BASE,
                        "logo": BASE + "icon-512.png"},
         "about": g.get('about', []),
         "citation": g.get('citations', [])},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": g.get('parent_name', 'Seller Guides'), "item": BASE + g.get('parent', 'guides.html')},
        ] + ([] if g['slug'] == g.get('parent', 'guides.html') else [{"@type": "ListItem", "position": 3, "name": g['crumb'], "item": url}])},
    ]
    if g.get('faqs'):
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in g['faqs']]})
    if g['slug'] == 'guides.html':
        ld[0]['@type'] = 'CollectionPage'
    ld_html = ''.join(f'<script type="application/ld+json">\n{json.dumps(x, indent=2, ensure_ascii=False)}\n</script>\n' for x in ld)
    t = t.replace('</head>', ld_html + GUIDE_CSS + '</head>', 1)
    # --- nav active state
    t = t.replace('<a href="testing.html" class="active">Testing</a>', '<a href="testing.html">Testing</a>')
    # --- body content: replace PAGE HERO .. end of FAQ section
    start = t.index('<!-- ===== PAGE HERO ===== -->')
    end = t.index('<!-- ===== LEAD CAPTURE FORM ===== -->')
    faq_block = ''
    if g.get('faqs'):
        faq_block = f'''<!-- ===== FAQ ===== -->
<section class="section section--alt" id="faq">
  <div class="container">
    <h2 class="section-title reveal">{g.get('faq_title', L['faq'])}</h2>
    <div class="faq-list">
{faq_html(g['faqs'])}
    </div>
  </div>
</section>

'''
    body = f'''<!-- ===== PAGE HERO ===== -->
<section class="page-hero">
  <div class="container">
    <h1>{g['h1']}</h1>
    <p>{g['hero_sub']}</p>
    <a href="#quote-form" class="btn-gold">{L['cta']}</a>
  </div>
</section>

<!-- ===== GUIDE ===== -->
<section class="section">
  <div class="guide-wrap">
    <p class="guide-meta">{L['by'] if g['slug'] != 'guides.html' else ''}{L['updated']} {L['date']}</p>
    {('<div class="answer-box"><h2>' + L['quick'] + '</h2><p>' + g['answer'] + '</p></div>') if g.get('answer') else ''}
    <div class="guide-body">
{g['body']}
{g.get('related', RELATED_ES if es else RELATED) if g['slug'] != 'guides.html' else ''}
    </div>
  </div>
</section>

{faq_block}'''
    t = t[:start] + body + t[end:]
    # --- no guides strip on guide pages (they have their own related block)
    t = re.sub(r'<!-- ===== SELLER GUIDES STRIP ===== -->.*?</section>\s*', '', t, count=1, flags=re.S)
    # --- entity summary
    t = re.sub(r'(<aside class="entity-summary"[^>]*>).*?(</aside>)', r'\1\n  ' + g['entity'] + r'\n\2', t, count=1, flags=re.S)
    open(g['slug'], 'w', encoding='utf-8').write(t)
    print('built', g['slug'])

RELATED = '''<div class="related">
  <h2>More seller guides</h2>
  <div class="guide-cards">
    <a class="guide-card" href="how-much-is-gold-worth.html"><h3>How much is my gold worth?</h3><p>10k, 14k, 18k and 24k value per gram, with the math.</p></a>
    <a class="guide-card" href="sell-or-pawn-gold.html"><h3>Sell or pawn your gold?</h3><p>How each option works in Georgia and which pays more.</p></a>
    <a class="guide-card" href="selling-gold-what-to-expect.html"><h3>What to bring &amp; what to expect</h3><p>ID, hours, testing, and payment &mdash; step by step.</p></a>
    <a class="guide-card" href="sell-silver-coins-flatware.html"><h3>Selling silver coins &amp; flatware</h3><p>Silver content of US coins, sterling vs. silverplate.</p></a>
    <a class="guide-card" href="sell-rolex-luxury-watch.html"><h3>Selling a Rolex or luxury watch</h3><p>What drives the offer and how to prepare.</p></a>
  </div>
</div>'''

LIVE_JS = '''<script>
(function(){
  var OZ=31.1035, K=[["24k",0.999],["22k",0.916],["18k",0.75],["14k",0.585],["10k",0.417]];
  function fill(spot){
    var el=document.getElementById('karat-live'); if(!el||!spot) return;
    var g=spot/OZ, rows='';
    K.forEach(function(k){ rows+='<tr><td>'+k[0]+'</td><td class="num">$'+(g*k[1]).toFixed(2)+'</td><td class="num">$'+(g*k[1]*1.555).toFixed(2)+'</td></tr>'; });
    el.innerHTML=rows;
    var s=document.getElementById('spot-live'); if(s) s.textContent='$'+spot.toLocaleString(undefined,{maximumFractionDigits:0})+' per troy ounce';
    var ex=document.getElementById('example-live'); if(ex) ex.textContent='$'+(10*0.585*g).toFixed(2);
  }
  function load(){
  fetch('https://api.gold-api.com/price/XAU',{signal:AbortSignal.timeout?AbortSignal.timeout(5000):undefined})
    .then(function(r){return r.json()}).then(function(d){ if(d&&d.price) fill(d.price); }).catch(function(){});
  }
  load(); setInterval(function(){ if(!document.hidden) load(); }, 60000);
})();
</script>'''

GUIDES = [
# ------------------------------------------------------------------ 1
dict(slug='how-much-is-gold-worth.html', crumb='How Much Is My Gold Worth?',
 title='How Much Is My Gold Worth? 10k, 14k & 18k Value per Gram | Georgia Gold Buyers',
 desc='How to figure out what your gold jewelry is worth: karat purity, weight in grams, and the live spot price. Includes a 10k–24k value-per-gram table and a worked example.',
 h1='How Much Is My <span>Gold Worth?</span>', h1_plain='How Much Is My Gold Worth? 10k, 14k, 18k and 24k Value per Gram',
 hero_sub='The simple math behind every gold offer &mdash; karat, weight, and today&rsquo;s spot price.',
 answer='Gold is worth its <strong>weight in grams &times; its purity &times; the spot price per gram</strong>. 10k gold is 41.7% pure, 14k is 58.5%, 18k is 75%, and 24k is 99.9%. A buyer&rsquo;s offer is a share of that &ldquo;melt value,&rdquo; so ask any buyer to show you the weight, the karat they tested, and the spot price they used.',
 about=[{"@type":"Thing","name":"Gold"},{"@type":"Thing","name":"Karat"},{"@type":"Thing","name":"Scrap gold"}],
 body='''<h2>The formula</h2>
<div class="formula"><strong>Melt value</strong> = weight (grams) &times; purity &times; (spot price &divide; 31.1035)</div>
<p>Gold is priced by the troy ounce, which is 31.1035 grams. Divide the spot price by 31.1035 to get the price of one gram of pure gold, then multiply by your item&rsquo;s purity and weight. Today&rsquo;s spot price is <strong id="spot-live">shown on our <a href="gold-prices.html">live gold prices page</a></strong>.</p>

<h2>Gold value per gram by karat</h2>
<p>Pure-gold content of each karat, and its melt value at today&rsquo;s spot price. Values update automatically when this page loads.</p>
<div class="table-scroll"><table>
<thead><tr><th>Karat</th><th>Melt value per gram</th><th>Per pennyweight (dwt)</th></tr></thead>
<tbody id="karat-live">
<tr><td>24k (99.9%)</td><td class="num" colspan="2">See <a href="gold-prices.html">live prices</a></td></tr>
<tr><td>22k (91.6%)</td><td class="num" colspan="2">&mdash;</td></tr>
<tr><td>18k (75.0%)</td><td class="num" colspan="2">&mdash;</td></tr>
<tr><td>14k (58.5%)</td><td class="num" colspan="2">&mdash;</td></tr>
<tr><td>10k (41.7%)</td><td class="num" colspan="2">&mdash;</td></tr>
</tbody></table></div>
<p class="note">Melt value is the value of the pure gold only. It is not an offer. A pennyweight (dwt) is 1.555 grams.</p>

<h2>Worked example: a 10-gram 14k chain</h2>
<p>10 grams &times; 0.585 purity = 5.85 grams of pure gold. Multiply by the price per gram of pure gold and you get the chain&rsquo;s melt value &mdash; about <strong id="example-live">see live prices</strong> today.</p>

<h2>How to tell what karat your gold is</h2>
<div class="table-scroll"><table>
<thead><tr><th>Stamp you may see</th><th>Karat</th><th>Gold content</th></tr></thead>
<tbody>
<tr><td>10K, 10KT, 417</td><td>10 karat</td><td class="num">41.7%</td></tr>
<tr><td>14K, 14KT, 585</td><td>14 karat</td><td class="num">58.5%</td></tr>
<tr><td>18K, 18KT, 750</td><td>18 karat</td><td class="num">75.0%</td></tr>
<tr><td>22K, 916</td><td>22 karat</td><td class="num">91.6%</td></tr>
<tr><td>24K, 999</td><td>24 karat</td><td class="num">99.9%</td></tr>
</tbody></table></div>
<p>Stamps like <strong>GF</strong> (gold filled), <strong>GP</strong> or <strong>GEP</strong> (gold plated), and <strong>HGE</strong> mean only a thin layer of gold. Stamps can also be worn off or wrong, which is why we test every piece in front of you with an XRF analyzer &mdash; see <a href="testing.html">how we test gold</a>.</p>

<h2>Why offers are lower than melt value</h2>
<p>Every buyer pays a share of melt value, because scrap gold has to be refined before it can be sold again, and refining, assaying, and shipping all cost money. The share varies by buyer, so the smartest thing you can do is compare offers the same way: <strong>ask for the weight, the karat, and the spot price used</strong>. At Georgia Gold Buyers we weigh on a precision scale and show you the math before you decide.</p>

<h2>What about stones, watches, and designer pieces?</h2>
<p>Scrap value covers the metal only. Diamonds, branded jewelry, and luxury watches can be worth more than their gold weight, and are evaluated separately. See <a href="services.html">what we buy</a>.</p>
''' + LIVE_JS,
 faqs=[
  ('Is 10k gold worth selling?', '10k gold is 41.7% pure gold, so it is worth less per gram than 14k or 18k, but it still has real melt value. Chains, class rings, and broken pieces add up. Bring it in for a free test and quote at our Valdosta or McDonough location.'),
  ('How much is a gram of 14k gold worth?', 'A gram of 14k gold contains 0.585 grams of pure gold. Its melt value is 0.585 &times; (the spot price per troy ounce &divide; 31.1035). The table on this page calculates it live from today&rsquo;s spot price.'),
  ('Why is my offer less than the spot price?', 'Spot price is the price of pure gold in large, refined bars. Jewelry is an alloy (14k is 58.5% gold) and has to be refined, which costs money. Every buyer pays a share of melt value; ask for the weight, karat, and spot price used so you can compare offers fairly.'),
  ('How do I know what karat my gold is?', 'Look for a stamp such as 10K, 14K, 18K, 417, 585, or 750, usually inside a ring band or near a chain clasp. Stamps can be missing or wrong, so we verify purity in front of you with an XRF analyzer at no charge.'),
  ('Do you buy broken or scrap gold?', 'Yes. Broken chains, single earrings, bent rings, and scrap gold are valued by weight and purity, the same as intact pieces. There is no minimum.'),
 ],
 citations=[],
 entity='Georgia Gold Buyers buys gold jewelry, scrap gold, coins, and bullion at 3996 N Valdosta Rd, Valdosta, GA 31602 ((229) 375-0015) and 120 S Point Blvd, McDonough, GA 30253 ((678) 919-9265). Offers are based on tested purity, precise weight, and the live spot price. Free testing, no obligation.'),
# ------------------------------------------------------------------ 2
dict(slug='sell-or-pawn-gold.html', crumb='Sell or Pawn Gold?',
 title='Should I Sell or Pawn My Gold? Georgia Guide | Georgia Gold Buyers',
 desc='Selling vs. pawning gold in Georgia: how each works, what pawn loans cost under Georgia law, and when each option makes sense.',
 h1='Sell or Pawn <span>Your Gold?</span>', h1_plain='Should I Sell or Pawn My Gold? A Georgia Guide',
 hero_sub='How each option works, what it really costs, and which one fits your situation.',
 answer='<strong>Sell</strong> if you don&rsquo;t need the item back &mdash; you get paid in full and owe nothing. <strong>Pawn</strong> only if you must keep the piece and can repay quickly: a pawn is a loan secured by your gold, and Georgia law allows pawn interest and fees of up to <strong>25% per month</strong> for the first 90 days. If you don&rsquo;t repay, you lose the item.',
 about=[{"@type":"Thing","name":"Pawn loan"},{"@type":"Thing","name":"Selling gold"}],
 citations=["https://consumered.georgia.gov/your-money/loans/title-pawns-and-cash-advances"],
 body='''<h2>Selling vs. pawning at a glance</h2>
<div class="table-scroll"><table class="wide">
<thead><tr><th></th><th>Selling</th><th>Pawning</th></tr></thead>
<tbody>
<tr><td>What it is</td><td>A sale. You&rsquo;re paid and the item is sold.</td><td>A loan. Your item is collateral.</td></tr>
<tr><td>What you owe</td><td>Nothing.</td><td>The loan plus interest and fees.</td></tr>
<tr><td>Cost in Georgia</td><td>None.</td><td>Up to 25% per month for the first 90 days<sup>1</sup></td></tr>
<tr><td>How much you get</td><td>Based on the item&rsquo;s value.</td><td>Usually a fraction of value, since the lender must cover the risk of default.</td></tr>
<tr><td>Keep the item?</td><td>No.</td><td>Yes, if you repay on time.</td></tr>
<tr><td>If you can&rsquo;t pay</td><td>Not applicable.</td><td>You lose the item.</td></tr>
</tbody></table></div>
<p class="note"><sup>1</sup> Georgia caps pawn interest at 25% per month (300% a year) for the first three months and 12.5% per month after that, according to the <a href="https://consumered.georgia.gov/your-money/loans/title-pawns-and-cash-advances" target="_blank" rel="noopener">Georgia Department of Law&rsquo;s Consumer Protection Division</a>.</p>

<h2>When selling makes sense</h2>
<ul>
<li>The piece is broken, out of style, a single earring, or sitting in a drawer.</li>
<li>You&rsquo;re settling an estate or clearing out inherited jewelry &mdash; see our <a href="estate-sales.html">estate guide</a>.</li>
<li>You want the most cash today with nothing to pay back.</li>
</ul>

<h2>When pawning can make sense</h2>
<ul>
<li>The item has sentimental value you can&rsquo;t replace.</li>
<li>You need a short-term loan and are confident you can repay within a month or two.</li>
</ul>
<p>Even then, add up the total you&rsquo;ll repay. On a $500 loan, 25% a month is $125 a month in interest and fees.</p>

<h2>What our customers tell us</h2>
<p>Many customers who shopped a pawn offer first tell us they received 20&ndash;40% more by selling to us. Either way, ask any buyer or lender to show you the weight, the karat, and the spot price behind their number &mdash; that&rsquo;s the only fair way to compare. Our testing and quotes are free, with no obligation to sell.</p>
''',
 faqs=[
  ('Do pawn shops pay less than gold buyers?', 'A pawn loan is usually a fraction of an item&rsquo;s value, because the lender has to cover the risk that you won&rsquo;t repay. A sale is based on the item&rsquo;s full melt or resale value. Compare by asking each for the weight, karat, and spot price they used.'),
  ('What is the interest rate on a pawn loan in Georgia?', 'Georgia allows pawn interest and fees of up to 25% per month for the first 90 days and 12.5% per month after that, according to the Georgia Department of Law&rsquo;s Consumer Protection Division.'),
  ('Can I get my gold back after I sell it?', 'No. A sale is final. If you need the item back later, a pawn loan is the only option &mdash; but you must repay the loan plus interest and fees on time.'),
  ('Does Georgia Gold Buyers offer pawn loans?', 'No. We only buy. You get paid in full at the time of sale and owe nothing afterward.'),
 ],
 entity='Georgia Gold Buyers is a gold and jewelry buyer (not a pawn shop) with locations in Valdosta, GA (3996 N Valdosta Rd, (229) 375-0015) and McDonough, GA (120 S Point Blvd, (678) 919-9265). Free testing and quotes, paid in full at the time of sale.'),
# ------------------------------------------------------------------ 3
dict(slug='selling-gold-what-to-expect.html', crumb='What to Bring & Expect',
 title='Selling Gold in Georgia: What to Bring & What to Expect | Georgia Gold Buyers',
 desc='What to bring when you sell gold, silver, or jewelry in Georgia — photo ID, your items, and paperwork — plus our hours and step-by-step process in Valdosta and McDonough.',
 h1='Selling Gold: <span>What to Bring &amp; Expect</span>', h1_plain='Selling Gold in Georgia: What to Bring and What to Expect',
 hero_sub='Everything you need for a smooth visit to our Valdosta or McDonough location.',
 answer='Bring a <strong>valid government-issued photo ID</strong> (Georgia law requires it, and you must be 18 or older) and your items. Walk-ins are welcome during business hours &mdash; <strong>Valdosta:</strong> Mon&ndash;Fri 10am&ndash;5pm, Sat 10am&ndash;6pm; <strong>McDonough:</strong> Mon&ndash;Sat 10am&ndash;6pm; both closed Sunday. We test and weigh in front of you, show you the math, and pay on the spot if you accept.',
 about=[{"@type":"Thing","name":"Selling gold"},{"@type":"Place","name":"Valdosta, Georgia"},{"@type":"Place","name":"McDonough, Georgia"}],
 citations=["https://georgiacommons.org/code/43-37-3/text"],
 body='''<h2>What to bring</h2>
<ul>
<li><strong>Valid government-issued photo ID</strong> &mdash; a driver&rsquo;s license, state ID, passport, or military ID. Georgia requires precious-metals dealers to record each seller&rsquo;s identity (<a href="https://georgiacommons.org/code/43-37-3/text" target="_blank" rel="noopener">O.C.G.A. &sect; 43-37-3</a>). You must be 18 or older.</li>
<li><strong>Your items</strong> &mdash; jewelry, coins, bullion, flatware, scrap, or broken pieces. No need to clean or sort them.</li>
<li><strong>Paperwork, if you have it</strong> &mdash; for watches and designer pieces, original boxes, papers, receipts, and appraisals can raise the value.</li>
</ul>

<h2>Hours and locations</h2>
<div class="table-scroll"><table>
<thead><tr><th>Location</th><th>Address</th><th>Hours</th></tr></thead>
<tbody>
<tr><td><a href="valdosta.html">Valdosta</a><br><a href="tel:+12293750015">(229) 375-0015</a></td><td>3996 N Valdosta Rd<br>Valdosta, GA 31602</td><td>Mon&ndash;Fri 10am&ndash;5pm<br>Sat 10am&ndash;6pm<br>Sun closed</td></tr>
<tr><td><a href="mcdonough.html">McDonough</a><br><a href="tel:+16789199265">(678) 919-9265</a></td><td>120 S Point Blvd<br>McDonough, GA 30253</td><td>Mon&ndash;Sat 10am&ndash;6pm<br>Sun closed</td></tr>
</tbody></table></div>
<p>Walk-ins are welcome. Booking ahead is recommended so we can give you our full attention &mdash; call or use the <a href="#quote-form">free quote form</a>.</p>

<h2>What happens at your visit</h2>
<ol>
<li><strong>We sort your items</strong> by metal and karat.</li>
<li><strong>We test purity in front of you</strong> using an XRF analyzer and other methods &mdash; <a href="testing.html">see how we test</a>. Testing does not damage your items.</li>
<li><strong>We weigh</strong> on a precision scale that reads to 0.01 gram.</li>
<li><strong>We show you the math</strong> &mdash; weight, purity, and the current spot price &mdash; and make you an offer.</li>
<li><strong>You decide.</strong> Accept and get paid on the spot, or take your items home. No fee, no pressure.</li>
</ol>

<h2>How you get paid</h2>
<p>We pay at the time of sale, in cash, or by check for larger transactions. There is no minimum.</p>

<h2>Good to know</h2>
<ul>
<li>Online quotes are estimates; the final offer is made after in-person testing.</li>
<li>Purchased items may be subject to a hold period required by local ordinances.</li>
<li>Not sure an item is real gold? Bring it anyway &mdash; testing is free.</li>
</ul>
''',
 faqs=[
  ('Do I need an ID to sell gold in Georgia?', 'Yes. Georgia requires precious-metals dealers to record each seller&rsquo;s identity, so bring a valid government-issued photo ID. You must be 18 or older to sell.'),
  ('Do I need an appointment?', 'No &mdash; walk-ins are welcome during business hours. Booking ahead is recommended so we can give you our full attention. Call Valdosta at (229) 375-0015 or McDonough at (678) 919-9265.'),
  ('What are your hours?', 'Valdosta: Monday&ndash;Friday 10am&ndash;5pm and Saturday 10am&ndash;6pm. McDonough: Monday&ndash;Saturday 10am&ndash;6pm. Both locations are closed Sunday.'),
  ('How will I be paid?', 'You are paid at the time of sale in cash, or by check for larger transactions. There is no minimum.'),
  ('Is there a fee for testing or a quote?', 'No. Testing and quotes are free, and you are never obligated to sell.'),
 ],
 entity='Georgia Gold Buyers: 3996 N Valdosta Rd, Valdosta, GA 31602, (229) 375-0015, open Mon–Fri 10am–5pm and Sat 10am–6pm; 120 S Point Blvd, McDonough, GA 30253, (678) 919-9265, open Mon–Sat 10am–6pm. Both closed Sunday. Photo ID required; sellers must be 18+. Paid on the spot in cash or check.'),
# ------------------------------------------------------------------ hub
dict(slug='guides.html', crumb='Seller Guides',
 title='Seller Guides: Gold Value, Selling vs. Pawning & More | Georgia Gold Buyers',
 desc='Straight answers for people selling gold, silver, and jewelry in Georgia: what it is worth, selling vs. pawning, what to bring, and how testing works.',
 h1='Seller <span>Guides</span>', h1_plain='Seller Guides from Georgia Gold Buyers',
 hero_sub='Straight answers before you sell &mdash; from the team in Valdosta and McDonough.',
 body='''<div class="guide-cards">
  <a class="guide-card" href="how-much-is-gold-worth.html"><h3>How much is my gold worth?</h3><p>10k, 14k, 18k and 24k value per gram, a worked example, and how to read karat stamps.</p></a>
  <a class="guide-card" href="sell-or-pawn-gold.html"><h3>Sell or pawn your gold?</h3><p>How each option works, what pawn loans cost under Georgia law, and which fits you.</p></a>
  <a class="guide-card" href="selling-gold-what-to-expect.html"><h3>What to bring &amp; what to expect</h3><p>Photo ID, hours, our step-by-step process, and how you get paid.</p></a>
  <a class="guide-card" href="sell-silver-coins-flatware.html"><h3>Selling silver coins &amp; flatware</h3><p>Silver content of pre-1965 coins, Morgan dollars, and sterling &mdash; and how to spot silverplate.</p></a>
  <a class="guide-card" href="sell-rolex-luxury-watch.html"><h3>Selling a Rolex or luxury watch</h3><p>Model, condition, box and papers &mdash; what decides the offer.</p></a>
  <a class="guide-card" href="sell-gold-coins-bullion.html"><h3>Selling gold coins &amp; bullion</h3><p>Eagles, Krugerrands, Maple Leafs, pre-1933 US gold, and bars &mdash; with live melt values.</p></a>
  <a class="guide-card" href="sell-platinum-palladium.html"><h3>Selling platinum &amp; palladium</h3><p>PT950, PLAT, and PD950 stamps explained, with live value per gram.</p></a>
  <a class="guide-card" href="dental-gold-value.html"><h3>Is dental gold worth anything?</h3><p>What crowns and bridges are made of and how they&rsquo;re valued.</p></a>
  <a class="guide-card" href="testing.html"><h3>How we test your gold</h3><p>XRF analysis, Sigma verification, acid testing, and precision scales.</p></a>
  <a class="guide-card" href="gold-prices.html"><h3>Live gold &amp; silver prices</h3><p>Today&rsquo;s spot prices and a scrap gold calculator.</p></a>
  <a class="guide-card" href="estate-sales.html"><h3>Selling inherited jewelry</h3><p>How to handle an estate or a loved one&rsquo;s collection.</p></a>
  <a class="guide-card" href="areas-we-serve.html"><h3>Areas we serve</h3><p>Drive times from Tifton, Moultrie, Thomasville, Stockbridge, and more.</p></a>
</div>
<h2>What&rsquo;s my item worth?</h2>
<div class="guide-cards">
  <a class="guide-card" href="class-ring-value.html"><h3>Class rings</h3><p>10k vs. 14k, non-gold alloys, and live values.</p></a>
  <a class="guide-card" href="gold-chain-value.html"><h3>Gold chains</h3><p>Solid vs. hollow, clasp stamps, and live values.</p></a>
  <a class="guide-card" href="wedding-band-value.html"><h3>Wedding bands</h3><p>Gold, platinum, or tungsten &mdash; and what each is worth.</p></a>
  <a class="guide-card" href="charm-bracelet-value.html"><h3>Charm bracelets</h3><p>Mixed-karat charms, tested one by one.</p></a>
  <a class="guide-card" href="how-to-choose-a-gold-buyer.html"><h3>How to choose a gold buyer</h3><p>Seven questions and the red flags to watch for.</p></a>
</div>
<h2>En español</h2>
<div class="guide-cards">
  <a class="guide-card" href="es-cuanto-vale-mi-oro.html"><h3>¿Cuánto vale mi oro?</h3><p>Valor por gramo de 10k a 24k.</p></a>
  <a class="guide-card" href="es-vender-o-empenar-oro.html"><h3>¿Vender o empeñar su oro?</h3><p>Cómo funciona cada opción en Georgia.</p></a>
  <a class="guide-card" href="es-que-traer-para-vender-oro.html"><h3>Qué traer y qué esperar</h3><p>Identificación, horarios y el proceso.</p></a>
  <a class="guide-card" href="es-vender-oro-stockbridge-ga.html"><h3>Vender oro cerca de Stockbridge</h3><p>A unos 20 minutos de McDonough.</p></a>
  <a class="guide-card" href="es-vender-oro-jonesboro-ga.html"><h3>Vender oro cerca de Jonesboro</h3><p>A unos 25 minutos de McDonough.</p></a>
  <a class="guide-card" href="es-vender-oro-tifton-ga.html"><h3>Vender oro cerca de Tifton</h3><p>A unos 50 minutos de Valdosta.</p></a>
  <a class="guide-card" href="es-vender-oro-moultrie-ga.html"><h3>Vender oro cerca de Moultrie</h3><p>A unos 55 minutos de Valdosta.</p></a>
</div>''',
 entity='Georgia Gold Buyers publishes plain-language guides for people selling gold, silver, coins, and jewelry in Georgia. Locations: Valdosta, GA and McDonough, GA.'),
]

SILVER_JS = '''<script>
(function(){
  function fill(s){
    var g=s/31.1035, set=function(id,v){var e=document.getElementById(id); if(e) e.textContent='$'+v.toFixed(2);};
    var sp=document.getElementById('silver-spot'); if(sp) sp.textContent='$'+s.toFixed(2)+' per troy ounce';
    set('ag-sterling-g', g*0.925); set('ag-coin-g', g*0.90);
    set('ag-face', s*0.715); set('ag-morgan', s*0.7734); set('ag-k64', s*0.3617); set('ag-k65', s*0.1479);
  }
  function load(){
  fetch('https://api.gold-api.com/price/XAG',{signal:AbortSignal.timeout?AbortSignal.timeout(5000):undefined})
    .then(function(r){return r.json()}).then(function(d){ if(d&&d.price) fill(d.price); }).catch(function(){});
  }
  load(); setInterval(function(){ if(!document.hidden) load(); }, 60000);
})();
</script>'''

NEW = [
dict(slug='sell-silver-coins-flatware.html', crumb='Selling Silver Coins & Flatware',
 title='Selling Silver Coins, Sterling Flatware & Silver Jewelry | Georgia Gold Buyers',
 desc='What your silver is worth: silver content of pre-1965 US coins, Morgan and Peace dollars, Kennedy halves, and sterling flatware — plus how to tell sterling from silverplate.',
 h1='Selling <span>Silver</span> Coins &amp; Flatware', h1_plain='Selling Silver Coins, Sterling Flatware, and Silver Jewelry',
 hero_sub='How much silver is really in your coins, flatware, and jewelry &mdash; and how to spot silverplate.',
 answer='US dimes, quarters, and half dollars dated <strong>1964 and earlier are 90% silver</strong> &mdash; every $1 of face value holds about <strong>0.715 troy ounces</strong> of silver. Kennedy halves from <strong>1965&ndash;1970 are 40% silver</strong>. Sterling silver (stamped <strong>Sterling</strong> or <strong>925</strong>) is 92.5% silver. Items marked <strong>EPNS</strong>, <strong>silverplate</strong>, or <strong>IS</strong> have only a thin silver coating and little melt value.',
 about=[{"@type":"Thing","name":"Silver"},{"@type":"Thing","name":"Junk silver coins"},{"@type":"Thing","name":"Sterling silver"}],
 citations=["https://goldsilver.com/industry-news/article/what-is-junk-silver/","https://en.wikipedia.org/wiki/Morgan_dollar","https://en.wikipedia.org/wiki/Kennedy_half_dollar"],
 body='''<p>Today&rsquo;s silver spot price: <strong id="silver-spot">see our <a href="gold-prices.html">live prices page</a></strong>. The values below update when this page loads and show <strong>melt value only</strong> &mdash; not an offer, and not collector value.</p>

<h2>Silver content of common US coins</h2>
<div class="table-scroll"><table>
<thead><tr><th>Coin</th><th>Silver</th><th>Pure silver</th><th>Melt value</th></tr></thead>
<tbody>
<tr><td>Dimes, quarters, halves 1964 and earlier (per $1 face)</td><td>90%</td><td class="num">0.715 oz</td><td class="num" id="ag-face">&mdash;</td></tr>
<tr><td>Morgan dollar (1878&ndash;1921) / Peace dollar (1921&ndash;1935)</td><td>90%</td><td class="num">0.7734 oz</td><td class="num" id="ag-morgan">&mdash;</td></tr>
<tr><td>1964 Kennedy half dollar</td><td>90%</td><td class="num">0.3617 oz</td><td class="num" id="ag-k64">&mdash;</td></tr>
<tr><td>1965&ndash;1970 Kennedy half dollar</td><td>40%</td><td class="num">0.1479 oz</td><td class="num" id="ag-k65">&mdash;</td></tr>
</tbody></table></div>
<p class="note">Silver content per the US Mint specifications summarized by <a href="https://goldsilver.com/industry-news/article/what-is-junk-silver/" target="_blank" rel="noopener">GoldSilver</a>, <a href="https://en.wikipedia.org/wiki/Morgan_dollar" target="_blank" rel="noopener">Morgan dollar</a> and <a href="https://en.wikipedia.org/wiki/Kennedy_half_dollar" target="_blank" rel="noopener">Kennedy half dollar</a> references. Dimes and quarters from 1965 on, and halves from 1971 on, contain no silver.</p>

<h2>Rare dates are worth more than melt</h2>
<p>Some coins &mdash; certain Morgan dollar dates and mint marks, high-grade coins, and proofs &mdash; sell for well above their silver value. Don&rsquo;t clean your coins (cleaning can cut collector value). Bring them as they are and we&rsquo;ll check dates and condition before quoting.</p>

<h2>Sterling vs. silverplate</h2>
<div class="table-scroll"><table>
<thead><tr><th>Mark</th><th>What it means</th><th>Melt value</th></tr></thead>
<tbody>
<tr><td>Sterling, 925, .925</td><td>92.5% silver throughout</td><td class="num" id="ag-sterling-g">&mdash;</td></tr>
<tr><td>Coin, 900</td><td>90% silver (older American flatware)</td><td class="num" id="ag-coin-g">&mdash;</td></tr>
<tr><td>EPNS, Silverplate, Silver on Copper, IS, Quadruple Plate</td><td>Thin silver coating over base metal</td><td>Little to none</td></tr>
</tbody></table></div>
<p class="note">Melt values in the table are per gram of item weight.</p>

<h2>Weighted sterling: knives, candlesticks, and hollowware</h2>
<p>Sterling knife handles, candlesticks, and some bowls are <strong>weighted</strong> &mdash; filled with cement, pitch, or another material, and often marked &ldquo;weighted&rdquo; or &ldquo;reinforced.&rdquo; Only the thin silver shell counts, so a weighted piece is worth far less than its total weight suggests. Knife blades are usually stainless steel. We separate these before weighing so you see a fair number.</p>

<h2>What we buy</h2>
<ul>
<li>Sterling flatware sets, tea sets, trays, and serving pieces (including Tiffany and Georg Jensen)</li>
<li>Pre-1965 US dimes, quarters, and halves; Morgan and Peace dollars; 40% Kennedy halves</li>
<li>Silver bullion bars and rounds (1 oz, 10 oz, 100 oz)</li>
<li>Sterling jewelry and scrap silver</li>
</ul>
''' + SILVER_JS,
 faqs=[
  ('How much silver is in a pre-1965 quarter?', 'US dimes, quarters, and half dollars dated 1964 and earlier are 90% silver. Every $1 of face value (for example, four quarters) contains about 0.715 troy ounces of pure silver.'),
  ('Are 1965 quarters silver?', 'No. US dimes and quarters dated 1965 and later are copper-nickel clad and contain no silver. Kennedy half dollars from 1965 to 1970 are 40% silver.'),
  ('Is silverplate worth anything?', 'Silverplate (marked EPNS, Silverplate, IS, or Quadruple Plate) has only a very thin silver layer, so it has little to no melt value. Sterling, marked Sterling or 925, is 92.5% silver and is valued by weight.'),
  ('Do you buy sterling silver flatware?', 'Yes. We buy sterling flatware sets, tea sets, trays, and serving pieces. Weighted handles and stainless knife blades are separated before weighing so the offer reflects the real silver content.'),
  ('Should I clean my silver coins before selling?', 'No. Cleaning can scratch coins and reduce their collector value. Bring them as they are.'),
 ],
 entity='Georgia Gold Buyers buys silver coins, sterling flatware, silver bullion, and sterling jewelry at 3996 N Valdosta Rd, Valdosta, GA 31602 ((229) 375-0015) and 120 S Point Blvd, McDonough, GA 30253 ((678) 919-9265). Free testing and quotes.'),

dict(slug='sell-rolex-luxury-watch.html', crumb='Selling a Rolex or Luxury Watch',
 title='How to Sell a Rolex or Luxury Watch in Georgia | Georgia Gold Buyers',
 desc='What decides a pre-owned Rolex, Omega, Cartier, or Breitling offer — model and reference, condition, box and papers, service history — and how to prepare before you sell.',
 h1='Selling a <span>Rolex</span> or Luxury Watch', h1_plain='How to Sell a Rolex or Luxury Watch in Georgia',
 hero_sub='What drives the offer, what to bring, and what not to do before you sell.',
 answer='A luxury watch is valued on <strong>brand, model and reference number, condition, and demand</strong> &mdash; not just its gold weight. Original <strong>box, papers, and service records</strong> can raise the offer but aren&rsquo;t required. Bring all removed bracelet links, and <strong>don&rsquo;t polish the watch</strong> first.',
 about=[{"@type":"Thing","name":"Rolex"},{"@type":"Thing","name":"Luxury watches"}],
 citations=[],
 body='''<h2>What decides the offer</h2>
<ul>
<li><strong>Brand and model</strong> &mdash; for example Rolex Submariner, Datejust, Day-Date, GMT-Master, or Daytona; Omega Speedmaster or Seamaster.</li>
<li><strong>Reference number</strong> &mdash; identifies the exact version, year range, dial, and bezel.</li>
<li><strong>Condition</strong> &mdash; case and bracelet wear, crystal, dial, and whether it keeps time.</li>
<li><strong>Completeness</strong> &mdash; original box, warranty card or papers, receipts, and extra links.</li>
<li><strong>Service history</strong> &mdash; recent service records from an authorized service center help.</li>
<li><strong>Metal</strong> &mdash; solid gold and platinum models have a higher floor value than steel.</li>
</ul>

<h2>How to prepare</h2>
<ol>
<li><strong>Find the papers.</strong> Box, warranty card, receipt, and service paperwork &mdash; if you have them.</li>
<li><strong>Gather every link.</strong> Removed bracelet links matter; a short bracelet lowers value.</li>
<li><strong>Don&rsquo;t polish or refinish.</strong> Buyers and collectors often prefer original, unpolished cases.</li>
<li><strong>Don&rsquo;t open the case</strong> or try to fix it yourself.</li>
<li><strong>Bring your photo ID.</strong> Required for every sale.</li>
</ol>

<h2>Brands we buy</h2>
<p>Rolex, Omega, Cartier, Breitling, TAG Heuer, Patek Philippe, Audemars Piguet, IWC, and other luxury and designer watches &mdash; steel, two-tone, gold, and platinum, vintage or current. See <a href="services.html">all services</a>.</p>

<h2>Broken or not running?</h2>
<p>We still buy it. A non-running luxury watch has value from its parts, and a solid-gold case or bracelet always has at least its metal value. Bring it in for a free evaluation.</p>
''',
 faqs=[
  ('Do I need box and papers to sell a Rolex?', 'No. Box and papers can increase the offer, but they are not required. We evaluate the watch itself: model, reference, condition, and demand.'),
  ('Do you buy broken or non-running watches?', 'Yes. Non-running luxury watches still have value, and solid-gold or platinum watches are worth at least their metal value.'),
  ('Should I polish my watch before selling it?', 'No. Polishing removes metal and can lower value, especially on collectible models. Bring it as it is.'),
  ('Which watch brands do you buy?', 'Rolex, Omega, Cartier, Breitling, TAG Heuer, Patek Philippe, Audemars Piguet, IWC, and other luxury and designer brands.'),
 ],
 entity='Georgia Gold Buyers buys pre-owned Rolex, Omega, Cartier, Breitling, TAG Heuer, and other luxury watches at 3996 N Valdosta Rd, Valdosta, GA 31602 ((229) 375-0015) and 120 S Point Blvd, McDonough, GA 30253 ((678) 919-9265). Free evaluations; box and papers not required.'),

dict(slug='dental-gold-value.html', crumb='Selling Dental Gold',
 title='Is Dental Gold Worth Anything? Selling Gold Crowns & Bridges | Georgia Gold Buyers',
 desc='What dental gold is made of, how buyers value gold crowns, bridges, and fillings, and how to sell them in Valdosta or McDonough, GA.',
 h1='Is Dental Gold <span>Worth Anything?</span>', h1_plain='Is Dental Gold Worth Anything? Selling Gold Crowns and Bridges',
 hero_sub='Yes &mdash; here&rsquo;s what&rsquo;s in it and how it&rsquo;s valued.',
 answer='Yes. Dental crowns, bridges, and inlays are often made from <strong>gold alloys that also contain palladium, platinum, or silver</strong>. Under the American Dental Association&rsquo;s classification, &ldquo;high noble&rdquo; alloys contain at least 60% noble metal, including at least 40% gold. Because the mix varies, dental gold should be <strong>tested, not guessed</strong> &mdash; we use an XRF analyzer to read the exact content in front of you.',
 about=[{"@type":"Thing","name":"Dental gold"},{"@type":"Thing","name":"Dental alloys"}],
 citations=["https://www.ada.org/resources/ada-library/oral-health-topics/materials-for-indirect-restorations"],
 body='''<h2>What dental gold is made of</h2>
<p>Dental work is rarely pure gold. The <a href="https://www.ada.org/resources/ada-library/oral-health-topics/materials-for-indirect-restorations" target="_blank" rel="noopener">American Dental Association</a> groups dental alloys by their noble-metal content:</p>
<div class="table-scroll"><table>
<thead><tr><th>ADA class</th><th>Noble metal content</th><th>Typical value</th></tr></thead>
<tbody>
<tr><td>High noble</td><td>At least 60% noble metal (gold, platinum, palladium), with at least 40% gold</td><td>Highest</td></tr>
<tr><td>Noble</td><td>At least 25% noble metal</td><td>Moderate</td></tr>
<tr><td>Predominantly base metal</td><td>Less than 25% noble metal</td><td>Low</td></tr>
</tbody></table></div>

<h2>How dental gold is valued</h2>
<ol>
<li><strong>Remove what isn&rsquo;t metal.</strong> Porcelain, tooth material, and cement are removed or accounted for so only metal is weighed.</li>
<li><strong>Test the alloy.</strong> Our XRF analyzer reads the percentage of gold, platinum, palladium, and silver without damaging the piece.</li>
<li><strong>Weigh</strong> on a precision scale.</li>
<li><strong>Price each metal</strong> from the live spot price, and show you the math.</li>
</ol>

<h2>Crowns with porcelain</h2>
<p>Many crowns are porcelain fused to metal, with a thin metal layer under the white porcelain. They still have value, but less metal than a full gold crown. Silver-colored crowns can also contain palladium or platinum &mdash; testing tells you.</p>

<h2>Is it legal to sell my dental gold?</h2>
<p>Yes. Crowns and bridges removed from your own mouth are your property. Ask your dentist to return them after a procedure. As with any sale, bring a valid photo ID.</p>
''',
 faqs=[
  ('Is dental gold real gold?', 'Usually it is a gold alloy mixed with other metals such as palladium, platinum, silver, or copper. High-noble dental alloys contain at least 40% gold and at least 60% noble metal in total, according to the American Dental Association&rsquo;s classification.'),
  ('How much is a gold crown worth?', 'It depends on the metal weight and the alloy mix, which vary widely. We test each piece with an XRF analyzer, weigh it, and price it from the live spot price at no charge.'),
  ('Do I need to clean my crowns before selling?', 'No. Bring them as they are, in a sealed bag. We account for porcelain, tooth material, and cement before weighing.'),
  ('Do you buy silver-colored dental work?', 'Yes. Some silver-colored crowns and bridges contain palladium or platinum. Testing shows what is there.'),
 ],
 entity='Georgia Gold Buyers buys dental gold, crowns, bridges, and dental alloys containing gold, platinum, and palladium at 3996 N Valdosta Rd, Valdosta, GA 31602 ((229) 375-0015) and 120 S Point Blvd, McDonough, GA 30253 ((678) 919-9265). XRF testing in front of you.'),
]

GUIDES[-1:-1] = NEW
from guides_batch3 import NEW3, RELATED_ES, spanish, town_pages, areas_hub, LOC
GUIDES[-1:-1] = NEW3
for _g in GUIDES:
    _g['alt'] = {'how-much-is-gold-worth.html':'es-cuanto-vale-mi-oro.html','sell-or-pawn-gold.html':'es-vender-o-empenar-oro.html','selling-gold-what-to-expect.html':'es-que-traer-para-vender-oro.html'}.get(_g['slug'], _g.get('alt'))
GUIDES += spanish(LIVE_JS)
_towns = town_pages()
for _p in _towns:
    _p['og'] = LOC[_p['town_meta'][3]]['og']
GUIDES += _towns + [areas_hub()]
from guides_batch4 import ITEMS, es_shell, es_towns
from guides_batch3 import TOWNS, town_slug, rmin
GUIDES[-1:-1] = []
_hub = [g for g in GUIDES if g['slug'] == 'guides.html'][0]
_i = GUIDES.index(_hub)
GUIDES[_i:_i] = ITEMS
_es_t = es_towns(TOWNS, LOC, town_slug, rmin)
for _p in _towns:
    for _e in _es_t:
        if _e['alt'] == _p['slug']: _p['alt'] = _e['slug']
GUIDES += _es_t

if __name__ == '__main__':
    for g in GUIDES:
        build(g)
        if g.get('lang') == 'es':
            p = g['slug']; s = open(p).read(); open(p, 'w').write(es_shell(s))

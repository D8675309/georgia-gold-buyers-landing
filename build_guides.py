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

def build(g):
    t = SRC
    url = BASE + g['slug']
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
    t = re.sub(r'<meta name="subject" content="[^"]*">', f'<meta name="subject" content="{html.escape(g["h1_plain"])}">', t, count=1)
    # --- schema: drop testing.html ld+json, insert ours
    t = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', t, flags=re.S)
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": g['h1_plain'], "description": g['desc'],
         "url": url, "mainEntityOfPage": url, "datePublished": TODAY, "dateModified": TODAY,
         "image": BASE + "og-image.jpg",
         "author": {"@type": "Organization", "name": "Georgia Gold Buyers", "url": BASE},
         "publisher": {"@id": BASE + "#business", "@type": "LocalBusiness", "name": "Georgia Gold Buyers", "url": BASE,
                        "logo": BASE + "icon-512.png"},
         "about": g.get('about', []),
         "citation": g.get('citations', [])},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Seller Guides", "item": BASE + "guides.html"},
        ] + ([] if g['slug'] == 'guides.html' else [{"@type": "ListItem", "position": 3, "name": g['crumb'], "item": url}])},
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
    <h2 class="section-title reveal">{g.get('faq_title', 'Frequently Asked Questions')}</h2>
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
    <a href="#quote-form" class="btn-gold">Get Your Free Quote</a>
  </div>
</section>

<!-- ===== GUIDE ===== -->
<section class="section">
  <div class="guide-wrap">
    <p class="guide-meta">{('By Georgia Gold Buyers &middot; ' if g['slug'] != 'guides.html' else '')}Updated {TODAY_H}</p>
    {('<div class="answer-box"><h2>Quick answer</h2><p>' + g['answer'] + '</p></div>') if g.get('answer') else ''}
    <div class="guide-body">
{g['body']}
{RELATED if g['slug'] != 'guides.html' else ''}
    </div>
  </div>
</section>

{faq_block}'''
    t = t[:start] + body + t[end:]
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
    <a class="guide-card" href="testing.html"><h3>How we test your gold</h3><p>XRF, Sigma verifier, acid, and precision scales explained.</p></a>
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
  fetch('https://api.gold-api.com/price/XAU',{signal:AbortSignal.timeout?AbortSignal.timeout(5000):undefined})
    .then(function(r){return r.json()}).then(function(d){ if(d&&d.price) fill(d.price); }).catch(function(){});
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
  <a class="guide-card" href="testing.html"><h3>How we test your gold</h3><p>XRF analysis, Sigma verification, acid testing, and precision scales.</p></a>
  <a class="guide-card" href="gold-prices.html"><h3>Live gold &amp; silver prices</h3><p>Today&rsquo;s spot prices and a scrap gold calculator.</p></a>
  <a class="guide-card" href="estate-sales.html"><h3>Selling inherited jewelry</h3><p>How to handle an estate or a loved one&rsquo;s collection.</p></a>
</div>''',
 entity='Georgia Gold Buyers publishes plain-language guides for people selling gold, silver, coins, and jewelry in Georgia. Locations: Valdosta, GA and McDonough, GA.'),
]

if __name__ == '__main__':
    for g in GUIDES:
        build(g)

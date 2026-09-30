# Batch 3 content: coins/bullion + platinum guides, Spanish guides, service-area town pages.
# Imported by build_guides.py
import json

GOLD_COIN_JS = '''<script>
(function(){
  function fill(s){
    var set=function(id,oz){var e=document.getElementById(id); if(e) e.textContent='$'+(s*oz).toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});};
    var sp=document.getElementById('gold-spot'); if(sp) sp.textContent='$'+s.toLocaleString(undefined,{maximumFractionDigits:0})+' per troy ounce';
    set('gc-1oz',1); set('gc-half',0.5); set('gc-quarter',0.25); set('gc-tenth',0.1);
    set('gc-20',0.9675); set('gc-10',0.48375); set('gc-5',0.24187); set('gc-250',0.12094);
  }
  function load(){
  fetch('https://api.gold-api.com/price/XAU',{signal:AbortSignal.timeout?AbortSignal.timeout(5000):undefined})
    .then(function(r){return r.json()}).then(function(d){ if(d&&d.price) fill(d.price); }).catch(function(){});
  }
  load(); setInterval(function(){ if(!document.hidden) load(); }, 60000);
})();
</script>'''

PT_JS = '''<script>
(function(){
  function go(sym,cb){ fetch('https://api.gold-api.com/price/'+sym,{signal:AbortSignal.timeout?AbortSignal.timeout(5000):undefined}).then(function(r){return r.json()}).then(function(d){ if(d&&d.price) cb(d.price); }).catch(function(){}); }
  function set(id,v){var e=document.getElementById(id); if(e) e.textContent='$'+v.toFixed(2);}
  function load(){
  go('XPT',function(s){ var g=s/31.1035; var e=document.getElementById('pt-spot'); if(e) e.textContent='$'+s.toLocaleString(undefined,{maximumFractionDigits:0})+' per troy ounce'; set('pt-950',g*0.95); set('pt-900',g*0.90); set('pt-850',g*0.85); });
  go('XPD',function(s){ var g=s/31.1035; var e=document.getElementById('pd-spot'); if(e) e.textContent='$'+s.toLocaleString(undefined,{maximumFractionDigits:0})+' per troy ounce'; set('pd-950',g*0.95); set('pd-500',g*0.50); });
  }
  load(); setInterval(function(){ if(!document.hidden) load(); }, 60000);
})();
</script>'''

# reuse the live karat JS from the English gold guide (defined in build_guides.py as LIVE_JS)

LOC = {
 'V': dict(name='Valdosta', page='valdosta.html', addr='3996 N Valdosta Rd, Valdosta, GA 31602', phone='(229) 375-0015', tel='+12293750015',
           hours='Monday&ndash;Friday 10am&ndash;5pm, Saturday 10am&ndash;6pm, closed Sunday', hours_short='Mon&ndash;Fri 10&ndash;5, Sat 10&ndash;6',
           map='https://maps.app.goo.gl/MDE1pakZBBCEd5v56', rating='4.9 stars on Google (115+ reviews)', og='og-valdosta.jpg'),
 'M': dict(name='McDonough', page='mcdonough.html', addr='120 S Point Blvd, McDonough, GA 30253', phone='(678) 919-9265', tel='+16789199265',
           hours='Monday&ndash;Saturday 10am&ndash;6pm, closed Sunday', hours_short='Mon&ndash;Sat 10&ndash;6',
           map='https://maps.app.goo.gl/vQGRfVUG9vskyoNFA', rating='4.7 stars on Google', og='og-mcdonough.jpg'),
}

def rmin(m):
    return int(5 * round(m / 5))

# town, state, county, loc, miles, minutes, route sentence, local note
TOWNS = [
 ('Tifton', 'GA', 'Tift County', 'V', 44, 50, 'Take I-75 South toward Valdosta and exit onto US 41 / North Valdosta Road.', 'Tifton sellers often combine the trip with errands in Valdosta; call ahead and we&rsquo;ll have your quote ready to review.'),
 ('Moultrie', 'GA', 'Colquitt County', 'V', 40, 55, 'Head east on GA 37 / GA 133 toward Valdosta, then north on US 41 / North Valdosta Road.', 'Moultrie is one of the farther drives we see regularly &mdash; submit a free online quote first so you know what to expect.'),
 ('Thomasville', 'GA', 'Thomas County', 'V', 49, 65, 'Take US 84 East to Valdosta, then continue north to North Valdosta Road.', 'For a trip of about an hour, we recommend booking a time so we&rsquo;re ready when you arrive.'),
 ('Quitman', 'GA', 'Brooks County', 'V', 24, 30, 'Take US 84 East into Valdosta, then north to North Valdosta Road.', 'Quitman is about half an hour away, which makes Valdosta the closest Georgia Gold Buyers location for Brooks County.'),
 ('Hahira', 'GA', 'Lowndes County', 'V', 9, 15, 'Take Old US 41 (North Valdosta Road) south toward Valdosta.', 'Our Valdosta store is on the north side of town, so Hahira is one of our closest communities.'),
 ('Lake Park', 'GA', 'Lowndes County', 'V', 23, 30, 'Take I-75 North through Valdosta and exit onto US 41 / North Valdosta Road.', 'Lake Park sellers can reach us in about half an hour without leaving I-75 for most of the trip.'),
 ('Adel', 'GA', 'Cook County', 'V', 21, 25, 'Take I-75 South toward Valdosta and exit onto US 41 / North Valdosta Road.', 'Adel is a short I-75 drive &mdash; about 25 minutes to the counter.'),
 ('Madison', 'FL', 'Madison County', 'V', 40, 55, 'Take SR 145 north into Georgia, then GA 31 and I-75 North to Valdosta.', 'North Florida sellers regularly make the drive to Valdosta. Bring a valid government-issued photo ID; an out-of-state license is fine.'),
 ('Jasper', 'FL', 'Hamilton County', 'V', 42, 50, 'Take US 41 North (or I-75 North) into Georgia and on to North Valdosta Road.', 'Jasper is about 50 minutes away. A valid Florida driver&rsquo;s license works as your photo ID.'),
 ('Stockbridge', 'GA', 'Henry County', 'M', 10, 20, 'Take I-75 South toward McDonough and follow signs to South Point Boulevard.', 'Stockbridge is a quick trip down I-75 &mdash; about 20 minutes.'),
 ('Hampton', 'GA', 'Henry County', 'M', 7, 10, 'Take GA 20 East toward McDonough to South Point Boulevard.', 'Hampton is one of the closest communities to our McDonough store.'),
 ('Locust Grove', 'GA', 'Henry County', 'M', 8, 10, 'Take I-75 North toward McDonough and follow signs to South Point Boulevard.', 'Locust Grove is about 10 minutes up I-75.'),
 ('Jonesboro', 'GA', 'Clayton County', 'M', 16, 25, 'Take GA 138 East to I-75 South toward McDonough.', 'Jonesboro and Clayton County sellers are about 25 minutes from our McDonough counter.'),
 ('Griffin', 'GA', 'Spalding County', 'M', 18, 30, 'Take GA 155 North toward McDonough.', 'Griffin and Spalding County sellers can reach us in about half an hour.'),
]

def town_slug(t, st):
    return f"sell-gold-{t.lower().replace(' ', '-')}-{st.lower()}.html"

def town_pages():
    out = []
    for town, st, county, lk, mi, mn, route, note in TOWNS:
        L = LOC[lk]; m = rmin(mn); slug = town_slug(town, st)
        out.append(dict(
         slug=slug, parent='areas-we-serve.html', parent_name='Areas We Serve', crumb=f'{town}, {st}', ld_type='WebPage',
         title=f'Sell Gold Near {town}, {st} | Georgia Gold Buyers {L["name"]} (~{m} min)',
         desc=f'Selling gold, silver, coins, or jewelry near {town}, {st}? Our {L["name"]} location is about {mi} miles (~{m} minutes) away. Free testing, cash on the spot.',
         h1=f'Selling Gold Near <span>{town}, {st}</span>', h1_plain=f'Selling Gold Near {town}, {st}',
         hero_sub=f'Our {L["name"]} location is about {m} minutes from {town}. Free testing, paid on the spot.',
         answer=f'The closest Georgia Gold Buyers location to {town} is our <strong>{L["name"]} store at {L["addr"]}</strong> &mdash; about <strong>{mi} miles, roughly {m} minutes</strong> by car. Hours: {L["hours"]}. Call <a href="tel:{L["tel"]}">{L["phone"]}</a>. We buy gold, silver, platinum, coins, jewelry, and luxury watches, test everything in front of you, and pay on the spot.',
         about=[{"@type": "Place", "name": f"{town}, {st}"}, {"@type": "AdministrativeArea", "name": f"{county}, {st}"}],
         body=f'''<h2>Getting here from {town}</h2>
<div class="table-scroll"><table>
<tbody>
<tr><td>Nearest location</td><td><a href="{L['page']}">Georgia Gold Buyers &ndash; {L['name']}</a></td></tr>
<tr><td>Address</td><td>{L['addr']}</td></tr>
<tr><td>Distance</td><td>About {mi} miles</td></tr>
<tr><td>Drive time</td><td>About {m} minutes in normal traffic</td></tr>
<tr><td>Hours</td><td>{L['hours']}</td></tr>
<tr><td>Phone</td><td><a href="tel:{L['tel']}">{L['phone']}</a></td></tr>
</tbody></table></div>
<p><strong>Route:</strong> {route} <a href="{L['map']}" target="_blank" rel="noopener">Open in Google Maps</a>.</p>
<p>{note}</p>

<h2>What we buy from {town} and {county}</h2>
<ul>
<li>Gold jewelry, chains, class rings, and broken or scrap gold &mdash; <a href="how-much-is-gold-worth.html">what is my gold worth?</a></li>
<li>Silver coins, sterling flatware, and bullion &mdash; <a href="sell-silver-coins-flatware.html">silver guide</a></li>
<li>Gold coins and bullion &mdash; <a href="sell-gold-coins-bullion.html">coins &amp; bullion guide</a></li>
<li>Platinum and palladium jewelry &mdash; <a href="sell-platinum-palladium.html">platinum guide</a></li>
<li>Rolex and luxury watches &mdash; <a href="sell-rolex-luxury-watch.html">watch guide</a></li>
<li>Dental gold, estate and inherited jewelry, designer jewelry, and handbags</li>
</ul>

<h2>Why people drive from {town}</h2>
<ul>
<li><strong>Testing in front of you</strong> with an XRF analyzer &mdash; <a href="testing.html">how we test</a></li>
<li><strong>Transparent math:</strong> weight, purity, and the live spot price, shown before you decide</li>
<li><strong>Paid on the spot</strong> in cash, or by check for larger sales. No minimum.</li>
<li><strong>Rated {L['rating']}</strong></li>
</ul>

<h2>Before you make the trip</h2>
<p>Bring a valid government-issued photo ID (required by Georgia law) and your items. Walk-ins are welcome, but for a drive of more than a few minutes, <a href="#quote-form">request a free quote</a> or call first. See <a href="selling-gold-what-to-expect.html">what to bring and what to expect</a>.</p>
''',
         faqs=[
          (f'Where can I sell gold near {town}, {st}?', f'Georgia Gold Buyers&rsquo; {L["name"]} location at {L["addr"]} is about {mi} miles (roughly {m} minutes) from {town}. Call {L["phone"]} or request a free quote online.'),
          (f'How far is Georgia Gold Buyers from {town}?', f'About {mi} miles, or roughly {m} minutes by car in normal traffic, to our {L["name"]} store.'),
          (f'What are your hours for {town} customers?', f'Our {L["name"]} store is open {L["hours"].replace("&ndash;", "–")}.'),
          ('Do I need an appointment?', 'No. Walk-ins are welcome during business hours. For a longer drive, we recommend calling ahead or requesting a free online quote first.'),
         ],
         entity=f'Georgia Gold Buyers serves {town}, {st} and {county} from its {L["name"]} location at {L["addr"]} ({L["phone"]}), about {mi} miles away. We buy gold, silver, platinum, coins, jewelry, and luxury watches. Open {L["hours"].replace("&ndash;", "–")}.',
         town_meta=(town, st, county, lk, mi, m),
        ))
    return out

def areas_hub():
    rows_v = ''.join(f'<a class="guide-card" href="{town_slug(t,s)}"><h3>{t}, {s}</h3><p>{c} &middot; about {mi} mi / {rmin(mn)} min to Valdosta</p></a>' for t,s,c,lk,mi,mn,_,_ in TOWNS if lk=='V')
    rows_m = ''.join(f'<a class="guide-card" href="{town_slug(t,s)}"><h3>{t}, {s}</h3><p>{c} &middot; about {mi} mi / {rmin(mn)} min to McDonough</p></a>' for t,s,c,lk,mi,mn,_,_ in TOWNS if lk=='M')
    return dict(slug='areas-we-serve.html', parent='areas-we-serve.html', parent_name='Areas We Serve', crumb='Areas We Serve', ld_type='CollectionPage',
     title='Areas We Serve: South Georgia, North Florida & Henry County | Georgia Gold Buyers',
     desc='Georgia Gold Buyers serves South Georgia and North Florida from Valdosta, and Henry County and South Metro Atlanta from McDonough. Find drive times from your town.',
     h1='Areas <span>We Serve</span>', h1_plain='Areas Served by Georgia Gold Buyers',
     hero_sub='Two locations. Drive times from the towns our customers come from.',
     answer='We have two locations. <strong>Valdosta</strong> (3996 N Valdosta Rd) serves Lowndes County, South Georgia, and North Florida. <strong>McDonough</strong> (120 S Point Blvd) serves Henry County and South Metro Atlanta. Pick your town below for distance, drive time, and directions.',
     body=f'''<h2>Near our Valdosta location</h2>
<p><a href="valdosta.html">3996 N Valdosta Rd, Valdosta, GA 31602</a> &middot; <a href="tel:+12293750015">(229) 375-0015</a> &middot; Mon&ndash;Fri 10am&ndash;5pm, Sat 10am&ndash;6pm</p>
<div class="guide-cards">{rows_v}</div>
<h2>Near our McDonough location</h2>
<p><a href="mcdonough.html">120 S Point Blvd, McDonough, GA 30253</a> &middot; <a href="tel:+16789199265">(678) 919-9265</a> &middot; Mon&ndash;Sat 10am&ndash;6pm</p>
<div class="guide-cards">{rows_m}</div>
<p class="note">Distances and drive times are approximate, from each town&rsquo;s center in normal traffic.</p>''',
     related='',
     entity='Georgia Gold Buyers serves South Georgia and North Florida from Valdosta, GA and Henry County and South Metro Atlanta from McDonough, GA.')

NEW3 = [
dict(slug='sell-gold-coins-bullion.html', crumb='Selling Gold Coins & Bullion',
 title='Selling Gold Coins & Bullion: Eagles, Krugerrands, Bars | Georgia Gold Buyers',
 desc='Gold content of American Eagles, Krugerrands, Maple Leafs, Buffalos, pre-1933 US gold coins, and gold bars — with live melt values and tips for selling.',
 h1='Selling Gold <span>Coins &amp; Bullion</span>', h1_plain='Selling Gold Coins and Bullion: Eagles, Krugerrands, and Bars',
 hero_sub='How much gold is in your coins and bars &mdash; and what raises or lowers the offer.',
 answer='Modern bullion coins are sold by their <strong>gold content</strong>: a 1 oz American Gold Eagle, Krugerrand, Canadian Maple Leaf, or American Buffalo each contains <strong>one troy ounce of pure gold</strong>. Eagles and Krugerrands are 22k (the coin weighs a bit more than an ounce); Maple Leafs and Buffalos are 24k. Pre-1933 US gold coins are 90% gold &mdash; a $20 Double Eagle holds <strong>0.9675 oz</strong>. Rare dates and high grades can be worth more than melt.',
 about=[{"@type":"Thing","name":"Gold bullion coins"},{"@type":"Thing","name":"American Gold Eagle"},{"@type":"Thing","name":"Krugerrand"}],
 body='''<p>Today&rsquo;s gold spot price: <strong id="gold-spot">see our <a href="gold-prices.html">live prices page</a></strong>. Values below are <strong>gold content &times; spot</strong> &mdash; not an offer, and not collector value.</p>

<h2>Modern bullion coins</h2>
<div class="table-scroll"><table>
<thead><tr><th>Coin</th><th>Purity</th><th>Pure gold</th><th>Melt value</th></tr></thead>
<tbody>
<tr><td>American Gold Eagle (1 oz)</td><td>22k (91.67%)</td><td class="num">1.000 oz</td><td class="num" id="gc-1oz">&mdash;</td></tr>
<tr><td>South African Krugerrand (1 oz)</td><td>22k (91.67%)</td><td class="num">1.000 oz</td><td class="num">same</td></tr>
<tr><td>Canadian Gold Maple Leaf (1 oz)</td><td>24k (99.99%)</td><td class="num">1.000 oz</td><td class="num">same</td></tr>
<tr><td>American Gold Buffalo (1 oz)</td><td>24k (99.99%)</td><td class="num">1.000 oz</td><td class="num">same</td></tr>
<tr><td>1/2 oz coins</td><td>&mdash;</td><td class="num">0.500 oz</td><td class="num" id="gc-half">&mdash;</td></tr>
<tr><td>1/4 oz coins</td><td>&mdash;</td><td class="num">0.250 oz</td><td class="num" id="gc-quarter">&mdash;</td></tr>
<tr><td>1/10 oz coins</td><td>&mdash;</td><td class="num">0.100 oz</td><td class="num" id="gc-tenth">&mdash;</td></tr>
</tbody></table></div>

<h2>Pre-1933 US gold coins</h2>
<div class="table-scroll"><table>
<thead><tr><th>Coin</th><th>Purity</th><th>Pure gold</th><th>Melt value</th></tr></thead>
<tbody>
<tr><td>$20 Double Eagle (Liberty or Saint-Gaudens)</td><td>90%</td><td class="num">0.9675 oz</td><td class="num" id="gc-20">&mdash;</td></tr>
<tr><td>$10 Eagle</td><td>90%</td><td class="num">0.4838 oz</td><td class="num" id="gc-10">&mdash;</td></tr>
<tr><td>$5 Half Eagle</td><td>90%</td><td class="num">0.2419 oz</td><td class="num" id="gc-5">&mdash;</td></tr>
<tr><td>$2.50 Quarter Eagle</td><td>90%</td><td class="num">0.1209 oz</td><td class="num" id="gc-250">&mdash;</td></tr>
</tbody></table></div>
<p>Many pre-1933 coins carry a premium over melt, and scarce dates, mint marks, or high grades can be worth much more. We check date, mint mark, and condition before quoting.</p>

<h2>Gold bars</h2>
<p>Bars from recognized refiners (such as PAMP Suisse, Valcambi, Credit Suisse, the Royal Canadian Mint, and Perth Mint) are valued by weight and purity, typically .9999 fine. Bars still sealed in their original assay card are easiest to verify, but we test unsealed bars too.</p>

<h2>Tips before you sell</h2>
<ul>
<li><strong>Don&rsquo;t clean coins.</strong> Cleaning can scratch them and cut collector value.</li>
<li><strong>Keep capsules and assay cards.</strong> We can test through most holders with our XRF analyzer.</li>
<li><strong>Bring any receipts or certificates</strong> (for example, graded-coin slabs).</li>
<li><strong>Counterfeits exist.</strong> We verify every coin and bar &mdash; see <a href="testing.html">how we test</a>.</li>
</ul>
''' + GOLD_COIN_JS,
 faqs=[
  ('How much gold is in a 1 oz American Gold Eagle?', 'Exactly one troy ounce of pure gold. The coin is 22 karat (91.67% gold), so it weighs slightly more than an ounce in total.'),
  ('Is a Krugerrand worth the same as a Gold Eagle?', 'By gold content, yes &mdash; both contain one troy ounce of pure gold. Offers can differ slightly with market demand for each coin.'),
  ('How much gold is in a $20 gold coin?', 'Pre-1933 $20 Double Eagles contain 0.9675 troy ounces of pure gold. Scarce dates and high-grade coins can be worth more than their gold value.'),
  ('Do you buy gold bars?', 'Yes. We buy gold bars from recognized refiners in all sizes, sealed or unsealed, and verify every bar before quoting.'),
 ],
 entity='Georgia Gold Buyers buys gold coins (American Eagles, Krugerrands, Maple Leafs, Buffalos, pre-1933 US gold) and gold bars at 3996 N Valdosta Rd, Valdosta, GA 31602 ((229) 375-0015) and 120 S Point Blvd, McDonough, GA 30253 ((678) 919-9265).'),

dict(slug='sell-platinum-palladium.html', crumb='Selling Platinum & Palladium',
 title='Selling Platinum & Palladium Jewelry and Bullion | Georgia Gold Buyers',
 desc='How to tell if your jewelry is platinum or palladium, what PT950, PLAT, and PD950 stamps mean, and live melt values per gram.',
 h1='Selling <span>Platinum &amp; Palladium</span>', h1_plain='Selling Platinum and Palladium Jewelry and Bullion',
 hero_sub='Stamps, purity, and live value per gram &mdash; for rings, bands, and bullion.',
 answer='Most platinum jewelry is <strong>95% platinum</strong>, stamped <strong>PT950</strong>, <strong>950 PLAT</strong>, or <strong>PLAT</strong>; some is 90% (PT900) or 85% (PT850). Palladium jewelry is usually <strong>95% (PD950)</strong> or sometimes 50% (PD500). Both are valued by <strong>weight &times; purity &times; spot price</strong>, and they look like white gold &mdash; so testing matters.',
 about=[{"@type":"Thing","name":"Platinum"},{"@type":"Thing","name":"Palladium"}],
 body='''<p>Platinum spot: <strong id="pt-spot">see <a href="gold-prices.html">live prices</a></strong>. Palladium spot: <strong id="pd-spot">see <a href="gold-prices.html">live prices</a></strong>.</p>

<h2>Common stamps and value per gram</h2>
<div class="table-scroll"><table>
<thead><tr><th>Stamp</th><th>Metal &amp; purity</th><th>Melt value per gram</th></tr></thead>
<tbody>
<tr><td>PT950, 950 PLAT, PLAT, PLATINUM</td><td>Platinum 95%</td><td class="num" id="pt-950">&mdash;</td></tr>
<tr><td>PT900, 900 PLAT</td><td>Platinum 90%</td><td class="num" id="pt-900">&mdash;</td></tr>
<tr><td>PT850</td><td>Platinum 85%</td><td class="num" id="pt-850">&mdash;</td></tr>
<tr><td>PD950, 950 PALL</td><td>Palladium 95%</td><td class="num" id="pd-950">&mdash;</td></tr>
<tr><td>PD500</td><td>Palladium 50%</td><td class="num" id="pd-500">&mdash;</td></tr>
</tbody></table></div>
<p class="note">Melt value of the metal only, not an offer. Values update when the page loads.</p>

<h2>Platinum vs. white gold</h2>
<p>White gold is gold alloyed with white metals and usually plated with rhodium. Platinum and white gold look almost identical, but platinum is heavier and is priced differently. Stamps like <strong>14K</strong> or <strong>18K</strong> mean white gold; <strong>PT</strong> or <strong>PLAT</strong> means platinum. If there&rsquo;s no stamp, our XRF analyzer tells the difference in seconds.</p>

<h2>Platinum and palladium bullion</h2>
<p>We buy American Platinum Eagles, Canadian Platinum and Palladium Maple Leafs, American Palladium Eagles, and platinum and palladium bars from recognized refiners.</p>

<h2>Other sources of platinum</h2>
<ul>
<li>Platinum wedding bands and engagement ring settings</li>
<li>Vintage and estate jewelry (platinum was common in early-1900s pieces)</li>
<li>Platinum dental work &mdash; see <a href="dental-gold-value.html">dental gold</a></li>
</ul>
''' + PT_JS,
 faqs=[
  ('How do I know if my ring is platinum?', 'Look inside the band for PT950, 950 PLAT, PLAT, or PLATINUM. If there is no stamp, we can test it with an XRF analyzer at no charge.'),
  ('Is platinum worth more than gold?', 'It depends on the market. Platinum and gold spot prices move independently, and the lead has changed over the years. See today&rsquo;s prices on our live prices page.'),
  ('Do you buy palladium?', 'Yes. We buy palladium jewelry (PD950, PD500) and palladium bullion coins and bars.'),
  ('What does PT950 mean?', 'PT950 means the piece is 95% pure platinum, the most common purity for platinum jewelry in the US.'),
 ],
 entity='Georgia Gold Buyers buys platinum and palladium jewelry, bands, dental work, coins, and bars at 3996 N Valdosta Rd, Valdosta, GA 31602 ((229) 375-0015) and 120 S Point Blvd, McDonough, GA 30253 ((678) 919-9265).'),
]

RELATED_ES = '''<div class="related">
  <h2>Más guías para vendedores</h2>
  <div class="guide-cards">
    <a class="guide-card" href="es-cuanto-vale-mi-oro.html"><h3>¿Cuánto vale mi oro?</h3><p>Valor por gramo de 10k a 24k, con el cálculo.</p></a>
    <a class="guide-card" href="es-vender-o-empenar-oro.html"><h3>¿Vender o empeñar su oro?</h3><p>Cómo funciona cada opción en Georgia.</p></a>
    <a class="guide-card" href="es-que-traer-para-vender-oro.html"><h3>Qué traer y qué esperar</h3><p>Identificación, horarios y el proceso paso a paso.</p></a>
  </div>
</div>'''

def spanish(LIVE_JS):
    return [
dict(slug='es-cuanto-vale-mi-oro.html', alt='how-much-is-gold-worth.html', lang='es', crumb='¿Cuánto vale mi oro?',
 title='¿Cuánto vale mi oro? Valor por gramo de 10k, 14k y 18k | Georgia Gold Buyers',
 desc='Cómo calcular el valor de sus joyas de oro: pureza en quilates, peso en gramos y el precio spot en vivo. Tabla de valor por gramo de 10k a 24k.',
 h1='¿Cuánto vale <span>mi oro?</span>', h1_plain='¿Cuánto vale mi oro? Valor por gramo de 10k, 14k, 18k y 24k',
 hero_sub='El cálculo detrás de cada oferta: quilates, peso y el precio del oro de hoy.',
 answer='El oro vale su <strong>peso en gramos &times; su pureza &times; el precio spot por gramo</strong>. El oro de 10k tiene 41.7% de oro puro, el de 14k 58.5%, el de 18k 75% y el de 24k 99.9%. La oferta de un comprador es una parte de ese &ldquo;valor de fundición&rdquo;, así que pida siempre el peso, los quilates y el precio spot que usaron.',
 body='''<h2>La fórmula</h2>
<div class="formula"><strong>Valor de fundición</strong> = peso (gramos) &times; pureza &times; (precio spot &divide; 31.1035)</div>
<p>El oro se cotiza por onza troy, que equivale a 31.1035 gramos. El precio spot de hoy es <strong id="spot-live">el que aparece en nuestra <a href="gold-prices.html">página de precios en vivo</a></strong>.</p>
<h2>Valor del oro por gramo según los quilates</h2>
<div class="table-scroll"><table>
<thead><tr><th>Quilates</th><th>Valor por gramo</th><th>Por pennyweight (dwt)</th></tr></thead>
<tbody id="karat-live">
<tr><td>24k (99.9%)</td><td class="num" colspan="2">Vea <a href="gold-prices.html">precios en vivo</a></td></tr>
<tr><td>22k (91.6%)</td><td class="num" colspan="2">&mdash;</td></tr>
<tr><td>18k (75.0%)</td><td class="num" colspan="2">&mdash;</td></tr>
<tr><td>14k (58.5%)</td><td class="num" colspan="2">&mdash;</td></tr>
<tr><td>10k (41.7%)</td><td class="num" colspan="2">&mdash;</td></tr>
</tbody></table></div>
<p class="note">Es el valor del oro puro únicamente, no una oferta. Un pennyweight (dwt) equivale a 1.555 gramos.</p>
<h2>Ejemplo: una cadena de 14k de 10 gramos</h2>
<p>10 gramos &times; 0.585 = 5.85 gramos de oro puro. Hoy eso equivale a unos <strong id="example-live">vea precios en vivo</strong> en valor de fundición.</p>
<h2>Cómo saber de cuántos quilates es su oro</h2>
<p>Busque un sello como <strong>10K / 417</strong>, <strong>14K / 585</strong> o <strong>18K / 750</strong>, normalmente dentro del anillo o cerca del broche. Los sellos <strong>GF</strong> (gold filled), <strong>GP</strong> o <strong>HGE</strong> indican solo una capa delgada de oro. Como los sellos pueden estar gastados o ser incorrectos, probamos cada pieza frente a usted con un analizador XRF.</p>
<h2>¿Por qué las ofertas son menores que el valor de fundición?</h2>
<p>El oro de chatarra se tiene que refinar antes de venderse de nuevo, y eso cuesta dinero. Cada comprador paga una parte distinta del valor de fundición; la mejor forma de comparar es pedir el peso, los quilates y el precio spot usados. Nosotros le mostramos el cálculo antes de que usted decida.</p>
''' + LIVE_JS,
 faqs=[
  ('¿Vale la pena vender oro de 10k?', 'Sí. El oro de 10k tiene 41.7% de oro puro; vale menos por gramo que el de 14k o 18k, pero cadenas, anillos de graduación y piezas rotas suman. La prueba y la cotización son gratis.'),
  ('¿Cuánto vale un gramo de oro de 14k?', 'Un gramo de 14k contiene 0.585 gramos de oro puro. Su valor de fundición es 0.585 &times; (precio spot por onza &divide; 31.1035). La tabla de esta página lo calcula en vivo.'),
  ('¿Compran oro roto?', 'Sí. Cadenas rotas, aretes sueltos y anillos doblados se valoran por peso y pureza, igual que las piezas enteras. No hay mínimo.'),
 ],
 entity='Georgia Gold Buyers compra joyas de oro, oro de chatarra, monedas y lingotes en 3996 N Valdosta Rd, Valdosta, GA 31602 ((229) 375-0015) y 120 S Point Blvd, McDonough, GA 30253 ((678) 919-9265). Prueba gratis y sin compromiso.'),

dict(slug='es-vender-o-empenar-oro.html', alt='sell-or-pawn-gold.html', lang='es', crumb='¿Vender o empeñar oro?',
 title='¿Vender o empeñar su oro? Guía para Georgia | Georgia Gold Buyers',
 desc='Vender vs. empeñar oro en Georgia: cómo funciona cada opción, cuánto cuestan los préstamos de empeño según la ley de Georgia y cuándo conviene cada una.',
 h1='¿Vender o <span>empeñar su oro?</span>', h1_plain='¿Vender o empeñar su oro? Guía para Georgia',
 hero_sub='Cómo funciona cada opción, lo que realmente cuesta y cuál le conviene.',
 answer='<strong>Venda</strong> si no necesita recuperar la pieza: recibe el pago completo y no debe nada. <strong>Empeñe</strong> solo si debe conservarla y puede pagar rápido: un empeño es un préstamo garantizado con su oro, y la ley de Georgia permite intereses y cargos de hasta <strong>25% al mes</strong> durante los primeros 90 días. Si no paga, pierde la pieza.',
 citations=["https://consumered.georgia.gov/your-money/loans/title-pawns-and-cash-advances"],
 body='''<h2>Vender vs. empeñar</h2>
<div class="table-scroll"><table class="wide">
<thead><tr><th></th><th>Vender</th><th>Empeñar</th></tr></thead>
<tbody>
<tr><td>Qué es</td><td>Una venta. Le pagan y la pieza se vende.</td><td>Un préstamo. Su pieza es la garantía.</td></tr>
<tr><td>Lo que debe</td><td>Nada.</td><td>El préstamo más intereses y cargos.</td></tr>
<tr><td>Costo en Georgia</td><td>Ninguno.</td><td>Hasta 25% al mes los primeros 90 días<sup>1</sup></td></tr>
<tr><td>¿Conserva la pieza?</td><td>No.</td><td>Sí, si paga a tiempo.</td></tr>
<tr><td>Si no puede pagar</td><td>No aplica.</td><td>Pierde la pieza.</td></tr>
</tbody></table></div>
<p class="note"><sup>1</sup> Georgia limita el interés de empeño a 25% mensual (300% anual) durante los primeros tres meses y 12.5% mensual después, según la <a href="https://consumered.georgia.gov/your-money/loans/title-pawns-and-cash-advances" target="_blank" rel="noopener">División de Protección al Consumidor del Departamento de Justicia de Georgia</a>.</p>
<h2>Cuándo conviene vender</h2>
<ul>
<li>La pieza está rota, pasada de moda o guardada en un cajón.</li>
<li>Está resolviendo una herencia o joyas heredadas.</li>
<li>Quiere el mayor pago hoy, sin nada que devolver.</li>
</ul>
<h2>Cuándo puede convenir empeñar</h2>
<ul>
<li>La pieza tiene un valor sentimental irremplazable.</li>
<li>Necesita un préstamo corto y está seguro de poder pagarlo en uno o dos meses.</li>
</ul>
<p>Sume el total que pagará: en un préstamo de $500, un 25% mensual son $125 al mes en intereses y cargos.</p>
<h2>Lo que nos dicen nuestros clientes</h2>
<p>Muchos clientes que primero recibieron una oferta de empeño nos dicen que obtuvieron entre 20% y 40% más al vendernos. La prueba y la cotización son gratis y sin compromiso.</p>
''',
 faqs=[
  ('¿Cuál es el interés de un empeño en Georgia?', 'Georgia permite intereses y cargos de hasta 25% al mes durante los primeros 90 días y 12.5% al mes después, según la División de Protección al Consumidor del Departamento de Justicia de Georgia.'),
  ('¿Puedo recuperar mi oro después de venderlo?', 'No. La venta es final. Si necesita recuperar la pieza más adelante, la única opción es un empeño, pagando el préstamo más intereses y cargos a tiempo.'),
  ('¿Georgia Gold Buyers ofrece préstamos de empeño?', 'No. Solo compramos. Le pagamos completo al momento de la venta y no debe nada después.'),
 ],
 entity='Georgia Gold Buyers es un comprador de oro y joyas (no una casa de empeño) con tiendas en Valdosta, GA (3996 N Valdosta Rd, (229) 375-0015) y McDonough, GA (120 S Point Blvd, (678) 919-9265).'),

dict(slug='es-que-traer-para-vender-oro.html', alt='selling-gold-what-to-expect.html', lang='es', crumb='Qué traer para vender oro',
 title='Vender oro en Georgia: qué traer y qué esperar | Georgia Gold Buyers',
 desc='Qué traer para vender oro, plata o joyas en Georgia: identificación con foto, sus piezas y documentos. Horarios y el proceso paso a paso en Valdosta y McDonough.',
 h1='Vender oro: <span>qué traer y qué esperar</span>', h1_plain='Vender oro en Georgia: qué traer y qué esperar',
 hero_sub='Todo lo que necesita para una visita sin complicaciones.',
 answer='Traiga una <strong>identificación oficial vigente con foto</strong> (la ley de Georgia lo exige y debe tener 18 años o más) y sus piezas. Puede llegar sin cita durante el horario &mdash; <strong>Valdosta:</strong> lunes a viernes 10am&ndash;5pm, sábado 10am&ndash;6pm; <strong>McDonough:</strong> lunes a sábado 10am&ndash;6pm; ambos cerrados el domingo. Probamos y pesamos frente a usted, le mostramos el cálculo y le pagamos en el momento si acepta.',
 citations=["https://georgiacommons.org/code/43-37-3/text"],
 body='''<h2>Qué traer</h2>
<ul>
<li><strong>Identificación oficial vigente con foto</strong>: licencia de conducir, identificación estatal, pasaporte o identificación militar. Georgia exige a los comerciantes de metales preciosos registrar la identidad de cada vendedor (<a href="https://georgiacommons.org/code/43-37-3/text" target="_blank" rel="noopener">O.C.G.A. &sect; 43-37-3</a>). Debe tener 18 años o más.</li>
<li><strong>Sus piezas</strong>: joyas, monedas, lingotes, cubiertos, chatarra o piezas rotas. No hace falta limpiarlas.</li>
<li><strong>Documentos, si los tiene</strong>: para relojes y piezas de diseñador, las cajas, papeles, recibos y avalúos pueden aumentar el valor.</li>
</ul>
<h2>Horarios y ubicaciones</h2>
<div class="table-scroll"><table>
<thead><tr><th>Tienda</th><th>Dirección</th><th>Horario</th></tr></thead>
<tbody>
<tr><td><a href="valdosta.html">Valdosta</a><br><a href="tel:+12293750015">(229) 375-0015</a></td><td>3996 N Valdosta Rd<br>Valdosta, GA 31602</td><td>Lun&ndash;Vie 10am&ndash;5pm<br>Sáb 10am&ndash;6pm<br>Dom cerrado</td></tr>
<tr><td><a href="mcdonough.html">McDonough</a><br><a href="tel:+16789199265">(678) 919-9265</a></td><td>120 S Point Blvd<br>McDonough, GA 30253</td><td>Lun&ndash;Sáb 10am&ndash;6pm<br>Dom cerrado</td></tr>
</tbody></table></div>
<h2>Qué pasa en su visita</h2>
<ol>
<li><strong>Separamos sus piezas</strong> por metal y quilates.</li>
<li><strong>Probamos la pureza frente a usted</strong> con un analizador XRF y otros métodos. La prueba no daña sus piezas.</li>
<li><strong>Pesamos</strong> en una báscula de precisión de 0.01 gramos.</li>
<li><strong>Le mostramos el cálculo</strong> (peso, pureza y precio spot actual) y le hacemos una oferta.</li>
<li><strong>Usted decide.</strong> Acepte y reciba su pago en el momento, o llévese sus piezas. Sin cargos ni presión.</li>
</ol>
<h2>Cómo le pagamos</h2>
<p>Pagamos al momento de la venta, en efectivo o con cheque para ventas grandes. No hay mínimo.</p>
''',
 faqs=[
  ('¿Necesito identificación para vender oro en Georgia?', 'Sí. Georgia exige a los comerciantes de metales preciosos registrar la identidad de cada vendedor, así que traiga una identificación oficial vigente con foto. Debe tener 18 años o más.'),
  ('¿Necesito cita?', 'No. Puede llegar sin cita durante el horario. Recomendamos llamar antes: Valdosta (229) 375-0015, McDonough (678) 919-9265.'),
  ('¿Cuál es su horario?', 'Valdosta: lunes a viernes de 10am a 5pm y sábado de 10am a 6pm. McDonough: lunes a sábado de 10am a 6pm. Ambas tiendas cierran el domingo.'),
 ],
 entity='Georgia Gold Buyers: 3996 N Valdosta Rd, Valdosta, GA 31602, (229) 375-0015, lunes a viernes 10am–5pm y sábado 10am–6pm; 120 S Point Blvd, McDonough, GA 30253, (678) 919-9265, lunes a sábado 10am–6pm. Se requiere identificación con foto.'),
    ]

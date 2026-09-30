# Batch 4: item-value pages + how to choose a gold buyer.
ITEM_JS = '''<script>
(function(){
  function fill(s){
    var g=s/31.1035;
    document.querySelectorAll('[data-g]').forEach(function(el){
      var v=g*parseFloat(el.getAttribute('data-g'))*parseFloat(el.getAttribute('data-p'));
      el.textContent='$'+v.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});
    });
    var sp=document.getElementById('gold-spot'); if(sp) sp.textContent='$'+s.toLocaleString(undefined,{maximumFractionDigits:0})+' per troy ounce';
  }
  function load(){
  fetch('https://api.gold-api.com/price/XAU',{signal:AbortSignal.timeout?AbortSignal.timeout(5000):undefined})
    .then(function(r){return r.json()}).then(function(d){ if(d&&d.price) fill(d.price); }).catch(function(){});
  }
  load(); setInterval(function(){ if(!document.hidden) load(); }, 60000);
})();
</script>'''

K = [('10k', 0.417), ('14k', 0.585), ('18k', 0.750)]

def table(label, weights):
    head = ''.join(f'<th>{k}</th>' for k, _ in K)
    rows = ''.join(f'<tr><td>{w} g {label}</td>' + ''.join(f'<td class="num" data-g="{w}" data-p="{p}">&mdash;</td>' for _, p in K) + '</tr>' for w in weights)
    return f'''<div class="table-scroll"><table>
<thead><tr><th>Example</th>{head}</tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="note">Melt value of the gold only, using today&rsquo;s spot price. Example weights, not averages &mdash; weigh your piece for a real number. Not an offer.</p>'''

SPOT = '<p>Today&rsquo;s gold spot price: <strong id="gold-spot">see our <a href="gold-prices.html">live prices page</a></strong>. Values update automatically.</p>'
ENT = 'Georgia Gold Buyers buys gold jewelry at 3996 N Valdosta Rd, Valdosta, GA 31602 ((229) 375-0015) and 120 S Point Blvd, McDonough, GA 30253 ((678) 919-9265). Free testing; paid on the spot.'

ITEMS = [
dict(slug='class-ring-value.html', crumb='Class Ring Value',
 title='How Much Is My Class Ring Worth? 10k & 14k Values | Georgia Gold Buyers',
 desc='What a gold class ring is worth: how to read the stamp, which metals aren’t gold (Siladium, Valadium, Lustrium), and live melt values by weight and karat.',
 h1='How much is my <span>class ring worth?</span>', h1_plain='How Much Is My Class Ring Worth?',
 hero_sub='Most of a class ring&rsquo;s value is its gold. Here&rsquo;s how to tell what you have.',
 answer='A gold class ring is worth its <strong>gold weight &times; karat purity &times; the spot price</strong>. Look inside the band: <strong>10K</strong> and <strong>14K</strong> are the most common. Stamps like <strong>Siladium, Valadium, Lustrium, Celestrium, or Ultrium</strong> mean it isn&rsquo;t gold. Synthetic stones usually add little, so the gold is where the value is.',
 about=[{"@type":"Thing","name":"Class ring"}],
 body=SPOT + '''<h2>Live value by weight and karat</h2>''' + table('ring', [8, 12, 18, 25]) + '''
<h2>How to read the stamp</h2>
<ul>
<li><strong>10K / 417</strong> &mdash; 41.7% gold. The most common class-ring gold.</li>
<li><strong>14K / 585</strong> &mdash; 58.5% gold.</li>
<li><strong>18K / 750</strong> &mdash; 75% gold. Less common.</li>
<li><strong>Siladium, Valadium, Lustrium, Celestrium, Ultrium, Lazon</strong> &mdash; trade names for non-gold alloys. They have little or no metal value.</li>
<li><strong>925 / Sterling</strong> &mdash; silver, not gold.</li>
</ul>
<p>Stamps wear off. If yours is unreadable, we test it free with an XRF analyzer &mdash; see <a href="testing.html">how we test</a>.</p>
<h2>Do the stones matter?</h2>
<p>Most class-ring stones are synthetic or lab-created and add little resale value. We weigh the gold without the stone, or account for it, and show you the math.</p>
<h2>Selling more than one ring?</h2>
<p>Bring them all. We separate by karat so each is paid at its own purity. See <a href="how-much-is-gold-worth.html">what gold is worth per gram</a>.</p>
''' + ITEM_JS,
 faqs=[
  ('Are class rings real gold?', 'Many are 10k or 14k gold, but many are made from non-gold alloys sold as Siladium, Valadium, Lustrium, Celestrium, or Ultrium. Check the stamp inside the band, or bring it in for a free test.'),
  ('How much is a 10k class ring worth?', 'Multiply the gold weight in grams by 0.417 and by the gold spot price per gram. The table on this page does the math live for common weights.'),
  ('Do you buy class rings with stones?', 'Yes. We buy class rings with or without stones and test the metal in front of you.'),
 ], entity=ENT),

dict(slug='gold-chain-value.html', crumb='Gold Chain Value',
 title='How Much Is My Gold Chain Worth? 10k, 14k & 18k | Georgia Gold Buyers',
 desc='What a gold chain is worth: solid vs. hollow, how to read the clasp stamp, plated and gold-filled chains, and live melt values by weight and karat.',
 h1='How much is my <span>gold chain worth?</span>', h1_plain='How Much Is My Gold Chain Worth?',
 hero_sub='Weight and karat decide the value &mdash; not length or style.',
 answer='A gold chain is worth its <strong>weight &times; karat purity &times; the spot price</strong>. The stamp is usually on the clasp or a tag near it: <strong>10K (417), 14K (585), or 18K (750)</strong>. <strong>Hollow chains</strong> look big but weigh less. <strong>GF, GP, HGE, or 925</strong> stamps mean plated, gold-filled, or silver &mdash; not solid gold.',
 about=[{"@type":"Thing","name":"Gold chain"}],
 body=SPOT + '''<h2>Live value by weight and karat</h2>''' + table('chain', [5, 10, 20, 40]) + '''
<h2>Where to find the stamp</h2>
<p>Check the clasp, the jump ring, or a small tag near the clasp. &ldquo;Italy&rdquo; is a country of origin, not a purity mark. If the stamp is worn or missing, we test it free.</p>
<h2>Solid vs. hollow</h2>
<p>Hollow chains use a thin gold tube, so a thick-looking hollow chain can weigh far less than a thin solid one. Because we pay by weight, the scale tells the real story.</p>
<h2>Not solid gold</h2>
<ul>
<li><strong>GF / Gold Filled / 1/20 12K GF</strong> &mdash; a thin gold layer bonded to a base metal.</li>
<li><strong>GP / HGE / RGP</strong> &mdash; gold plated.</li>
<li><strong>925 or Sterling with a gold color</strong> &mdash; gold-plated silver (vermeil). We buy it as silver &mdash; see our <a href="sell-silver-coins-flatware.html">silver guide</a>.</li>
</ul>
<h2>Broken chains count</h2>
<p>Knotted, snapped, or missing-clasp chains are worth the same per gram as perfect ones. No need to fix them first.</p>
''' + ITEM_JS,
 faqs=[
  ('How much is a 14k gold chain worth?', 'Weight in grams &times; 0.585 &times; the gold spot price per gram. A 10-gram 14k chain holds 5.85 grams of pure gold; the table on this page shows its value live.'),
  ('Do you buy broken gold chains?', 'Yes. Broken, knotted, and tangled chains are valued by weight and purity just like intact ones.'),
  ('Is a chain stamped Italy real gold?', '“Italy” is where it was made, not what it’s made of. Look for a karat stamp like 14K or 585, or bring it in for a free test.'),
 ], entity=ENT),

dict(slug='wedding-band-value.html', crumb='Wedding Band Value',
 title='How Much Is My Gold Wedding Band Worth? | Georgia Gold Buyers',
 desc='What a gold or platinum wedding band is worth: reading the stamp, tungsten and titanium bands, and live melt values by weight and karat.',
 h1='How much is my <span>wedding band worth?</span>', h1_plain='How Much Is My Gold Wedding Band Worth?',
 hero_sub='Gold, platinum, or something else &mdash; the stamp inside the band tells you.',
 answer='A gold wedding band is worth its <strong>weight &times; karat purity &times; the spot price</strong>. Look inside the band for <strong>10K, 14K, or 18K</strong>. <strong>PT950 or PLAT</strong> means platinum (see our <a href="sell-platinum-palladium.html">platinum guide</a>). <strong>Tungsten, titanium, cobalt, and stainless</strong> bands have little or no resale metal value.',
 about=[{"@type":"Thing","name":"Wedding band"}],
 body=SPOT + '''<h2>Live value by weight and karat</h2>''' + table('band', [3, 5, 8, 12]) + '''
<h2>Read the inside of the band</h2>
<ul>
<li><strong>10K, 14K, 18K</strong> (or 417, 585, 750) &mdash; gold.</li>
<li><strong>PT950, PT900, PLAT</strong> &mdash; platinum.</li>
<li><strong>W, TC, TUNGSTEN, TI, COBALT, 316L</strong> &mdash; not precious metal.</li>
</ul>
<h2>Bands with diamonds</h2>
<p>We weigh and test the metal and look at any diamonds separately. Small accent diamonds usually add little resale value.</p>
<h2>Selling after a divorce or loss</h2>
<p>We handle these sales privately and without pressure. If you&rsquo;re settling an estate, see our <a href="estate-sales.html">inherited jewelry guide</a>.</p>
''' + ITEM_JS,
 faqs=[
  ('How much is a 14k wedding band worth?', 'Weight in grams &times; 0.585 &times; the gold spot price per gram. The table on this page calculates common weights live.'),
  ('Do you buy tungsten or titanium rings?', 'Tungsten, titanium, cobalt, and stainless steel have little or no resale metal value, so we generally do not buy them.'),
  ('Do you buy platinum wedding bands?', 'Yes. Platinum bands stamped PT950, PT900, or PLAT are valued by weight, purity, and the platinum spot price.'),
 ], entity=ENT),

dict(slug='charm-bracelet-value.html', crumb='Charm Bracelet Value',
 title='How Much Is My Gold Charm Bracelet Worth? | Georgia Gold Buyers',
 desc='What a gold charm bracelet is worth: mixed-karat charms, soldered vs. jump-ring charms, silver charms, and live melt values.',
 h1='How much is my <span>charm bracelet worth?</span>', h1_plain='How Much Is My Gold Charm Bracelet Worth?',
 hero_sub='Charms are often different karats &mdash; each one counts.',
 answer='A gold charm bracelet is worth the <strong>gold weight of the bracelet and every charm</strong>, each at its own karat. Charms are often mixed &mdash; a 14k bracelet can carry 10k, 18k, and even silver charms. We test each piece so nothing gets paid at the lowest karat.',
 about=[{"@type":"Thing","name":"Charm bracelet"}],
 body=SPOT + '''<h2>Live value by weight and karat</h2>''' + table('bracelet', [10, 20, 35, 50]) + '''
<h2>Why charms are tested one by one</h2>
<p>Charm bracelets are often built over years, so the pieces vary. Lumping everything at the lowest karat underpays you. We test the bracelet and each charm, group them by purity, and show you the math.</p>
<h2>Things that aren&rsquo;t gold</h2>
<ul>
<li>Enamel, glass, or stone inserts (we deduct their weight)</li>
<li>Sterling silver charms (bought as silver)</li>
<li>Gold-plated or gold-filled charms</li>
</ul>
<h2>Designer and collectible charms</h2>
<p>Some designer charms and bracelets can sell for more than melt. Bring any boxes or papers. See <a href="services.html">designer jewelry</a>.</p>
''' + ITEM_JS,
 faqs=[
  ('Are all the charms on my bracelet the same karat?', 'Often not. Charms are frequently added over time and can be 10k, 14k, 18k, silver, or plated. We test each one.'),
  ('Do I need to remove the charms?', 'No. We can test them attached; if needed, we weigh groups separately with your permission.'),
  ('Do you buy silver charm bracelets?', 'Yes. Sterling silver charm bracelets are valued by silver weight and the silver spot price.'),
 ], entity=ENT),

dict(slug='how-to-choose-a-gold-buyer.html', crumb='How to Choose a Gold Buyer',
 title='How to Choose a Gold Buyer: Red Flags & Questions to Ask | Georgia Gold Buyers',
 desc='How to pick a trustworthy gold buyer in Georgia: questions to ask, red flags (no weight shown, mixed karats, mail-in kits, pop-up hotel buyers), and your rights.',
 h1='How to choose <span>a gold buyer</span>', h1_plain='How to Choose a Gold Buyer: Red Flags and Questions to Ask',
 hero_sub='Seven questions that separate a fair offer from a bad one.',
 answer='A trustworthy gold buyer <strong>tests and weighs in front of you</strong>, tells you the <strong>weight, karat, and spot price</strong> behind the offer, pays each karat separately, uses a <strong>state-inspected scale</strong>, and lets you walk away with no fee. Red flags: offers &ldquo;per piece,&rdquo; hidden scales, pressure to decide now, and buyers who won&rsquo;t explain the math.',
 citations=["https://www.agr.georgia.gov/weights-measures","https://georgiacommons.org/code/43-37-3/text"],
 body='''<h2>Seven questions to ask</h2>
<ol>
<li><strong>&ldquo;What does it weigh?&rdquo;</strong> In grams or pennyweight, on a scale you can see.</li>
<li><strong>&ldquo;What karat did you test it as?&rdquo;</strong> And how &mdash; acid, electronic, or XRF.</li>
<li><strong>&ldquo;What spot price are you using?&rdquo;</strong> Compare it with a live source like our <a href="gold-prices.html">prices page</a>.</li>
<li><strong>&ldquo;Are you paying each karat separately?&rdquo;</strong> 10k, 14k, and 18k should never be lumped together.</li>
<li><strong>&ldquo;Is your scale inspected?&rdquo;</strong> The <a href="https://www.agr.georgia.gov/weights-measures" target="_blank" rel="noopener">Georgia Department of Agriculture</a> inspects commercial scales for accuracy.</li>
<li><strong>&ldquo;Are there any fees?&rdquo;</strong> Testing and quotes should be free.</li>
<li><strong>&ldquo;Can I think about it?&rdquo;</strong> The answer should always be yes.</li>
</ol>
<h2>Red flags</h2>
<ul>
<li><strong>Offers &ldquo;per piece&rdquo; or &ldquo;for the lot&rdquo;</strong> with no weight or karat.</li>
<li><strong>Scale out of sight</strong>, or items taken to a back room.</li>
<li><strong>Pressure</strong> &mdash; &ldquo;this price is only good right now.&rdquo;</li>
<li><strong>Pop-up buyers</strong> in hotel rooms with no permanent address to go back to.</li>
<li><strong>Mail-in kits</strong> where your gold leaves your hands before you see an offer.</li>
<li><strong>No ID requested.</strong> Georgia precious-metal dealers must record seller identification (<a href="https://georgiacommons.org/code/43-37-3/text" target="_blank" rel="noopener">O.C.G.A. &sect; 43-37-3</a>). A buyer who skips it is cutting corners.</li>
</ul>
<h2>Compare offers the right way</h2>
<p>Don&rsquo;t compare dollar totals alone. Compare the <strong>weight</strong>, <strong>karat</strong>, and <strong>percentage of melt value</strong> each buyer is paying. See <a href="how-much-is-gold-worth.html">how to calculate melt value</a>.</p>
<h2>How we do it</h2>
<p>At Georgia Gold Buyers, every item is tested with an XRF analyzer and weighed on a precision scale in front of you. We show the weight, purity, and spot price, pay each karat separately, and there&rsquo;s never a fee to walk away. See <a href="selling-gold-what-to-expect.html">what to expect</a>.</p>
''',
 faqs=[
  ('How do I know if a gold buyer is fair?', 'A fair buyer weighs and tests in front of you, tells you the weight, karat, and spot price used, pays each karat separately, and lets you leave without a fee.'),
  ('Should gold buyers weigh in front of me?', 'Yes. You should see the scale and the reading. The Georgia Department of Agriculture inspects commercial scales for accuracy.'),
  ('Are mail-in gold buying kits safe?', 'Your items leave your hands before you see an offer, which makes comparing and walking away harder. A local buyer who tests in front of you avoids that.'),
  ('Do gold buyers need my ID in Georgia?', 'Yes. Georgia law requires precious-metal dealers to record seller identification, so bring a valid government-issued photo ID.'),
 ], entity='Georgia Gold Buyers tests and weighs every item in front of the seller at 3996 N Valdosta Rd, Valdosta, GA 31602 ((229) 375-0015) and 120 S Point Blvd, McDonough, GA 30253 ((678) 919-9265).'),
]

# ---------- Spanish page shell ----------
ES_SHELL = [
 ('>Call Us<', '>Llámenos<'), ('>Get Free Quote<', '>Cotización gratis<'), ('>Home<', '>Inicio<'), ('>Services<', '>Servicios<'),
 ('>Gold Prices<', '>Precios del oro<'), ('>Testing<', '>Pruebas<'), ('>Estate Sales<', '>Herencias<'), ('>About<', '>Nosotros<'),
 ('>Locations<', '>Ubicaciones<'), ('>Get a Quote<', '>Cotizar<'), ('>Guides<', '>Guías<'),
 ('Gold prices are near record highs —', 'El oro está cerca de precios récord —'),
 ('now is the best time to sell. Get your free appraisal today.', 'es un buen momento para vender. Pida su tasación gratis hoy.'),
 ('Google Reviews<', 'reseñas en Google<'),
 ('>Get Your Free Quote<', '>Obtenga su cotización gratis<'),
 ('Fill out the form below and a specialist will contact you within minutes.', 'Llene el formulario y un especialista se comunicará con usted en minutos.'),
 ('>Full Name<', '>Nombre completo<'), ('>Phone Number<', '>Teléfono<'), ('>Email<', '>Correo electrónico<'), ('>(optional)<', '>(opcional)<'),
 ('>What would you like to sell?<', '>¿Qué desea vender?<'), ('>Gold Jewelry<', '>Joyas de oro<'), ('>Silver Items<', '>Artículos de plata<'),
 ('>Coins &amp; Bullion<', '>Monedas y lingotes<'), ('>Diamonds &amp; Gems<', '>Diamantes y gemas<'), ('>Platinum / Palladium<', '>Platino / paladio<'),
 ('>Luxury Watch<', '>Reloj de lujo<'), ('>Designer Handbag<', '>Bolso de diseñador<'), ('>Designer Jewelry<', '>Joyas de diseñador<'),
 ('>Estate Sale / Inherited Collection<', '>Herencia / colección heredada<'), ('>Multiple Items<', '>Varios artículos<'), ('>Other / Not Sure<', '>Otro / no estoy seguro<'),
 ('>Preferred Location<', '>Ubicación preferida<'), ('>Additional Details<', '>Detalles adicionales<'),
 ('>Text Me My Free Quote<', '>Envíenme mi cotización por texto<'),
 ('By tapping “Text Me My Free Quote,” you agree to receive text messages from Georgia Gold Buyers about your quote and appointment. Message frequency varies. Msg &amp; data rates may apply. Reply HELP for help, STOP to opt out.',
  'Al tocar “Envíenme mi cotización por texto”, acepta recibir mensajes de texto de Georgia Gold Buyers sobre su cotización y cita. La frecuencia varía. Pueden aplicarse tarifas de mensajes y datos. Responda HELP para ayuda o STOP para cancelar.'),
 ('>Privacy Policy<', '>Política de privacidad<'), ('>Terms<', '>Términos<'),
 ('Your information is secure and will never be shared.', 'Su información está segura y nunca se compartirá.'),
 ("Georgia's trusted gold, silver, and jewelry buyers since 2012. Two locations serving McDonough and Valdosta. Free appraisals, instant cash payment.",
  'Compradores de oro, plata y joyas de confianza en Georgia desde 2012. Dos ubicaciones: McDonough y Valdosta. Tasación gratis y pago inmediato.'),
 ('>Quick Links<', '>Enlaces<'), ('>Seller Guides<', '>Guías para vendedores<'), ('>Areas We Serve<', '>Áreas que servimos<'), ('>About Us<', '>Nosotros<'),
 ('>Leave a Review<', '>Déjenos una reseña<'), ('>McDonough Review<', '>Reseña McDonough<'), ('>Valdosta Review<', '>Reseña Valdosta<'),
 ('>Contact Us<', '>Contacto<'), ('All rights reserved.', 'Todos los derechos reservados.'), ('>Terms of Service<', '>Términos de servicio<'),
 ('>Which location would you like to call?<', '>¿A qué tienda desea llamar?<'), ('>Call Now<', '>Llamar<'),
 ('placeholder="Your full name"', 'placeholder="Su nombre completo"'), ('placeholder="you@email.com"', 'placeholder="usted@correo.com"'),
 ("placeholder=\"Describe what you'd like to sell, quantity, condition, etc.\"", 'placeholder="Describa lo que desea vender, cantidad, estado, etc."'),
 ('aria-label="Call us"', 'aria-label="Llámenos"'), ('aria-label="Menu"', 'aria-label="Menú"'),
 ("btn.textContent = 'Sending...';", "btn.textContent = 'Enviando...';"),
 ('btn.textContent = "Thank You! We\'ll Call You Shortly.";', 'btn.textContent = "¡Gracias! Le llamaremos pronto.";'),
 ('(Testing Page)', '(Guía en español)'),
 ('\n      Call Now\n', '\n      Llamar\n'), ('\n      Get Free Quote\n', '\n      Cotización gratis\n'),
]

def es_shell(t):
    for a, b in ES_SHELL:
        t = t.replace(a, b)
    return t

# ---------- Spanish town pages ----------
ES_TOWNS = ['Stockbridge', 'Jonesboro', 'Tifton', 'Moultrie']

def es_towns(TOWNS, LOC, town_slug, rmin):
    out = []
    H = {'V': 'lunes a viernes de 10am a 5pm y sábado de 10am a 6pm; cerrado el domingo', 'M': 'lunes a sábado de 10am a 6pm; cerrado el domingo'}
    R = {
     'Tifton': 'Tome la I-75 sur hacia Valdosta y salga a la US 41 / North Valdosta Road.',
     'Moultrie': 'Tome la GA 37 / GA 133 al este hacia Valdosta y luego la US 41 / North Valdosta Road al norte.',
     'Stockbridge': 'Tome la I-75 sur hacia McDonough y siga las señales a South Point Boulevard.',
     'Jonesboro': 'Tome la GA 138 al este hasta la I-75 sur hacia McDonough.',
    }
    for town, st, county, lk, mi, mn, route, note in TOWNS:
        if town not in ES_TOWNS: continue
        L = LOC[lk]; m = rmin(mn); cty = county.replace(' County', '')
        en = town_slug(town, st)
        slug = f"es-vender-oro-{town.lower()}-{st.lower()}.html"
        out.append(dict(slug=slug, alt=en, lang='es', parent='areas-we-serve.html', parent_name='Áreas que servimos', crumb=f'{town}, {st}', ld_type='WebPage', og=L['og'],
         title=f'Vender oro cerca de {town}, {st} | Georgia Gold Buyers {L["name"]} (~{m} min)',
         desc=f'¿Quiere vender oro, plata, monedas o joyas cerca de {town}, {st}? Nuestra tienda de {L["name"]} está a unas {mi} millas (~{m} minutos). Prueba gratis y pago en el momento.',
         h1=f'Vender oro cerca de <span>{town}, {st}</span>', h1_plain=f'Vender oro cerca de {town}, {st}',
         hero_sub=f'Nuestra tienda de {L["name"]} está a unos {m} minutos de {town}. Prueba gratis y pago en el momento.',
         answer=f'La tienda de Georgia Gold Buyers más cercana a {town} es la de <strong>{L["name"]}, en {L["addr"]}</strong>, a unas <strong>{mi} millas, aproximadamente {m} minutos</strong> en auto. Horario: {H[lk]}. Llame al <a href="tel:{L["tel"]}">{L["phone"]}</a>. Compramos oro, plata, platino, monedas, joyas y relojes de lujo; probamos todo frente a usted y pagamos en el momento.',
         about=[{"@type": "Place", "name": f"{town}, {st}"}, {"@type": "AdministrativeArea", "name": f"Condado de {cty}, {st}"}],
         body=f'''<h2>Cómo llegar desde {town}</h2>
<div class="table-scroll"><table><tbody>
<tr><td>Tienda más cercana</td><td><a href="{L['page']}">Georgia Gold Buyers &ndash; {L['name']}</a></td></tr>
<tr><td>Dirección</td><td>{L['addr']}</td></tr>
<tr><td>Distancia</td><td>Unas {mi} millas</td></tr>
<tr><td>Tiempo en auto</td><td>Unos {m} minutos con tráfico normal</td></tr>
<tr><td>Horario</td><td>{H[lk].capitalize()}</td></tr>
<tr><td>Teléfono</td><td><a href="tel:{L['tel']}">{L['phone']}</a></td></tr>
</tbody></table></div>
<p><strong>Ruta:</strong> {R[town]} <a href="{L['map']}" target="_blank" rel="noopener">Abrir en Google Maps</a>.</p>
<h2>Qué compramos</h2>
<ul>
<li>Joyas de oro, cadenas, anillos de graduación y oro roto &mdash; <a href="es-cuanto-vale-mi-oro.html">¿cuánto vale mi oro?</a></li>
<li>Monedas de plata, cubiertos de plata sterling y lingotes</li>
<li>Monedas y lingotes de oro, platino y paladio</li>
<li>Relojes Rolex y de lujo, joyas de diseñador y bolsos</li>
</ul>
<h2>Antes de venir</h2>
<p>Traiga una identificación oficial vigente con foto (la ley de Georgia lo exige) y sus piezas. Puede llegar sin cita, pero si viene de lejos, <a href="#quote-form">pida una cotización gratis</a> o llame antes. Vea <a href="es-que-traer-para-vender-oro.html">qué traer y qué esperar</a>. ¿Prefiere comparar primero? Lea <a href="es-vender-o-empenar-oro.html">vender o empeñar</a>.</p>
''',
         faqs=[
          (f'¿Dónde puedo vender oro cerca de {town}, {st}?', f'En Georgia Gold Buyers {L["name"]}, {L["addr"]}, a unas {mi} millas (unos {m} minutos) de {town}. Llame al {L["phone"]}.'),
          (f'¿Qué tan lejos está Georgia Gold Buyers de {town}?', f'Unas {mi} millas, aproximadamente {m} minutos en auto con tráfico normal.'),
          ('¿Necesito cita?', 'No. Puede llegar sin cita durante el horario. Si viene de lejos, recomendamos llamar antes.'),
         ],
         entity=f'Georgia Gold Buyers atiende a {town}, {st} desde su tienda de {L["name"]} en {L["addr"]} ({L["phone"]}), a unas {mi} millas. Horario: {H[lk]}.'))
    return out

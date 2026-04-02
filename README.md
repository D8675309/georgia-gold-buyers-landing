# Georgia Gold Buyers — Landing Page

High-converting landing page for Georgia Gold Buyers, a local gold, silver, jewelry, and coin buying business with locations in McDonough, GA and Valdosta, GA.

## Live Preview

Deploy as a static site — single `index.html` file with no dependencies.

## Features

- **Conversion-optimized** — hero with dual CTAs, lead capture form, click-to-call, Google Maps directions
- **Mobile-first** — sticky bottom bar with Call Now + Get Directions on mobile
- **Real social proof** — 6 verified Google reviews (5.0 rating, 84+ reviews)
- **Trust-focused** — designed for adults 35–75 selling valuables for cash
- **SEO-ready** — Schema.org LocalBusiness JSON-LD, meta tags, Open Graph
- **Fast** — single file, no external dependencies beyond Google Fonts

## Page Sections

1. Sticky header with phone + CTA
2. Hero with headline, subheadline, trust bar
3. What We Buy (6 categories with SVG icons)
4. How It Works (3 steps)
5. Customer Reviews (6 real Google reviews)
6. Why Choose Us (4 trust pillars)
7. Lead Capture Form
8. Locations (McDonough + Valdosta)
9. FAQ (6 accordion items)
10. Footer

## Locations

| Location | Address | Phone |
|----------|---------|-------|
| McDonough | 120 S Point Blvd, McDonough, GA 30253 | (678) 919-9265 |
| Valdosta | 3996 N Valdosta Rd, Valdosta, GA 31602 | (229) 375-0015 |

## Tech Stack

- Single HTML file (~60KB)
- Embedded CSS (no separate stylesheet)
- Vanilla JavaScript (FAQ accordion, form validation, sticky header)
- Google Fonts (DM Sans)
- Inline SVG icons

## Deployment

This is a static site. Deploy to any hosting platform:

```bash
# Netlify
netlify deploy --prod --dir=.

# Vercel
vercel --prod

# GitHub Pages
# Enable in repo Settings → Pages → Deploy from branch

# GoHighLevel
# Paste into a Custom Code funnel page or use as reference for the page builder
```

## Form Integration

The lead capture form currently submits to `#`. To connect it:

1. **GoHighLevel**: Replace `action="#"` with your GHL form webhook URL
2. **Any webhook**: Point the form action to your CRM/automation endpoint
3. **Netlify Forms**: Add `netlify` attribute to the `<form>` tag

## License

Private — Georgia Gold Buyers. All rights reserved.

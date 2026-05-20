#!/usr/bin/env python3
"""
Fix conversion tracking across all HTML files:
1. Add onclick handler to every <a href="tel:..."> to fire Phone Call conversion
2. Add onclick handler to every Maps link (maps.app.goo.gl, maps.google.com) to fire Maps conversion
3. Re-route lead form submission send_to label to the correct Submit Lead Form action
4. Re-route any plain `mailto:` links to fire Email conversion (bonus)

Conversion labels (from Google Ads API):
  Email:        AW-16941991771/xH6vCLTht88aENuOyY4_
  Phone Call:   AW-16941991771/FJz9CITzxM8aENuOyY4_
  Google Maps:  AW-16941991771/dHuGCN-Sxc8aENuOyY4_
  Lead Form:    AW-16941991771/zCH5CJP9xs8aENuOyY4_
"""
import re, os, sys, glob

WRONG_LEAD_FORM_LABEL = "AW-16941991771/xH6vCLTht88aENuOyY4_"  # Email label being used for lead form
CORRECT_LEAD_FORM_LABEL = "AW-16941991771/zCH5CJP9xs8aENuOyY4_"
PHONE_LABEL = "AW-16941991771/FJz9CITzxM8aENuOyY4_"
MAPS_LABEL = "AW-16941991771/dHuGCN-Sxc8aENuOyY4_"
EMAIL_LABEL = "AW-16941991771/xH6vCLTht88aENuOyY4_"

# Helper script we inject once per page (idempotent)
TRACKER_SCRIPT = """<!-- Conversion tracking helpers (added by axon-ads) -->
<script>
window.__gads_fire = function(label) {
  if (typeof gtag === 'function') {
    try { gtag('event', 'conversion', { 'send_to': label }); } catch(e) {}
  }
  return true; // always allow default link behavior
};
</script>"""

# Patterns
TEL_PATTERN = re.compile(r'(<a\s[^>]*?href=["\']tel:[^"\']+["\'])([^>]*?)>', re.IGNORECASE)
MAPS_PATTERN = re.compile(r'(<a\s[^>]*?href=["\'](?:https?://maps\.app\.goo\.gl/[^"\']+|https?://maps\.google\.com/[^"\']+|https?://www\.google\.com/maps[^"\']*)["\'])([^>]*?)>', re.IGNORECASE)
MAILTO_PATTERN = re.compile(r'(<a\s[^>]*?href=["\']mailto:[^"\']+["\'])([^>]*?)>', re.IGNORECASE)

def add_onclick(match, label):
    """Add or merge an onclick attribute that fires the conversion label."""
    pre, post = match.group(1), match.group(2)
    if 'onclick=' in (pre + post).lower():
        # Merge into existing onclick
        def inject_into_onclick(m):
            quote = m.group(1)
            current = m.group(2)
            # Only add if not already firing this exact label
            if label in current:
                return m.group(0)
            return f'onclick={quote}window.__gads_fire(\\\'{label}\\\');{current}{quote}'
        attrs = pre + post
        new_attrs = re.sub(r'onclick=(["\'])(.*?)\1', inject_into_onclick, attrs, flags=re.IGNORECASE | re.DOTALL)
        return new_attrs + ">"
    else:
        return f"{pre}{post} onclick=\"window.__gads_fire('{label}')\">"

def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()
    new = original

    # 1) Inject tracker script if not present (before </head>)
    if "window.__gads_fire" not in new:
        if "</head>" in new:
            new = new.replace("</head>", TRACKER_SCRIPT + "\n</head>", 1)
        else:
            # Fallback: prepend to body
            new = TRACKER_SCRIPT + "\n" + new

    # 2) Fix tel: links
    tel_count = 0
    def tel_sub(m):
        nonlocal tel_count
        # Skip if our onclick is already there
        full = m.group(0)
        if PHONE_LABEL in full:
            return full
        tel_count += 1
        return add_onclick(m, PHONE_LABEL)
    new = TEL_PATTERN.sub(tel_sub, new)

    # 3) Fix maps: links
    maps_count = 0
    def maps_sub(m):
        nonlocal maps_count
        full = m.group(0)
        if MAPS_LABEL in full:
            return full
        maps_count += 1
        return add_onclick(m, MAPS_LABEL)
    new = MAPS_PATTERN.sub(maps_sub, new)

    # 4) Fix mailto: links
    mail_count = 0
    def mail_sub(m):
        nonlocal mail_count
        full = m.group(0)
        if EMAIL_LABEL in full:
            return full
        mail_count += 1
        return add_onclick(m, EMAIL_LABEL)
    new = MAILTO_PATTERN.sub(mail_sub, new)

    # 5) Fix lead form send_to label — replace wrong label with correct one ONLY in the form-submit handler context
    # We look for the gtag conversion fire AFTER /api/leads/submit
    form_fixed = 0
    if "/api/leads/submit" in new and WRONG_LEAD_FORM_LABEL in new:
        # Find the segment that contains 'leads/submit' and replace the next occurrence of the wrong label
        # Use a non-greedy search within ~1500 chars after the submit URL
        idx = new.find("/api/leads/submit")
        if idx > -1:
            window_end = idx + 1500
            window_seg = new[idx:window_end]
            if WRONG_LEAD_FORM_LABEL in window_seg:
                new_window = window_seg.replace(WRONG_LEAD_FORM_LABEL, CORRECT_LEAD_FORM_LABEL, 1)
                new = new[:idx] + new_window + new[window_end:]
                form_fixed = 1

    if new != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"{path}: tel+={tel_count}, maps+={maps_count}, mail+={mail_count}, form-label-fix={form_fixed}")
        return True
    else:
        print(f"{path}: (no changes)")
        return False

if __name__ == "__main__":
    files = sorted(glob.glob("*.html"))
    changed = 0
    for p in files:
        if fix_file(p):
            changed += 1
    print(f"\nDone. {changed}/{len(files)} files modified.")

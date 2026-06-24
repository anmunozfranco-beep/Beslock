# NEXT TASK – Align Fallback Metadata for LinkedIn Preview

## Context

The Open Graph diagnosis confirmed that:

* `og:title` exists and is correct.
* `og:description` exists and is correct.
* `og:image` exists and points to a valid public PNG.
* The image is accessible to both normal clients and `LinkedInBot`.
* Cloudflare is not blocking LinkedInBot.
* There are no duplicate OG tags.

However, LinkedIn Post Inspector still shows:

* Title: Home
* Image: No image found
* Description: Seguridad inteligente para hogares, oficinas y accesos exteriores.

Codex detected that the current HTML has no proper `<title>` tag and that fallback/schema signals still contain “Home”.

## Objective

Align all fallback metadata for the homepage so LinkedIn, search engines and social platforms receive consistent signals.

Target URL:

https://beslock.com.co/

## Required Changes

### 1. Add or correct homepage `<title>`

Ensure the rendered homepage HTML contains:

```html
<title>BESLOCK® Smart Security Solutions</title>
```

This must appear inside `<head>`.

If WordPress/SiteSEO can set this cleanly through settings, prefer that.

If not, extend the existing WPCode snippet only for the homepage.

---

### 2. Add or correct meta description

Ensure the rendered homepage HTML contains:

```html
<meta name="description" content="Seguridad inteligente para hogares, oficinas y accesos exteriores.">
```

There must not be an empty meta description overriding it.

If an empty `<meta name="description" content="">` currently exists, remove, replace or override it cleanly.

---

### 3. Check JSON-LD / Schema fallback

Inspect rendered homepage source for JSON-LD or schema values containing:

* `"name":"Home"`
* `"headline":"Home"`
* breadcrumb name `Home`

If possible, replace homepage schema name with:

```text
BESLOCK® Smart Security Solutions
```

Do not break WooCommerce, breadcrumbs, product schema or navigation.

If changing JSON-LD is risky, report it and leave it unchanged.

---

### 4. Preserve existing Open Graph tags

Do not remove the existing Open Graph snippet unless necessary.

Preserve:

```html
<meta property="og:title" content="BESLOCK® Smart Security Solutions" />
<meta property="og:description" content="Seguridad inteligente para hogares, oficinas y accesos exteriores." />
<meta property="og:image" content="https://beslock.com.co/wp-content/uploads/2026/06/beslock-og-linkedin-1200x627-1.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="627" />
<meta property="og:image:type" content="image/png" />
```

---

## Verification

After changes, run:

```bash
curl -L https://beslock.com.co/ -o /tmp/beslock-home.html
```

Verify:

1. `<title>` exists and equals `BESLOCK® Smart Security Solutions`.
2. `meta name="description"` exists and is not empty.
3. `og:title` exists and is correct.
4. `og:description` exists and is correct.
5. `og:image` exists and points to the valid PNG.
6. No duplicate conflicting `og:title`, `og:description`, or `og:image`.
7. Search the HTML for `Home` and report where it still appears.

Also test as LinkedInBot:

```bash
curl -L -A "LinkedInBot/1.0" https://beslock.com.co/ -o /tmp/beslock-linkedinbot.html
```

Confirm LinkedInBot receives the same metadata.

## Deliverables

1. Summary of changes made.
2. Exact metadata now rendered in `<head>`.
3. Whether `Home` still appears in fallback/schema.
4. Any risks or remaining issues.
5. Do not claim LinkedIn is fixed unless Post Inspector confirms it.

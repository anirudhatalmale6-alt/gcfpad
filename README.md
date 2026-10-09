# GCFPAD — Global Confederation for Promotion and Development

Static website. Nine pages, no framework, no build step required to serve it.
Open `index.html` in a browser and it works.

```
index.html          Home — the five sections from the brief
about.html          Who we are: vision, mission, six values
what-we-do.html     The six areas of work + the five-step approach
our-work.html       Projects, featuring Saint Francis Mission & Foundation for Caring
partnerships.html   The seven partner categories + the inquiry form
leadership.html     Governance and leadership
contact.html        Inquiry form and how to reach GCFPAD
privacy.html        Privacy policy (draft — needs legal review)
terms.html          Terms of use (draft — needs legal review)

assets/style.css    One stylesheet for every page
assets/site.js      Sticky nav, mobile drawer, scroll reveal, the inquiry form
assets/img/         Placeholder artwork + favicon
build/              The generators. You never need to run these to use the site.
```

---

## What still needs content from you

Nothing on this site is invented. Where I did not have a fact, the page says so
in a marked box rather than carrying a plausible-looking guess. An
institutional site that is caught with a made-up address or a made-up board
member does not recover from it.

The boxes are marked **Content to add** and they are on:

- **about.html** — organizational background, history, legal status
- **what-we-do.html** — the detail behind each of the six areas
- **our-work.html** — the Saint Francis project description, location, partners, results
- **leadership.html** — every name, title, photograph and biography, and a check
  that the six governing bodies match your actual statutes
- **contact.html** — registered address, telephone, social media accounts
- **privacy.html / terms.html** — the registered entity name, and a legal review

## Replacing the placeholder artwork with real photographs

Every image is a single file in `assets/img/`. Drop a photograph in with the
same name and nothing else changes — the aspect boxes are fixed, so the layout
cannot shift.

| File | Where it appears | Suggested size |
|---|---|---|
| `hero.svg` | Homepage hero | 1920 × 1080 or wider |
| `project.svg` | Featured project | 1600 × 1100 |
| `approach.svg` | spare | 1920 × 900 |
| `about.svg` `whatwedo.svg` `work.svg` `partners.svg` `leadership.svg` `contact.svg` | Internal page headers | 1600 × 900 |
| `person-1.svg` … `person-6.svg` | Leadership portraits | 800 × 800, square |

If you supply `.jpg` files instead, change the extension in the matching
`<img src="assets/img/…">` — that is the only edit.

The logo is the small mark beside "GCFPAD" in the header and footer. It is
drawn in SVG inside `build/make_pages.py` (the `MARK` constant) and appears on
every page, so when the real logo file arrives it is one replacement there and
a rebuild.

## The inquiry form

🚨 **The form does not post anywhere yet, and it says so rather than pretending.**

A contact form that validates nicely and quietly drops the message is worse
than no form at all, because the visitor believes they have been in touch.
So the top of `assets/site.js` has two lines:

```js
var ENDPOINT = '';     // the URL that receives the inquiry
var WHATSAPP = '';     // or a WhatsApp number, digits only, no +
```

- Fill in `ENDPOINT` and the form posts JSON `{name, organization, email,
  country, interest, message}` and expects `{"ok":true}` back.
- Fill in `WHATSAPP` instead and the button opens WhatsApp with the inquiry
  already written out.
- Leave both empty and the form tells the visitor honestly that it is not
  connected yet.

## Rebuilding

Only needed if you change the shared navigation, footer or head block.

```sh
python3 build/make_images.py    # regenerates the placeholder artwork
python3 build/make_pages.py     # regenerates the nine HTML pages
```

The generators exist so that the menu and footer cannot drift out of sync
across nine pages. The output is ordinary readable HTML.

## Notes

- Typefaces are Newsreader and Public Sans, loaded from Google Fonts. Nothing
  else is loaded from anybody else's server — no icon fonts, no analytics, no
  tracking scripts, no CSS frameworks.
- Mobile-first, tested at 390 px and 1440 px.
- Respects `prefers-reduced-motion`: the entrance animations switch off for
  visitors who have asked their device for less movement.

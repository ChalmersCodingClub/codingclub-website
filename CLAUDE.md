# Chalmers Coding Club – webbplats

Statisk sajt för chalmerscoding.club. Ren HTML, en css-fil och ett litet
byggskript. Ingen pakethanterare, inget ramverk. Filerna i repot är de som
deployas.

## Struktur

| Sökväg                     | Vad                                                  |
| -------------------------- | ---------------------------------------------------- |
| `index.html`               | Startsidan. En sektion per verksamhet, kort text + länk |
| `meetup/`                  | Tisdagsträffarnas schema (hämtas som CSV från Google Sheets) |
| `chalmerschallenge/`       | Alla års Chalmers Challenge                          |
| `bootcamp/`                | Alla års boot camps                                  |
| `golf/`                    | Alla års golfmästerskap                              |
| `resor/`                   | Reseberättelser (EUC, NWERC, NCPC)                   |
| `euc24/`, `euc25/`, `nwerc22.html`, `nwerc24.html` | Själva resebloggarna, egen stil |
| `partials/header.html`     | Gemensam header, klistras in av `build.py`           |
| `styling2.css`             | All gemensam css                                     |
| `img/`                     | Bilder (webp)                                        |
| `.htaccess`                | Redirects (`/discord`, `/blimedlem`, gamla `/en.html`) |

## Bygg: `python3 build.py`

Headern finns på ett ställe, `partials/header.html`, och klistras in i varje
sida mellan markörerna

```html
<!-- include:header -->
<!-- /include:header -->
```

Kör `python3 build.py` efter att ha ändrat något i `partials/`. Skriptet
skriver om innehållet mellan markörerna i alla `*.html` och är idempotent.
`python3 build.py --check` avslutar med fel om någon sida är inaktuell.
`git-hooks/pre-commit` kör bygget och sedan prettier; installera kroken med
`ln -sf ../../git-hooks/pre-commit .git/hooks/pre-commit`.

Ändra aldrig headern direkt i en sida, ändringen skrivs över vid nästa bygge.
Länkarna i partialen är rotrelativa (`/index.html#...`, `/logo.webp`) så att
samma fragment fungerar från alla kataloger.

## Lägga till ett nytt år

Startsidan ska inte växa. Varje verksamhet har en undersida med en `article`
per år, nyast först. Lägg det nya året överst där. Startsidans sektion har
bara den generiska texten, en eventuell bild och en länk till undersidan.

Mall för en undersida: kopiera t.ex. `golf/index.html`. Heron sätter bara sin
färg via en palettvariabel (`--c-golf` osv), resten kommer från
`.page-hero`, `.page-main`, `article` och `.page-back` i `styling2.css`.

## Bilder

Alla bilder är webp, max 1600 px på långsidan, kvalitet 80. Konvertera nya
bilder med ffmpeg innan de läggs i repot:

```sh
ffmpeg -i foto.jpg -vf "scale=w='min(1600,iw)':h='min(1600,ih)':force_original_aspect_ratio=decrease" -c:v libwebp -quality 80 img/foto.webp
```

ffmpeg roterar enligt EXIF automatiskt. Alla `<img>` utom headerloggan har
`loading="lazy"`. `width`-attribut går bra, css:en krymper bilder till
skärmbredden på mobil.

## Färger och kontrast

Paletten ligger som variabler i `:root` i `styling2.css` (`--c-about`,
`--c-cc`, `--c-bootcamp` ...). Sektioner och undersidornas heros använder
variablerna, så en färg ändras på ett ställe.

Länkfärgen styrs av `--link` per sektion. Kravet är WCAG AA, minst 4.5:1 mot
bakgrunden: mörkblå på ljusa bakgrunder (standard), vit på sektioner med vit
text (`.shadowed`), nästan svart marinblå på den lila boot camp-sektionen.
Kontrollera kontrasten om en bakgrundsfärg ändras.

## Mobil

Alla sidor har `<meta name="viewport">`. Brytpunkterna i `styling2.css` är
1000 px (smalare header) och 700 px (mindre rubriker, header slutar vara
sticky, mindre marginaler). Navlänken för reseberättelser heter "Resor" för
att åtta länkar ska få plats på en rad på desktop.

## Cache

`styling2.css` länkas med `?v=DATUM`. Bumpa versionen i alla sidor när css:en
ändras: `grep -rl 'styling2.css?v=' --include=*.html . | xargs sed -i 's/v=GAMMAL/v=NY/'`.

## Regler

- Committa eller pusha aldrig utan att bli ombedd.
- Sajten finns bara på svenska. Den gamla engelska sidan är borttagen och
  `/en.html` omdirigeras till startsidan.

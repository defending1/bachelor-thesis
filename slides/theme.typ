#import "@preview/touying:0.6.1": *
#import themes.metropolis: *

// Palette di colori accademica (UniPi Blue)
#let primary-color = rgb("#003366")
#let secondary-color = rgb("#4A6B82")
#let accent-color = rgb("#D9534F")
#let bg-light = rgb("#F8F9FA")

#let setup-presentation(
  title: [Titolo della Presentazione],
  subtitle: [Sottotitolo o Tipologia Elaborato],
  author: [Nome Cognome],
  institution: [Università di Pisa],
  date: datetime.today(),
  body,
) = {
  show: metropolis-theme.with(
    aspect-ratio: "16-9",
    config-info(
      title: title,
      subtitle: subtitle,
      author: author,
      institution: institution,
      date: date,
    ),
    config-colors(
      primary: primary-color,
      secondary: secondary-color,
      neutral-dark: rgb("#1F2937"),
      neutral-light: bg-light,
    ),
  )

  body
}

// Block helper per definizioni
#let def-box(title: "", body) = block(
  fill: rgb("#EFF6FF"),
  stroke: (left: 4pt + primary-color),
  inset: (x: 12pt, y: 10pt),
  radius: (right: 4pt),
  width: 100%,
  [
    #text(weight: "bold", fill: primary-color)[
      Definizione #if title != "" [(#title)]
    ]
    #v(4pt)
    #body
  ]
)

// Block helper per teoremi
#let thm-box(title: "", body) = block(
  fill: rgb("#F0FDF4"),
  stroke: (left: 4pt + rgb("#166534")),
  inset: (x: 12pt, y: 10pt),
  radius: (right: 4pt),
  width: 100%,
  [
    #text(weight: "bold", fill: rgb("#166534"))[
      Teorema #if title != "" [(#title)]
    ]
    #v(4pt)
    #body
  ]
)

// Block helper per esempi/note
#let example-box(title: "", body) = block(
  fill: rgb("#FFFBEB"),
  stroke: (left: 4pt + rgb("#B45309")),
  inset: (x: 12pt, y: 10pt),
  radius: (right: 4pt),
  width: 100%,
  [
    #text(weight: "bold", fill: rgb("#B45309"))[
      Esempio #if title != "" [(#title)]
    ]
    #v(4pt)
    #body
  ]
)

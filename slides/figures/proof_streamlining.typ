#import "@preview/cetz:0.3.3": canvas, draw

#let cDark = rgb("#1e293b")
#let cBlue = rgb("#0284c7")
#let cGreen = rgb("#16a34a")
#let cPurple = rgb("#9333ea")

#let bgKruskal = rgb("#f8fafc")
#let bgStegeman = rgb("#f0f9ff")
#let bgLandsberg = rgb("#f0fdf4")
#let bgRhodes = rgb("#faf5ff")

#let proof-streamlining-fig = canvas(length: 1.3cm, {
  import draw: *

  // Node 1: Kruskal (1977)
  rect((-4.2, 2.5), (4.2, 4.2), fill: bgKruskal, stroke: 2pt + cDark, radius: 0.3)
  content((0, 3.55), text(size: 14pt, weight: "bold", fill: cDark)[Kruskal (1977)])
  content((0, 2.95), text(size: 11.5pt, fill: cDark.lighten(20%))[40 pagine])

  // Arrow 1 -> 2
  line((0, 2.5), (0, 1.0), stroke: 2pt + cDark, mark: (end: "stealth", fill: cDark))
  content((0.25, 1.75), anchor: "west", text(size: 10.5pt, style: "italic", fill: gray.darken(40%))[semplificazione])

  // Node 2: Stegeman & Sidiropoulos (2007)
  rect((-5.0, -0.7), (5.0, 1.0), fill: bgStegeman, stroke: 2pt + cBlue, radius: 0.3)
  content((0, 0.35), text(size: 14pt, weight: "bold", fill: cBlue.darken(20%))[Stegeman & Sidiropoulos (2007)])
  content((0, -0.25), text(size: 11.5pt, fill: cBlue.darken(30%))[16 pagine])

  // Branching arrows
  line((0, -0.7), (-4.0, -2.2), stroke: 2pt + cBlue, mark: (end: "stealth", fill: cBlue))
  line((0, -0.7), (4.0, -2.2), stroke: 2pt + cBlue, mark: (end: "stealth", fill: cBlue))

  // Node 3: Landsberg (2010)
  rect((-7.8, -3.9), (-0.6, -2.2), fill: bgLandsberg, stroke: 2pt + cGreen, radius: 0.3)
  content((-4.2, -2.85), text(size: 13.5pt, weight: "bold", fill: cGreen.darken(20%))[Landsberg (2010)])
  content((-4.2, -3.45), text(size: 11.5pt, fill: cGreen.darken(30%))[4 pagine — *Approccio geometrico*])

  // Node 4: Rhodes (2009)
  rect((0.6, -3.9), (7.8, -2.2), fill: bgRhodes, stroke: 2pt + cPurple, radius: 0.3)
  content((4.2, -2.85), text(size: 13.5pt, weight: "bold", fill: cPurple.darken(20%))[Rhodes (2009)])
  content((4.2, -3.45), text(size: 11.5pt, fill: cPurple.darken(30%))[9 pagine — *Approccio algebrico*])
})

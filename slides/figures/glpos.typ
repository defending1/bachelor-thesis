#import "@preview/cetz:0.3.3": canvas, draw

#let cPurple = rgb("#8863A8")
#let cPurpleDark = cPurple.darken(35%)
#let cPurpleLight = cPurple.lighten(85%)

#let glpos-fig = canvas(length: 1.85cm, {
  import draw: *

  // ================= 4-POSIZIONE GENERALE =================
  group({
    // Title
    content((0, 3.3), text(size: 15pt, weight: "bold")[$4$-posizione generale])

    // Piano H (2-piano)
    line((-3.2, -1.4), (1.6, -1.4), (3.2, 1.5), (-1.6, 1.5), close: true, fill: cPurpleLight, stroke: 2pt + cPurple)
    content((-1.6, 1.65), anchor: "south-west", padding: (bottom: 2pt), text(fill: cPurpleDark, weight: "bold", size: 12pt)[Piano $H$ ($2$-piano)])

    // Altezza / proiezione per il punto fuori dal piano
    line((0.4, 2.3), (0.4, 0.8), stroke: (dash: "dashed", paint: cPurpleDark.lighten(30%), thickness: 1.5pt))
    circle((0.4, 0.8), radius: 4pt, fill: cPurpleDark.lighten(30%), stroke: none)

    // Punti Q1, Q2, Q3 sul piano H (solid filled circles)
    circle((-1.8, -0.4), radius: 6pt, fill: cPurpleDark, stroke: none)
    content((-1.8, -0.4), anchor: "east", padding: 6pt, text(fill: cPurpleDark, weight: "bold", size: 13pt)[$q_1$])

    circle((-0.3, 0.7), radius: 6pt, fill: cPurpleDark, stroke: none)
    content((-0.3, 0.7), anchor: "south-east", padding: 6pt, text(fill: cPurpleDark, weight: "bold", size: 13pt)[$q_2$])

    circle((1.2, -0.6), radius: 6pt, fill: cPurpleDark, stroke: none)
    content((1.2, -0.6), anchor: "north-west", padding: 6pt, text(fill: cPurpleDark, weight: "bold", size: 13pt)[$q_3$])

    // Punto Q4 fuori dal piano H (solid filled circle)
    circle((0.4, 2.3), radius: 6pt, fill: cPurpleDark, stroke: none)
    content((0.4, 2.3), anchor: "south", padding: 6pt, text(fill: cPurpleDark, weight: "bold", size: 13pt)[$q_4$])
  })
})

#glpos-fig

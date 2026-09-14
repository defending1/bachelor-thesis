#import "@preview/cetz:0.3.3": canvas, draw

#let cBlue = rgb("#4F8FE0")
#let cBlueDark = cBlue.darken(25%)
#let cPurple = rgb("#8863A8")
#let cPurpleDark = cPurple.darken(25%)
#let cPurpleLight = cPurple.lighten(85%)

#let glpos-fig = canvas(length: 1.0cm, {
  import draw: *

  // ================= 3-POSIZIONE GENERALE =================
  group({
    translate((-3.6, 0))

    // Title
    content((0, 3.2), text(size: 12pt, weight: "bold")[$3$-posizione generale])

    // Retta \ell (1-piano)
    line((-3.2, -1.0), (2.8, 1.4), stroke: 2pt + cBlue)
    content((2.7, 1.4), anchor: "south-east", padding: (bottom: 3pt),
      text(fill: cBlueDark, size: 9.5pt)[Retta $ell$ ($1$-piano)])

    // Punti P1, P2 sulla retta \ell
    circle((-1.8, -0.44), radius: 3pt, fill: cBlueDark, stroke: cBlueDark)
    content((-1.8, -0.44), anchor: "north-west", padding: 3pt, text(fill: cBlueDark, size: 10pt)[$p_1$])

    circle((1.2, 0.76), radius: 3pt, fill: cBlueDark, stroke: cBlueDark)
    content((1.2, 0.76), anchor: "north-west", padding: 3pt, text(fill: cBlueDark, size: 10pt)[$p_2$])

    // Punto P3 fuori dalla retta
    circle((-0.5, 1.5), radius: 3pt, fill: cBlueDark, stroke: cBlueDark)
    content((-0.5, 1.5), anchor: "south", padding: 3pt, text(fill: cBlueDark, size: 10pt)[$p_3$])
  })

  // ================= 4-POSIZIONE GENERALE =================
  group({
    translate((3.6, 0))

    // Title
    content((0, 3.2), text(size: 12pt, weight: "bold")[$4$-posizione generale])

    // Piano H (2-piano)
    line((-3.0, -1.3), (1.5, -1.3), (3.0, 1.5), (-1.5, 1.5), close: true, fill: cPurpleLight, stroke: 1.5pt + cPurple)
    content((-1.5, 1.6), anchor: "south-west", padding: (bottom: 2pt), text(fill: cPurpleDark, weight: "bold", size: 9.5pt)[Piano $H$ ($2$-piano)])

    // Altezza / proiezione per il punto fuori dal piano
    line((0.4, 2.3), (0.4, 0.8), stroke: (dash: "dashed", paint: gray.darken(20%), thickness: 1pt))
    circle((0.4, 0.8), radius: 2pt, fill: gray.darken(20%), stroke: none)

    // Punti Q1, Q2, Q3 sul piano H
    circle((-1.8, -0.4), radius: 3pt, fill: cPurpleDark, stroke: cPurpleDark)
    content((-1.8, -0.4), anchor: "east", padding: 3pt, text(fill: cPurpleDark, size: 10pt)[$q_1$])

    circle((-0.3, 0.7), radius: 3pt, fill: cPurpleDark, stroke: cPurpleDark)
    content((-0.3, 0.7), anchor: "south-east", padding: 3pt, text(fill: cPurpleDark, size: 10pt)[$q_2$])

    circle((1.2, -0.6), radius: 3pt, fill: cPurpleDark, stroke: cPurpleDark)
    content((1.2, -0.6), anchor: "north-west", padding: 3pt, text(fill: cPurpleDark, size: 10pt)[$q_3$])

    // Punto Q4 fuori dal piano H
    circle((0.4, 2.3), radius: 3pt, fill: cPurpleDark, stroke: cPurpleDark)
    content((0.4, 2.3), anchor: "south", padding: 3pt, text(fill: cPurpleDark, size: 10pt)[$q_4$])
  })
})

#import "@preview/cetz:0.3.3": canvas, draw

#let cSlate = rgb("#334155")
#let cSlateDark = rgb("#0f172a")
#let bgSlate = rgb("#f8fafc")

#let cAmber = rgb("#d97706")
#let cAmberDark = rgb("#b45309")
#let bgAmber = rgb("#fff7ed")

#let cPurple = rgb("#9333ea")
#let cPurpleDark = rgb("#6b21a8")
#let bgPurple = rgb("#faf5ff")

#let algorithm-tensor-flow-fig = canvas(length: 1.50cm, {
  import draw: *

  // Card dimensions for 3 enlarged minimal cards
  let card-w = 5.2
  let card-h = 4.7
  let r = 0

  // Centers for 3 cards
  let x1 = -6.2
  let x2 = 0.0
  let x3 = 6.2
  let y0 = 0.0

  // ================= CARD 1: CLASSICAL ALGORITHM =================
  group({
    translate((x1, y0))

    // Card boundary
    rect((-card-w/2, -card-h/2), (card-w/2, card-h/2), fill: bgSlate, stroke: 2.5pt + cSlate, radius: r)

    // Header banner
    rect((-card-w/2, card-h/2 - 1.0), (card-w/2, card-h/2), fill: cSlate, stroke: 2.5pt + cSlate, radius: (top: r, bottom: 0))
    content((0, card-h/2 - 0.5), text(fill: white, weight: "bold", size: 19.5pt)[Algoritmo Classico])

    // Center Graphic: Standard Matrix Multiplication with all 3 square matrices (A, B, C)
    group({
      translate((0, 0.25))

      // Matrix A (Square n x n)
      rect((-2.2, -0.5), (-1.2, 0.5), fill: cSlate.lighten(80%), stroke: 1.6pt + cSlate)
      content((-1.7, 0.0), text(size: 17pt, weight: "bold", fill: cSlateDark)[$A$])

      content((-0.8, 0.0), text(size: 19pt, weight: "bold", fill: cSlateDark)[$times$])

      // Matrix B (Square n x n)
      rect((-0.45, -0.5), (0.55, 0.5), fill: cSlate.lighten(80%), stroke: 1.6pt + cSlate)
      content((0.05, 0.0), text(size: 17pt, weight: "bold", fill: cSlateDark)[$B$])

      content((0.95, 0.0), text(size: 19pt, weight: "bold", fill: cSlateDark)[$=$])

      // Matrix C (Square n x n)
      rect((1.3, -0.5), (2.3, 0.5), fill: cSlate.lighten(60%), stroke: 1.8pt + cSlateDark)
      content((1.8, 0.0), text(size: 17pt, weight: "bold", fill: cSlateDark)[$C$])
    })

    // Essential metric at bottom
    content((0, -1.45), text(size: 24pt, weight: "bold", fill: cSlateDark)[$n^3$])
  })


  // ================= CARD 2: LOW-RANK REDUCTION =================
  group({
    translate((x2, y0))

    // Card boundary
    rect((-card-w/2, -card-h/2), (card-w/2, card-h/2), fill: bgAmber, stroke: 2.5pt + cAmber, radius: r)

    // Header banner
    rect((-card-w/2, card-h/2 - 1.0), (card-w/2, card-h/2), fill: cAmber, stroke: 2.5pt + cAmber, radius: (top: r, bottom: 0))
    content((0, card-h/2 - 0.5), text(fill: white, weight: "bold", size: 19.5pt)[Riduzione di Rango])

    // Center Graphic: CP Decomposition formula
    group({
      translate((0, 0.25))

      // Outer badge containing CP decomposition equation


      content((0, 0.05), text(size: 21pt, weight: "bold", fill: cAmberDark)[$T = sum_(r=1)^R a_r \u{2297} b_r \u{2297} c_r$])
    })

    // Essential metric at bottom
    content((0, -1.45), text(size: 22pt, weight: "bold", fill: cAmberDark)[$R < n^3$])
  })


  // ================= CARD 3: FAST ALGORITHM =================
  group({
    translate((x3, y0))

    // Card boundary
    rect((-card-w/2, -card-h/2), (card-w/2, card-h/2), fill: bgPurple, stroke: 2.5pt + cPurple, radius: r)

    // Header banner
    rect((-card-w/2, card-h/2 - 1.0), (card-w/2, card-h/2), fill: cPurple, stroke: 2.5pt + cPurple, radius: (top: r, bottom: 0))
    content((0, card-h/2 - 0.5), text(fill: white, weight: "bold", size: 19.5pt)[Algoritmo Veloce])

    // Center Graphic: Box containing Bilinear Computation formula
    group({
      translate((0, 0.25))
      content((0, 0.05), text(size: 21pt, weight: "bold", fill: cPurpleDark)[$sum_(r=1)^R (a_r^top u)(b_r^top v) c_r$])
    })

    // Essential metric at bottom
    content((0, -1.45), text(size: 21pt, weight: "bold", fill: cPurpleDark)[$O(n^omega), quad omega <= log_n R$])
  })


  // ================= CONNECTING ARROWS =================
  let arrow-y = 0.0

  // Arrow 1 -> 2
  line((-3.4, arrow-y), (-2.7, arrow-y), stroke: 2.8pt + cSlate, mark: (end: "stealth", fill: cSlate, scale: 2.2))

  // Arrow 2 -> 3
  line((2.7, arrow-y), (3.4, arrow-y), stroke: 2.8pt + cAmberDark, mark: (end: "stealth", fill: cAmberDark, scale: 2.2))

})



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

#let algorithm-tensor-flow-fig = canvas(length: 1.55cm, {
  import draw: *

  // Card dimensions for 3 enlarged cards
  let card-w = 4.4
  let card-h = 5.8
  let r = 0.25

  // Centers for 3 cards
  let x1 = -5.4
  let x2 = 0.0
  let x3 = 5.4
  let y0 = 0.0

  // ================= CARD 1: CLASSICAL ALGORITHM =================
  group({
    translate((x1, y0))

    // Card boundary
    rect((-card-w/2, -card-h/2), (card-w/2, card-h/2), fill: bgSlate, stroke: 2.5pt + cSlate, radius: r)

    // Header banner
    rect((-card-w/2, card-h/2 - 0.85), (card-w/2, card-h/2), fill: cSlate, stroke: 2.5pt + cSlate, radius: (top: r, bottom: 0))
    content((0, card-h/2 - 0.425), text(fill: white, weight: "bold", size: 13pt)[1. ALGORITMO CLASSICO])

    // Subtitle & Math (Square case)
    content((0, 1.6), text(weight: "bold", fill: cSlateDark, size: 15pt)[Mappa Bilineare])
    content((0, 1.05), text(fill: cSlateDark, size: 13pt)[$phi : RR^(n times n) times RR^(n times n) -> RR^(n times n)$])

    // Illustration: Standard Matrix Multiplication (Square n x n)
    group({
      translate((0, -0.2))
      // Matrix A
      rect((-1.45, -0.5), (-0.5, 0.5), fill: cSlate.lighten(80%), stroke: 1.4pt + cSlate)
      content((-0.975, 0.0), text(size: 12.5pt, weight: "bold", fill: cSlateDark)[$A_(n times n)$])

      content((-0.25, 0.0), text(size: 13pt, weight: "bold", fill: cSlateDark)[$times$])

      // Matrix B
      rect((0.0, -0.5), (0.95, 0.5), fill: cSlate.lighten(80%), stroke: 1.4pt + cSlate)
      content((0.475, 0.0), text(size: 12.5pt, weight: "bold", fill: cSlateDark)[$B_(n times n)$])

      content((1.2, 0.0), text(size: 13pt, weight: "bold", fill: cSlateDark)[$=$])

      // Matrix C
      rect((1.45, -0.5), (1.85, 0.5), fill: cSlate.lighten(60%), stroke: 1.6pt + cSlateDark)
      content((1.65, 0.0), text(size: 11.5pt, weight: "bold", fill: cSlateDark)[$C$])
    })

    // Key properties
    line((-card-w/2 + 0.35, -1.25), (card-w/2 - 0.35, -1.25), stroke: 0.8pt + cSlate.lighten(50%))
    content((0, -1.65), text(size: 12pt, fill: cSlateDark)[Prodotto standard])
    content((0, -2.2), text(size: 14pt, weight: "bold", fill: cSlateDark)[$R_("std") = n^3$ molt.])
  })


  // ================= CARD 2: LOW-RANK REDUCTION =================
  group({
    translate((x2, y0))

    // Card boundary
    rect((-card-w/2, -card-h/2), (card-w/2, card-h/2), fill: bgAmber, stroke: 2.5pt + cAmber, radius: r)

    // Header banner
    rect((-card-w/2, card-h/2 - 0.85), (card-w/2, card-h/2), fill: cAmber, stroke: 2.5pt + cAmber, radius: (top: r, bottom: 0))
    content((0, card-h/2 - 0.425), text(fill: white, weight: "bold", size: 13pt)[2. RIDUZIONE DI RANGO])

    // Subtitle & Math
    content((0, 1.6), text(weight: "bold", fill: cAmberDark, size: 15pt)[Decomposizione CP])
    content((0, 1.05), text(fill: cAmberDark, size: 12.5pt)[$T = sum_(r=1)^R a_r \u{2297} b_r \u{2297} c_r$])

    // Illustration: CP Decomposition into rank-1 triads
    group({
      translate((0, -0.2))

      content((-1.55, 0.05), text(size: 14pt, weight: "bold", fill: cAmberDark)[$sum_(r=1)^R$])

      // Rank-1 outer product components
      group({
        translate((-0.1, 0))

        // Vector a_r (vertical line/pill)
        rect((-0.65, -0.5), (-0.35, 0.6), fill: cAmber.lighten(60%), stroke: 1.4pt + cAmberDark, radius: 0.07)
        content((-0.5, 0.05), text(size: 11pt, weight: "bold", fill: cAmberDark)[$a_r$])

        content((-0.1, 0.05), text(size: 12pt, weight: "bold", fill: cAmberDark)[$\u{2297}$])

        // Vector b_r (horizontal pill)
        rect((0.15, -0.2), (0.85, 0.22), fill: cAmber.lighten(40%), stroke: 1.4pt + cAmberDark, radius: 0.07)
        content((0.5, 0.015), text(size: 11pt, weight: "bold", fill: cAmberDark)[$b_r$])

        content((1.1, 0.05), text(size: 12pt, weight: "bold", fill: cAmberDark)[$\u{2297}$])

        // Vector c_r (depth pill)
        line((1.3, -0.4), (1.55, -0.05), (1.85, 0.5), (1.6, 0.15), close: true, fill: cAmber.lighten(20%), stroke: 1.4pt + cAmberDark)
        content((1.575, 0.05), text(size: 11pt, weight: "bold", fill: white)[$c_r$])
      })
    })

    // Key properties
    line((-card-w/2 + 0.35, -1.25), (card-w/2 - 0.35, -1.25), stroke: 0.8pt + cAmber.lighten(50%))
    content((0, -1.65), text(size: 11.5pt, fill: cAmberDark)[Fattorizzazione a rango $R < n^3$])
    content((0, -2.2), text(size: 13.5pt, weight: "bold", fill: cAmberDark)[es. $R = 7 < 8$ per $n=2$])
  })


  // ================= CARD 3: FAST ALGORITHM =================
  group({
    translate((x3, y0))

    // Card boundary
    rect((-card-w/2, -card-h/2), (card-w/2, card-h/2), fill: bgPurple, stroke: 2.5pt + cPurple, radius: r)

    // Header banner
    rect((-card-w/2, card-h/2 - 0.85), (card-w/2, card-h/2), fill: cPurple, stroke: 2.5pt + cPurple, radius: (top: r, bottom: 0))
    content((0, card-h/2 - 0.425), text(fill: white, weight: "bold", size: 13pt)[3. ALGORITMO VELOCE])

    // Subtitle & Math
    content((0, 1.6), text(weight: "bold", fill: cPurpleDark, size: 15pt)[Sintesi Ricorsiva])
    content((0, 1.05), text(fill: cPurpleDark, size: 12.5pt)[$O(n^omega)$ con $omega = log_n R$])

    // Illustration: Box containing ONLY Bilinear Computation formula
    group({
      translate((0, -0.2))

      // Outer speed badge containing ONLY the formula
      rect((-2.1, -0.65), (2.1, 0.75), fill: cPurple.lighten(85%), stroke: 2.2pt + cPurpleDark, radius: 0.2)

      // Only the bilinear computation formula inside the box
      content((0, 0.05), text(size: 16pt, weight: "bold", fill: cPurpleDark)[$sum_(r=1)^R (a_r^top u)(b_r^top v) c_r$])
    })

    // Key properties
    line((-card-w/2 + 0.35, -1.25), (card-w/2 - 0.35, -1.25), stroke: 0.8pt + cPurple.lighten(50%))
    content((0, -1.65), text(size: 12pt, fill: cPurpleDark)[Complessità sub-cubica])
    content((0, -2.2), text(size: 14pt, weight: "bold", fill: cPurpleDark)[$O(n^(2.81))$ (Strassen)])
  })


  // ================= CONNECTING ARROWS =================
  let arrow-y = 0.0

  // Arrow 1 -> 2
  line((-3.0, arrow-y), (-2.4, arrow-y), stroke: 2.5pt + cSlate, mark: (end: "stealth", fill: cSlate))
  content((-2.7, arrow-y + 0.55), text(size: 8pt, weight: "bold", fill: cSlate)[Riduzione CP])

  // Arrow 2 -> 3
  line((2.4, arrow-y), (3.0, arrow-y), stroke: 2.5pt + cAmberDark, mark: (end: "stealth", fill: cAmberDark))
  content((2.7, arrow-y + 0.55), text(size: 8pt, weight: "bold", fill: cAmberDark)[Sintesi])

})

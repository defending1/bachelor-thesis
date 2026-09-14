#import "@preview/cetz:0.4.2"

#set page(width: auto, height: auto, margin: 0.8cm)

#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  // Style definitions
  let box-stroke = 0.85pt + luma(30)
  let inner-stroke = 0.45pt + luma(100)
  let branch-stroke = 0.65pt + luma(80)

  // Helper: Draw 2x2 Matrix with block letter entries
  let draw-labeled-matrix(
    center,
    label: "",
    entries: (top-left: "", top-right: "", bot-left: "", bot-right: ""),
    size: 1.4,
  ) = {
    let (cx, cy) = center
    let half = size / 2

    // Outer box
    rect(
      (cx - half, cy - half),
      (cx + half, cy + half),
      stroke: box-stroke,
      fill: rgb("#fcfcfc"),
    )

    // Grid lines
    line((cx - half, cy), (cx + half, cy), stroke: inner-stroke)
    line((cx, cy - half), (cx, cy + half), stroke: inner-stroke)

    // Entries
    let q = half / 2
    content((cx - q, cy + q), text(size: 11pt, style: "italic")[#entries.top-left])
    content((cx + q, cy + q), text(size: 11pt, style: "italic")[#entries.top-right])
    content((cx - q, cy - q), text(size: 11pt, style: "italic")[#entries.bot-left])
    content((cx + q, cy - q), text(size: 11pt, style: "italic")[#entries.bot-right])

    // Matrix Label above
    if label != "" {
      content((cx, cy + half + 0.35), text(size: 12pt, weight: "bold")[#label])
    }
  }

  // Helper: Draw term box [ f_r | g_r ]
  let draw-term-box(
    center,
    f-label: $f_1$,
    g-label: $g_1$,
    w: 1.35,
    h: 0.75,
  ) = {
    let (cx, cy) = center
    let hw = w / 2
    let hh = h / 2

    // Outer rectangle
    rect(
      (cx - hw, cy - hh),
      (cx + hw, cy + hh),
      stroke: box-stroke,
      fill: rgb("#fafafa"),
    )

    // Vertical dividing line
    line((cx, cy - hh), (cx, cy + hh), stroke: inner-stroke)

    // Content labels
    content((cx - hw / 2, cy), text(size: 11pt)[#f-label])
    content((cx + hw / 2, cy), text(size: 11pt)[#g-label])
  }

  // ==========================================
  // Top Level: Matrices A and B
  // ==========================================
  draw-labeled-matrix(
    (-1.4, 7.0),
    label: "A",
    entries: (top-left: "a", top-right: "c", bot-left: "b", bot-right: "d"),
    size: 1.4,
  )

  draw-labeled-matrix(
    (1.4, 7.0),
    label: "B",
    entries: (top-left: "e", top-right: "g", bot-left: "f", bot-right: "h"),
    size: 1.4,
  )

  // ==========================================
  // Level 1 Expression (Left-Aligned, starting X = -5.3)
  // ==========================================
  let y1 = 4.2
  let tw = 1.35
  let th = 0.75

  // Level 1 Label on Left
  content((-7.0, y1), text(size: 11pt, weight: "bold", fill: rgb("#333333"))[Livello 1])

  draw-term-box((-5.3, y1), f-label: $f_1$, g-label: $g_1$, w: tw, h: th)
  content((-4.25, y1), text(size: 13pt)[$+$])

  draw-term-box((-3.2, y1), f-label: $f_2$, g-label: $g_2$, w: tw, h: th)
  content((-2.15, y1), text(size: 13pt)[$+$])

  draw-term-box((-1.1, y1), f-label: $f_3$, g-label: $g_3$, w: tw, h: th)
  content((-0.05, y1), text(size: 13pt)[$+$])

  content((0.8, y1), text(size: 13pt)[$dots.h$])
  content((1.65, y1), text(size: 13pt)[$+$])

  draw-term-box((2.7, y1), f-label: $f_R$, g-label: $g_R$, w: tw, h: th)

  // Row 1 Multiplication Count Label
  content((5.2, y1), text(size: 11pt)[$R$ moltiplicazioni])

  // ==========================================
  // Branching Lines from Level 1 to Level 2
  // ==========================================
  let y2 = 1.8
  let top-y1-bot = y1 - th / 2

  // Branch 1 (down-left)
  line((-5.3, top-y1-bot), (-6.5, y2 + th / 2 + 0.3), stroke: branch-stroke)
  // Branch 2 (to Livello 2's [f1|g1])
  line((-3.2, top-y1-bot), (-2.2, y2 + th / 2 + 0.1), stroke: branch-stroke)
  // Branch 3 (to Livello 2's [f2|g2])
  line((-1.1, top-y1-bot), (-0.1, y2 + th / 2 + 0.1), stroke: branch-stroke)
  // Branch 4 (to Livello 2's [fR|gR])
  line((2.7, top-y1-bot), (3.3, y2 + th / 2 + 0.1), stroke: branch-stroke)

  // ==========================================
  // Level 2 Expression (Shifted to Right, starting X = -2.2)
  // ==========================================

  // Level 2 Label on Left
  content((-3.8, y2), text(size: 11pt, weight: "bold", fill: rgb("#333333"))[Livello 2])

  draw-term-box((-2.2, y2), f-label: $f_1$, g-label: $g_1$, w: tw, h: th)
  content((-1.15, y2), text(size: 13pt)[$+$])

  draw-term-box((-0.1, y2), f-label: $f_2$, g-label: $g_2$, w: tw, h: th)
  content((0.95, y2), text(size: 13pt)[$+$])

  content((1.6, y2), text(size: 13pt)[$dots.h$])
  content((2.25, y2), text(size: 13pt)[$+$])

  draw-term-box((3.3, y2), f-label: $f_R$, g-label: $g_R$, w: tw, h: th)

  // Row 2 Multiplication Count Label
  content((5.2, y2), text(size: 11pt)[$R$ molt.])

  // ==========================================
  // Branching Lines from Level 2 to Level i
  // ==========================================
  let top-y2-bot = y2 - th / 2
  line((-2.2, top-y2-bot), (-3.5, 0.7), stroke: branch-stroke)
  line((-0.1, top-y2-bot), (-1.4, 0.7), stroke: branch-stroke)
  line((3.3, top-y2-bot), (2.0, 0.7), stroke: branch-stroke)

  content((-0.7, -0.1), text(size: 16pt)[$dots.v$])

  // ==========================================
  // Level i Base Case Expression (Positioned More at Left, starting X = -5.3)
  // ==========================================
  let yi = -1.8

  // Level i Label on Left
  content((-7.0, yi), text(size: 11pt, weight: "bold", fill: rgb("#333333"))[Livello $i$])


  draw-term-box((-5.3, yi), f-label: $f_1$, g-label: $g_1$, w: tw, h: th)
  content((-4.25, yi), text(size: 13pt)[$+$])

  draw-term-box((-3.2, yi), f-label: $f_2$, g-label: $g_2$, w: tw, h: th)
  content((-2.15, yi), text(size: 13pt)[$+$])

  content((-1.2, yi), text(size: 13pt)[$dots.h$])
  content((-0.45, yi), text(size: 13pt)[$+$])

  draw-term-box((0.6, yi), f-label: $f_R$, g-label: $g_R$, w: tw, h: th)

  // Bottom Row Multiplication Count Label
  content((5.2, yi), text(size: 11pt)[$R$ molt.])

  // ==========================================
  // Far Right Brace & Level Annotation
  // ==========================================
  let bx = 6.8
  let y-top = 7.8
  let y-bot = -2.4
  let y-mid = (y-top + y-bot) / 2
  let brace-stroke = 0.85pt + luma(40)

  // Classic mathematical right curly brace
  bezier((bx, y-top), (bx + 0.35, y-mid), (bx + 0.25, y-top - 0.25), (bx + 0.15, y-mid + 0.6), stroke: brace-stroke)
  bezier((bx + 0.35, y-mid), (bx, y-bot), (bx + 0.15, y-mid - 0.6), (bx + 0.25, y-bot + 0.25), stroke: brace-stroke)

  // Label next to brace
  content((bx + 1.2, y-mid), text(size: 12pt)[$i$ livelli])
})

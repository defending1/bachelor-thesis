#import "@preview/touying:0.6.1": *
#import "../theme.typ": *

= Seconda Sezione

== Ambienti Personalizzati

#def-box(title: "Titolo Definizione")[
  Inserisci qui il testo della definizione:
  $ f(x) = sum_(i=1)^n x_i $
]

#pause

#thm-box(title: "Titolo Teorema")[
  Inserisci qui l'enunciato del teorema.
]

== Layout a Due Colonne

#grid(
  columns: (1fr, 1fr),
  gutter: 16pt,
  [
    === Colonna Sinistra
- Contenuto colonna 1
- Altri punti
  ],
  [
    === Colonna Destra
- Contenuto colonna 2
- Altri punti
  ]
)

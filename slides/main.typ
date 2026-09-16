#import "lib.typ": *



#show: simple-theme.with(
  aspect-ratio: "4-3",
  footer: [],
  config-common(frozen-counters: (theorem-counter,)),  // freeze theorem counter for animation
  config-info(
    title: [Tensor Canonical Polyadic Decomposition\ and the Complexity of Matrix Multiplication
  ],
  subtitle: [Tesi di laurea triennale],
  author: [AUTHOR],
  date: "25 Settembre 2026",
  institution: [Università di Pisa],
  // logo: emoji.school,
),
)

#show: show-theorion
#set text(lang: "it")
#show: show-bibliography-as-footnote


#set heading(numbering: numbly("{1}.", default: "1.1"))

#title-slide()

#include "sections/00-section.typ"
#include "sections/01-section.typ"
#include "sections/02-section.typ"
#include "sections/03-section.typ"
#include "sections/04-section.typ"


= Bibliografia

#bibliography("Thesis.bib", title: none)


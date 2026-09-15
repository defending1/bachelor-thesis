#import "lib.typ": *



#show: simple-theme.with(
  aspect-ratio: "4-3",
  footer: [],
)

#show: show-theorion
#set text(lang: "it")
#show: show-bibliography-as-footnote

#include "sections/00-section.typ"
#include "sections/01-section.typ"
#include "sections/02-section.typ"
#include "sections/03-section.typ"
#include "sections/04-section.typ"


= Bibliografia

#bibliography("Thesis.bib", title: none)


// Centralized prelude for packages, theme, and tensor math helpers
#import "@preview/theorion:0.6.0": *
#import "@preview/touying:0.6.1": *
#import "@preview/dashy-todo:0.1.3": todo
#import themes.simple: *
#import "theme.typ": *
#import "tensors.typ": *
#import "@preview/mannot:0.3.0" as mannot: mark, annot
#import "@preview/pavemat:0.2.0": pavemat

// Bibliography footnote support for Typst 0.12+ & Touying
#let bib-cells = state("bib-cells", ())
#let bib-keys = state("bib-keys", ())

#let show-bibliography-as-footnote(body) = {
  show cite: it => {
    let key-str = str(it.key)
    bib-keys.update(k => if key-str not in k { k + (key-str,) } else { k })
    box(width: 0pt, hide(it))
    context {
      let keys = bib-keys.final()
      let global-num = if key-str in keys {
        keys.position(k => k == key-str) + 1
      } else {
        1
      }
      let cells = bib-cells.final()
      let item = if cells.len() > 2 * (global-num - 1) + 1 {
        cells.at(2 * (global-num - 1) + 1)
      } else {
        [#key-str]
      }
      footnote(numbering: _ => "[" + str(global-num) + "]", item)
    }
  }

  show bibliography: it => {
    show grid.cell: c => {
      bib-cells.update(v => v + (c.body,))
      c
    }
    set text(size: 0.7em)
    it
  }

  body
}



// Define a function for custom equation tags
#let named-eq(tag, body) = math.equation(
  numbering: _ => "(" + tag + ")",
  block: true,
  body,
)



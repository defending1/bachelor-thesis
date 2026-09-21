// Centralized prelude for packages, theme, and tensor math helpers
#import "@preview/theorion:0.6.0": *
#import "touying/lib.typ": *
#import "@preview/dashy-todo:0.1.3": todo
#import themes.simple: *
#import "@preview/numbly:0.1.0": numbly
#import "theme.typ": *
#import "tensors.typ": *
#import "@preview/mannot:0.4.0": *
#import "@preview/pavemat:0.2.0": pavemat
#import "@preview/cetz:0.5.2"
#import "@preview/fletcher:0.5.8" as fletcher: node, edge
#import "wave.typ": wave

// Bibliography footnote support for Typst 0.12+ & Touying
#let show-bibliography-as-footnote(body) = {
  set footnote(numbering: n => "[" + str(n) + "]")
  show footnote.entry: it => it.note.body

  show cite: it => {
    if it.form != "full" {
      footnote(cite(it.key, form: "full"))
    } else {
      it
    }
  }

  body
}



// Define a function for custom equation tags
#let named-eq(tag, body) = math.equation(
  numbering: _ => "(" + tag + ")",
  block: true,
  body,
)


#let cetz-canvas = touying-reducer.with(reduce: cetz.canvas, cover: cetz.draw.hide.with(bounds: true))
#let fletcher-diagram = touying-reducer.with(reduce: fletcher.diagram, cover: fletcher.hide)


#let tens-hl(content) = text(purple)[#content]
#let mat-hl(content) = text(blue)[#content]

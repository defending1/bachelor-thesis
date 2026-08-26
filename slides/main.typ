#import "@preview/touying:0.6.1": *
#import "theme.typ": *

#show: setup-presentation.with(
  title: [Titolo della Presentazione],
  subtitle: [Sottotitolo della Presentazione],
  author: [Nome Cognome],
  institution: [Università / Ente],
  date: datetime.today(),
)

// Slide del titolo
#title-slide()

// Indice dei contenuti
== Indice dei Contenuti

#components.adaptive-columns(
  outline(title: none, indent: 1.5em)
)

// Sezioni della presentazione
#include "sections/01-section.typ"
#include "sections/02-section.typ"
#include "sections/03-section.typ"

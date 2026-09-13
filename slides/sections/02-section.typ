#import "../lib.typ": *


= Il teorema di Kruskal

== Essenziale unicità

#definition[Essenziale unicità][
  hi
]<def:essunq>

== k-rango

#definition[$k$-rango][
  Dato un sottoinsieme di punti $cal(S) subset bb(P)$, il #emph[$k$-rango] è il massimo intero
  positivo $r$ tale che i punti di $cal(S)$ sono in posizione generale.
]
Lo indichiamo con $ krank(cal(S)) .$

#remark[][
  La definizione originale di Kruskal era: data una matrice $M$, $krank(M)$ è il massimo intero
  positivo $r$ tale che ogni sottoinsieme di $r$ colonne di $M$ sono vettori linearmente
  indipendenti.
]

#todo[Qui fare gli show con esempi punti, piano]

== Enunciato


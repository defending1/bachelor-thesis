#import "@preview/theorion:0.6.0": *
#import "@preview/touying:0.6.1": *
#import "@preview/dashy-todo:0.1.3": todo
#import themes.simple: *


#show: simple-theme.with(
  aspect-ratio: "16-9",
  footer: [],
)

#show: show-theorion
#set text(lang: "it")


#let krank(A) = $bold(k)_#A$
#let proj(n, K) = $bb(P)^#n (#K) $

== Indice

#definition[Euclid's Theorem][
  There are infinitely many prime numbers.
] <thm:euclid>

== Notazione


== La fattorizzazione CP

Definizione


= Il problema del rango
In questa parte vediamo molte peculiarità dei tensori, dove "smonto" quello che
funziona per le matrici ma non per i tensori


== Rango CP

== Border rank

== Rango tipico

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

#todo[Qui fare gli show con esempi punti, piano]



== Enunciato



== Applicazioni (omini e spettroscopia)

= Applicazione alla complessità aritmetica

Problema: Matmul si può vedere come mappa bilineare

introduco $<m,n,p>$

bilnear computation

Spoiler: equazioni -> biliner comp -> tensore


== L'esponente

Def di circuito, L, bilinear computation
Def di omega


== L'algoritmo di Strassen

(qui spiego che strassen riducendo le eq classiche trova un algoritmo con meno moltiplicazioni)

Riscrittura moderna: da quello classico trovo bilinear computation (e poi tensore)

In questo modo posso riscrivere tensorialmente l'algoritmo di Strassen

Si può migliorare -> no: teorema di Winograd

Utilità? con tecniche più avanzate si trovano algoritmi/riduzioni sftuttando la geometria dei
tensori: esempio $<3,3,3>$ non è semplice da ridurre, ma manipolare eq a mano più difficiile.

=== alcune stime sul border rank (se tempo)



== Algoritmi approssimati

bini et al provano...

tensore che trovano

=== Cenni sull'errore

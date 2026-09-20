#import "../lib.typ": *

= La fattorizzazione CP e il rango tensoriale

== Tensori
Siano $A,B,C$ degli spazi vettoriali di dimensione finita sul campo $KK in {RR, CC}.$
#pause
#definition[Mappa/forma bilineare][
  Una *mappa bilineare* è un'applicazione $phi : A times B -> C$ lineare in ogni componente. Se $C=
  KK$ è detta *forma bilineare*.
]
#pause
#definition[Spazio dei tensori][
  Indichiamo lo *spazio dei tensori* di
  ordine tre con $A topp B topp C$. Lo definiamo come
  l'insieme delle forme trilineari $phi : A^* times B^* times C^* -> KK$.
]

#pagebreak()
#definition[
  Indichiamo con $RR^(m times n times p)$ lo *spazio standard dei
  tensori* di ordine $3$ di $RR^m topp RR^n topp RR^p$.
]

#align(center)[#image("../figures/unfoldings.pdf", width: 95%)]

#pagebreak()
#definition[][
  Un *tensore di rango uno* è un elemento
  $
  a topp b topp c in A topp B topp C.
  $
  tale che
  $
  a topp b topp c (alpha, beta, gamma) = alpha(a)beta(b)gamma(c),
  $
  per ogni $(alpha, beta, gamma) in A^* times B^* times C^*.$
]

#pagebreak()
#example[][
  In $RR^(m times n)$, fissati dei vettori $a = [a_1, dots, a_m]^top$ e $b = [b_1, dots, b_n]^top,$
  $
  a topp b = a b^top =
  mat(a_1b_1, a_1b_2, dots.c, a_1 b_n; a_2 b_1, a_2 b_2, dots, a_2 b_n; dots.v, dots.v, dots.down,
  dots.v; a_m b_1, a_m b_2, dots, a_m b_n, delim:"[") in RR^(m times n)
  $
]

== La decomposizione CP

#definition[Canonical Polyadic Decomposition][
  Dati degli spazi $A,B,C$ e dei vettori $a_r in A, b_r in B, c_r in C$.
  Un tensore $T in A topp B topp C$ ammette una *fattorizzazione CP* di rango $R$ se si può
  scrivere come somma di $R$ tensori di rango uno
  $
  T = a_1 topp b_1 topp c_1 + a_2 topp b_2 topp c_2 + dots + a_R topp b_R topp c_R.
  $
]

#pause
In $RR^(m times n times p)$ la indichiamo con $T = cp(A,B,C),$ dove
$
A = mat(a_1|dots.c|a_R, delim:"["),quad B =
mat(b_1|dots.c|b_R, delim:"["),quad C = mat(c_1|dots|c_R, delim:"[").
$

#definition[][
  Il *rango* $rk(T)$ è il minimo intero positivo $R$ tale che $T$ ammette una decomposizione CP di rango $R$.
]




== Il problema del rango

Ci aspettiamo che il rango #tens-hl[tensoriale] si comporti come il rango #mat-hl[matriciale].

== Complessità

#property[Håstad@haastad1989tensor][
  Il rango #tens-hl[tensoriale] è NP-hard.
]

== Approssimazione low-rank
#corollary[Eckart-Young-Mirsky][
  Un'approssimazione low-rank di una #mat-hl[matrice] $M$ è la sua decomposizione SVD
  $
  M = U Sigma V^* = sum_(r=1)^(rank(M)) sigma_r u_r topp v_r, wide sigma_r >= sigma_(r+1).
  $
]
#pause
#property[
  Per un #tens-hl[tensore] $T$, calcolare il miglior approssimante $hat(T) = cp(A,B,C)$ di rango $R$
  $
  min_(A, B, C) norm(T - a_1 topp b_1 topp c_1 - dots.c - a_r topp b_r topp c_r)
  $
  è mal posto.
]


== Border rank

#property[
  Una successione di #mat-hl[matrici] di rango $r$ tende a una matrice di rango $<= r$.
]

#pagebreak()

#property[
  L'insieme dei #tens-hl[tensori]
  $
  {T in A topp B topp C | T "ha rango "r}
  $
  non è chiuso.
]

#align(center)[#image("../figures/border-rank.pdf", width: 80%)]

#example[][
  La successione di tensori di rango $2$
  $
  T_epsilon = 1/epsilon (a_1 + epsilon a_2) topp (b_1 + epsilon b_2) topp (c_1 + epsilon c_2) -
  1/epsilon a_1 topp b_1 topp c_1,
  $
  per $epsilon -> 0$ converge a un tensore di rango $3$
  $
  T = a_1 topp b_1 topp c_2 topp + a_1 topp b_2 topp c_1 + a_2 topp b_1 topp c_1,
  $
  in quanto
  $
  T_epsilon = T + O(epsilon).
  $
]

#definition[Border rank][
  Un tensore $T$ ha *border rank* $r$ se è limite di una successione di rango $r$ ma non è limite di
  una successione di tensori di rango $s$, per ogni $s<r$.
]



== Rango massimo

#property[
  Per i #tens-hl[tensori] $n times m times p$ il rango può superare le dimensioni degli spazi.
]




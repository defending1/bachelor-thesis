#import "../lib.typ": *

= La fattorizzazione CP e il rango tensoriale

== Tensori
Siano $A,B,C$ degli spazi vettoriali di dimensione finita sul campo $KK in {RR, CC}.$

#definition[Mappa/forma bilineare][
  Una *mappa bilineare* è un'applicazione $phi : A times B -> C$ lineare in ogni componente. Se $C=
  KK$ è detta *forma bilineare*.
]
#definition[Spazio dei tensori][
  Dati degli spazi vettoriali di dimensione finita $A,B,C$ indichiamo lo *spazio dei tensori* di
  ordine tre con $A topp B topp C$. Lo definiamo come
  l'insieme delle mappe bilineari $phi : A^* times B^* times C^* -> KK$.
]

#definition[
  Quando $A = RR^m, B= RR^n, C = RR^p$, indichiamo con $RR^(m times n times p)$ lo *spazio dei
  tensori (in coordinate)* di ordine $3$.
]

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
A = [a_1, dots, a_R], B =
[b_1, dots, b_R], C = [c_1, dots, c_R].
$

#definition[][
  Il *rango* $rk(T)$ è il minimo intero positivo $R$ tale che $T$ ammette una decomposizione CP di rango $R$.
]




= Il problema del rango

Ci aspettiamo che il rango tensoriale si comporti come il rango matriciale.

== Complessità

- Calcolare il rango tensoriale è NP-hard REF

- Il miglior approssimante di una matrice $M$ di rango $R$ è la decomposizione SVD
$
M = U Sigma V^* = sum_(r=1)^(rank(A)) sigma_r u_r topp v_r, wide sigma_r >= sigma_(r+1).
$

Per un tensore $T$, calcolare il miglior approssimante $hat(T) = cp(A,B,C)$ di rango $R$
$
min_(A, B, C) norm(T - a_1 topp b_1 topp c_1 - dots.c - a_r topp b_r topp c_r)
$
è mal posto.


== Border rank

#property[
  Una successione di matrici di rango $r$ tende a una matrice di rango $<= r$.
]

#pagebreak(weak: true)

#property[
  L'insieme dei tensori
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
  una successione di tensori di rango $s$, per ogni $s<r$. Lo indichiamo con $brk(T)$.
]



== Rango massimo

#property[
  Il rango massimo di una matrice $m times n$ è $min(m,n)$
]
#property[
  Per i tensori $n times m times p$ il rango può superare le dimensioni degli spazi.
]
#example[
  Nel caso $2 times 2 times 2$ il rango massimo è $3$.
]


== Rango tipico

#property[
  Ogni matrice ha rango massimo con probabilità $1$.
]

#property[
  I tensori possono avere più ranghi per un certo formato. Tale fenomeno è detto *rango tipico*.
]

#example[
  Per un tensore reale $2 times 2 times 2$, i ranghi tipici sono ${2,3}$.
]




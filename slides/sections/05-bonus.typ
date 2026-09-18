#import "../lib.typ": *

= Bonus
== Rango tipico

#property[
  Ogni #mat-hl[matrice] ha rango massimo con probabilità $1$.
]

#property[
  I #tens-hl[tensori] possono avere più ranghi per un certo formato. Tale fenomeno è detto *rango tipico*.
]

#example[
  Per un tensore reale $2 times 2 times 2$, i ranghi tipici sono ${2,3}$.
]



== Teorema di Kruskal

=== Semplificazione delle dimostrazioni

#import "../figures/proof_streamlining.typ": proof-streamlining-fig

#align(center + horizon)[
  #proof-streamlining-fig
]

== Il Teorema di Kruskal in dimensione $d$
#theorem[Kruskal, Sidiropoulos e Bro][
  Sia $T in A_1 topp A_2 topp dots.c topp A_d$ un tensore che ammette una fattorizzazione $ T =
  sum_(r = 1)^R u^1_r topp
  u^2_r topp dots.c topp u^d_r. $ Siano $cal(S)_(A_k) = {[u^k_r]}$. Se vale
  $
  sum_(k=1)^R krank(cal(S)_(A_k)) >= 2R + d - 1
  $
  allora $T$ ha rango $R$ e la sua fattorizzazione è essenzialmente unica.
]<thm-krk-gen>

#remark[
  Per le matrici, l'unicità si ha solo per $R=1$, dove $T = u topp v$. In tal caso $cal(S)_A =
  {[u]}, cal(S)_B = {[v]}$ e le ipotesi del @thm-krk-gen non sono
  rispettate, in quanto
  $
  krank(cal(S)_A) + krank(cal(S)_B) = 1 + 1 = 2 >= 2R + 2 - 1 >= 2 + 2 - 1 = 3.
  $
]

== Caso speciale

#proposition[Landsberg @landsberg2009kruskalstheorem][
  Dati degli spazi vettoriali $A,B,C$ di dimensioni $dim(A) = dim(B) = dim(C) = bold(a)$ e un
  tensore $T$ di rango multilineare $(bold(a), bold(a), bold(a))$. Se $T$ ha rango $bold(a)$ allora la
  fattorizzazione è unica. In particolare, quando $krank(cal(S)_A) = krank(cal(S)_B) =
  krank(cal(S)_C) = bold(a)$, la condizione dell'@eq-kruskal si estende ad
  $
  bold(a) <= R <= 1/2 (bold(a) + bold(a)+ bold(a)) = 3/2 bold(a) - 1.
  $
]

== Complessità aritmetica

=== Bilinear computation

Sia $phi : U times V -> W$ una mappa bilineare. Per ogni $r = 1, ..., R$ siano $f_r in U^*, g_r in
V^*$ dei funzionali e $w_r in W$ un vettore tali che
$
phi(u,v) = sum_(r = 1)^R f_r (u) g_r (v) w_r,
$
per ogni vettore $u in U, v in V$.

La $r$-upla $(f_1,g_1,w_1, dots, f_r,g_r,w_r)$ è detta *bilinear computation*.
La lunghezza di una bilinear computation è detta *bilinear complexity (o rango)* di $phi$, e si indica
con $rk(phi)$.

=== Rappresentazione low-rank di forme bilineari

#proposition[][
  Data una decomposizione $ T = sum_(r=1)^R a_r topp b_r topp c_r $

  Possiamo scrivere una forma bilineare $phi : U times V arrow.r W$ come una bilinear computation
  della forma $ phi(u,v) = sum_(r=1)^R
  (a_r^top u) (b_r^top v)c_r. $
]

=== Derivazione algoritmo classico

$
mat(a_11, a_12; a_21, a_22, delim: "[")
mat(b_11, b_12; b_21, b_22, delim: "[")
& = mat(a_11b_11 + a_12b_21, a_11b_12 + a_12b_22; a_21b_11 + a_22 b_21, a_21b_12 + a_22b_22, delim:
"[") \
& = mat(m_1 + m_2, m_3 + m_4; m_5 + m_6, m_7 + m_8, delim: "[") \
& = mat(c_11, c_12; c_21, c_22, delim: "[")
$
#speaker-note[Qui add animations]

Fissata la base standard $E_11, E_12, E_21, E_22$ dello spazio delle matrici $2 times 2$, possiamo
scrivere la bilinear computation
$
C = &c_11 E_11 + c_12 E_12 + c_21 E_21 + c_22 E_22 \
= &(m_1 + m_2)E_11 + (m_3 + m_4)E_12 \
+ &(m_5 + m_6)E_21 + (m_7 + m_8)E_22 \
= &sum_(r = 1)^8 m_r w_r.
$

L'algoritmo corrisponde al tensore
$
algob(2) = &(a_11 topp b_11 + a_12 topp b_21) topp c_11 \
+ &(a_21 topp b_11 + a_22 topp b_21) topp c_21 \
+ &(a_11 topp b_12 + a_12 topp b_22) topp c_12 \
+ &(a_21 topp b_12 + a_22 topp b_22) topp c_22.
$

=== Algoritmi approssimati

Bini et al. partendo dall'algoritmo classico $algob(2)$ e ponendo l'entrata $a_22 = 0$,
$
mat(a_11, a_12; a_21, 0, delim: "[")
mat(b_11, b_12; b_21, b_22, delim: "[")
& = mat(a_11b_11 + a_12b_21, a_11b_12 + a_12b_22; a_21b_11 , a_21b_12, delim:
"["). \
$

Trovano il tensore di rango $6$
$
algob(2)^(#text[red])
:= &a_(11) topp (b_(11) topp c_(11) + b_(12) topp c_(12)) \
+ &a_(12) topp (b_(21) topp c_(11) + b_(22) topp c_(12))      \
+ &a_(21) topp (b_(11) topp c_(21) + b_(12)
topp c_(22)).
$
Nel tentativo di ridurre numericamente il rango a $5$, trovano un tensore
$
algob(2)^("red")_t = &(a_(12) + t a_(11)) topp (b_(12) + t b_(22) topp c_(12))                                   \
+ &(a_(21) + t a_(11)) topp b_(11) topp (c_(11) + t c_(21))                                   \
+ &a_(12) topp b_(12) topp ((c_(11) + c_(12)) + t c_(22))                                    \
+ &a_(21) topp ((b_(11) + b_(12)) + t b_(21)) topp c_(11)                                    \
+ &(a_(12) + a_(21)) topp (b_(12) + t b_(21)) topp (c_(11) + t c_(22))
$

Scoprendo (accidentalmente) che
$
lim_(t -> 0) algob(2)^("red")_t = algob(2)^(#text[red])
$
Ovvero
$
brk(algob(2)^("red")) <= 5
$


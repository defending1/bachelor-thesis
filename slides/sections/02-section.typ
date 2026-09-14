#import "../lib.typ": *


= Il teorema di Kruskal

== Il caso matriciale

La decomposizione di una matrice $M$ in somma di $r$ matrici di rango uno
$
M = U V^top = u_1 v_1 + u_2 v_2 + dots.c + u_r v_r.
$
*non* è mai unica, in quanto esistono infinite matrici invertibili $P$ tali che
$
M = U P P^(-1) V^(top) = (U P)(V P^(-top))^(top).
$

PAUSE
Per i tensori c'è speranza!
L'unicità per la fattorizzazione CP esiste a meno di permutazioni e riscalamento dei fattori.

== Essenziale unicità


#definition[Essenziale unicità][
  Una fattorizzazione $ T = sum_(r=1)^R a_r topp b_r topp c_r in A topp B topp C $ di rango $R$ è *essenzialmente unica* se esistono degli
  scalari $ alpha_1,beta_1,gamma_1,alpha_2,beta_2, gamma_2, dots, alpha_R, beta_R, gamma_R $ tali
  che $alpha_r beta_r gamma_r = 1$ e una permutazione $sigma in frak(S)_R$ tali che
  $
  T = sum_(r=1)^R alpha_r a_(sigma(r)) topp beta_r b_(sigma(r)) topp c_r c_(sigma(r)).
  $
]<def:essunq>

== k-rango

#definition[$r$-posizione generale][
  Dato uno spazio vettoriale finito $W$ e sia $cal(S) subset PP W$ un insieme di punti. Diciamo che
  i punti di $cal(S)$ sono in
- *$2$-posizione generale* se nessuna coppia di punti coincide.
- *$3$-posizione generale* se nessuna terna di punti giace su una retta.
- *$4$-posizione generale* se nessuna quadrupla di punti giace su un piano.
*$r$-posizione generale* se nessuna $r$-upla giace su un sottospazio proiettivo di dimensione $r-2$.
]
#definition[$k$-rango][
  Dato un sottoinsieme di punti $cal(S) subset bb(P)$, il *$k$-rango* è il massimo intero
  positivo $r$ tale che i punti di $cal(S)$ sono in posizione generale.
]
Lo indichiamo con $ krank(cal(S)) .$

QUI FIGURA
#todo[Qui fare gli show con esempi punti, piano]

#remark[][
  La definizione originale di Kruskal era: data una matrice $M$, il $k$-rango $krank(M)$ è il massimo intero
  positivo $r$ tale che ogni sottoinsieme di $r$ colonne di $M$ sono vettori linearmente
  indipendenti.
]



== Il Teorema di Kruskal

#theorem[Kruskal @KRUSKAL197795 @landsberg2009kruskalstheorem][
  Sia $T in A topp B topp C$ un tensore che ammette una fattorizzazione $ T = sum_(r = 1)^R u_r topp
  v_r topp w_r. $ Siano $cal(S)_A = {[u_r]}, cal(S)_B ={[v_r]}, cal(S)_C = {[w_r]}$. Se vale
  #named-eq("K-3D")[
    $ R <= 1/2 (krank(cal(S)_A) + krank(cal(S)_B) + krank(cal(S)_C)) - 1, $
  ] <eq-kruskal>
  allora $T$ ha rango $R$ e la sua fattorizzazione è essenzialmente unica.
]

=== Il permutation lemma

#proposition[Permutation lemma][
  Siano $SS = {p_1, dots, p_R}$ e $tilde(SS) = {q_1, dots, q_R}$ due insiemi di punti in $PP W$ a
  due a due distinti, e supponiamo che $ango(tilde(SS)) = W$. Se ogni iperpiano $H subset PP W$ che
  contiene almeno $dim(H) + 1$ punti di $tilde(SS)$ è tale che $\#(SS inter H) <= \#(tilde(SS) inter
  H)$, allora $SS = tilde(SS)$.
]
#proof[Idea deall dimostrazione][
]

#pagebreak(weak: true)

=== Caso speciale (probabilmente in fondo)

#proposition[Landsberg @landsberg2009kruskalstheorem][
  Dati degli spazi vettoriali $A,B,C$ di dimensioni $dim(A) = dim(B) = dim(C) = bold(a)$ e un
  tensore $T$ di rango multilineare $(bold(a), bold(a), bold(a))$. Se $T$ ha rango $bold(a)$ allora la
  fattorizzazione è unica. In particolare, quando $krank(cal(S)_A) = krank(cal(S)_B) =
  krank(cal(S)_C) = bold(a)$, la condizione dell'@eq-kruskal si estende ad
  $
  bold(a) <= R <= 1/2 (bold(a) + bold(a)+ bold(a)) = 3/2 bold(a) - 1.
  $
]

== Il Teorema di Kruskal in dimensione $d$
#theorem[Kruskal, Sidiropoulos e Bro @sidiropoulos2000uniqueness][
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

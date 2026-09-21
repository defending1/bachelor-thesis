#import "../lib.typ": *



= Un teorema di unicità


== Controesempio

La decomposizione di una #mat-hl[matrice] $M$ in somma di $R$ matrici di rango uno
$
M = U V^top = u_1 v_1 + u_2 v_2 + dots.c + u_R v_R.
$
#pause
*non* è mai unica: esistono infinite scritture
$
M = U P P^(-1) V^(top) = (U P)(V P^(-top))^(top).
$

\
#pause
#align(center)[#text(35pt, weight: "bold", fill: gradient.radial(..color.map.rainbow))[\*Per i tensori c'è speranza!\*]]

== Enunciato (provvisorio)

#theorem[Kruskal][
  Data una decomposizione $ T = sum_(r=1)^R a_r topp b_r topp c_r $ di lunghezza $R$, se i fattori $a_r,
  b_r, c_r$ sono #underline(stroke: wave(period: 20pt, nperiods: 10, amplitude: 2pt, stroke: (thickness: 0.75pt,
  paint: red, dash: "densely-dashed"), multiple: (2pt, )))[abbastanza indipendenti], allora $T$ ha
  rango $R$ e
  #underline(stroke: wave(period: 20pt, nperiods: 10, amplitude: 2pt, stroke: (thickness: 0.75pt,
  paint: red, dash: "densely-dashed"), multiple: (2pt, )))[la decomposizione è unica].
]

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
Sia $W$ uno spazio vettoriale di dimensione finita.
#definition[$r$-posizione generale][
  Sia $cal(S) subset
  PP W$ un sottoinsieme di punti. Gli elementi di $cal(S)$ si dicono in *$r$-posizione generale* se
  nessuna $r$-upla di punti giace su un sottospazio proiettivo di dimensione $r-2$.
]
#pause
#remark[
- *$2$-posizione generale* se nessuna coppia di punti coincide.
- *$3$-posizione generale* se nessuna terna di punti giace su una retta.
]
#pagebreak()
#definition[$k$-rango][
  Il *$k$-rango* di un sottoinsieme $SS subset PP W$ è il massimo intero
  positivo $r$ tale che i punti di $cal(S)$ sono in $r$-posizione generale. Lo indichiamo con $ krank(cal(S)) .$
]

#import "../figures/glpos.typ": glpos-fig

#align(center)[#glpos-fig]

#speaker-note[
  La definizione originale di Kruskal era: data una matrice $M$, il $k$-rango $krank(M)$ è il massimo intero
  positivo $r$ tale che ogni sottoinsieme di $r$ colonne di $M$ sono vettori linearmente
  indipendenti.
]



== Il Teorema di Kruskal

#theorem[Kruskal @KRUSKAL197795 @landsberg2009kruskalstheorem][
  Sia $T in A topp B topp C$ un tensore che ammette una fattorizzazione $T = sum_(r = 1)^R u_r topp
  v_r topp w_r$ di lunghezza $R$.
  Siano $cal(S)_A = {[u_r]}, cal(S)_B ={[v_r]}, cal(S)_C = {[w_r]}$. Se vale
  #named-eq("K-3D")[
    $ 2(R + 1) <= krank(cal(S)_A) + krank(cal(S)_B) + krank(cal(S)_C), $
  ] <eq-kruskal>
  allora $T$ ha rango $R$ e la sua fattorizzazione è essenzialmente unica.
]

#pagebreak()
#proposition[Permutation lemma][
  Siano $SS = {p_1, dots, p_R}$ e $tilde(SS) = {q_1, dots, q_R}$ due insiemi di punti a due a due
  distinti in $PP W$. Supponiamo che $ango(tilde(SS)) = W$.
  Se ogni iperpiano $H subset PP W$ tale che $\#(tilde(SS) inter H) >= dim(H) + 1$ allora soddisfa $ \#(tilde(SS) inter
  H) <= \#(SS inter H). $ Allora $markhl(SS =
  tilde(SS), #<tesi>) #annot(<tesi>)[]$.
]
_Idea._
Consideriamo la proprietà
$
(cal(P)_k):"Ogni" k"-piano" L "tale che" \#(tilde(SS) inter L) >= dim(L)+1 = k+1,\ "allora"
\#(tilde(SS) inter L) <= \#(SS inter L).
$
#pagebreak()
$(cal(P)_0)$ è vera e implica $markhl(SS =
tilde(SS), #<tesi>) #annot(<tesi>)[]$.\
#pause
Per ipotesi induttiva $(cal(P)_(bold(w)-2))$ è vera.\
#pause
Mostriamo $(cal(P)_(k+1)) => (cal(P)_k)$. Da cui otteniamo
$
(cal(P)_(bold(w)-2)) => (cal(P)_(bold(w)- 3)) => dots.c => (cal(P)_1) => (cal(P)_0) => markhl(SS =
tilde(SS), #<tesi>).
#annot(<tesi>)[Tesi]
$
#pause
#align(center)[#image("../figures/drawing.pdf", width: 72%)]

#pagebreak(weak:true)
_Idea (Teorema di Kruskal)._
+ Consideriamo $ T = sum_(r = 1)^R u_r topp v_r topp w_r = sum_(r = 1)^R tilde(u)_r topp
tilde(v)_r topp tilde(w)_r. $
#pause
+ Applichiamo il permutation lemma per mostrare che $ SS_A = tilde(SS)_A, quad SS_B = tilde(SS)_B, quad
SS_C = tilde(SS)_C. $
#pause
+ A questo punto esistono $sigma, tau in frak(S)_R$ tali che $ T = sum_(r = 1)^R u_r topp v_r topp
w_r = sum_(r = 1)^R u_r topp v_sigma(r) topp
w_tau(r). $
#pause
+ Se $sigma = tau => $ Unicità.\ Se $sigma != tau => $ Contraddizione.

#pagebreak(weak: true)



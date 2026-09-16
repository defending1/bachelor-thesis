= Bonus: Teorema di Kruskal

== Semplificazione delle dimostrazioni

#import "../figures/proof_streamlining.typ": proof-streamlining-fig

#align(center + horizon)[
  #proof-streamlining-fig
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

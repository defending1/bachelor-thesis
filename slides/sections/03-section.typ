#import "../lib.typ": *


= Applicazione all'analisi di segnali

== Localizzazione di omini

#align(center)[
  #image("../figures/antennae.pdf", width: 80%)
]

#pagebreak(weak: true)

#align(center)[
  #image("../figures/antennae_step2.pdf", width: 80%)
]
Messaggio $s_r = [s_(1r), dots, s_(K r)]$.

#pagebreak(weak: true)

#align(center)[
  #image("../figures/antennae_step3.pdf", width: 80%)
]
Otteniamo una matrice $T = sum_(r=1)^R a_r topp s_r$, ma *non c'è unicità*.


#pagebreak(weak: true)

#align(center)[
  #image("../figures/antennae_step4.pdf", width: 80%)
]
Messaggio $s_r = [s_(1r), dots, s_(K r)]$ e codice $c_r = [c_(1r), dots, c_(J r)]$.

#pagebreak(weak: true)

#align(center)[
  #image("../figures/antennae_step5.pdf", width: 80%)
]
Otteniamo un tensore $T =cp(A,S,C) = sum_(r=1)^R a_r topp s_r topp c_r$.

== Esperimento numerico

La condizione di Kruskal
$
2(R + 1) <= krank(A) + krank(S) + krank(C)
$
diventa (i fattori $A,S,C$ hanno rango massimo)
$
2(R + 1) <= min(I, R) + min(K, R) + min(J, R)
$
Per $R = 4, K=100, I= 5, J = 16$ è soddisfatta:
$
2(4 + 1) = 10 <= 4 + 4 + 4
$

Recuperiamo il tensore $T$ approssimandolo con un tensore $hat(T)$
tramite l'algoritmo CP ALS
$
min_(hat(A), hat(S), hat(C)) norm( T - cp(hat(A), hat(S), hat(T)) ).
$

#align(center)[
  #image("../figures/antenna_localization_plot.pdf", width: 85%)
]

Se a $T$ aggiungiamo del rumore gaussiano $W_sigma$ in scala $sigma$ variabile, otteniamo
$
T_sigma' = T + W_sigma,
$

#table(
  columns: 3,
  stroke: none,
  align: center + horizon,
  table.header(
    [*Rumore*],
    [$sigma$],
    [*Scenario fisico*],
  ),

  [$sigma_0$], [$0.0000$], [Assenza di rumore],
  [$sigma_1$], [$0.0173$], [Segnale ottimo],
  [$sigma_2$], [$0.0403$],[Segnale buono],
  [$sigma_3$], [$0.0691$],[Segnale debole],
  [$sigma_4$], [$0.1037$],[Segnale quasi assente],
  [$sigma_5$], [$0.1382$], [Rumore fortissimo],
)

#align(center)[
  #image("../figures/antenna_localization_plot.pdf", width: 85%)
]

#align(center)[
  #image("../figures/dscdma_noise_experiment.pdf", width: 85%)
]

#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  header: align(right, text(fill: gray, size: 9pt)[Sperimentazione DS-CDMA -- Decomposizione Tensoriale e Localizzazione Antenne]),
  footer: [
    #line(length: 100%, stroke: 0.5pt + gray)
    #align(center, text(fill: gray, size: 9pt)[Pagina #context counter(page).display()])
  ]
)
#set text(font: "Liberation Serif", lang: "it", size: 11pt)
#set par(justify: true, leading: 0.65em)

#align(center)[
  #v(1em)
  #text(size: 18pt, weight: "bold")[Generazione Dataset, Decomposizione Tensoriale e Localizzazione Antenne] \
  #v(0.6em)
  #text(size: 12pt, style: "italic", fill: luma(80))[Modello DS-CDMA, Algoritmo CP-ALS e Analisi dell'Ambiguità di Permutazione]
  #v(1em)
  #line(length: 40%, stroke: 1pt + gray)
]

#v(1.5em)

= 1. Generazione dei Fattori e Costruzione del Tensore Denso (Capitolo 1, Sezione 1.5)

== 1.1 Generazione delle Matrici Fattore $A$, $C$ ed $S$

Nel modello DS-CDMA tri-lineare, il tensore delle misurazioni $T in bb(R)^(I times J times K)$ viene sintetizzato a partire dalle tre matrici fattore $A$, $C$ ed $S$, ciascuna delle quali rispecchia un aspetto fisico del canale di propagazione, del codice di estensione di banda e dei simboli trasmessi:

1. *Matrice di Canale Spaziale $A in bb(R)^(I times R)$*: descrive l'attenuazione del segnale tra le $I$ antenne riceventi e i $R$ utenti trasmittenti nello spazio 2D.
   - Le posizioni 2D delle antenne $p_i = (x_i, y_i) in bb(R)^2$ ($i = 1, dots, I$) e degli utenti $u_r = (x_r, y_r) in bb(R)^2$ ($r = 1, dots, R$) vengono generate uniformemente nel dominio $[0, L]^2$.
   - La distanza euclidea tra l'antenna $i$-esima e l'utente $r$-esimo è $d_(i, r) = \|p_i - u_r\|_2 = sqrt((x_i - x_r)^2 + (y_i - y_r)^2)$.
   - Gli elementi $a_(i, r)$ sono modellati secondo l'inverso della distanza (con soglia di sicurezza $d_("min") > 0$ per evitare singolarità):
     $ a_(i, r) = frac(1, max(d_(i, r), d_("min"))) $

2. *Matrice delle Sequenze di Spreading $C in \{-1, +1\}^(J times R)$*: contiene i codici di cifratura pseudo-casuali (chip) assegnati a ciascuna delle $R$ sorgenti.
   - Ciascun chip $c_(j, r)$ ($j = 1, dots, J$, $r = 1, dots, R$) è generato come variabile casuale binaria equiprobabile (BPSK):
     $ c_(j, r) in \{-1, +1\}, quad P(c_(j, r) = +1) = P(c_(j, r) = -1) = 1/2 $
   - Di conseguenza, ogni colonna $c_r$ possiede una norma euclidea costante pari a $\|c_r\|_2 = sqrt(J)$.

3. *Matrice dei Simboli di Trasmissione $S in bb(R)^(K times R)$*: rappresenta il carico di informazione inviato dai $R$ utenti lungo $K$ periodi di simbolo.
   - I valori del segnale $s_(k, r)$ ($k = 1, dots, K$, $r = 1, dots, R$) vengono campionati direttamente da una distribuzione gaussiana standard $s_(k, r) ~ cal(N)(0, 1)$ (oppure da un alfabeto binario BPSK $\{-1, +1\}$ per trasmissione digitale).

== 1.2 Unfolding e Costruzione del Tensore Denso

A partire dalle tre matrici fattore $A$, $C$ ed $S$, il tensore delle misurazioni $T in bb(R)^(I times J times K)$ è sintetizzato in forma denso attraverso la decomposizione CP di rango $R$:

$ T_(i, j, k) = sum_(r=1)^R a_(i, r) c_(j, r) s_(k, r) $

Come descritto nella Sezione 1.5 del Capitolo 1, la costruzione computazionale del tensore denso si effettua mediante l'unfolding matriciale sul modo uno:

$ cases(R_"mat" = S circle.tiny C in bb(R)^(K J times R), Y = A \, R_"mat"^T in bb(R)^(I times K J), T = "reshape"(Y, I times J times K) in bb(R)^(I times J times K).) $

Il costo computazionale ottimale è di $O(J K R)$ per formare $R_"mat"$ e di $O(I J K R)$ per formare $Y$.

#v(1em)

= 2. Ricostruzione dei Simboli $S$ con $A$ e $C$ Fissati (Capitolo 4, righe 210--215)

In accordo con le righe 210--215 del Capitolo 4 della tesi:
#quote(block: true, attribution: [Capitolo 4, righe 210--215])[
  _«Il recupero di $T$ avviene con l'algoritmo ALS, fissando le matrici $A, C$ e facendo variare la matrice $S$, minimizzando la funzione $\|T - sum_(r=1)^R s_r circle c_r circle a_r\|^2$.»_
]

Fissando le matrici $A in bb(C)^(I times R)$ e $C in bb(R)^(J times R)$, la soluzione esatta ai minimi quadrati per la matrice dei simboli $S in \{-1, +1\}^(K times R)$ è data in forma chiusa da:

$ S = T_((3)) \, M_3^* [(A^H A) times (C^H C)]^(-T) $

dove $M_3 = A circle.tiny C in bb(C)^(I J times R)$ e $T_((3)) in bb(C)^(K times I J)$ è l'unfolding del tensore lungo la terza modalità.
I simboli BPSK stimati sono $hat(s)_(k,r) = "sign"(Re(s_(k,r)))$.

#block(
  fill: rgb("f9f9fb"),
  inset: 8pt,
  radius: 3pt,
  stroke: 0.5pt + rgb("e0e0e5"),
  [
    #text(weight: "bold")[Nota sull'Assenza di Ambiguità di Scala:] \
    Poiché le matrici $A$ e $C$ sono assunte note _a fortiori_ (con i loro valori fisici esatti $a_(i, r) = 1/d_(i, r)$ e $\|c_r\|_2 = sqrt(J)$), la ricostruzione in forma chiusa di $S$ *non richiede alcun ripristino di scala*. L'equazione ai minimi quadrati determina direttamente $S$ nella sua ampiezza e scala fisica corretta.
  ]
)

#v(1em)

= 3. Risultati Numerici della Ricostruzione del Tensore

Riportiamo i risultati numerici del solutore `sandbox/dscdma/run_cp_solver.py` su due diversi scenari di simulazione.

#align(center)[
  #table(
    columns: (2.3fr, 2fr, 2fr),
    inset: 7pt,
    align: (left, center, center),
    stroke: 0.5pt + luma(150),
    fill: (x, y) => if y == 0 { rgb("eef0f5") } else { none },
    [*Metrica di Valutazione*], [*Scenario A ($R=3, I=4, J=16, K=100$)*], [*Scenario B ($R=4, I=6, J=32, K=500$)*],
    [Dimensioni Tensore $(I, J, K)$], [$(4, 16, 100)$], [$(6, 32, 500)$],
    [Norma di Frobenius $\|T\|_F$], [$114.6298$], [$593.4164$],
    [Errore Relativo Tensore ($epsilon_("rel")$)], [$3.523867 times 10^(-16)$], [$3.857824 times 10^(-16)$],
    [MSE Matrice $S$ (Simboli)], [$1.323170 times 10^(-31)$], [$1.288063 times 10^(-31)$],
    [Errori sui Simboli], [$0 \/ 300$], [$0 \/ 2000$],
    [*Bit Error Rate (BER)*], [*0.000000*], [*0.000000*]
  )
]

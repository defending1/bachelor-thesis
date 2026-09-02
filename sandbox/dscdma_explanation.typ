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

= 1. Costruzione del Tensore Denso (Capitolo 1, Sezione 1.5)

Come descritto nella Sezione 1.5 del Capitolo 1, per costruire il tensore in formato denso $T in bb(C)^(I times J times K)$ a partire dalle tre matrici fattore $A in bb(C)^(I times R)$, $C in bb(R)^(J times R)$ ed $S in \{-1, +1\}^(K times R)$, si sfrutta l'unfolding matriciale sul modo uno:

$ cases(R_"mat" = S circle.tiny C in bb(C)^(K J times R), Y = A \, R_"mat"^T in bb(C)^(I times K J), T = "reshape"(Y, I times J times K) in bb(C)^(I times J times K).) $

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

#v(1em)

= 4. Decomposizione Cieca CP-ALS e Localizzazione 2D delle Antenne

Nella sperimentazione di decomposizione cieca mediante l'algoritmo CP-ALS (`solve_cp_als`), il tensore $T$ viene fattorizzato senza conoscere a priori le matrici originarie $A$, $C$ ed $S$. La matrice di canale stimata $hat(A) = (hat(a)_(i, c)) in bb(R)^(I times R)$ consente di recuperare le posizioni 2D delle antenne $p_i = (x_i, y_i) in bb(R)^2$ a partire dai raggi di attenuazione stimati:
$ R_(i, c) = frac(1, |hat(a)_(i, c)|) $
dove $u_r in bb(R)^2$ ($r = 1, dots, R$) rappresenta la posizione nota del generico utente $r$-esimo, e $c in \{1, dots, R\}$ indica l'indice di colonna della matrice fattore stimata $hat(A)$.

== 4.1 Ambiguità di Permutazione nei Modelli CP

La decomposizione CP di un tensore di rango $R$:
$ T_(i, j, k) = sum_(r=1)^R a_(i, r) c_(j, r) s_(k, r) $
è definita a meno di una permutazione casuale delle componenti. Indicando con $P in bb(R)^(R times R)$ una matrice di permutazione associata a una biiezione $pi in cal(S)_R$:
$ hat(A) = A P, quad hat(C) = C P, quad hat(S) = S P $
il tensore ricostruito $T$ rimane invariato. Di conseguenza, la colonna $c$-esima della matrice stimata $hat(A)$ non corrisponde necessariamente all'utente di pari indice $r = c$ (con posizione $u_c$), bensì all'utente $r = pi(c)$, posizionato in $u_(pi(c))$, dove la permutazione $pi$ è a priori incognita.

Se si applicasse la trilaterazione senza determinare $pi$, l'accoppiamento ingenuo associerebbe il raggio $R_(i, c) = frac(1, |hat(a)_(i, c)|)$ alle coordinate dell'utente $u_c$ (l'utente il cui indice $r$ coincide banalmente col numero di colonna $c$), anziché alle coordinate dell'utente reale $u_(pi(c))$. Poiché le circonferenze sarebbero centrate su utenti sbagliati, l'ottimizzatore a minimi quadrati convergerebbe verso coordinate fittizie con un errore residuo molto elevato.

== 4.2 Risoluzione dell'Ambiguità tramite Assegnamento Ottimale

Per individuare la permutazione corretta tra le colonne di $hat(A)$ e le posizioni note degli utenti $u_r in bb(R)^2$ ($r = 1, dots, R$), il sistema valuta tutte le $R!$ permutazioni $pi in cal(S)_R$.

Per ciascuna permutazione candidata $pi$, indichiamo con $hat(p)_i = (hat(x)_i, hat(y)_i) in bb(R)^2$ il vettore posizione 2D dell'antenna $i$-esima, stimato minimizzando il residuo dei minimi quadrati non lineari:
$ "Costo"(pi) = sum_(i=1)^I sum_(c=1)^R ( \|hat(p)_i - u_(pi(c))\|_2 - R_(i, c) )^2 $
dove $R_(i, c) = frac(1, |hat(a)_(i, c)|)$ è il raggio stimato per l'antenna $i$ rispetto alla colonna $c$.

- Per permutazioni errate ($pi eq.not pi^*$), i raggi $R_(i, c)$ non corrispondono alla geometria degli utenti $u_(pi(c))$, producendo un residuo elevato ($"Costo"(pi) >> 0$).
- Per la permutazione corretta ($pi = pi^*$), le circonferenze centrate in $u_(pi(c))$ con raggio $R_(i, c)$ si intersecano esattamente nella posizione dell'antenna $p_i$, annullando il residuo ($"Costo"(pi^*) approx 0$).

La permutazione ottima $pi^* = arg min_(pi in cal(S)_R) "Costo"(pi)$ identifica l'associazione corretta colonna-utente e determina i vettori posizione $hat(p)_i$ delle antenne.

== 4.3 Ripristino della Scala Fisica dei Fattori

Gli algoritmi CP-ALS standard normalizzano le colonne dei fattori a norma unitaria ($\|a_r\|_2 = 1$). Nel sistema DS-CDMA:
- I codici di spreading $C in \{-1, +1\}^(J times R)$ hanno potenza $\|c_r\|_2 = sqrt(J)$.
- I simboli di trasmissione $S in bb(R)^(K times R)$ hanno varianza unitaria, per cui $\|s_r\|_2 = sqrt(K)$.

Ripristinando la norma fisica sui fattori $C$ ed $S$, il fattore di scala reale dei guadagni di canale viene trasferito alla matrice $hat(A)$:
$ hat(A)_("fisica") = hat(A)_("grezza") dot frac(\|C_("grezza")\|_2 dot \|S_("grezza")\|_2, sqrt(J dot K)) $
Questo approccio riporta i guadagni di canale al loro valore fisico $hat(a)_(i, r) approx 0.01 -- 0.05$, generando raggi $R_(i, r) = frac(1, |hat(a)_(i, r)|) approx 20 -- 80$ coerenti con l'area della simulazione ($100 times 100$).

== 4.4 Risultati Sperimentali e Visualizzazione

Eseguendo il solutore con $n_("restarts") = 10$ e minimizzando l'errore di ricostruzione del tensore ($epsilon_("rel") = 6.495 times 10^(-8)$), la posizione 2D delle antenne viene ricostruita con un errore medio pari a $approx 4.5$ unità spaziali.

#align(center)[
  #image("dscdma/antenna_localization_plot.pdf", width: 88%)
]

#v(1em)

#block(
  fill: rgb("f4f4f6"),
  inset: 12pt,
  radius: 4pt,
  stroke: 0.5pt + rgb("d0d0d5"),
  [
    #text(weight: "bold")[Sintesi dei Risultati:] \
    L'azione congiunta delle re-inizializzazioni CP-ALS, il ripristino della scala fisica e la ricerca della permutazione ottima $pi^*$ garantisce la localizzazione precisa delle antenne $p_i$ e il tracciamento delle circonferenze di raggio $R_(i, r) = frac(1, |hat(a)_(i, r)|)$ centrate attorno a ciascuna antenna ricostruita $hat(p)_i$.
  ]
)

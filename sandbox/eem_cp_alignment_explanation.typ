#set page(
  paper: "a4",
  margin: (x: 2.2cm, y: 2.2cm),
  header: align(right)[
    #text(size: 8.5pt, fill: rgb("#4a5568"))[Analisi Spettroscopia EEM -- Funzione align_components e Riscalamento CP]
  ],
  footer: context [
    #line(length: 100%, stroke: 0.5pt + rgb("#e2e8f0"))
    #v(3pt)
    #align(center)[#text(size: 8.5pt, fill: rgb("#718096"))[Pagina #counter(page).display() di #counter(page).final().at(0)]]
  ]
)

#set text(
  font: "Liberation Serif",
  size: 10.5pt,
  lang: "it"
)

#set par(justify: true, leading: 0.6em)
#set heading(numbering: "1.1")

#align(center)[
  #v(0.5em)
  #text(size: 17pt, weight: "bold", fill: rgb("#1a365d"))[Allineamento e Riscalamento delle Componenti nell'Esperimento Tensoriale EEM]
  #v(0.4em)
  #text(size: 11pt, style: "italic", fill: rgb("#2b6cb0"))[Spiegazione Intuitiva, Matematica ed Implementativa di `align_components` e del Riscalamento]
  #v(0.8em)
  #line(length: 100%, stroke: 1pt + rgb("#cbd5e0"))
  #v(0.6em)
]

= 1. Spiegazione Intuitiva (L'Analogia dell'Assaggiatore Bendato)

Prima di addentrarci nei dettagli matematici, è utile capire *perché* abbiamo bisogno dell'allineamento e del riscalamento usando una semplice analogia.

Immagina di avere 18 frullati diversi (i *campioni*), e ciascuno è composto da un mix segreto di 3 ingredienti (i *fluorofori*: Phe, Trp-Gly, Val-Tyr-Val). Tu possiedi la ricetta esatta (la *matrice di riferimento*).

Fai assaggiare questi 18 frullati a un "assaggiatore bendato" molto esperto (l'*Algoritmo CP*). L'assaggiatore riesce a identificare perfettamente 3 profili di sapore distinti e la quantità di ciascun sapore in ogni frullato. Tuttavia, l'assaggiatore ha due limiti:

1. *Indeterminazione di Permutazione (Il Problema dei Nomi)*: L'assaggiatore ti restituisce i risultati etichettati semplicemente come "Sapore 1", "Sapore 2" e "Sapore 3", ordinati in base al sapore più forte in generale. Non conosce i veri nomi degli ingredienti.
   - *La Soluzione (Allineamento)*: Confronti l'andamento del "Sapore 1" nei 18 frullati con il tuo ricettario. Se il "Sapore 1" aumenta e diminuisce esattamente negli stessi frullati in cui hai aggiunto "Phe", deduci che "Sapore 1 = Phe". Lo facciamo usando la "Similarità Coseno" (un modo matematico per confrontare l'andamento o il pattern).

2. *Indeterminazione di Scala (Il Problema delle Unità di Misura)*: L'assaggiatore valuta la quantità di ogni sapore su una scala arbitraria da 0 a 1. Ma il tuo ricettario usa unità di misura fisiche (micromoli, $10^{-6}$ M).
   - *La Soluzione (Riscalamento)*: Trovi il frullato con la quantità assoluta più alta di "Phe" nella tua ricetta (es. 6 micromoli). Guardi il punteggio dell'assaggiatore per quello stesso frullato (es. 0.2). A questo punto, moltiplichi *tutti* i punteggi "Phe" dell'assaggiatore per un fattore (6 / 0.2) in modo che il punteggio massimo raggiunga esattamente la soglia delle 6 micromoli. Ora i numeri dell'assaggiatore coincidono con le unità fisiche della tua ricetta e puoi confrontarli visivamente sullo stesso grafico.

#v(1em)

= 2. Introduzione e Motivazione Teorica

Nello studio della spettroscopia di matrice di eccitazione-emissione (EEM, *Excitation-Emission Matrix*), una miscela chimica contenente $R$ fluorofori viene misurata su $N$ campioni, producendo un tensore di terzo ordine:

$ cal(X) in bb(R)_+^(N times J times K) $

dove:
- *Modo 1* ($N = 18$): Campioni delle miscele chimiche ($i = 1, dots, N$).
- *Modo 2* ($J = 251$): Lunghezze d'onda di emissione ($lambda_("em") in [275, 525]\ "nm"$, $j = 1, dots, J$).
- *Modo 3* ($K = 21$): Lunghezze d'onda di eccitazione ($lambda_("ex") in [220, 300]\ "nm"$, $k = 1, dots, K$).

In base alle leggi fisiche della spettrofluorimetria (Beer-Lambert e Parker), l'intensità di fluorescenza è trilineare e viene modellata tramite decomposizione *Canonical Polyadic Non-Negativa (CP / PARAFAC)* di rango $R$:

$ cal(X)_(i,j,k) approx sum_(r=1)^R lambda_r A_(i,r) B_(j,r) C_(k,r) quad <==> quad cal(X) approx [| bold(lambda); bold(A), bold(B), bold(C) |] $

dove $bold(A) in bb(R)_+^(N times R)$ rappresenta i profili di concentrazione (*loadings*), $bold(B) in bb(R)_+^(J times R)$ gli spettri di emissione, $bold(C) in bb(R)_+^(K times R)$ gli spettri di eccitazione, e $bold(lambda) in bb(R)_+^R$ i pesi associati a ciascuna componente.

== Le Due Indeterminazioni della Decomposizione CP

Nonostante la decomposizione CP goda dell'unicità essenziale (condizione di Kruskal), essa presenta due simmetrie matematiche intrinseche:
1. *Indeterminazione di Permutazione*: L'ordine delle colonne $r = 1, dots, R$ estratte dagli algoritmi di ottimizzazione (ad es. CP-ALS) è del tutto arbitrario e privo di consapevolezza dell'identità chimica del fluoroforo.
2. *Indeterminazione di Scala*: Per ogni tripla di scalari positivi $alpha_r, beta_r, gamma_r > 0$ tali che $alpha_r beta_r gamma_r = 1$, il riscalamento $bold(A)_(::,r) <- alpha_r bold(A)_(::,r)$, $bold(B)_(::,r) <- beta_r bold(B)_(::,r)$, e $bold(C)_(::,r) <- gamma_r bold(C)_(::,r)$ lascia invariato il tensore ricostruito.

Per confrontare le concentrazioni stimate $bold(A)$ con la matrice di riferimento *ground-truth* $bold(M) in bb(R)_+^(N times 3)$ contenente le concentrazioni reali dei fluorofori (*Phenylalanine*, *Tryptophan-Glycine*, *Valine-Tyrosine-Valine*), è indispensabile risolvere entrambe le indeterminazioni.

#v(0.5em)

= 3. Normalizzazione dei Fattori e Riordinamento per Peso

Prima dell'allineamento, le matrici fattore estratte da CP-ALS vengono normalizzate per colonna in norma $l_2$:

$ d_(m, r) = ||bold(F)_("::", r)^((m))||_2, quad m in {1, 2, 3}, \; r in {1, dots, R} $
$ bold(hat(F))_("::", r)^((m)) = (bold(F)_("::", r)^((m))) / d_(m, r), quad lambda_r <- lambda_r · product_(m=1)^3 d_(m, r) $

Trasferito tutto l'assorbimento delle norme nel vettore dei pesi $bold(lambda)$, le componenti vengono ordinate in modo decrescente rispetto a $lambda_r$. Le matrici fattore risultanti sono $bold(hat(A)), bold(hat(B)), bold(hat(C))$.

#v(0.5em)

= 4. Allineamento delle Componenti (`align_components`)

Poiché il riordinamento basato su $lambda_r$ risponde solo all'energia del segnale, la colonna $j$-esima di $bold(hat(A))$ non corrisponde necessariamente alla sostanza $j$-esima presente in $bold(M)$.

== Formulazione Matematica dell'Allineamento

1. *Normalizzazione dei Riferimenti*:
   $ bold(hat(M))_(::, k) = (bold(M)_(::, k)) / (||bold(M)_(::, k)||_2), quad k = 1, dots, M_("ref") $

2. *Matrice di Similarità Coseno*:
   Per ogni componente calcolata $j in {1, dots, R}$ in $bold(hat(A))$, si calcola il valore assoluto del prodotto scalare con le sostanze di riferimento $k in {1, dots, M_("ref")}$:
   $ S(j, k) = | bold(hat(A))_(::, j)^top bold(hat(M))_(::, k) | $

3. *Regola di Assegnamento Ottimale*:
   L'indice del composto di riferimento che meglio approssima la componente $j$ è dato da:
   $ k^*(j) = arg max_(k in {1, dots, M_("ref")}) S(j, k) $

4. *Costruzione della Matrice Riordinata*:
   $ bold(M)_("matched")[:, j] = bold(M)[:, k^*(j)], quad forall j = 1, dots, R $

== Codice Sorgente in `alignment.py`

La funzione `align_components` è implementata nel modulo `experiments/utils/cp/alignment.py`:

#block(
  fill: rgb("#f8fafc"),
  inset: 10pt,
  radius: 4pt,
  stroke: 0.5pt + rgb("#cbd5e0"),
  [
```python
import numpy as np

def align_components(norm_A: np.ndarray, norm_mixtures: np.ndarray) -> np.ndarray:
    """
    Per ogni colonna calcolata in norm_A, trova la colonna di riferimento
    in norm_mixtures che massimizza la similarità coseno in valore assoluto.
    """
    n_comp = norm_A.shape[1]
    n_mixtures = norm_mixtures.shape[1]
    matched_mixtures = np.zeros_like(norm_A)
    for j in range(n_comp):
        similarities = [
            np.abs(np.dot(norm_A[:, j], norm_mixtures[:, k]))
            for k in range(n_mixtures)
        ]
        best_k = int(np.argmax(similarities))
        matched_mixtures[:, j] = norm_mixtures[:, best_k]
    return matched_mixtures
```
  ]
)

#v(0.5em)

= 5. Riscalamento di Picco per il Confronto Grafico

Anche dopo l'allineamento, permane una discrepanza di scala tra $bold(hat(A))_(::, j)$ e $bold(M)_("matched")[:, j]$:
- $bold(hat(A))_(::, j)$ è a norma unitaria $l_2$, con valori numerici adimensionati nell'intervallo $~ 0.1 - 0.3$.
- Le concentrazioni reali $bold(M)$ sono espresse in concentrazioni molari sull'ordine di $10^(-6)\ "M"$ (valori tra $0$ e $6 times 10^(-6)\ "M"$).

== Algoritmo di Riscalamento in `viz_eem_cp.py`

Per permettere la sovrapposizione visiva su grafici a barre affiancate, `viz_eem_cp.py` esegue le seguenti operazioni per ciascuna componente $j$:

1. *Calcolo della Scala del Riferimento*:
   $ "scale"_j = max_(i) (bold(M)_("matched")[i, j]) times 10^6 $
   $ "scaled_mixtures"[:, j] = bold(M)_("matched")[:, j] times 10^6 $

2. *Riscalamento del Fattore Calcolato*:
   $ "max_a"_j = max_(i) (bold(hat(A))[i, j]) $
   $ "scaled_A"[:, j] = (bold(hat(A))_(::, j)) / ("max_a"_j) times "scale"_j $

== Significato Geometrico

Grazie a questa trasformazione:
$ max_(i) ("scaled_A"[i, j]) = "scale"_j = max_(i) ("scaled_mixtures"[i, j]) $

Entrambi i profili (quello calcolato da CP e quello reale ground-truth) raggiungono esattamente la stessa altezza massima sul grafico a barre, rendendo immediatamente confrontabili le variazioni relative di concentrazione campione per campione (da 1 a 18).

#v(0.5em)

= 6. Workflow Completo di Visualizzazione (`viz_eem_cp.py`)

La pipeline completa eseguita dalla funzione `visualize_eem_cp()` è la seguente:

#block(
  fill: rgb("#f7fafc"),
  inset: 10pt,
  radius: 4pt,
  stroke: 0.5pt + rgb("#e2e8f0"),
  [
    *Sequenza delle Operazioni:*
    1. *Stima CP*: Fittaggio CP-ALS non-negativo di rango $R=3$ sul tensore $cal(X) in bb(R)^(18 times 251 times 21)$.
    2. *Normalizzazione e Ordinamento*: Normalizzazione $l_2$ dei fattori, aggiornamento di $bold(lambda)$, e ordinamento decrescente.
    3. *Allineamento Coseno*: Esecuzione di `align_components(norm_A, norm_mixtures)` per accoppiare ogni componente calcolata alla relativa sostanza chimica (*Phe*, *Trp-Gly*, *Val-Tyr-Val*).
    4. *Riscalamento di Picco*: Normalizzazione rispetto ai picchi massimi per portare sia `scaled_A` sia `scaled_mixtures` sulla scala $10^(-6)$.
    5. *Generazione Grafica*: Creazione della griglia $3 times 3$ con i tre modi di decompressione salvata in `eem_model.pdf` e `eem_model.png`.
  ]
)

#v(1em)

#block(
  fill: rgb("#ebf8ff"),
  inset: 12pt,
  radius: 4pt,
  stroke: 0.5pt + rgb("#3182ce"),
  [
    #text(weight: "bold", fill: rgb("#2b6cb0"))[Sintesi Focale:] \
    L'allineamento risolve l'ambiguità di permutazione garantendo l'associazione corretta tra componenti calcolate e fluorofori reali. Il riscalamento di picco ancorando il valore massimo di ciascuna componente consente un confronto visivo diretto delle concentrazioni relative su un asse verticale unificato.
  ]
)

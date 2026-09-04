#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  header: align(right, text(fill: gray, size: 9pt)[Analisi Spettroscopia EEM -- Funzione align_components e Visualizzazione CP]),
  footer: [
    #line(length: 100%, stroke: 0.5pt + gray)
    #align(center, text(fill: gray, size: 9pt)[Pagina #context counter(page).display()])
  ]
)
#set text(font: "Liberation Serif", lang: "it", size: 11pt)
#set par(justify: true, leading: 0.65em)

#align(center)[
  #v(0.5em)
  #text(size: 18pt, weight: "bold")[Allineamento delle Componenti nella Decomposizione CP Spettroscopica EEM] \
  #v(0.6em)
  #text(size: 12pt, style: "italic", fill: luma(80))[Analisi Matematica di `align_components` ed Utilizzo nel Modulo `viz_eem_cp.py`]
  #v(0.8em)
  #line(length: 40%, stroke: 1pt + gray)
]

#v(1em)

= 1. Introduzione e Motivazione Teorica

Nello studio della spettroscopia di matrice di eccitazione-emissione (EEM, *Excitation-Emission Matrix*), una miscela chimica contenente $R$ fluorofori viene modellata mediante decomposizione tensoriale non-negativa *Canonical Polyadic* (CP / PARAFAC) di rango $R$:

$ X_(i, j, k) approx sum_(r=1)^R lambda_r A_(i, r) B_(j, r) C_(k, r) $

dove:
- $A in bb(R)_+^(N times R)$ rappresenta i profili di concentrazione o *loadings* dei campioni (modo 1, campioni $i = 1, dots, N$),
- $B in bb(R)_+^(J times R)$ rappresenta i profili di spettro di emissione (modo 2, lunghezze d'onda di emissione),
- $C in bb(R)_+^(K times R)$ rappresenta i profili di spettro di eccitazione (modo 3, lunghezze d'onda di eccitazione).

== Ambiguità di Permutazione nei Modelli CP

La decomposizione CP gode dell'unicità essenziale a meno di *riscalamento* e *permutazione*. Ciò significa che l'ordine delle colonne $r = 1, dots, R$ estratte dalle matrici fattore $A, B, C$ dall'algoritmo di ottimizzazione (ad es. CP-ALS) è *arbitrario*. 

Quando si confrontano i profili di concentrazione stimati $A$ con le concentrazioni reali di riferimento delle sostanze chimiche note $M in bb(R)_+^(N times M)$ (ad esempio i fluorofori *Phenylalanine*, *Tryptophan-Glycine*, *Valine-Tyrosine-Valine*), la colonna $j$-esima di $A$ non corrisponde necessariamente alla colonna $j$-esima della matrice di riferimento $M$.

La funzione `align_components` risolve questa ambiguità riordinando le colonne della matrice di riferimento $M$ in modo da farle corrispondere alle componenti stimate nella matrice $A$.

#v(1em)

= 2. Formulazione Matematica di `align_components`

La funzione prende in ingresso due matrici:
- $A_"norm" in bb(R)^(N times R)$: matrice fattore stimata (tipicamente normalizzata per colonna),
- $M_"norm" in bb(R)^(N times M)$: matrice delle concentrazioni di riferimento (ground-truth).

== Metrica di Similarità Coseno

Per ogni colonna estratta $j in \{1, dots, R\}$ di $A_"norm"$, la funzione calcola la similarità coseno in valore assoluto con ciascuna colonna di riferimento $k in \{1, dots, M\}$ di $M_"norm"$:

$ S(j, k) = | bold(A)_("norm")[:, j] dot bold(M)_("norm")[:, k] | $

Se i vettori colonna sono a norma unitaria, $S(j, k)$ coincide esattamente con la similarità coseno.

== Regola di Assegnamento Ottimale

L'indice del composto di riferimento che meglio approssima la componente $j$-esima viene determinato massimizzando la similarità:

$ k^*(j) = arg max_(k in \{1, dots, M\}) S(j, k) $

La matrice riordinata finale $M_"matched" in bb(R)^(N times R)$ viene definita colonna per colonna impostando:

$ bold(M)_("matched")[:, j] = bold(M)[:, k^*(j)], quad forall j = 1, dots, R $

#v(1em)

= 3. Codice Sorgente di `align_components`

La funzione è definita nel modulo `experiments/utils/cp/alignment.py`:

#block(
  fill: rgb("f8f9fa"),
  inset: 10pt,
  radius: 4pt,
  stroke: 0.5pt + rgb("d0d0d5"),
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

#v(1em)

= 4. Utilizzo all'interno di `viz_eem_cp.py`

Nel modulo di visualizzazione `experiments/tensor_data_eem/plots/viz_eem_cp.py`, la funzione `visualize_eem_cp()` segue una pipeline ben strutturata per la validazione visiva della decomposizione CP di rango 3 su dati EEM18:

#v(0.5em)

== 4.1 Sequenza Operativa

1. *Fittaggio ed Estrazione dei Fattori*: Si esegue CP-ALS sul tensore $X$ ottenendo i vettori peso $lambda$ e le matrici fattore $A, B, C$.
2. *Normalizzazione e Riordinamento*:
   - I fattori vengono normalizzati per colonna $\|A_{:, r}\|_2 = 1, \|B_{:, r}\|_2 = 1, \|C_{:, r}\|_2 = 1$.
   - L'assorbimento delle norme trasferisce l'intensità assoluta al vettore dei pesi $lambda$.
   - Le componenti vengono ordinate in modo decrescente in base al peso $lambda_r$.
3. *Chiamata a `align_components`*:
   #block(
     fill: rgb("f8f9fa"),
     inset: 8pt,
     radius: 3pt,
     stroke: 0.5pt + rgb("e0e0e5"),
     [
```python
norm_mixtures = mixtures / np.linalg.norm(mixtures, axis=0)

matched_mixtures_unscaled = align_components(norm_A, mixtures)
matched_mixtures_norm = align_components(norm_A, norm_mixtures)
```
     ]
   )
   - `matched_mixtures_unscaled`: allinea le concentrazioni reali non scalate alla sequenza di componenti ordinate in `norm_A`.
   - `matched_mixtures_norm`: effettua l'allineamento sulle matrici a norma unitaria.
4. *Riscalamento e Confronto Grafico*:
   - Per ciascuna delle 3 componenti, le concentrazioni stimate (`scaled_A`) e quelle reali (`scaled_mixtures`) vengono riportate alla stessa scala molecolare ($10^6$).
   - Viene generato un grafico a barre affiancate (*Campione*, colonne di sinistra) che visualizza il confronto campione per campione (da 1 a 18) tra i valori stimati dalla CP e le reali concentrazioni chimiche.

#v(1em)

#block(
  fill: rgb("edf2fa"),
  inset: 12pt,
  radius: 4pt,
  stroke: 0.5pt + rgb("b0c4de"),
  [
    #text(weight: "bold", fill: rgb("1a365d"))[Sintesi dell'Utilità:] \
    Senza l'utilizzo di `align_components`, l'ordine arbitrario restituito dalla decomposizione tensoriale causerebbe l'accoppiamento errato delle barre di concentrazione calcolata rispetto alle sostanze di riferimento chimico (*Phe*, *Trp-Gly*, *Val-Tyr-Val*), falsando il confronto visivo nei grafici pubblicabili.
  ]
)

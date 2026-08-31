# DS-CDMA Exact Rank-R Tensor Dataset Generator

Questo modulo Python implementa la generazione di dataset sintetici per la
**Blind deconvolution of DS-CDMA signals**.

## Modello Matematico

Il segnale ricevuto all'antenna $i$, al chip $j$ e al tempo di simbolo $k$ è
rappresentato dal tensore a 3 vie di rango $R$:

$$T_{ijk} = \sum_{r=1}^R a_{ir} \, c_{jr} \, s_{kr}$$

Dove:

- $a_{ir} \in \mathbb{C}$: Guadagno/fading complesso dell'antenna $i$ per
  l'utente $r$, $a_{ir} \sim \mathcal{CN}(0, 1)$.
- $c_{jr} \in \{-1, +1\}$: Sequenza di spreading ortogonale di Walsh-Hadamard di
  lunghezza $J$.
- $s_{kr} \in \{-1, +1\}$: Simboli d'informazione BPSK inviati al tempo $k$.

Il modello è **privo di rumore** e **senza memoria** (assenza di ICI ed ISI,
trasmissione in linea d'aria).

## Struttura del Modulo

- `config.py`: Definizione dei parametri della simulazione ($R, I, J, K$, seed).
- `codes.py`: Generazione delle sequenze di spreading di Walsh-Hadamard.
- `channel.py`: Generazione della matrice di guadagni complessi d'antenna $A$.
- `generator.py`: Generazione del tensore 3D $T_{ijk}$ tramite prodotti esterni
  ed `np.einsum`.
- `exporter.py`: Salvataggio e caricamento nativo in formato compresso `.npz`.
- `run_generator.py`: Script eseguibile da riga di comando.
- `tests/test_tensor_exact.py`: Suite di unit test pytest.

## Esecuzione dei Test

Per eseguire i test di correttezza matematica:

```bash
pytest sandbox/dscdma/tests/
```

## Esempio di Utilizzo da CLI

```bash
python sandbox/dscdma/run_generator.py -r 3 -i 2 -j 16 -k 100 -o dataset_cap4.npz
```

# DS-CDMA Spatial 3D Tensor Generator & CP-ALS Factor Recovery

Questo modulo Python implementa la generazione di dataset sintetici per la
**Blind deconvolution of DS-CDMA signals** con modello di canale spaziale 2D e la decomposizione CP-ALS per il recupero delle matrici dei fattori $(A, C, S)$.

## Modello Matematico

Il segnale ricevuto all'antenna $i$, al chip $j$ e al tempo di simbolo $k$ è
rappresentato dal tensore reale a 3 vie di rango $R$:

$$T_{ijk} = \sum_{r=1}^R a_{ir} \, c_{jr} \, s_{kr}$$

Dove:

- $a_{ir} \in \mathbb{R}$: Guadagno di canale tra l'antenna $i$ e l'utente $r$, definito da $a_{ir} = \text{Re}(1 / d_{ir}) = 1 / d_{ir}$, dove $d_{ir}$ è la distanza euclidea 2D tra l'antenna $i$ e l'utente $r$.
- $c_{jr} \in \{-1, +1\}$: Sequenza di spreading binaria casuale di lunghezza chip $J$.
- $s_{kr} \in \mathbb{R}$: Segnale generico reale trasmesso dall'utente $r$ al tempo $k$.

Il modello è **privo di rumore** e **senza memoria**.

## Decomposizione CP-ALS (TensorLy)

Le matrici dei fattori $(\hat{A}, \hat{C}, \hat{S})$ vengono stimate tramite decomposizione CP in TensorLy (`tensorly.decomposition.parafac`).
La corrispondenza tra i fattori stimati e quelli reali viene calcolata risolvendo l'ambiguità di permutazione delle colonne (con `scipy.optimize.linear_sum_assignment`) e l'ambiguità di scala intrinseca del modello CP.

## Struttura del Modulo

- `pyproject.toml`: Configurazione delle dipendenze del progetto per `uv` (`tensorly`, `numpy`, `scipy`, `pytest`).
- `config.py`: Definizione dei parametri di simulazione ($R, I, J, K$, area 2D, seed).
- `channel.py`: Dispersione 2D di utenti ed antenne e calcolo della matrice $A$ basata su $1 / d_{ir}$.
- `codes.py`: Generazione delle sequenze di spreading binaria casuale $C \in \{-1, +1\}^{J \times R}$.
- `generator.py`: Generazione del segnale reale $S$ e costruzione del tensore 3D $T_{ijk}$.
- `cp_solver.py`: Decomposizione CP-ALS tramite TensorLy e allineamento dei fattori $(\hat{A}, \hat{C}, \hat{S})$.
- `exporter.py`: Salvataggio e caricamento del dataset in formato `.npz`.
- `run_cp_solver.py`: Script di test per la decomposizione CP-ALS ed il calcolo delle metriche di errore.
- `run_generator.py`: Script CLI per generare e salvare un dataset.
- `tests/`: Suite di unit test pytest (`test_tensor_exact.py`, `test_cp_solver.py`).

## Gestione Dipendenze ed Esecuzione con `uv`

Tutti i comandi possono essere eseguiti tramite `uv` all'interno della cartella `sandbox/dscdma`:

```bash
uv sync
uv run pytest
uv run python run_cp_solver.py -r 3 -i 4 -j 16 -k 100
```

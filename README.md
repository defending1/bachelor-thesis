# Stato progetto

## 4.06

Stato:

- studiato fino a costruzione del tensore in formato denso. Studiate
  applicazioni CP.
- Letto prima parte ref errore (serve tempo per capirla)
- Letta prima parte altra ref
- Alcuni passaggi da chiedere
- Alcune cose scritte in tex

Discutere:

- Qualche idea sull'implementazione
- Capire idea articolo su errore: cosa andremo a studiare?
- Giustificazione passaggio con master theorem, sì o no?

# Todo

- Dove chiaro dal contesto, sostituire decomposizione CP di rango r con
  decomposizione di rango r
- Probabilmente cambiare la notazione X(i1, ..., in) per i tensori con un
  subscript, in quanto è less chunky
- Aggiungere esempi per i modes
- Fatto interessante: il rango e il border rank nel caso 2x2 è 7. In aggiunta, 7
  è il minimo numero possibile di moltiplicazioni tra matrici per il caso 2x2.
- vedi: M. Landsberg, The border rank of the multiplication of 2 × 2 matrices is
  seven, J. Amer. Math. Soc., 19 (2005), pp. 447–45
- Kroneker perfect shuffle
- Problema della definizione di rango. Vedi sec 2.4 Hackbush, c'è una
  definizione un pelo più pulita.
- Implementazione Strassen/lab 1
- Proprietà subito dopo prodotto esterno
-

# Implementazione

CUTLASS Dgem in cuda con decomposizioni CP lowrank Oppure stessa cosa con MPI
gdem su cluster (in rust?).

MPI dgem (slides cineca)

Scalapack

ḾPI.jl

# Sketch

Structure:

La fattorizzazione CP:

- Calcolo tensoriale:
  - definizioni, prodotto dei modi
  - operazioni
- Rango CP e il problema del border rank
- Cenni sul calcolo CP

Fast matrix multiplication

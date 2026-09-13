#import "../lib.typ": *


= Applicazione alla complessità aritmetica

#definition[][
  Un *algoritmo di moltiplicazione veloce* è un algoritmo che usa asintoticamente un numero di
  moltiplicazioni rispetto alle addizioni.
]

#definition(title: [Moltiplicazione matriciale])[
  Fissati degli interi positivi $m, n, p$, la moltiplicazione tra due matrici $m times n$ e $n times p$ è una mappa bilineare
  $
  algob(m, n, p) : bb(C)^(m times n) times bb(C)^(n times p) &-> bb(C)^(m times p) \
  (A, B) &|-> C = A B.
  $
  Spesso ci riferiremo a $algob(m, n, p)$ chiamandolo "algoritmo", ad esempio nel contesto degli algoritmi di moltiplicazione veloce.
]


== Domanda:

Possiamo descrivere un algoritmo di moltiplicazione con un tensore e sperare di ridurre la
complessità aritmetica?

(risposta sì)

== Rappresentazione low-rank di forme bilineari

Data una decomposizione $ T = sum_(r=1)^R a_r topp b_r topp c_r $

Possiamo scrivere una forma bilineare $phi : U times V arrow.r W$ come $ phi(u,v) = sum_(r=1)^R
f_r (u)g_r (v) c_r, $
dove $f_r (u) = a_r^top u$ e $g_r (v) = b_r^top v$ sono dei funzionali.

== Bilinear computation

Forse prima?
#definition[Bilinear computation][
  Qui definizione
]

== Rappresentazione low-rank del prodotto matriciale

Date due matrici $A in RR^(m times n)$ e $B in RR^(n times p)$, poste $u = vec(A)$, $v = vec(B)$
abbiamo un algoritmo di moltiplicazione veloce a partire da una bilinear computation
$
vec(C^top) = phi(u,v) &= sum_(r=1)^R (f_r (u) dot g_r (v)) c_r \
&= sum_(r=1)^R (a_r^top u dot b_r^top v) c_r,
$
dove $dot$ denota le active multiplications.

== Il rango

So far:
$
rk(phi) &= #text["Lunghezza di una bilinear computation"] \
&= #text["Rango del tensore associato"].
$

Vorremmo mostrare che
$
rk(phi) &= #text["Numero di moltiplicazioni matriciali"].
$

Spoiler: equazioni -> biliner comp -> tensore

#pagebreak()

== L'esponente

#definition[
  L'*esponente della moltiplicazione matriciale* è il numero
  $
  omega := inf_n { tau in RR | &#text[La moltiplicazione tra due matrici in ] RR^(n times n) \ &#text[ha costo] o(n^tau)}.
  $
]
#speaker-note[Se avanza spazio/tempo notazione più precisa]

=== Stime note su $omega$

#align(center)[
  #image("../figures/matrix_multiplication_timeline_slides.pdf", width: 90%)
]

== L'algoritmo classico

$
mat(a_11, a_12; a_21, a_22, delim: "[")
mat(b_11, b_12; b_21, b_22, delim: "[")
& = mat(a_11b_11 + a_12b_21, a_11b_12 + a_12b_22; a_21b_11 + a_22 b_21, a_21b_12 + a_22b_22, delim:
"[") \
& = mat(f_1 g_1 + f_2 g_2, f_3 g_3 + f_4 g_4; f_5 g_5 + f_6 g_6, f_7 g_7 + f_8 g_8, delim: "[") \
& = mat(m_1 + m_2, m_3 + m_4; m_5 + m_6, m_7 + m_8, delim: "[") \
& = mat(c_11, c_12; c_21, c_22, delim: "[")
$
#speaker-note[Qui add animations]

Fissata la base standard $E_11, E_12, E_21, E_22$ dello spazio delle matrici $2 times 2$, possiamo
scrivere la bilinear computation
$
C = &c_11 E_11 + c_12 E_12 + c_21 E_21 + c_22 E_22 \
= &(m_1 + m_2)E_11 + (m_3 + m_4)E_12 \
+ &(m_5 + m_6)E_21 + (m_7 + m_8)E_22 \
= &sum_(r = 1)^8 m_r w_r.
$

L'algoritmo corrisponde al tensore
$
algob(2) &= (a_11 topp b_11 + a_12 topp b_21) topp c_11 \
&+ (a_21 topp b_11 + a_22 topp b_21) topp c_21 \
&+ (a_11 topp b_12 + a_12 topp b_22) topp c_12 \
&+ (a_21 topp b_12 + a_22 topp b_22) topp c_22.
$

== L'algoritmo di Strassen

Facendo alcune semplificazioni del risultato del prodotto matriciale, troviamo l'algoritmo di
Strassen in forma tensoriale

QUI

#pagebreak()

Due domande:

Come calcolare la complessità quando si usano i due algoritmi ricorsivamente?

Come ridurre il rango migliora la complessità?


== Stimare la complessità nel caso generale

QUI ALBERO?

Date due matrici di taglia $2^i times 2^i$ possiamo fare $i$ livelli di ricorsione e ottenere che
$ rk(algob(2^i)) = rk(algob(2)^(topp i)) <= rk(algob(2))^i <= r^i. $

Nel caso generale, dato $n>2$, possiamo fare un padding di zeri

$
pavemat(
  delim: "[",
  [
    a_11 & a_12 & & b_1 \
    a_21 & a_22 &             & b_2 \
    c_1  & c_2  &             & d
  ]
)
$

#proposition[
  Se $rk(algob(n)) <= r$ per degli interi positivi $n, r$, allora $r^(omega) <= r$.
]

== Il teorema di Strassen

Abbiamo dimostrato che $omega <= log_n rk(algob(n)),$ dunque
$
omega <= inf_n log_n rk(algob(n)).
$
Vorremmo che
$
omega = liminf_(n -> +oo) log_n rk(algob(n)).
$




== Algoritmi approssimati

bini et al provano...

tensore che trovano

=== Cenni sull'errore

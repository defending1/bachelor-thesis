#import "../lib.typ": *
#import "../figures/algorithm_to_tensor_flow.typ": algorithm-tensor-flow-fig


= Applicazione alla complessità aritmetica

#definition[][
  Un *algoritmo di moltiplicazione veloce* è un algoritmo che usa asintoticamente un numero minore di moltiplicazioni rispetto alle addizioni.
]

#definition(title: [Moltiplicazione matriciale])[
  Fissati degli interi positivi $m, n, p$, *la moltiplicazione tra due matrici* $m times n$ e $n times p$ è una mappa bilineare
  $
  algob(m, n, p) : bb(C)^(m times n) times bb(C)^(n times p) &-> bb(C)^(m times p) \
  (A, B) &|-> C = A B.
  $
  Spesso ci riferiremo a $algob(m, n, p)$ chiamandolo "algoritmo".
]


== Idea:

Possiamo descrivere un algoritmo di moltiplicazione con un tensore e sperare di ridurre la
complessità aritmetica.

#v(0.3em)
#align(center)[
  #algorithm-tensor-flow-fig
]


== Bilinear computation

Data una mappa bilineare $phi : U times V -> W$, per ogni $r = 1, ..., R$ siano $f_r in U^*, g_r in
V^*, w_r in W$ tali che
$
phi(u,v) = sum_(r = 1)^R f_r (u) g_r (v) w_r,
$
per ogni $u in U, v in V$.

La $r$-upla $(f_1,g_1,w_1, dots, f_r,g_r,w_r)$ è detta *bilinear computation*.
#pause La lunghezza di una bilinear computation è detta *bilinear complexity (o rango)* di $phi$, e si indica
con $rk(phi)$.
== Rappresentazione low-rank di forme bilineari

#proposition[][
  Data una decomposizione $ T = sum_(r=1)^R a_r topp b_r topp c_r $

  Possiamo scrivere una forma bilineare $phi : U times V arrow.r W$ come una bilinear computation
  della forma $ phi(u,v) = sum_(r=1)^R
  (a_r^top u) (b_r^top v)c_r. $
]

== Rappresentazione low-rank del prodotto matriciale


Date due matrici $A in RR^(m times n)$ e $B in RR^(n times p)$, poste $u = vec(A)$, $v = vec(B)$
abbiamo un algoritmo di moltiplicazione veloce a partire da una bilinear computation
$
vec(C^top) = phi(u,v)
&= sum_(r=1)^R markub((a_r^top vec(A)), #red, #<left>, bracket: brace.b) mark(dot, #<dot>, #green)
markub((b_r^top vec(B)), #blue,
#<right>, bracket: brace.b) c_r,
#annot(<dot>, pos: bottom, dy: +2.5em, leader-connect: "elbow")[Active multiplications]
#annot(<left>)[$f_r$]
#annot(<right>)[$g_r$]
$

\
\
Conseguenza: $rk(algob(n,m,p)) = "\"Numero di moltiplicazioni matriciali\"."$

== Il rango (cambiare)

Vorremmo tenere traccia della complessità ogni volta che troviamo una decomposizione di $algob(n)$ di
rango minore al variare di $n$.

#pagebreak()

== L'esponente

#definition[
  Un *circuito aritmetico* $Gamma$ è un grafo diretto, orientato, aciclico, finito, formato dai
  seguenti vertici:
- *Inputs:* Vertici di grado entrante $0$ con etichette in $KK union {x_1, dots, x_n}$.
- *Gates:* Vertici di grado entrante $2$ con etichette $+$ oppure $*$.
- *Output:* L'unico vertice di grado uscente $0$.
]
#pagebreak()
#definition[Funzione costo][
  Sia una mappa bilineare $phi : U times V -> W$, sia $Gamma$ un circuito aritmetico. La *funzione
  costo* associata a $Gamma$ è definita come
  $
  C_(Gamma)^("tot")(phi) &= "#moltiplicazioni e addizioni per calcolare" phi "su" Gamma.
  $
]
#definition[Complessità aritmetica][
  Fissato $cal(C)_phi = {"circuiti" Gamma' "che calcolano" phi}$,
  definiamo
  $
  L^("tot")(phi) &= inf_(Gamma in cal(C)_phi) C_(Gamma)(phi), quad #text[la *complessità totale* di]
  phi.
  $
]
#definition[
  Denotiamo il *numero di moltiplicazioni aritmetiche* necessarie a calcolare $algob(n)$ con
  $
  M_(KK)(n) = L^("tot")(algob(n))
  $
]

#definition[
  L'*esponente della moltiplicazione matriciale* è il numero
  $
  omega &:= inf_n { tau in RR | #text[La moltiplicazione tra due matrici in ] RR^(n times n) \
  &wide wide wide med #text[ha costo] o(n^tau).} \
  &= inf_(n) {tau in RR | M_(KK)(n) = o(n^tau).}
  $
]
#remark[$omega <= 3$]
#conjecture[$omega = 2$]

== Stime note su $omega$

#align(center + horizon)[
  #image("../figures/matrix_multiplication_timeline_slides.pdf", width: 100%, height: 92%, fit: "contain")
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
$
algob(2) & = (a_(11) + a_(22)) topp (b_(11) + b_(22)) topp (c_(11) + c_(22)) \
& + (a_(21) + a_(22)) topp b_(11) topp (c_(21) - c_(22))            \
& + a_(11) topp (b_(12) - b_(22)) topp (c_(12) + c_(22))            \
& + a_(22) topp (-b_(11) + b_(21)) topp (c_(21) + c_(11))           \
& + (a_(11) + a_(12)) topp b_(22) topp (-c_(11) + c_(12))           \
& + (-a_(11) + a_(21)) topp (b_(11) + b_(12)) topp c_(22)           \
&+ (a_(12) - a_(22)) topp (b_(21) + b_(22)) topp c_(11).
$
Che mostra $rk(algob(2)) =7$.


== Approccio divide et impera

La formula
$
vec(C^top) = sum_(r=1)^R (a_r^top vec(A))mark(dot, #red)
(b_r^top vec(B)) c_r,
$
si può utilizzare in maniera ricorsiva.

Idea: Si applica la formula ricorsivamente su $mark(dot, #red)$ fino al caso base.


Due domande:

Costo computazionale della ricorsione?

Come ridurre il rango migliora $omega$?


== Stimare la complessità nel caso generale

Date due matrici di taglia $2^i times 2^i$ possiamo fare $i$ livelli di ricorsione e ottenere che
$ rk(algob(2^i)) = rk(algob(2)^(topp i)) <= rk(algob(2))^i <= r^i. $

Nel caso generale, dato $n>2$, possiamo fare un padding di zeri
$
mat(
  A, display(mat(delim: #none, 0;0;0));
  display(mat(delim: #none, 0, 0, 0)), 0
  , delim: "["
) quad
mat(
  B, display(mat(delim: #none, 0;0;0));
  display(mat(delim: #none, 0, 0, 0)), 0
  , delim: "["
)
$

fino a raggiungere la taglia $2^(ceil(log_2 n))$.

La complessità sarà comunque limitata da $R$:
$
rk(algob(n)) &<= rk(algob(2^(ceil(log_2 n))))  \
&<= rk(algob(2))^(ceil(log_2 n)) \
&<= R^(ceil(log_2 n)) \
&<= R dot n^(log_2 R)
$
Da cui (sostituendo $2$ con $hat(n)$)

#proposition[
  Se $rk(algob(hat(n))) <= R$ per degli interi positivi $n, R$, allora $omega <= log_(hat(n))
  rk(algob(hat(n))).$
]<prop-omega-bound>

Da cui,
$
omega <= inf_n log_n rk(algob(n)).
$

=== Applicazione all'algoritmo di Strassen

Dalla @prop-omega-bound troviamo
$
omega <= log_2 rk(algob(2)) = log_2 7 approx 2.81.
$
Che è il bound più basso per $omega$ ottenibile da $algob(2)$.


== Il teorema di Strassen

Vorremmo che
$
omega = liminf_(n -> +oo) log_n rk(algob(n)).
$

#theorem[Strassen @strassen69 @burgisser2013algebraic][
  $
  omega = inf_n { tau in RR | rk(algob(n)) = O(n^tau)}.
  $
  Ovvero, moltiplicare due matrici $n times n$ costa $O(n^(omega + epsilon))$ operazioni
  aritmetiche se e solo se $rk(algob(n)) = O(n^(omega + epsilon)).$
]<thm-strassen>

== Algoritmi approssimati

Bini et al.CITE partendo dall'algoritmo classico $algob(2)$ e ponendo l'entrata $a_22 = 0$,
$
mat(a_11, a_12; a_21, 0, delim: "[")
mat(b_11, b_12; b_21, b_22, delim: "[")
& = mat(a_11b_11 + a_12b_21, a_11b_12 + a_12b_22; a_21b_11 , a_21b_12, delim:
"["). \
$

Trovano il tensore di rango $6$
$
algob(2)^(#text[red])
:= &a_(11) topp (b_(11) topp c_(11) + b_(12) topp c_(12)) \
+ &a_(12) topp (b_(21) topp c_(11) + b_(22) topp c_(12))      \
+ &a_(21) topp (b_(11) topp c_(21) + b_(12)
topp c_(22)).
$
Nel tentativo di ridurre numericamente il rango a $5$, trovano un tensore
$
algob(2)^("red")_t = &(a_(12) + t a_(11)) topp (b_(12) + t b_(22) topp c_(12))                                   \
+ &(a_(21) + t a_(11)) topp b_(11) topp (c_(11) + t c_(21))                                   \
+ &a_(12) topp b_(12) topp ((c_(11) + c_(12)) + t c_(22))                                    \
+ &a_(21) topp ((b_(11) + b_(12)) + t b_(21)) topp c_(11)                                    \
+ &(a_(12) + a_(21)) topp (b_(12) + t b_(21)) topp (c_(11) + t c_(22))
$

Scoprendo (accidentalmente) che
$
lim_(t -> 0) algob(2)^("red")_t = algob(2)^(#text[red])
$
Ovvero
$
brk(algob(2)^("red")) <= 5
$
Da cui ricavano l'algoritmo $algob(3,2,2)$ di complessità $3 log_12 10 approx 2.7799$.

== Confronto numerico

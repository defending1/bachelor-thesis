#import "../lib.typ": *
#import "../figures/algorithm_to_tensor_flow.typ": algorithm-tensor-flow-fig


= Applicazione alla complessità aritmetica

#definition[][
  Un *algoritmo di moltiplicazione veloce* è un algoritmo che usa asintoticamente un numero minore di moltiplicazioni rispetto alle addizioni.
]

#pause
#remark(title: [Moltiplicazione matriciale])[
  La moltiplicazione tra due matrici $m times n$ e $n times p$ è una mappa bilineare
  $
  algob(m, n, p) : bb(R)^(m times n) times bb(R)^(n times p) &-> bb(R)^(m times p) \
  (A, B) &|-> C = A B.
  $
]
#pause
Possiamo vedere $algob(m,n,p)$ come un tensore $m n times n p times m p$.

== Idea:


#v(3em)
#align(center)[
  #algorithm-tensor-flow-fig
]


== Rappresentazione low-rank del prodotto matriciale

#definition[][
  Date due matrici $A in RR^(m times n)$ e $B in RR^(n times p)$, consideriamo $u = vec(A)$, $v = vec(B)$.
  Definiamo la *rappresentazione low-rank* di $algob(m,n,p)$ come
  $
  vec(C^top)
  &= sum_(r=1)^R markub((a_r^top vec(A)), #red, #<left>, bracket: brace.b) mark(dot, #<dot>, #green)
  markub((b_r^top vec(B)), #blue,
  #<right>, bracket: brace.b) c_r,
  #annot(<dot>, pos: bottom, dy: +2.5em, leader-connect: "elbow")[Active multiplications]
  #annot(<left>)[$f_r$]
  #annot(<right>)[$g_r$]
  $
]

\
\
#pause
Conseguenza: $ rk(algob(n,m,p)) = "\"Numero di moltiplicazioni matriciali\"." $



#pagebreak()

== L'esponente

#speaker-note[Idea: tenere traccia della complessità ogni volta che troviamo una decomposizione di $algob(n)$ di
rango minore al variare di $n$.]


#definition[
  Un *circuito aritmetico* $Gamma$ è un grafo diretto, orientato, aciclico, finito, formato dai
  seguenti vertici:
- *Inputs:* Vertici di grado entrante $0$ con etichette in $KK union {x_1, dots, x_n}$.
- *Gates:* Vertici di grado entrante $2$ con etichette $+$ oppure $*$.
- *Output:* Un unico vertice di grado uscente $0$.
]
#pagebreak()

#definition[Funzione costo][
  Sia $Gamma$ un circuito aritmetico. La *funzione
  costo* associata a $Gamma$ è definita come
  $
  C_(Gamma)^("tot")(algob(n)) = &"#moltiplicazioni e addizioni"\ &"per calcolare" algob(n) "su" Gamma.
  $
]
#pause
#definition[Complessità aritmetica][
  Sia $cal(C)_phi = {"circuiti" Gamma' "che calcolano" algob(n)}$.
  definiamo
  $
  M_(KK) (n) := inf_(Gamma in cal(C)_phi) C_(Gamma)(algob(n)), quad
  $
  il numero di operazione necessarie a calcolare $algob(n)$.
]

#pagebreak()
#definition[Esponente della matrix multiplication][
  $
  omega &:= inf_n { tau in RR | #text[La moltiplicazione tra due matrici in ] RR^(n times n) \
  &wide wide wide med #text[ha costo] o(n^tau).} \
  &= inf_(n) {tau in RR | M_(KK)(n) = o(n^tau).}
  $
]
#pause
#remark[
  $omega <= 3.$
]
#conjecture[$omega = 2.$]

#empty-slide[
  #align(center + horizon)[
    #image("../figures/matrix_multiplication_timeline_slides.pdf", width: 100%, height: 100%, fit: "contain")
  ]
]

== L'algoritmo classico

$
mat(a_11, a_12; a_21, a_22, delim: "[")
mat(b_11, b_12; b_21, b_22, delim: "[")
& = mat(a_11b_11 + a_12b_21, a_11b_12 + a_12b_22; a_21b_11 + a_22 b_21, a_21b_12 + a_22b_22, delim:
"[") \
& = mat(c_11, c_12; c_21, c_22, delim: "[")
$
#speaker-note[Qui add animations]
#pause
L'algoritmo corrisponde al tensore
$
algob(2) = &(a_11 topp b_11 + a_12 topp b_21) topp c_11 \
+ &(a_21 topp b_11 + a_22 topp b_21) topp c_21 \
+ &(a_11 topp b_12 + a_12 topp b_22) topp c_12 \
+ &(a_21 topp b_12 + a_22 topp b_22) topp c_22.
$

== L'algoritmo di Strassen

Facendo alcune semplificazioni troviamo l'algoritmo di
Strassen in forma tensoriale
$
algob(2) = & (a_(11) + a_(22)) topp (b_(11) + b_(22)) topp (c_(11) + c_(22)) \
+&(a_(21) + a_(22)) topp b_(11) topp (c_(21) - c_(22))            \
+&a_(11) topp (b_(12) - b_(22)) topp (c_(12) + c_(22))            \
+&a_(22) topp (-b_(11) + b_(21)) topp (c_(21) + c_(11))           \
+&(a_(11) + a_(12)) topp b_(22) topp (-c_(11) + c_(12))           \
+&(-a_(11) + a_(21)) topp (b_(11) + b_(12)) topp c_(22)           \
+ &(a_(12) - a_(22)) topp (b_(21) + b_(22)) topp c_(11).
$
Che mostra $rk(algob(2)) =7$.


== Approccio divide et impera

L'algoritmo
$
vec(C^top) = sum_(r=1)^R (a_r^top vec(A))mark(dot, #red)
(b_r^top vec(B)) c_r,
$
è ricorsivo.

#speaker-note[Idea: Si applica la formula ricorsivamente su $mark(dot, #red)$ fino al caso base.]

#pagebreak()
=== Stima della complessità

Per il caso base $algob(2)$.

Input: matrici $2^i times 2^i$.
Facciamo $i$ livelli di ricorsione e troviamo
$ rk(algob(2^i)) <= R^i. $
#pause
Input: matrici $n times n$ con $n>2$. Possiamo fare un padding di zeri
$
markub(
  mat(
    A, display(mat(delim: #none, 0;0;0));
    display(mat(delim: #none, 0, 0, 0)), 0
    , delim: "["
  )
  , #black, #<left>, bracket: brace.b
)
quad
markub(
  mat(
    B, display(mat(delim: #none, 0;0;0));
    display(mat(delim: #none, 0, 0, 0)), 0
    , delim: "["
  ), #black, #<right>, bracket: brace.b
)
#annot(<left>)[$2^(ceil(log_2 n))$]
#annot(<right>)[$2^(ceil(log_2 n))$]
$

#pagebreak()
La complessità sarà comunque limitata da $R$:
$
rk(algob(n)) <= R dot n^(log_2 R)
$
Da cui (sostituendo $2$ con $hat(n)$)

#proposition[
  Se $rk(algob(hat(n))) <= R$ per degli interi positivi $n, R$, allora $omega <= log_(hat(n))
  R.$
]<prop-omega-bound>
#pause
Da cui,
$
omega <= inf_n log_n rk(algob(n)).
$
#pagebreak()
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

== Esperimento numerico

Bini et Al.@bini1979n2 trovano l'algoritmo $algob(3,2,2)$ di complessità $3 log_12 10 approx
2.7799$, che migliora $omega$.

#empty-slide[
  #align(center + horizon)[
    #image("../figures/bini_combined_4x3.pdf", width: 100%, height: 100%, fit: "contain")
  ]
]



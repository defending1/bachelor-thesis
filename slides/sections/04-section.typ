#import "../lib.typ": *
#import "../figures/algorithm_to_tensor_flow.typ": algorithm-tensor-flow-fig


= Applicazione alla complessità aritmetica

#definition[][
  Un *algoritmo di moltiplicazione veloce* è un algoritmo che usa asintoticamente un numero minore di moltiplicazioni rispetto alle addizioni.
]

#pause
#remark[
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
  &= sum_(r=1)^R (a_r^top vec(A)) mark(dot, #<dot>, #green)
  (b_r^top vec(B)) c_r,
  #annot(<dot>, pos: bottom, dy: +2.5em, leader-connect: "elbow")[Active multiplications]
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

#definition[Esponente della matrix multiplication][
  $
  omega &:= inf_n { tau in RR | #text[La moltiplicazione tra due matrici in ] RR^(n times n) \
  &wide wide wide med #text[ha costo] o(n^tau).}
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

== Approccio divide et impera

L'algoritmo
$
vec(C^top) = sum_(r=1)^R (a_r^top vec(A))mark(dot, #red)
(b_r^top vec(B)) c_r,
$
è ricorsivo.

#speaker-note[Idea: Si applica la formula ricorsivamente su $mark(dot, #red)$ fino al caso base.]

#pagebreak()
=== Stima della complessità ricorsiva con caso base $algob(2)$.

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

#theorem[Strassen @strassen69 @burgisser2013algebraic][
  $
  omega = liminf_(n -> +oo) log_n rk(algob(n)).
  $
  Ovvero, moltiplicare due matrici $n times n$ costa $O(n^(omega + epsilon))$ operazioni
  aritmetiche se e solo se $rk(algob(n)) = O(n^(omega + epsilon)).$
]<thm-strassen>



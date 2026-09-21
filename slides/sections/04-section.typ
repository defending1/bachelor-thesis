#import "../lib.typ": *
#import "../figures/algorithm_to_tensor_flow.typ": algorithm-tensor-flow-fig


= Applicazione: complessità del prodotto tra matrici

#definition[][
  Un *algoritmo di moltiplicazione veloce* è un algoritmo che usa asintoticamente un numero minore
  di operazioni rispetto all'algoritmo standard.
]

#pause
#remark[
  La moltiplicazione tra due matrici $n times n$ è una mappa bilineare
  $
  algob(n) : bb(R)^(n times n) times bb(R)^(n times n) &-> bb(R)^(n times n) \
  (A, B) &|-> C = A B.
  $
]
#pause
Possiamo vedere $algob(n)$ come un tensore $n^2 times n^2 times n^2$.

== Idea:


#v(3em)
#align(center)[
  #algorithm-tensor-flow-fig
]


== Rappresentazione low-rank del prodotto matriciale

#definition[][
  Date due matrici $A in RR^(n times n)$ e $B in RR^(n times n)$, consideriamo $vec(A)$, $vec(B)$.
  Definiamo la *rappresentazione low-rank* di $algob(n) = cp(U,V,W)$ come
  $
  vec(C^top)
  &= sum_(r=1)^R (u_r^top vec(A)) mark(dot, #<dot>, #green)
  (v_r^top vec(B)) w_r,
  #annot(<dot>, pos: bottom, dy: +2.5em, leader-connect: "elbow")[Active multiplications]
  $
]

\
\
#pause
Conseguenza: $ rk(algob(n)) = "\"Numero di moltiplicazioni matriciali\"." $



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
  $2 <=omega <= 3.$
]
#pause
#conjecture[$omega = 2.$]

#empty-slide[
  #align(center + horizon)[
    #image("../figures/matrix_multiplication_timeline_slides.pdf", width: 100%, height: 100%, fit: "contain")
  ]
]

== Come stimare $omega$?

#proposition[
  Se $rk(algob(n)) <= R$ per degli interi positivi $n, R$, allora $omega <= log_(n)
  R.$
]<prop-omega-bound>
#pause
Da cui,
$
omega <= inf_n log_n rk(algob(n)).
$
#pagebreak()

#example[
  $
  omega <= log_2 rk(algob(2)) = log_2 7 approx 2.81.
  $
  Che è il bound più basso per $omega$ ottenibile da $algob(2)$.
]

== Una stima accurata su $omega$

#theorem[Strassen @strassen69 @burgisser2013algebraic][
  $
  omega = liminf_(n -> +oo) log_n rk(algob(n)).
  $
  Ovvero, moltiplicare due matrici $n times n$ costa $O(n^(omega + epsilon))$ operazioni
  aritmetiche se e solo se $rk(algob(n)) = O(n^(omega + epsilon)).$
]<thm-strassen>



#import "../lib.typ": *


== La fattorizzazione CP

#definition[Tensore di rango uno e Decomposizione CP][
- Un tensore $T in bb(R)^(n_1 times dots times n_d)$ si dice di *rango uno* se si scrive come $T = a^((1)) topp a^((2)) topp dots topp a^((d))$.
- Una *Decomposizione CP* (Canonical Polyadic Decomposition) rappresenta $T$ come somma di $r$ tensori di rango uno:
$ T = sum_(j=1)^r a_j^((1)) topp a_j^((2)) topp dots topp a_j^((d)) = lr([| A_1, A_2, dots, A_d |]) $
dove $A_k = [a_1^((k)) | a_2^((k)) | dots | a_r^((k))] in bb(R)^(n_k times r)$ sono le *factor matrices*.
]

= Il problema del rango
In questa parte vediamo molte peculiarità dei tensori, dove "smonto" quello che
funziona per le matrici ma non per i tensori

== Rango CP

#definition[Rango Tensoriale][
  Il *rango* di un tensore $T$ (denotato con $rk(T)$) è il minimo intero positivo $r$ tale che $T$ ammette una decomposizione CP di rango $r$:
  $ rk(T) = min { r in bb(N) | T = sum_(j=1)^r a_j^((1)) topp a_j^((2)) topp dots topp a_j^((d)) } $
]

== Proprietà del Rango Tensoriale

#def-box(title: "Peculiarità del Rango Tensoriale")[
  Rispetto al rango matriciale classico:
- *Complessità*: Il calcolo del rango tensoriale è NP-hard (Håstad, 1990).
- *Rango Massimo*: Per tensori $n_1 times dots times n_d$ può superare $\min(n_i)$ (es. per $2 times 2 times 2$ il rango max è 3).
]

== Border rank

Split come due slides, contenuto al centro in grande
#property[
  Una successione di matrici di rango $ r$ tende a una matrice di rango $<= r$.
]

#pagebreak(weak: true)

#todo[illustration brank]

#property[
  Una successione di tensori di rango $r$ può tendere a un tensore di rango $> r$.
]

#example[][
  Tensore di rango $2$ che tende a uno di rango $3$.
]

== Rango tipico

Una matrice $M$ ha rango massimo con probabilità $1$, i tensori possono avere più ranghi per un certo formato.




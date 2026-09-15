// Notazione tensoriale e operatori per Typst slides

#let rk(T) = $bold(R)(#T)$
#let rank = math.op("rank")
#let brk(T) = $underline(bold(R))(#T)$

#let multirk = math.op("multirk")
#let krank(A) = $bold(k)_#A$
#let proj(n, K) = $bb(P)^#n (#K)$
#let vec = math.op("vec")
#let algob(..args) = {
  let pos = args.pos()
  if pos.len() == 1 {
    let n = pos.at(0)
    $lr(chevron.l #n, #n, #n chevron.r)$
  } else {
    $lr(chevron.l #pos.join([, ]) chevron.r)$
  }
}

#let ango(W) = $chevron.l #W chevron.r$

#let SS = $cal(S)$

// Operatori principali (con spaziatura binaria corretta)
#let topp = math.class("binary", "\u{2297}") // Prodotto tensore / esterno (⊗)
#let krn = math.class("binary", "\u{22a0}")  // Prodotto di Kronecker (⊠)
#let krp = math.class("binary", "\u{2299}")  // Prodotto Khatri-Rao (⊙)
#let had = math.class("binary", sym.ast)     // Prodotto di Hadamard (*)
#let ttm(k) = $times_#k$                      // Prodotto mode-k (×_k)

// Formattazione tensori e matricizzazioni
#let unf(T, k) = $bold(#T)_((#k))$
#let cp(..args) = $lr([| #args.pos().join(", ") |])$

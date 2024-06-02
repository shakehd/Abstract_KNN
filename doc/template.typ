#import "@preview/ctheorems:1.1.2": *




// The project function defines how your document looks.
// It takes your content and some metadata and formats it.
// Go ahead and customize it to your liking!
#let project(title: "", authors: (), body) = {
  // Set the document's basic properties.
  set document(author: authors, title: title)
  set page(numbering: "1",
           number-align: center,
           paper: "a4")
  set text(
    font: "New Computer Modern",
    size: 11pt,
    lang: "en"
  )
  set heading(numbering: "1.1")
  set terms(hanging-indent: 0pt)
  show bibliography: set heading(numbering: none)
  set math.equation(supplement: [Eq.])

  show: thmrules.with(qed-symbol: $square$)
  show list: it => [#pad(left: 15pt, it)]
  show enum: it => [#pad(left: 15pt, it)]
  show math.equation: set text(weight: 400)
  show heading: it =>  if it.numbering != none {
    set  text(size: 1em)
    counter(heading).display() + [ ] + it.body
    linebreak()
  } else {
    it.body
  }

  show "P(x)": _ => [$sans(P)^(epsilon)(x)$]
  show "GKNN": _ => $"XXYYZZ"$
  show "AGKNN": _ => $"XXYYZZ"^A$
  show "AGKNN2": _ => $"XXYYZZ2"^A$
  // show "GKNN": _ => $"G-"k"NN"$

  show figure.caption.where(
    kind: "Algorithm"
  ): it => [
    #align(
      alignment.left,
      rect(
        width: 100%,
        stroke: (top: 1pt + black, bottom: 1pt + black),
        [ #strong([#it.supplement #it.counter.display(it.numbering):])
        #it.body]
      )
    )
  ]
  // Title row.
  align(center)[
    #block(text(weight: 700, 2em, title))
  ]

  linebreak();

  // Main body.
  set par(
    justify: true,
    leading: 0.52em,
  )

  body
}

#let pert(point) = [$sans(P)^(epsilon)(#point)$]

#let pre(x1, x2, x: [x]) = [$#x1 attach(prec.eq, br: #x) #x2$]
#let npre(x1, x2, x: [x]) = [$#x1 attach(prec.eq.not, br: #x) #x2$]

#let apre(x1, x2, x: [x]) = [
  $#x1 attach(prec.eq, tr: sscript(A), br:#x) #x2$]
#let napre(x1, x2, x: [x]) = [
  $#x1 attach(prec.eq.not, tr: sscript(A), br: #x) #x2$]


#let theorem = thmbox("theorem", "Theorem", inset: (left: 0em),
                      base_level: 1)
#let corollary = thmplain(
  "corollary",
  "Corollary",
  base: "theorem",
  titlefmt: strong
)
#let definition = thmbox("definition", "Definition",
                         inset: (left: 0em))

#let example = thmplain("example", "Example", inset: (left: 0em)).with(base_level: 1)
#let proof = thmproof("proof", "Proof", inset: (left: 0em))
#let prop = thmbox("prop", "Prop", base_level: 1, inset: (left: 0em))

#import "@preview/algo:0.3.3": algo, i, d, comment, code


#let algorithm(body,
               title: "",
               output: (),
               input: (),
               position: auto,
               text-style: ()) = {

  let header = if input.len() > 0 [
    #stack(
      dir: ltr,
      spacing: 5pt,
      [*Input*],
      grid(
        columns: 2,
        gutter: 5pt,
        ..input
      )
    )
  ]

  if output.len() > 0 {
    header += [
      #stack(
        dir: ltr,
        spacing: 5pt,
        [*Output*],
        grid(
          columns: 2,
          gutter: 5pt,
          ..output
        ),
      )
      // #linebreak()
    ]
  }


  figure(
    block(
      width: 100%,
      fill: none,
      radius: 2.5pt
      )[
        #rect(stroke: (bottom: 1pt + black), width: 100%)[
          #algo(
            header: pad(left: 15pt, header),
            indent-guides: 1pt + gray,
            radius: 2.5pt,
            stroke: none,
            fill: none,
            block-align: left,
            indent-size: 10pt,
            main-text-styles: text-style,
            breakable: true,
            comment-prefix: [#sym.triangle.stroked.r ],
            comment-styles: (fill: rgb(100%, 0%, 0%))
          )[#body]
        ]
      ],
      caption: figure.caption(
        position: top,
        [#title]
      ),
      kind: "Algorithm",
      supplement: [Algorithm],
      placement: position,
      gap: 0em
  )
}

#let var(name) = $mono(#name)$
#let func(name, ..params) = {

  let inputs = params
                 .pos()
                 .join(", ")

  [#text(weight: "semibold",
         font: "DejaVu Sans Mono",
         size: 0.9em)[#name]$(inputs)$]
}
#let line(..lines) = {
  let line_num = lines.pos()
  if line_num.len() == 2 [
    line #line_num.at(0)-#line_num.at(1)
    // line $mono([#line_num.at(0)-#line_num.at(1)])$
  ] else [
    line #line_num.at(0)
    // line $mono([#line_num.at(0)])$
  ]
}

#let setv(var) = {$mono("set")(var)$}
#let reqv(var) = {$mono("req")(var)$}
#let lenv(var) = {$mono("len")(var)$}
#let predv(var) = {$mono("pred")(var)$}
#let samedistv(var) = {$mono("same_dist")(var)$}

#let setp(var) = {$mono("set")^(star)(var)$}
#let reqp(var) = {$mono("req")^(star)(var)$}
#let lenp(var) = {$mono("len")^(star)(var)$}
#let sign(content) = {$op(italic("sign"))(content)$}

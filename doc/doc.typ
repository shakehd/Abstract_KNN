#import "utils.typ": algorithm, var, func, setv, reqv, lenv, predv, setp, reqp, lenp, line, sign, samedistv
#import "template.typ": project, prop, proof, definition, example,theorem, pert, pre, apre, npre, napre
#import "@preview/algo:0.3.3": i, d, comment, code, no-emph
#import "@preview/diagraph:0.2.1": *
#import "@preview/cetz:0.2.1"
#import "@preview/tablex:0.0.8": tablex, rowspanx, colspanx


#show: project.with(
  title: [Graph based $k$NN (GKNN)],
  authors: (
    "Shakeel",
  ),
)

#outline(
  title: [Contents],
  indent: 2em,
)

#pagebreak()

= Concrete algorithm

Given a set of labels $cal(L)$ and the dataset $S = {(bold(s)^(i),
bold(y)^(i)) | bold(s)^(i) in bb(R)^n, bold(y)^(i) in cal(L)}$ and the
input sample $bold(x) in bb(R)^n$, $"GKNN": bb(R)^n -> cal(P)(cal(L))$
is function that classify the input with the most frequent label
within the $k$ closest samples to the input like the $k$NN algorithm
but differs from it in the way those samples are found. Rather than
sort the samples in oder of their proximity to the input and then
select the first $k$ samples, GKNN use the relation of "being closer
to the input" between pair of samples w.r.t. the euclidean norm to
select the $k$ closest samples. The relation is defined as follow:

#definition([Relation $attach(prec.eq, br: bold(x))$])[Given the
points $bold(x), bold(s)_i, bold(s)_j in bb(R)^n$,
$
  bold(s)_i attach(prec.eq, br: bold(x)) bold(s)_j
  arrow.l.r.double.long ||bold(x) - bold(s)_i|| lt.eq
  ||bold(x) - bold(s)_j||
$
The subscript $bold(x)$ will be omitted when is clear from the
context.]

GKNN first build a "precedence" graph $bb(G)$ in which nodes
represents the samples in $S$ and edges model the relation
$attach(prec.eq, br: x)$ (i.e. the tail is closer to the input than
the head) and then classify the input with the most frequent labels
within the vertices composing the valid paths #footnote[The definition
of a valid is given later in @path-sec] of length $k-1$ starting from
the samples closest to the input.

== Precedence graph

Given the set of samples $S$ the precedence graph $bb(G)_bold(x) =
(V, E)$ is a graphical representation of the totally ordered set
$(S, attach(prec.eq, br: x))$>

- $V = S$
- $E = {(bold(s)_i, bold(s)_j) bar.v  bold(s)_i prec.eq bold(s)_j "is true"}$
where $||dot.op||_p$ is the minkowski norm.

The graph is implemented using adjacent lists so each vertex object
has a list of adjacent vertices. Moreover given a vertex $bold(s)$:

  - $predv(bold(s))$ denotes the set of vertices $bold(s)_i$
    such that there is an edge from $bold(s)_i$ to $bold(s)$ but not
    the other way around that is
    $
      (bold(s)_i, bold(s)) in E and (bold(s), bold(s)_i)  in.not E
    $

  - $samedistv(bold(s))$ represents the set of vertices
    $bold(s)_i$ such that there is a bidirectional edge between
    $bold(s)_i$ and $bold(s)$ that is
    $
      (bold(s)_i, bold(s))  in E and (bold(s), bold(s)_i) in E
    $

This means that
$
  forall bold(s)_j in predv(bold(s)) space bold(s)_j prec.eq bold(s)
  and bold(s) prec.eq.not bold(s)_j
$

This observation will be used for the generation of valid paths
based on how close the samples are to the input sample.

@create_precedence_graph shows how the precendence graph is created.
Given the sample dataset $S$ and the input sample $bold(x)$, it first
create the graph $bb(G)$ with only the vertices habing no adjacent
vertex. attributes set to the (line $mono("1")$). Then for each
unordered pair of samples $(bold(s)_i, bold(s)_j)$ the closer sample
to the input $bold(x)$ w.r t. the euclidean norm is determined and
update the adjacent lists of both vertices accordingly (line
$mono("2-12")$). Finally the created graph is returned
(line $mono("15")$).

#algorithm(
  title: [$mono("create_precedence_graph")$ method],
  output: ([$bb(G)_bold(x)$: precedence graph],),
  input: (
    [*$var(S)$*: samples dataset],
    [*$var(x)$*: the input sample]
  ))[
    $bb(G)_bold(x) <-$#func("initialize_graph", $var(S)$)\

    for $(s_i, s_j)$ in ${(s_i,s_j)| s_i,s_j in var(S), s_i eq.not s_j}$
    do#i\
      if $s_i prec.eq s_j$ and $s_j prec.eq s_i$ then#i\
        add $s_j$ to adjacent of $s_i$\
        add $s_i$ to adjacent of $s_j$#d\
      else if $s_i prec.eq s_j$ then#i\
        add $s_j$ to adjacent of of $s_i$\
      else#i\
        add $s_i$ to adjacent of of $s_j$\
      end#d\
    end\
    return $bb(G)_bold(x)$
  ]<create_precedence_graph>

#example[
Consider a dataset $S subset bb(R)^(2) times cal(L)$ composed by the
following samples

- $bold(a) = ((0,1), 1)$
- $bold(b) = ((2,0), -1)$
- $bold(c) = ((2.25,0), 1)$

and the input sample $bold(x) = (1, 1)$. In this setup the samples
$bold(a)$ and $bold(b)$ are equidistant from the input $bold(x)$ while
$bold(c)$ is the furthest one so we have the following precedence
graph:

#figure([#render("
  digraph {
    a -> b[color=red]
    b -> a[color=green]
    a -> c[color=green]
    b -> c[color=red]
    {rank=same a, b}
  }",
  labels: (:
    a: [*a*],
    b: [*b*],
    c: [*c*]
  )
)],
caption: "Example of precedence graph.")
]<example11>

== Paths generation<path-sec>

In order to have a sound classification the paths within the
precedence graph used to classify the input must satisfy all the
proximity relation among the samples that is if $bold(s)_i prec.eq
bold(s)_j$ but $bold(s)_j prec.eq.not bold(s)_i$ then every path in
which $bold(s)_j$ occurs must also contain $bold(s)_i$ and it must
precede $bold(s)_j$. This means that not all paths starting from the
closest sample can be used to classify the input. For example in the
graph of @example11 the path [$bold(b)$, $bold(c)$] is not a valid
because $bold(a) prec.eq bold(c)$ but $bold(c) prec.eq.not bold(a)$
so this means that in every valid path $bold(c)$ must be preceded by
$bold(a)$. This observation leads to the following definition fo a
valid path:

#definition("Valid path")[
A path $cal(P)$ in a precedence graph is _valid_ if and only if
$forall bold(s)_i in cal(P)$:
$
 forall bold(s)_j in predv(bold(s)_i) space bold(s)_j
 "is a predecessor of " bold(s)_i "in" cal(P)
$]<def-valid-path>

By this definition in the graph of @example11 only the edges
highlighted with the same color form valid paths which are:

- [$bold(b)$, $bold(a)$,$bold(c)$]
- [$bold(a)$, $bold(b)$,$bold(c)$]

#prop[Every valid path starts with a vertex $v_i$ such that the sample
$bold(s)_i$ is one of the closest sample to the input $bold(x)$]<prop00>
#proof[Follows directly from the definition of valid path.]

#prop[If a vertex $bold(s)$ do not occur in a valid path $cal(P)$ and
every vertex in $predv(bold(s))$ is in $cal(P)$ then the path
$cal(P) + [bold(s)]$ is still valid.]<prop11>
#proof[Follows directly from the definition of valid path.]

#definition("safe vertex")[Given the valid path $cal(P) =[bold(s)_0,
bold(s)_1,dots, bold(s)_m]$ the vertex $bold(s)$ is _safe_ for
$cal(P)$ if the path $cal(P) + [bold(s)]$ is a valid path.]

#prop[Valid paths of length $k-1$ starting from vertices $bold(s)_i$
such that $predv(bold(s)) = emptyset$ contains the $k$ closest samples
from the input.]<prop12>
#proof[Follows directly from the definitions of a path in a graph and
  valid paths.]

The generation of paths is done by traversing the graph in the same
fashion of the BFS algorithm while respecting the condition of a
valid path. @path_generation shows how paths are generated given the
the precedence graph $bb(G)_bold(x)$ and the desired length $n$ of the
path. The algorithm make use of a FIFO queue (the variable
$var("queue")$) to maintain the list of all valid paths of length less
than $k < n$. First it initialize the queue with the vertices
$bold(s)$ such that $predv(bold(s)) = emptyset$ (lines $mono("1-2")$)
which means the traversal starts from the samples closest to the input
$bold(x)$. A counter $k$ which denotes the length of the paths in the
queue is initialized with 0 (line $mono(3))$. Then until the queue is
not empty extracts all the paths present in the queue and check
whether their length is equal to desired length (i.e the input *n*)
and if this is the case the it simply returns the extracted paths
(lines $mono("6-7")$) otherwise iteratively extend each path with
every safe vertex within the adjacent of the path's last sample and
add the extended paths to the queue for the next iteration of the loop
(lines $mono("8-15"))$. Before the next loop the counter $k$ is also
incremented to reflect the length of the paths in the queue (line
$mono(16))$.

#prop[Given as input the the precedence graph $bb(G)_bold(x)$ and
$n in bb(N)$ @path_generation returns all the valid paths of length
#footnote[The convention used for path of length 0 is that it
contains only the starting vertex.] $n$ within $bb(G)_bold(x)$.]
<prop13>
#proof[
The proposition can be proved by showing, that at the $k$-th iteration
of the while loop at line 5 (ie. before the check on the length of the
paths on the queue), the queue contains all the valid path of length
$k-1$. We use induction on $k$ to prove this:

 - (*$k=1$*): In the first iteration of the loop the queue contains
   all the paths composed vertices $bold(s)$ such that $predv(bold(s))
   = emptyset$ which are of length 0 and surely are valid by
   definition.

- (*$k=h+1$*): At iteration $h + 1$, the paths inside the queue at
  line 5 are obtained by extending all the paths in the queue in the
  $h$-th iteration with every safe vertex among the adjacent of the
  path's last vertex. By induction hypothesis the queue in the $h$-th
  iteration contains all the valid paths of length $h-1$ and so in the
  $h+1$ iteration, by definition of safe vertex, the queue contains
  all the valid paths of length $h$.

This means when the method returns, at iteration $n$, the queue
contains all the possible valid path of length $n-1$.]

#algorithm(title: [$mono("generate_paths")$ method],
           output: ([Set of valid paths],),
           input: (
            [*$var(G_bold(x))$*: precedence graph,],
            [*var(n)*: length of the path]
           ))[
  $var("closest_samples") <- {[s_i] | s_i in var(G_bold(x)) and
  predv(s_i) = emptyset}$\
  $var("queue") <- func("create_queue", var("closest_samples"))$\
  $var("k") <- 0$\
  while #var("queue") not *empty* do#i\
    $var("current_paths") <- var("queue").func("popAll")$\

    if #var("k") = *n* then#i\
      return #var("current_paths")#d\

    for #var("current_path") in #var("current_paths") do#i\

      $var("last_vertex") <- var("current_path").mono("last")()$\

      for #var("adj") in $var("last_vertex").mono("adjacent")$ do#i\

        if $var("adj") bold("is safe") #no-emph("for")
           var("current_path")$
        then#i\
          $var("queue").func("append", var("current_path") +
           [var("adj")])$#d\
        end#d\
      end#d\
    end\
    $var("k") <- var("k") + 1$#d\
  end\
]<path_generation>

== GKNN algorithm

@gknn-algh shows the pseudocode of the algorithm. Given a set of
samples $S$ and the input sample $bold(x)$ the algorithm first build
the precedence graph $bb(G)_bold(x)$ (line $mono(1)$). Then the
$mono("generate_paths")$ method is used to find the valid paths
of length length $k-1$ within the graph (line $mono(2)$).
Afterwards the set containing the most frequent labels within the
samples composing each path is computed and returned as the possible
classifications of the input sample (line $mono("3-8")$).

Since there could be multiple valid paths in the graph due to
samples in $S$ equidistant to the input, the latter could be
classified with different labels hence the need to return a set of
labels rather than a single value.

#theorem[Given a dataset $S = {(bold(s)_(i), bold(y)_(i)) |
bold(s)_(i) in bb(R)^n, bold(y)_(i) in bb(R)}$ and the input sample
$bold(x)$, GKNN returns all the possible classifications of the input
$bold(x)$.]
#proof[
  GKNN compute the set of possible classification by finding the most
  frequent labels in the paths returned by the
  $mono("generate_paths")$ method which, by @prop12 and @prop13,
  returns all the possible $k$ closest samples to the input.
  Therefore GKNN surely returns all the possible classification of
  the input $bold(x)$.
]

#example[Consider the setup of @example11. Running GKNN with $k =
 3$ will return the singleton {1} because the most frequent label in
 all the valid path is exactly 1 meanwhile with $k=2$ the result is
 the set {1, -1} because there is a ties in both paths.
]

#algorithm(
  title: "GKNN algoritm",
  output: ([Set of possible classification of $x$],),
  input: (
    [*$var(x)$*: the input sample],
    [*$var(S)$*: samples dataset],
    [*$var(k)$*: number of neighbours],
  ))[

  $bb(G)_bold(x) <-$  #func("create_precedence_graph", $S$, $x$)\

  $var("paths") <-$ #func("generate_paths", $bb(G)_bold(x)$, $k-1$)\
  $var("classification") <- {}$\
  for #var("path") in #var("paths") do#i\
    $var("labels") <- "most frequent labels in "mono("path")$\
    $var("classification") <- var("labels") union
                              var("classification")$#d\
  end\
  return #var("classification")
]<gknn-algh>

= Graph construction optimization

One problem with GKNN is that it not really efficient because it
requires the iteration over all the pairs of samples for the
construction of the graph which in the worst case can be fully
connected. So the overall complexity of the algorithm is $O(n^2)$
where $n$ is number of samples in the dataset but hides an important
constant which is the dimension of the samples.

One way to optimize the construction of the graph is reduce the
number of samples used to create the graph since not all are needed
for the classification. One method to reduce the number of samples is
the following:

+ Partition the the dataset so that each partition contain at most a
  $m$ of samples where $k <= m << n$.
+ Find the partition $P$ containing the input $x$.
+ Compute the distance $r$ between $x$ and the $k$-th closest sample
  to $x$ in $P$.
+ Find the partitions $P S$ intersecting the hypersphere centered in
  $x$ and radius $r$.
+ Build the graph with the points in partitions $P S$ that are inside
  the hypershpere.

== Dataset partitioning

The dataset is partitioned with a binary space partition tree
(BSP-Tree) @BSPTree using random projection @RandProj like is done in
the ANNOY tool @Annoy. The main idea is to split the hyperspace along
a random hyperplane which will in turn split the dataset in two and
then recursively split again the two half spaces in the same manner
until the subspace can't be further halved because it contains the
minimum number of samples. With this procedure a BSP-Tree is built in
which leafs are the partitions of the space while the internal nodes
split the space according to the random hyperplane. @bsp-tree shows
how the BSP-Tree is constructed. Given the dataset $S$ and the minimum
size of a partition $m$, it first check whether the dataset has size
less than $m$ in which is case just return a tree made of a single
leaf initialized with the dataset (line $mono("1-3")$) otherwise split
the dataset with $mono("split_dataset")$ method which in addition to
the two datasets returns also the splitting hyperplane (line
$mono(4)$). Then builds the left and right BSP-Tree by calling itself
on the "left" and "right" dataset (line $mono("5-6")$) to then return
the node initialized with the splitting hyperplane and the subtrees
constructed before (line $mono(7)$).

#algorithm(title: [$mono("build_bsp_tree")$ method],
           input: ([*$var(S)$*: samples dataset,],
                   [*$var(m)$*: the minimum size of a partition]),
           output: ([BSP-Tree ],))[

  if $|var(S)| <= var(m)$ then#i\
   return #func("Leaf", $var(S)$)#d\
  end\

  $var("left_dataset"), var("right_dataset"), var("hyperplane") <-
          func("split_dataset", var(S))$\

  $var("left_tree")<- func("build_bsp_tree",var("left_dataset"), var(m))$\
  $var("right_tree")<- func("build_bsp_tree", var("right_dataset"),
                            var(m))$\

  return #func("Node", var("hyperplane"),  var("left_tree"),
               var("right_tree"))
]<bsp-tree>

=== Dataset split

One way to split dataset is for example to simply pick two random
sample and split the dataset using the perpendicular bisector of the
two samples. Another method is to use $k$-Means with $k=2$ which will
split the dataset in two and the splitting hyperplane would be the
perpendicular bisector of the two cluster centers. The problem with
both strategies is that they don't guarantee a balanced tree and
partitions with at least $k$ samples.

One method that ensures both requirements are satisfied is to first
split the dataset according to the perpendicular bisector of two
random points $p_1$ and $p_2$ and then move the splitting hyperplane
along the line joining the two points in the direction of the point
having the most closer samples until one half space contains at most
one sample more than the other. The method $mono("split_dataset")$
illustrated by @split-dataset does exactly this. Given the dataset
$S$ it starts  by sampling two random points $p_1$ and $p_2$ and then
split dataset according to their perpendicular bisector thus creating
the datasets $S_0$ and $S_1$ (line $mono("1-4")$). Suppose now _max_
and _min_ are the indices of dataset with most samples and the one
with fewer samples respectively. Then the algorithm calculate the
number of samples, denoted by $var("to_move")$, that need to be moved
from $S_max$ to $S_min$ so that the difference between their sizes is
almost 1 (line $mono("5-6")$). Afterwards moves $var("to_move")$
samples from $S_max$ to $S_min$ and each time translate the splitting
hyperplane along line joining the points $p_1$ and $p_2$ in the
direction of $p_max$ by the amount $d_s'$ which is the distance
between the samples being moved and the current hyperplane (line
$mono("7-15")$). Finally moves the the splitting hyperplane again in
the same direction as before by $d_s'/2$ where $d_s'$ is the distance
between the sample in $S_max$ closest to the splitting hyperplane and
then return the the two dataset and the hyperplane (line
$mono("16-19")$). The last translation of the hyperplane is done so
that so it split the samples as evenly as possible.

#algorithm(title: [$mono("split_dataset")$ method],
           input: ([*$S$*: samples dataset],),
           output: ([*$S_0$*: the left side dataset],
                    [*$S_1$*: the right side dataset],
                    [*$pi$*: the splitting hyperplane]))[

  $var(p_0), var(p_1) <- func("random_points", 2)$\

  $pi <-$ perpendicular bisector of $var(s_1)$ and $var(s_2)$\

  $S_0 <- {s | s in S,space pi(s) >= 0}$\
  $S_1 <- {s | s in S,space pi(s) < 0}$\

  $max, min  <- limits("argmax")_(i in {0, 1}) |S_i| ,
                limits("argmin")_(i in {0, 1}) |S_i|$\

  $var("to_move") <- round((|S_0| - |S_1|)/2)$\


  $var("moved") <- 0$\

  while $var("moved") eq.not var("to_move")$ do#i\
    $s' <- $ sample in $S_max$ closest to $pi$\
    $d_s' <-$ distance between $s'$ and $pi$\

    $S_min <- S_min union {s'}$\
    $S_max <- S_max without {s'}$\

     $pi <- func("translate", pi, d_s', arrow(p_min p_max))$\

    $var("moved") <- var("moved") + 1$#d\
  end\

  $s' <- $ sample in $S_max$ closest to $pi$\
  $d_s' <-$ distance between $s'$ and $pi$\

  $pi <- func("translate", pi, d_s'/2, arrow(p_min p_max))$\

  return ($S_max, S_min, pi$)

]<split-dataset>

== Finding partitions by point or hypersphere

Finding the partition to which a point belongs or the ones that
intersect a hypersphere can be done by traversing the BSP-Tree from
top to bottom until leaf nodes are not reached like in any binary
search tree. @tree-traversal shows how this search is executed. Given
a BSP-Tree and the input query which can be a point or a hypersphere,
it first initialize a queue, which contains the nodes that need to be
traversed, with the root of the tree (line $mono(1)$). Then until the
queue is not empty extracts a node from the queue and check whether is
a leaf in which case collect the dataset associated with the leaf
(line $mono("5-6")$) otherwise compute the next nodes to traverse by
calling the $mono("next_nodes")$ method and add this nodes to the
queue (line $mono("7-9")$). If the input is a point then
$mono("next_nodes")$ returns the subtree associated with the half
space in which the input resides by checking on which side of the
splitting hyperplane associated with the node the input is located
(if the point is exactly on the hyperplane then returns both
subtree). On the other hand if the input is a hypersphere then first
checks if the splitting hyperplane intersect the hypersphere in which
case returns both subtree otherwise return the subtree associated
with the half space where the hypersphere resides. At the end returns
the collected partitions which in the case of a point is the
partition in which the point is located while for a hypershpere are
the partitions that intersect with it (line $mono(12)$).

#algorithm(title: [$mono("query_partition")$ method],
           input: ([*$var("BSP-T")$*: the BSP-Tree, ],
                   [*$var(x)$*: the input query(point or hypershpere)]),
           output: ([Set of partitions],))[

  $var("queue") <- func("create_queue", {"BSP-T".italic("root")})$\
  $var("partitions") <- emptyset$\
  while #var("queue") is not *empty* do#i\
    $var("current_node") <- var("queue").func("pop")$\
    if #var("current_node") is *Leaf* then#i\
      $var("partitions") <- var("partitions") union
                            {var("current_node".func("dataset"))}$#d\
    else#i\
     $var("new_nodes") <- func("next_nodes", var("current_node"), x)$\
     $var("queue").func("append", var("new_nodes"))$#d\
    end#d\
  end\
  return #var("partitions")
]<tree-traversal>


#pagebreak()
= Abstract classifier

In the abstract case there is the same datasets $S = {(bold(s)_i,
bold(y)_i) | bold(s)_i in bb(R)^n, bold(y)_i in bb(R)}$ but the input
query is not a single point $bold(x) in bb(R)^n$ but instead is region
of space around the point $x$. This region of space, denoted with
$pert(bold(x))$, represents a (small) perturbation of the point
$bold(x)$ and is defined as the $ell_infinity$ ball centered in
$bold(x)$ and radius $epsilon$:

#block()[
  #set math.equation(numbering: "(1)")
  $
    pert(bold(x)) = {bold(x)' | bold(x)' in bb(R)^n and
    ||bold(x)'- bold(x)||_infinity <= epsilon}
  $<pert>
]

In this case the abstract classifier $"AGKNN":  cal(P)(bb(R)^n) ->
cal(P)(cal(L))$ is a function that takes as input a region of space
(i.e, $pert(x)$) and outputs a set of labels. The condition that the
abstract classifier must satisfy is that it has to be a _sound
abstraction_ of the concrete classifier over the perturbation of the
input $bold(x)$ which means the returned set of labels must contains
all the output of the concrete classifier on each point of region
that is
#block()[
  #set math.equation(numbering: "(1)")
  $
   "AGKNN"(R) supset.eq limits(union.big)_(bold(x)' in R) "GKNN"(x')
  $<output>
]

Computing $"AGKNN"(pert(bold(x)))$ by applying the concrete classifier
on each point of the perturbation is obviously unfeasible since it
contains an infinite number of points. But notice that the output of
the concrete classifier depends manly on the valid paths within the
precedence graph it builds. So following this observation
$"AGKNN"(R)$ can be computed as follow:

+ Create an (abstract) precedence graph $bb(G)^A_(bold(x))$ such that
  it contains all the valid paths of any concrete precedence graph
  $bb(G)_bold(x)'$ where $bold(x)' in pert(bold(x))$;

+ Collect every path in $bb(G)^A_(bold(x))$ which is a valid path in
  some concrete precedence graph $bb(G)_bold(x)'$

+ Classify the perturbation with most frequent labels in each path
  collected in the previous step.

With the above procedure the output of AGKNN can be computed
since the number of valid paths to explore is finite.

== Abstract precedence graph<apg>

To understand how to construct the abstract precedence graph
$bb(G)^A_(bold(x))$ suppose for example there are two samples
$bold(s)_1, bold(s)_2 in S$ and points $x_1, x_2 in pert(bold(x))$ such that
$
  cases(
    pre(bold(s)_1, bold(s)_2, x: bold(x)_1) "and"
    npre(bold(s)_2, bold(s)_1, x: bold(x)_1),
    pre(bold(s)_2, bold(s)_1, x: bold(x)_2) "and"
    npre(bold(s)_1, bold(s)_2, x: bold(x)_2)
  )
$
that is $bold(s)_1$ is strictly closer to $bold(x)_1$ than $bold(s)_2$
while $bold(s)_2$ is strictly closer to $bold(x)_2$ than $bold(s)_1$.
In this case paths in which $bold(s)_1$ is a predecessor of
$bold(s)_2$ and those in which $bold(s)_2$ is a predecessor of
$bold(s)_1$ are valid paths in $bb(G)_(bold(x)_1)$ and
$bb(G)_(bold(x)_2)$ respectively and so they need to be both valid
paths in the abstract precedence graph $bb(G)^A_(bold(x))$ as well.
This leads to the definition of the following relation between
samples:

#definition([$attach(
prec.eq, tr: sscript(A), br: (bold(x), epsilon))$ relation])[
Given $bold(x) in bb(R)^n, epsilon in bb(N)$ and $bold(s)_1,
bold(s)_2 in S$
$
  bold(s)_1 attach(prec.eq, tr: sscript(A), br:(bold(x), epsilon))
  bold(s)_2 arrow.l.r.double.long exists bold(x)_i in pert(bold(x))
  space pre(bold(s)_1, bold(s)_2, x: bold(x)_i)
$
In the following, for ease of the notation, the subscript $epsilon$
will be dropped since it is constant.]

By this definition $apre(bold(s)_1, bold(s)_2)$ and
$apre(bold(s)_2, bold(s)_1)$ and so there should be a edge between
$bb(G)^A_(bold(x))[bold(s)_1]$ and $bb(G)^A_(bold(x))[bold(s)_2]$ in
both direction. If instead $apre(bold(s)_1, bold(s)_2)$ but
$napre(bold(s)_2, bold(s)_1)$ then there is only an edge from
$bb(G)^A_(bold(x))[bold(s)_1]$ to $bb(G)^A_(bold(x))[bold(s)_2]$
but not the other way around.

To determine if the relation $attach(prec.eq, tr: A, br: bold(x))$
exists between two samples $bold(s)_1, bold(s)_2$, one would need to
verify for each point $bold(x)_1 in pert(bold(x))$ whether
$pre(bold(s)_1, bold(s)_2, x: bold(x)_1)$ holds. However, this
approach is impractical due to the infinite number of points in
$pert(bold(x))$. A more feasible method is to check whether the
perpendicular bisector of $bold(s)_1$ and $bold(s)_2$ intersect with
$pert(bold(x))$. The following result shows a sufficient condition
that can be used to check this intersection efficiently:

#definition([$italic("pos_neg")$ function])[
  Given $x in bb(R)$ let $italic("pos_neg"): bb(R)^n ->
  {-1, 1}$ defined as

  $
  italic("pos_neg")(x) = bb(H)(x) - 1 dot.op (1 - bb(H)(x)) =
  cases(
    thick thick thin 1  &"if" x >= 0,
    -1 &"otherwise"
  )
  $
  where $bb(H)$ is the heaveside step function with the convention
  that $bb(H)(0)$ = 1.
]

#definition([Hyperplane])[Given $bold(n), bold(v) in bb(R)^n, b in
bb(R)$ let $pi attach(:=, t:"def") bold(n) dot bold(v) - b = 0$ be an
equation of an hyperplane then given $bold(w) in bb(R)^n$:
 - $pi(bold(w))$ denotes the value $bold(n) dot bold(w) - b$
 - _poly_($pi$) is the polynomial expression of the hyperplane
   equation that is #linebreak() _poly_($pi$) $ attach(:=, t:"def")
   sum_(i=1)^(i=n) n_i v_i - b$

]

#prop[Given $bold(n), bold(v) in bb(R)^n, b in bb(R)$ let
$pi_(bold(n), b) attach(:=, t:"def") bold(n) dot bold(v) - b = 0$ be
an hyperplane and $pert(bold(x))$ a perturbation of a point
$bold(x) in bb(R)^n$ defined as @pert then
$
  pi_(bold(n), b) "interesect" pert(x) arrow.l.r.double.long
  bold(x) in pi "or" sign(pi_(bold(n), b)(bold(x))) eq.not
  sign(pi_(bold(n), b)(bold(x')))
$
where $bold(x') = bold(x) - epsilon dot sign(pi_(bold(n), b)
(bold(x))) dot italic("pos_neg")^(star)(bold(n))$ and
$italic("pos_neg")^(star)$ is the component-wise $italic("pos_neg")$
operation over vectors in $bb(R)^n$. Essentially the
hyperplane $pi$ interesect the perturbation of $bold(x)$ if and only
if $bold(x)$ and the point $bold(x')$, which is the vertex of the
hypercube $pert(x)$ in the direction of $pi$ from $bold(x)$, are on
the oppisite side of $pi$.
]
#proof[
The proposition can be proved by demonstrating each directions of the
implication separetly:

- ($arrow.r.double.long$): Suppose $pi_(bold(n), b) "interesect"
  pert(x)$ and $bold(x) in.not pi$. Since $pi_(bold(n), b)$ is the
  perpendicular bisector between $s_1$ and $s_2$ it means there
  exists a point $bold(x)'' in pert(bold(x))$ such that it is
  equidistant to both samples (i.e. $bold(x)'' in pi_(bold(n), b)$).
  Because $bold(x)'' in pert(bold(x))$ it can be defined as
  $
    bold(x)'' = bold(x) - sign(pi_(bold(n), b)(bold(x))) dot
    bold(epsilon)'' dot.circle italic("pos_neg")^(star) (bold(n))
  $
  where $dot.circle$ denotes the _Hadamard_ product and
  $bold(epsilon)'' in bb(R)^n$ is a positive vector such that
  $||bold(epsilon)''||_infinity <= epsilon$. $bold(x)'$ can also be
  defined in terms of
  $bold(x)''$ as
  $
    bold(x)'
    &= bold(x)'' -  sign(pi_(bold(n), b)(bold(x))) dot
       bold(epsilon)' dot.circle italic("pos_neg")^(star) (bold(n)) \
    &= bold(x) - sign(pi_(bold(n), b)(bold(x))) dot
       (bold(epsilon)'' + bold(epsilon)') dot.circle
       italic("pos_neg")^(star) (bold(n))
  $
  for some $bold(epsilon)' in bb(R)^n$ positive vector such that
  $|epsilon''_i + epsilon'_i| = epsilon$. With this setup $sign(pi_(
  bold(n), b)(bold(x')))$ is as follow:

  $
    sign(pi_(bold(n), b)(bold(x')))

    &= sign(bold(n) dot [bold(x) -
       overbrace(sign(pi_(bold(n), b)(bold(x))), s)  dot
       (bold(epsilon)'' + bold(epsilon)') dot.circle
       overbrace(italic("pos_neg")^(star) (bold(n)), bold("dir"))]
       + b) \

    &= sign(bold(n) dot [bold(x) - s dot
       (bold(epsilon)'' dot.circle bold("dir") +
        bold(epsilon)'  dot.circle bold("dir"))] + b) \

    &= sign(bold(n) dot [(bold(x) - s dot bold(epsilon)'' dot.circle
       bold("dir")) - s dot bold(epsilon)' dot.circle bold("dir")]
       + b) \

    &= sign(bold(n) dot (bold(x) - s dot bold(epsilon)''
       dot.circle bold("dir")) + b - s dot bold(n) dot
       bold(epsilon)' dot.circle bold("dir")) \

    &= sign(bold(n) dot bold(x)'' + b - s dot bold(n) dot
       bold(epsilon)' dot.circle bold("dir")) \

    &= sign(overbrace(bold(n) dot bold(x)'' + b, = 0) - s dot bold(n)
       dot bold(epsilon)' dot.circle bold("dir")) \

    &= sign(-sign(pi_(bold(n), b)(bold(x))) dot overbrace(
       bold(n) dot bold(epsilon)' dot.circle italic("pos_neg")^(star)
       (bold(n)), "positive")) #<crucial>\

    &= -sign(pi_(bold(n), b)(bold(x))) eq.not
    sign(pi_(bold(n), b)(bold(x)))
  $

  In @crucial $forall i in {0, dots, n-1}$ if $n_i eq.not 0$ then the
  sign of $epsilon'_i dot italic("pos_neg")(n_i)$ is the same as
  $n_i$ and so the sign of $n_i dot epsilon'_i dot italic("pos_neg")
  (n_i)$ is always postive hence $bold(n) dot bold(epsilon)'
  dot.circle italic("pos_neg")^(star) (bold(n))$ is a positive value.

  In the case $bold(x) in pi_(bold(n), b)$ then the implication holds
  vacuously.

- ($arrow.l.double.long$): if $bold(x) in pi_(bold(n), b) "or"
  sign(pi_(bold(n), b) (bold(x))) eq.not sign(pi_(bold(n), b)
  (bold(x')))$ then it means $pi_(bold(n), b) "surely interesect"
  pert(x) $.
]

The procedure to create the abstract precedence graph is the same as
@create_precedence_graph with the only difference being the order
relation used which is $attach(prec.eq, tr: A, br: x)$.

#example[Consider the setup of @example11 and perturbation $pert(x)$
where $epsilon = 0.25$ shown in the plot in @abstract-example a).
In this case:

- $apre(a, b) and apre(b, a)$
- $apre(a, c) and napre(c,a)$
- $apre(b, c) and apre(b, c)$

and so the abstract precedence is the one shown in @abstract-example
b). The abstract precedence graph contains an additional valid path
w.r.t the concrete precedence graph which is:
$
  [bold(b),bold(c),bold(a)]
$
because there are points (e.g., the point $x'$) in the perturbation
such that $pre(c, a, x: "") and npre(a, c, x: "")$ and so in the
abstract case there are 3 valid paths.

#prop[
Given a sample $bold(s) in S$ and an abstract Precedence graph
$bb(G)^A_bold(x)$
$
mono("pred")^(A)(bold(s)) = limits(\u{22C2})_(bold(x)' in
pert(bold(x))) mono("pred")_(bold(x)')(bold(s))
$
where $mono("pred")^(A)(bold(s))$ and $mono("pred")_(bold(x)')
(bold(s))$  are the value of $predv(bold(s))$ in the graph
$bb(G)^A_bold(x)$ ahd $bb(G)_bold(x)'$ respectively.
]<prop-31>
#proof[Follows from the definition of$attach(prec.eq, tr: sscript(A),
br: x)$
]

#figure(grid(columns: 2, row-gutter: 10mm, column-gutter: 15mm,

  [#align(center)[#cetz.canvas({
    import cetz.draw: *
    import cetz.plot
    import cetz.palette

    let opts = (
      x-tick-step: 1, y-tick-step: 1, size: (6,6),
      y-minor-tick-step: .25, x-minor-tick-step: .25,
      x-grid: "both", y-grid: "both",
      x-min: -0.5, x-max: 2.5, y-min: -0.5, y-max: 2.5,
      plot-style: palette.dark-green
    )
    let points = ((0,1), (2,1), (2.25,1),)
    let pert = ((0.75,0.75), (0.75,1.25),
                (1.25,1.25),  (1.25,0.75), (0.75,0.755))
    let colors = cetz.palette.new(colors: (red, blue, green, black))

    set-style(axes:(tick: (minor-length: 0pt)))
    plot.plot(axis-style: "school-book", ..opts, name: "plot", {
      plot.add(((0,1),), style: (stroke: none), mark: "o",
        mark-size: 0.15, label: $a$)
      plot.add(((2,1),), style: (stroke: none), mark: "o",
        mark-size: 0.15, label: $b$)
      plot.add(((2.25,1),), style: (stroke: none), mark: "o",
        mark-size: 0.15, label: $c$)
      plot.add(((1, 1),), style: (stroke: none), mark: "x",
        mark-size: 0.15,
        mark-style: palette.dark-green(2, stroke: true),label: $x$)
      plot.add(((1.18, 1),), style: (stroke: none,), mark: "+",
        mark-size: 0.15, label: $x'$)
      plot.add(pert, style: palette.gray(2, stroke: true),
        fill: true, fill-type:"shape")

      plot.annotate(content((0.1,1.1), [$a$]))
      plot.annotate(content((2.1,1.1), [$b$]))
      plot.annotate(content((2.35,1.1), [$c$]))
      plot.annotate(content((1.1,1.1), [$x$]))
      plot.annotate(content((1.28,0.9), [$x'$]))


    })
  })]],
  [ #v(50pt)#align(center)[#render("
  digraph {
    a -> b
    b -> a
    a -> c
    b -> c
    c -> b
    {rank=same a, b}
  }",
  labels: (:
    a: [*a*],
    b: [*b*],
    c: [*c*]
  )
)]],

  [a) Plot of dataset and perturbation of @example11],
  [b) Abstract precedence graph])
)<abstract-example>]

== Path generation

Another difference between the concrete and abstract case is the
definition of a valid path. To see why consider for example the set
of samples:

- *$bold(s)_0$*: (0.75, 1.3)
- *$bold(s)_1$*: (1.0, 1.3)
- *$bold(s)_2$*: (1.25, 1.3)

and the input perturbation $pert((1,1))$ with $epsilon = 0.05$.
@incomplete-example a) shows the plot of the samples and the
perturbation region while @incomplete-example b) illustrate the
abstract graph. According to @def-valid-path the valid paths in
the abstract precedence graph are the permutations of the sequence of
vertices $[bold(s_0), bold(s_1), bold(s_2)]$ in particular:

+ $[bold(s_0), bold(s_1), bold(s_2)]$
+ $[bold(s_0), bold(s_2), bold(s_1)]$

but notice that there is no $bold(x)'in pert(bold(x))$ such that
second path is a valid order of precedence in $bb(G)_bold(x)'$. This
is because the regions of space containing the points closer the
sample $bold(s)_0$ (i.e. the blue region) and the one with points
closer to sample $bold(s)_2$ than $bold(s)_1$ (i. e. the green region)
do not intersect.


#figure(grid(columns: 2, row-gutter: 10mm, column-gutter: 15mm,

  [#align(center)[#cetz.canvas({
    import cetz.draw: *
    import cetz.plot
    import cetz.palette

    let opts = (
      x-tick-step: 1, y-tick-step: 1, size: (6,6),
      y-minor-tick-step: .10, x-minor-tick-step: .10,
      x-grid: "both", y-grid: "both",
      x-min: 00.5, x-max: 1.5, y-min: 0.5, y-max: 1.5,
      plot-style: palette.dark-green
    )
    let points = ((0,1), (2,1), (2.25,1),)
    let pert = ((0.75,0.75), (0.75,1.25),
                (1.25,1.25),  (1.25,0.75), (0.75,0.755))

    set-style(axes:(tick: (minor-length: 5pt)))

    plot.plot(axis-style: "school-book", ..opts, name: "plot", {
      plot.add(((0.75,1.3),), style: (stroke: none), mark: "o",
        mark-size: 0.2)
      plot.add(((1.0,1.3),), style: (stroke: none), mark: "o",
        mark-size: 0.2)
      plot.add(((1.25,1.3),), style: (stroke: none), mark: "o",
        mark-size: 0.2)
      plot.add(((1, 1),), style: (stroke: none), mark: "x",
        mark-size: 0.2,
        mark-style: palette.dark-green(2, stroke: true))
      plot.add(pert, style: palette.gray(1, stroke: true),
        fill: true, fill-type:"shape", )

      plot.add-vline(1.75/2, 2.25/2,
                      style: (stroke: (dash: "dashed"))
                      // style: palette.blue(2, stroke: true)
                      )

      plot.annotate({
        rect((0.75,0.75), (1.75/2,1.25),  fill: rgb(0,0,255,90),
        stroke: gray)
      })
      plot.annotate({
        rect((2.25/2,0.75), (1.25,1.25),  fill: rgb(0,255,0,50),
        stroke: gray)
      })

      plot.annotate(content((0.76,1.37), [$s_0$]))
      plot.annotate(content((1.01,1.37), [$s_1$]))
      plot.annotate(content((1.26,1.37), [$s_2$]))
      plot.annotate(content((1.02,1.05), [$x$]))

    })
  })]],
  [#v(50pt)#align(center)[#render("
  digraph {
    s_0 -> s_1
    s_1 -> s_0
    s_0 -> s_2
    s_2 -> s_0
    s_1 -> s_2
    s_2 -> s_1
    {rank=same s_0, s_1}
  }",
   labels: (:
    s_0: [$bold(s_0)$],
    s_1: [$bold(s_1)$],
    s_2: [$bold(s_2)$]
  )
)]],

  [a) Plot of dataset and perturbation],
  [b) Abstract precedence graph]),
  gap: 1em,
  caption: [Example of invalid path],
  placement:  top
)<incomplete-example>


== Valid Path

The previous example illustrate that when adding a vertex $v$ to a
path $p$ checking only the predecessors of the vertex do not suffice
and the existence of a region of the perturbation containing points
such that the samples satisfy the precedence order in $p$ must also be
taken into consideration. This leads to the following definition for
a valid path in the abstract case:

#definition("Valid path")[Given an abstract precedence graph
$bb(G)^A_bold(x)'$ let $cal(P) =[bold(v_0), bold(v_1),dots,
bold(v_m)]$ be a path in $bb(G)^A_x$. The path $cal(P)$ is _valid_
if and only if

 - $forall bold(s)_i in cal(P). space forall bold(x)_j in
    predv(bold(x)_i). space bold(x)_j "is a predecessor of "
    bold(s)_i "in" cal(P)$
 - $exists R subset.eq pert(bold(x)) "s.t." R eq.not emptyset and
    forall bold(bold(x))'in R. space cal(P) "is a valid path in"
    bb(G)_bold(bold(x))$
]<def-abs-valid-path>

The definition of a safe vertex reamins unchanged.


To see how the sub region $R$ can be calculated consider the samples
of the previous example. The path $[bold(s_1)]$ is valid if there is
a region of points $R_1 in pert(bold(x))$ such that the sample
$bold(s_1)$ is the closest to them. This means that points in $R_1$
must satisfy the following linear system of inequalities:
$
  cases(
    x_1 - 1.125 <= 0,
    -x_1 + 0.75 <= 0,
    0.75 <= x_1 <= 1.75,
    0.75 <= x_2 <= 1.75,
  )
$
where $x_1 - 1.25 = 0$ and $x_1 - 0.75 = 0$ are the perpendicular
bisector between the samples $bold(s_1)$ and $bold(s_0)$ and
samples $bold(s_1)$ and $bold(s_2)$ respectively. This region is shown
in @sub-reg a). Consider now the path $[bold(s_1), bold(s_0)]$. This
path is valid if it exists a region of points $R_2 in pert(bold(x))$
such that the closest samples is $bold(s_1)$ and the second closest
is $bold(s_0)$. So points in $R_2$ must satisfy the following linear
system of inequalities:
$
  cases(
    x_1 - 1.25 <= 0,
    -x_1 + 0.75 <= 0,
    x_1 - 1 <= 0,
    0.75 <= x_1 <= 1.75,
    0.75 <= x_2 <= 1.75,
  )
$<linear-system>
where the first two inequalities define the $R_1$ region while the
third inequality exclude from $R_1$ those points that are strictly
closer to the sample $bold(s_2)$ than $bold(s_0)$ resulting in the
blue region illustrated in @sub-reg b). Finally the same logic
applies to path $[bold(s_1), bold(s_0), bold(s_2)]$ which defines
the same the linear system as @linear-system.

On the other hand the linear system of inequalities associated with
path $[bold(s_0), bold(s_2)]$ is
$
  cases(
    x_1 - 1 <= 0,
    x_1 - 0.875 <= 0,
    -x_1 + 1.25 <= 0,
    0.75 <= x_1 <= 1.75,
    0.75 <= x_2 <= 1.75,
  )
$
and is shown in @incomplete-example a). As can be seen from the plot
the two regions (i.e. the blue one containing points for which the
sample $bold(s_0)$ is the closest one and the green containing
points for which the sample $bold(s_2)$ is closer than $bold(s_1)$)
do not intersect hence the linear system has no solutions. So the
path $[bold(s_0), bold(s_2)]$ and consequently $[bold(s_0),
bold(s_2), bold(s_1)] $ are not valid paths.

To summarize, given a path $cal(P)$, the idea is to identify a
polytope inside the perturbation region using a linear system of
inequalities which contiains only those points for which the sequence
of samples defined by $cal(P)$ is ordered according to distance to
this points. Then if this polytope exists (i.e the linear system
has solutions) it means that there is at least one concrete
precedence graphs $bb(G)_(bold(x)')$ for some $bold(x)' in pert(x)$
such that $cal(P)$ is valid in $bb(G)_(bold(x)')$. Conversely, if the
linear system has no solutions, it means that no point in the
perturbation region can produce the sequence of samples as defined by
the path.

#figure(grid(columns: 2, row-gutter: 10mm, column-gutter: 15mm,

  [#align(center)[#cetz.canvas({
    import cetz.draw: *
    import cetz.plot
    import cetz.palette

    let opts = (
      x-tick-step: 1, y-tick-step: 1, size: (5,5),
      y-minor-tick-step: .10, x-minor-tick-step: .10,
      x-grid: "both", y-grid: "both",
      x-min: 00.5, x-max: 1.5, y-min: 0.5, y-max: 1.5,
      plot-style: palette.dark-green,
    )
    let points = ((0,1), (2,1), (2.25,1),)
    let pert = ((0.75,0.75), (0.75,1.25),
                (1.25,1.25),  (1.25,0.75), (0.75,0.755))

    set-style(axes:(tick: (minor-length: 5pt)))

    plot.plot(axis-style: "school-book", ..opts, name: "plot", {
      plot.add(((0.75,1.3),), style: (stroke: none), mark: "o",
        mark-size: 0.2)
      plot.add(((1.0,1.3),), style: (stroke: none), mark: "o",
        mark-size: 0.2)
      plot.add(((1.25,1.3),), style: (stroke: none), mark: "o",
        mark-size: 0.2)
      plot.add(((1, 1),), style: (stroke: none), mark: "x",
        mark-size: 0.2,
        mark-style: palette.dark-green(2, stroke: true))
      plot.add(pert, style: palette.gray(1, stroke: true),
        fill: true, fill-type:"shape", )

      plot.add-vline(1.75/2, 2.25/2,
                     style: (stroke: (dash: "dashed")))

      plot.annotate({
        rect((1.75/2,0.75),(2.25/2, 1.25),  fill: rgb(255,0,0,90),
        stroke: gray)
      })

      plot.annotate(content((0.76,1.37), [$s_0$]))
      plot.annotate(content((1.01,1.37), [$s_1$]))
      plot.annotate(content((1.26,1.37), [$s_2$]))
      plot.annotate(content((1.02,1.05), [$x$]))

    })
  })]],
  [#align(center)[#cetz.canvas({
    import cetz.draw: *
    import cetz.plot
    import cetz.palette

    let opts = (
      x-tick-step: 1, y-tick-step: 1, size: (5,5),
      y-minor-tick-step: .10, x-minor-tick-step: .10,
      x-grid: "both", y-grid: "both",
      x-min: 00.5, x-max: 1.5, y-min: 0.5, y-max: 1.5,
      plot-style: palette.dark-green
    )
    let points = ((0,1), (2,1), (2.25,1),)
    let pert = ((0.75,0.75), (0.75,1.25),
                (1.25,1.25),  (1.25,0.75), (0.75,0.755))

    set-style(axes:(tick: (minor-length: 5pt)))

    plot.plot(axis-style: "school-book", ..opts, name: "plot", {
      plot.add(((0.75,1.3),), style: (stroke: none), mark: "o",
        mark-size: 0.2)
      plot.add(((1.0,1.3),), style: (stroke: none), mark: "o",
        mark-size: 0.2)
      plot.add(((1.25,1.3),), style: (stroke: none), mark: "o",
        mark-size: 0.2)
      plot.add(((1, 1),), style: (stroke: none), mark: "x",
        mark-size: 0.2,
        mark-style: palette.dark-green(2, stroke: true))
      plot.add(pert, style: palette.gray(1, stroke: true),
        fill: true, fill-type:"shape", )

      plot.add-vline(1, style: (stroke: (dash: "dashed")))

      plot.annotate({
        rect((1.75/2,0.75),(2.25/2, 1.25),  fill: rgb(255,0,0,40),
        stroke: gray)
      })

      plot.annotate({
        rect((1.75/2,0.75),(1, 1.25),  fill: rgb(0,0,255,90),
        stroke: gray)
      })

      plot.annotate(content((0.76,1.37), [$s_0$]))
      plot.annotate(content((1.01,1.37), [$s_1$]))
      plot.annotate(content((1.26,1.37), [$s_2$]))
      plot.annotate(content((1.02,1.05), [$x$]))

    })
  })]],
  [a) Region of points satisfying the path [$bold(v_1)$]],
  [b) Region of points satisfying the path [$bold(v_1), bold(v_2)$]]),
  gap: 1em,
  caption: [Example of region of points denoted by a path],
  placement: top
)<sub-reg>

@valid-path shows hoe to construct a polytope given a path and
the bounds of the perturbation as a set, where each element is of the
form $italic(min)_1 <= x_i <= italic(max)_i$. It builds the linear
system of inequalities using the $mono("bisector")$ function, which,
given two samples $bold(s)_i$ and $bold(s)_j$​, returns the
perpendicular bisector $beta$ between them such that $beta(bold(s)_j)
>= 0$. The algorithm begins by creating the linear system of
inequalities from the bounds provided in the input (line $mono(1)$).
Then it adds inequalities to ensure that the sample $bold(s)_0$ (i.e.
the path first sample) is the closest to the perturbation (lines
$mono("2-5")$). This is achieved by constructing the perpendicular
bisector between $bold(s)_0$ and the samples in $samedistv(bold(s)_0)$
using the $mono("bisector")$ function, and imposing that the
perturbation region lies in the half-space containing $bold(s)_0$
(lines $mono(2-4)$). Subsequently, for each next sample $bold(s)_i$ in
the path, inequalities are added to ensure that the sample
$bold(s)_i$ is the closest to the perturbation region after the sample
$bold(s)_j$ $0 <= j < i$ (lines $mono(7-17)$). This is done by first
constraining the sample $bold(s)_i$ to be closer to the perturbation
than each sample in $samedistv(bold(s)_i)$ (lines $mono("8-11")$), and
then ensuring that samples $bold(s)_j$ for $0 <= j < i$ are closer
than sample $bold(s)_i$ (lines $mono("12-17")$). Finally, the created
linear system is returned (line $mono(18)$).

#algorithm(title: [$mono("build_polyhedron")$ method],
           input: ([*$var("path")$*: A sequence of vertices, ],
                   [*$var("bounds")$*: Bounds of the perturbation
                     given as a set whose elements are of the form
                     $italic(min)_1 <= x_i <= italic(max)_i$
                   ]),
           output: ([A linear system of inequalities],))[

  $var("LSI") <- bold("bounds")$\

  for $var("vertex")$ in $samedistv(var("path")[1])$ do#i\
    $beta <- func("bisector", var("path")[1], var("vertex"))$\
    $var("LSI") <- var("LSI") union {italic("poly")(beta) <=0 }$#d\
  end\

  $var("n") <- func("length", bold("path"))$\
  for $var(i)$ *from* $2$ to $var("n")$ do#i\

    for $var("vertex")$ in $samedistv(var("path")[i])$ do#i\
      $beta <- func("bisector", var("path")[i], var("vertex"))$\
      $var("LSI") <- var("LSI") union {italic("poly")(beta) <=0 }$#d\
    end\

    for $var(j)$ *from* $1$ to $var(i)-1$ do#i\
      if $var("path")[j] in.not samedistv(var("path")[i])
         and var("path")[j] in.not predv(var("path")[i])$ then #i\
        $beta <- func("bisector", var("path")[j], var("path")[i])$\
        $var("LSI") <- var("LSI") union {italic("poly")(beta) <=0}$#d\
      end#d\
    end#d\
  end\

  return $var("LSI")$
]<valid-path>

== Valid path generation

@abstract-path-generation shows how the valid paths on length $n$ are
generated given the abstract precedence graph $bb(G)^A_bold(x)$.
Essentially the algorithm is same as the @path_generation with the
only difference being that before starting to construct the paths of
the desired length it checks whether the initial paths (i.e. those
containing a single vertex) are valid or not (line $mono("2-7")$).

#algorithm(title: [$mono("abstract_generate_paths")$ method],
           output: ([Set of valid paths of length *n*],),
           input: (
            [*$G_x$*: precedence graph,],
            [*n*: length of the path]
           ))[
  $var("closest_vertices") <- {v_i | v_i in bb(G)_x,space
  predv(v_i) = emptyset}$\
  $var("init_paths") <- {}$\
  for $var("vertex")$ in $var("closest_vertices")$ do#i\
    if $var("vertex") bold("is safe") #no-emph("for")
       bold("empty_path")$ then#i\
      $var("init_paths") <- var("init_paths") union
                           {[var("vertex")]}$#d\
    end#d\
  end\

  $var("queue") <- func("create_queue", var("init_paths"))$\
  $var("k") <- 0$\
  while #var("queue") not *empty* do#i\
    $var("current_paths") <- var("queue").func("popAll")$\

    if #var("k") = *n* then#i\
      return #var("current_paths")#d\

    for #var("current_path") in #var("current_paths") do#i\

      $var("last_vertex") <- var("current_path").mono("last")()$\

      for #var("adj") in $var("last_vertex").mono("adjacent")$ do#i\

        if $var("adj") bold("is safe") #no-emph("for")
           var("current_path")$
        then#i\
          $var("queue").func("append", var("current_path") +
           [var("adj")])$#d\
        end#d\
      end#d\
    end\
    $var("k") <- var("k") + 1$#d\
  end\
]<abstract-path-generation>

#prop[Given as input the the abstract precedence graph
$bb(G)^A_bold(x)$ and the length $n in bb(N)$
@abstract-path-generation returns all the valid paths of length $n$
within $bb(G)^A_bold(x)$.]<abs-valid-paths>
#proof[The proposition can be proved by showing, using induction on
$k$, that at the $k$-th iteration of the while loop, at line 11 the
queue contians all the valid paths of length $k-1$:

  - ($k=1$):In the first iteration of the loop the queue contains all
    the path made of a single sample $bold(s)_i$ such that:

      - $predv(bold(s))_i = emptyset$ since $bold(s)_i in
         var("closest_vertices")$ by defintion (line $mono("1")$);
      - $exists R in pert(x) "s.t." forall bold(x)' in R. "sample"
        bold(s_i)$ is the closest sample by defintoin (lines
        $mono("3-7")$)
    This means that the path $[bold(s)_i ]$ is a valid path by
    definition

  - ($k=h+1$): At iteration $h + 1$, the paths inside the queue at
    line 11 are obtained by extending all the paths in the queue in
    the $h$-th iteration with every safe vertex among the adjacent
    of the path's last vertex. By induction hypothesis the queue in
    the $h$-th iteration contains all the valid paths of length $h$
    and since they are extended with every safe vertices it means that
    in the $h + 1$ iteration the queue contains only and all the valid
    paths of length $h = k - 1$.
]

== AGKNN Algorithm

@agknn-algh shows how the abstract classifier works. Given the samples
dataset $bold(S)$, the input sample $bold(x)$ and the number $k$ of
neighbours to consider fot the classification, tt stars by
constructing the abstract precedence graph $bb(G)^A_bold(x)$ as
described in @apg (line $mono(("1"))$). Afterwards extracts all the
valid paths within $bb(G)^A_bold(x)$ (line $mono(("2"))$) to then
collect the most frequent labels in each path (line $mono("3-7")$).
Finally the collected labels are return as the classification of the
input (line $mono("8")$).

#algorithm(
  title: "AGKNN algoritm",
  output: ([Set of possible classification of $x$],),
  input: (
    [*$var(x)$*: the input sample],
    [*$var(S)$*: samples dataset],
    [*$var(k)$*: number of neighbours],
  ))[

  $bb(G)^A_bold(x) <-$  #func("create_abstract_precedence_graph",
                              $var(S)$, $var(x)$)\

  $var("paths") <-$ #func("abstract_generate_paths", $bb(G)^A_bold(x)$,
                          $k-1$)\
  $var("classification") <- {}$\
  for #var("path") in #var("paths") do#i\
    $var("labels") <- "most frequent labels in "mono("path")$\
    $var("classification") <- var("labels") union
                              var("classification")$#d\
  end\
  return #var("classification")
]<agknn-algh>

=== Completeness
As mentioned in the beginning of this chapter, given the perturbation
$pert(bold(x))$, the abstract classifier is said to be _sound_ if the
computed set of labels contains all the output of the concrete
classifier on each point of the perturbation that is when
$
limits(union.big)_(bold(x)' in pert(bold(x))) "GKNN"(bold(x)', S, k) subset.eq
                                  "AGKNN"(pert(bold(x)), S, k)
$<sound>

Actually the abstract classifier satisfy the stronger condition of
being _exact_ (or _complete_) where the equality sign in @sound holds.
In fact, as the following result shows, the abstract classifier output
contains all and only the outputs of the concrete classifier for each
point within the perturbation.

#theorem[Given a dataset $S = {(bold(s)_i, bold(y)_i) | bold(s)_i in
bb(R)^n, bold(y)_i in cal(L)}$ and the perturbation $pert(bold(x))$ of
the input sample $bold(x)$, then
$
limits(union.big)_(bold(x)' in pert(bold(x))) "GKNN"(bold(x)', S, k) =
                            "AGKNN"(pert(bold(x)), S, k)
$]
#proof[The main difference, other than the precedence relation,
between the concrete and abstract classifier is the way they collect
the valid paths. Since @prop13 and @abs-valid-paths ensures that both
algorithms consider all and only the valid paths of length $k$ for
the classification the preposition can be proven by separately
demonstrating that:

 + $limits(union.big)_(bold(x)' in pert(bold(x))) mono("valid_path")
    (bb(G)_(bold(x)_i)) subset.eq mono("valid_path")
    (bb(G)^A_(bold(x)))$

 + $limits(union.big)_(bold(x)' in pert(bold(x))) mono("valid_path")
    (bb(G)_(bold(x)_i)) supset.eq mono("valid_path")
    (bb(G)^A_(bold(x)))$

where $mono("valid_path")(G)$ denotes the set of valid paths in a
graph G.

/ 1): Without loss of generality consider a valid path $cal(P)=[
      bold(s)_0, bold(s)_1,dots,bold(s)_(k-1)]$ of length $k$ in
      $bb(G)_(bold(x)_i)$ for some  $bold(x)_i in pert(bold(x))$. By
      definition of path in graph and $pre("", "", x: bold(x)_i)$ we
      have that
      $
        apre(s_0,
          apre(s_1,
           apre(dots, s_(k-1), x: bold(x)_i),
          x: bold(x)_i),
        x: bold(x)_i)
      $
      This means that $cal(P)$ is also a path in $bb(G)^A_bold(x)$.
      Moreover since $cal(P)$ is a valid path and, by @prop-31,
      $forall v_i in cal(P)$
      $
        predv(bb(G)^A_(bold(x))[s_i]) subset.eq
        predv(bb(G)_(bold(x)_i)[s_i])
      $
      it means that $p$ satisfy both the condition of
      @def-abs-valid-path hence $p in
      mono("valid_path")(bb(G)^A_(bold(x)))$.

/ 2): Suppose $p$ is a valid path in $bb(G)^A_(bold(x))$. Then, by
  definition of valid path, it means there exists $bold(x)' in
  pert(bold(x))$ such that the path represents a valid order of
  precedence according to the distance between the samples and
  $bold(x)'$. This means that $p in mono("valid_path")
  (bb(G)_(bold(x)'))$
]

== Abstract precedence graph construction optimization

Since in the abstract case the query is the perturbation of the input
rather the a single point, the algorithm to reduce the set of sample
used for the precedence graph construction needs to be changed. The
only difference with the concrete counterpart is the step 4) because,
in order to ensure the soundness of the abstract classifier, the
hypershpere must contain all the $k$ closest sample of each point in
the perturbation.

In order to find the minimum radius $r$ of the hypershpere consider
the $k$ closest sample $A = {bold(s)_1, bold(s)_2, dots, bold(s)_k}$
to the input $bold(x)$ and let $s_k$ be the furthest sample from
$bold(x)$ with distance $d$. Now consider a generic point $bold(x)' in
pert(bold(x))$ and the hypershpere $H_bold(x)'$ centered in $bold(x)'$
and radius the distance between $bold(x)'$ and $bold(s)_bold(x)' =
limits("argmax")_(bold(s)_i in A) ||bold(x)'- bold(s)_i||$. Surely the
set of samples in $H_bold(x)'$ is $A union B$ where B is the set
(possibly empty) of samples closer to $bold(x)'$ than any sample in
$A$. So the enclosing hypershpere $H$ of all the hyperspheres
$H_bold(x)'$ for every $bold(x)' in pert(bold(x))$ is the one that
surely contains all the $k$ closest sample of each point in the
perturbation.

Notice that given a points $bold(y) in bb(R)^n$ and
$bold(x)'in pert(bold(x))$
$
  ||bold(x)' - bold(y)|| <= ||bold(x) - bold(x)'|| +
  ||bold(x) - bold(y)||
$
due to the triangular inequality property of norms. So this means that
for every $bold(x)'in pert(bold(x))$
$
  ||bold(x)' - bold(s)_bold(x)'|| <= ||bold(x) - bold(x)'|| +
  ||bold(x) -  bold(s)_bold(x)'|| <= sqrt(N) dot epsilon + d
$

Since the maximum radius of $H_x'$ for any $x' in pert(x)$ is
$sqrt(N) dot epsilon + d$ it means the hypershpere of interest $H$ is
centered in the input $x$ and has radius $2epsilon sqrt(N) + d$.

#pagebreak()

== Comparison with NAVe

Some comparisons with Nave tool using the euclidean norm and interval
domain.

#tablex(
  columns: 10,
  align: center + horizon,
  auto-vlines: false,
  repeat-header: true,
  header-rows: 2,

  /* --- header --- */
  rowspanx(2)[*Dataset*],
  rowspanx(2)[*$epsilon$*],
  colspanx(2)[*Runtime (mm:ss)*], (), (),
  rowspanx(2)[],
  colspanx(2)[*Stability*], (),
  rowspanx(2)[],
  colspanx(2)[*Robustness*], (),

  (), (), [*NAVe*], [*AGKNN*], (), [*NAVe*], [*AGKNN*],
  (), (), [*NAVe*], [*AGKNN*],
  /* -------------- */
  rowspanx(10)[Fourclass],
  rowspanx(5)[$0.01$], rowspanx(5)[00:01], rowspanx(5)[00:01],
  [k=1], [99.2], [99.6], [], [99.2], [99.6],
  [k=2], [98.4], [98.4], [], [98.4], [98.4],
  [k=3], [99.6], [99.6], [], [99.6], [99.6],
  [k=5], [98.4], [98.8], [], [98.4], [98.8],
  [k=7], [97.7], [98.4], [], [97.7], [98.4],
  rowspanx(5)[$0.05$], rowspanx(5)[00:01], rowspanx(5)[00:04],
  [k=1], [45.0], [71.3], [], [45.0], [71.3],
  [k=2], [39.9], [65.1], [], [39.9], [65.1],
  [k=3], [42.6], [71.7], [], [42.6], [71.7],
  [k=5], [40.3], [72.8], [], [40.3], [72.8],
  [k=7], [37.6], [74.4], [], [37.6], [74.4],

  rowspanx(10)[Pendigits],
  rowspanx(5)[$0.01$], rowspanx(5)[11:39], rowspanx(5)[00:37],
  [k=1], [96.7], [97.8], [], [95.6], [96.5],
  [k=2], [94.0], [96.2], [], [93.3], [95.2],
  [k=3], [96.1], [98.1], [], [95.3], [96.8],
  [k=5], [95.7], [98.3], [], [94.9], [96.6],
  [k=7], [95.0], [98.1], [], [94.1], [96.2],
  rowspanx(5)[$0.05$], rowspanx(5)[11:53], rowspanx(5)[07:14],
  [k=1], [59.0], [81.7], [], [59.0], [81.5],
  [k=2], [52.6], [79.7], [], [52.6], [79.5],
  [k=3], [60.6], [85.4], [], [60.6], [85.2],
  [k=5], [59.8], [86.2], [], [59.7], [85.9],
  [k=7], [58.9], [86.6], [], [58.9], [86.2],

  rowspanx(10)[Letter],
  rowspanx(5)[$0.01$],rowspanx(5)[29:45], rowspanx(5)[06:55],
  [k=1], [82.7], [88.7], [], [82.2], [87.9],
  [k=2], [70.4], [79.9], [], [70.4], [79.7],
  [k=3], [75.1], [87.4], [], [75.0], [86.8],
  [k=5], [69.5], [86.6], [], [69.4], [85.8],
  [k=7], [65.2], [86.0], [], [65.1], [85.1],

  rowspanx(5)[$0.02$],rowspanx(5)[30:30], rowspanx(5)[10:47],
  [k=1], [54.6], [73.0], [], [54.6], [72.9],
  [k=2], [42.1], [61.4], [], [42.1], [61.4],
  [k=3], [45.4], [70.6], [], [45.4], [70.6],
  [k=5], [40.3], [70.8], [], [40.3], [70.7],
  [k=7], [37.0], [69.6], [], [37.0], [69.5]
)


#pagebreak()
#bibliography("bibliography.bib")

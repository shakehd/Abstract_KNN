#import "utils.typ": algorithm, var, func, setv, reqv, lenv, predv, setp, reqp, lenp, line
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

= Concrete algorithm

Given a set of labels $cal(L)$ and the dataset $S = {(s^(i), y^(i)) |
s^(i) in bb(R)^n, y^(i) in cal(L)}$ and the input sample $x in
bb(R)^n$, $"GKNN": bb(R)^n -> cal(P)(cal(L))$ is function that
classify the input with the most frequent label within the $k$
closest samples to the input like the $k$NN algorithm but differs
from it in the way those samples are found. Rather than sort the
samples in oder of their proximity to the input and then select the
first $k$ samples, GKNN use the relation of "being closer to the
input" between pair of samples w.r.t. the minkowski norm to select
the $k$ closest samples. The relation is defined as follow:

#definition([Relation $prec.eq$])[Given the points $x,
s_i, s_j in bb(R)^n$, "$s_i attach(prec.eq, br: x) s_j$" means $s_i$
is closer to the input than $s_i$ w.r.t. the minkowski norm that is
$|| x - s^(i) ||_p lt.eq || x - s^(j) ||_p$. The subscript
$x$ will be omitted when is clear from the context.]

GKNN first build a "precedence" graph $bb(G)$ in which nodes
are the samples in $S$ and edges model the relation $attach(prec.eq,
br: x)$ (i.e. the tail is closer to the input than the head) and then
classify the input with the most frequent labels within the vertices
composing the valid paths #footnote[The definition of a valid is given
later in @path-sec] of length $k-1$ starting from the samples closest
to the input.

== Precedence graph

The precedence graph $bb(G)_x = (V, E)$ is a graphical representation
of the totally ordered set $(S, attach(prec.eq, br: x))$:

- $V = S$
- $E = {(v_i, v_j) bar.v || x - s^(i) ||_p lt.eq || x - s^(j) ||_p }$
where $||dot.op||_p$ is the minkowski norm.

The graph is implemented using adjacent lists so each vertex object
has a list of adjacent vertices. Moreover each vertex $v_i$ also has a
set attribute, named $mono("predecessors")$, that contains all the
vertices $v_j$ such that there is an incoming edge from $v_j$ but not
an outgoing edge that is
$
  (v_j, v_i) in E "and" (v_i, v_j) in.not E
$
This means that
$
  forall v_j in v_i.mono("predecessors") space  v_j prec.eq v_i
  " and " v_i prec.eq.not v_j
$

This information will be used for the generation of valid paths
based on how close the samples are to the input sample. In the
remainder of the document the vertex associated with sample $s_i$
is denoted with $bb(G)_(x)[s_i]$ while the sample associated with the
vertex $v_j$ is denoted simply with $s_j$.

@create_precedence_graph shows how the graph is created. Given the
sample dataset $S$ and the input sample $x$, it first create the
graph $bb(G)$ with only the vertices with their
$mono("predecessors")$ and $mono("adjacent")$ attributes set to the
empty set (line $mono(1)$). Then for each unordered pair of samples
$(s_i,s_j)$ we check which sample between $s_i$ and $s_j$ is closer
to the input sample $x$ w.r t. the minkowski norm and update both
vertex attributes accordingly (line $mono(2-12)$). If $s_i$ and $s_j$
are equidistant than only the adjacent lists are updated since $s_j
prec.eq s_i$ and $s_i prec.eq s_j$ (line $mono(3-5)$). Finally the
created graph is returned (line $mono(15)$).

#algorithm(
  title: [$mono("create_precedence_graph")$ method],
  output: ([$bb(G)_x$: precedence graph],),
  input: (
    [*$S$*: samples dataset],
    [*$x$*: the input sample]
  ))[
    $bb(G)_x <-$#func("initialize_graph", $S$)\

    for $(s_i, s_j)$ in ${(s_i,s_j)| s_i,s_j in S, s_i eq.not s_j}$
    do#i\
      if $s_i prec.eq s_j$ and $s_j prec.eq s_i$ then#i\
        add $bb(G)_(x)[s_j]$ to $bb(G)_(x)[s_i].mono("adjacent")$\
        add $bb(G)_(x)[s_i]$ to $bb(G)_(x)[s_j].mono("adjacent")$#d\
      else if $s_i prec.eq s_j$ then#i\
        add $bb(G)[s_j]$ to $bb(G)_(x)[s_i].mono("adjacent")$\
        add $bb(G)[s_i]$ to $bb(G)_(x)[s_j].mono("predecessors")$#d\
      else#i\
        add $bb(G)_(x)[s_i]$ to $bb(G)_(x)[s_j].mono("adjacent")$\
        add $bb(G)_(x)[s_j]$ to $bb(G)_(x)[s_i].mono("predecessors")$#d\
      end#d\
    end\
    return $bb(G)_x$
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
proximity relation among the samples that is if $v_i prec.eq v_j$ but
$v_j prec.eq.not v_i$ then every path in which $v_j$ occurs must also
contain $v_i$ and it must precede $v_j$. This means that not all
paths starting from the input sample can be used to classify the
input. For example in the graph of @example11 the path [$bold(b)$,
$bold(c)$] is not a valid because $bold(a) prec.eq bold(c)$ but
$bold(c) prec.eq.not bold(a)$ so this means that in every valid
path $bold(c)$ must be preceded by $bold(a)$. This observation leads
to the following definition fo a valid path:

#definition("Valid path")[
A path $cal(P)$ in a precedence graph is _valid_ if and only if
$forall v_i in cal(P)$:
$
 forall v_j in v_i.mono("predecessors") space v_j
 "is a predecessor of " v_i "in" cal(P)
$]

By this definition in the graph of @example11 only the edges
highlighted with the same color form valid path which are:

- [$bold(b)$, $bold(a)$,$bold(c)$]
- [$bold(a)$, $bold(b)$,$bold(c)$]

#prop[Every valid path starts with a vertex $v_i$ such that the sample
$s_i$ is one of the closest sample to the input $x$]<prop00>
#proof[Follows directly from the definition of valid path.]

#prop[If a vertex $v$ do not occur in a valid path $cal(P)$ and
every vertex in $v.mono("predecessors")$ is in $cal(P)$ then the path
$cal(P) + [v]$ is still valid.]<prop11>
#proof[Follows directly from the definition of valid path.]

#definition("Safe vertex")[A vertex satisfying the conditions of
@prop11 for a path $cal(P)$ is called a _safe_ vertex for $cal(P)$.]

#prop[Valid paths of length $k-1$ starting from vertices $v_i$ with
empty $v_i.mono("predecessors")$ contains the $k$ closest samples
from the input.]<prop12>
#proof[Notice that if the set $mono("predecessors")$ of a vertex $v_i$
  is empty it means that the associated sample $s_i$ is one of the
  closest sample to the input $x$ since $exists.not s_j in S "s.t."
  s_j prec.eq s_i "and" s_i prec.eq.not s_j$. Then the proposition
  follows directly from the definitions of a path in a graph and
  valid paths.]

The generation of paths is done by traversing the graph in the same
fashion of the BFS algorithm while respecting the condition of a
valid path. @path_generation shows how path are generated given the
the precedence graph $bb(G)_x$ and the desired length $n$ of the path.
The algorithm make use of a FIFO queue (the variable $var("queue")$)
to maintain the list of all valid paths of length less than $k < n$.
First it initialize the queue with the vertices having an empty set as
$mono("predecessors") $(lines $mono(1-2)$) which means the traversal
starts from the vertex associated with samples closest to the input
$x$. A counter $k$ which denotes the length of the paths in the queue
is initialized with 0 (line $mono(3))$. Then until the queue is not
empty extracts all the paths present in the queue and check whether
their length is equal to desired length (i.e the input *n*) and if
this is the case the it simply returns the extracted paths (lines
$mono(6-7)$) otherwise iteratively extend each path with every safe
vertex among the adjacent of the path's last vertex and add the
extended paths to the queue for the next iteration of the loop (lines
$mono(8-15))$. Before the next loop the counter $k$ is also
incremented to reflect the length of the paths in the queue (line
$mono(16))$.

#prop[Given as input the the precedence graph $bb(G)_x$ abd $n in
bb(N)$ @path_generation returns all the valid paths of length
#footnote[The convention used for path of length 0 is that it
contains only the starting vertex.] $n$ within $bb(G)_x$.]
<prop13>
#proof[
The proposition can be proved by showing, that at the $k$-th iteration
of the while loop at line 5 (ie. before the check on the length of the
paths on the queue), the queue contains all the valid path of length
$k-1$. We use induction on $k$ to prove this:

 - (*$k=1$*): In the first iteration of the loop the queue contains
   all the paths composed vertices with empty $mono("predecessors")$
   which are of length 0 and surely are valid by definition.

- (*$k=h+1$*): At iteration $h + 1$, the paths inside the queue at
  5 are obtained by extending all the paths in the queue in the $h$-th
  iteration with every safe vertex among the adjacent of the path's
  last vertex. By induction hypothesis the queue in the $h$-th
  iteration contains all the valid paths of length $h-1$ and so in the
  $h+1$ iteration the queue contains all the valid paths of length
  $h$.

This means when the method returns, at iteration $n$, the queue
contains all the possible valid path of length $n-1$.]

#algorithm(title: [$mono("generate_paths")$ method],
           output: ([Set of valid paths],),
           input: (
            [*$G_x$*: precedence graph,],
            [*n*: length of the path]
           ))[
  $var("closest_vertices") <- {[v_i] | v_i in bb(G)_x,space
  v_i.mono("precedence") = emptyset}$\
  $var("queue") <- func("create_queue", var("closest_vertices"))$\
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
samples $S$ and the input sample $x$ the algorithm first build the
precedence graph $bb(G)$ (line $mono(1)$). Then the
$mono("generate_paths")$ method is used to find the valid paths
of length length $k-1$ within the graph (line $mono(2)$).
Afterwards the set containing the most frequent labels within the
samples composing each path is computed and returned as the possible
classifications of the input sample (line $mono(3)$-$mono(8)$).

Since there could be multiple valid paths in the graph due to
samples in $S$ equidistant to the input, the latter could be
classified with different labels hence the need to return a set of
labels rather than a single value.

#theorem[Given a dataset $S = {(s^(i), y^(i)) | s^(i) in bb(R)^n,
y^(i) in bb(R)}$ and the input sample $x$, GKNN returns all
the possible classifications of the input $x$.]
#proof[
  GKNN compute the set of possible classification by finding the most
  frequent labels in the paths returned by the
  $mono("generate_paths")$ method which, by @prop12 and @prop13,
  returns all the possible $k$ closest samples to the input.
  Therefore GKNN surely returns all the possible classification of
  the input $x$.
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
    [*$x$*: the input sample],
    [*$S$*: samples dataset],
    [*$k$*: number of neighbours],
  ))[

  $bb(G)_x <-$  #func("create_precedence_graph", $S$, $x$)\

  $var("paths") <-$ #func("generate_paths", $bb(G)_x$, $k-1$)\
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
           input: ([*$S$*: samples dataset,],
                   [*$m$*: the minimum size of a partition]),
           output: ([BSP-Tree ],))[

  if $|S| <= m$ then#i\
   return #func("Leaf", $S$)#d\
  end\

  $var("left_dataset"), var("right_dataset"), var("hyperplane") <-
          func("split_dataset", S)$\

  $var("left_tree")<- func("build_bsp_tree",var("left_dataset"), m)$\
  $var("right_tree")<- func("build_bsp_tree", var("right_dataset"),
                            m)$\

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
           input: ([*$"BSP-T"$*: the BSP-Tree, ],
                   [*$x$*: the input query(point or hypershpere)]),
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
= Naive abstract classifier

In the abstract case there is the same datasets $S = {(s^(i),
y^(i)) | s^(i) in bb(R)^n, y^(i) in bb(R)}$ but the input query is
not a single point $x in bb(R)^n$ but instead is region of space.
around the point $x$. This region of space, denoted with P(x),
represents a (small) perturbation of the point $x$ and is defined as
the $ell_infinity$ ball centered in $x$ and radius $epsilon$:
$
 pert(x) = {x' | x' in bb(R)^n,space ||x'- x||_infinity <= epsilon}
$
In this case the abstract classifier $"AGKNN":  cal(P)(bb(R)^n) ->
cal(P)(cal(L))$ is a function that takes as input a region of space
(i.e, $pert(x)$) and outputs a set of labels. The condition that the
abstract classifier must satisfy is that it has to be a _sound
abstraction_ of the concrete classifier over the perturbation of the
input $x$ which means the returned set of labels must contains all the
output of the concrete classifier on each point of region that is
#block()[
  #set math.equation(numbering: "(1)")
  $
   "AGKNN"(R) supset.eq limits(union.big)_(x' in R) "GKNN"(x')
  $<output>
]

Computing $"AGKNN"(pert(x))$ by applying the concrete classifier to
each point of the perturbation is obviously unfeasible since it
contains an infinite number of points. But notice that the output of
the concrete classifier depends manly on the valid paths within the
precedence graph it builds. So by applying GKNN with a precedence
graph (i.e., the one created in line $mono(1)$ in @gknn-algh) that
contains all the valid paths of each graph constructed by the
concrete classifiers in @output, the output of AGKNN can be computed
because the number of valid paths to explore is finite. This leads to
@agknn-algh which shows the abstract classifier to be the same as
@gknn-algh with the only difference being the creation of the
precedence graph from which extracts the valid paths.

#algorithm(
  title: "AGKNN algoritm",
  output: ([Set of possible classification of $x$],),
  input: (
    [*$x$*: the input sample],
    [*$epsilon$*: the degree of perturbation],
    [*$S$*: samples dataset],
    [*$k$*: number of neighbours],
  ))[

  $bb(G)^A_(x) <-$  #func("create_abstract_precedence_graph",
                      $S$, $x$, $epsilon$)\

  $var("paths") <-$ #func("generate_paths", $bb(G)^A_(x)$, $k-1$)\
  $var("classification") <- {}$\
  for #var("path") in #var("paths") do#i\
    $var("labels") <- "most frequent labels in "mono("path")$\
    $var("classification") <- var("labels") union
                              var("classification")$#d\
  end\
  return #var("classification")
]<agknn-algh>

== Abstract precedence graph

Let $bb(G)^A_(x)$ be the (abstract) precedence graph build by AGKNN
when called with the perturbation $pert(x)$ and suppose for example
there are two samples $s_1, s_2 in S$ and points $x_1, x_2 in
pert(x)$ such that$
  cases(
    pre(s_1, s_2, x: "x1") "and" npre(s_2, s_1, x: "x1"),
    pre(s_2, s_1, x: "x2") "and" npre(s_1, s_2, x: "x2")
  )
$
that is $s_1$ is strictly closer to $x_1$ than $s_2$ while $s_2$ is
strictly closer to $x_2$ than $s_1$. In this case paths in which
$s_1$ is a predecessor of $s_2$ and those in which $s_2$ is a
predecessor of $s_1$ are valid paths in $bb(G)_(x_1)$ and
$bb(G)_(x_2)$ respectively and so they need to be both valid paths in
the abstract precedence graph $bb(G)^A_(x)$ as well. This leads to the
definition of the following relation between samples:

#definition([$attach(
prec.eq, tr: sscript(A), br: (x, epsilon))$ relation])[
Given $x in bb(R)^n, epsilon in bb(N)$ and $s_1 s_2 in S$
$
  s_1 attach(prec.eq, tr: sscript(A), br:(x, epsilon)) s_2
   arrow.l.r.double.long exists x_i in pert(x) space
  pre(s_1, s_2, x: x_i)
$
In the following, for ease of the notation, the subscript $epsilon$
will be dropped since it is assumed to be constant.]

By this definition $apre(s_1, s_2)$ and $apre(s_2, s_1)$ and so there
should be a edge between $bb(G)^A_(x)[s_1]$ and $bb(G)^A_(x)[s_2]$ in
both direction. Consequently just as the concrete precedence graph is
the graphical representation of the total order $(S, attach(prec.eq,
br: x))$, the abstract precedence graph is the graphical
representation of the total order $(S, attach(prec.eq, tr: A, br: x))
$. So the procedure $mono("create_abstract_precedence_graph")$ is the
same as @create_precedence_graph with the only difference that the
order relation used is $attach(prec.eq, tr: A, br: x)$.

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
Given a sample $s in S$
$
bb(G)^A_(x)[s].mono("predecessors") = limits(\u{22C2})_(x' in pert(x))
bb(G)_(x_i)[s].mono("predecessors")
$
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

== Soundness of the abstract classifier<sec-complete>

Given the perturbation $pert(x)$, the abstract classifier is said to
be _sound_ if the computed set of labels contains all the output of
the concrete classifier on each point of the perturbation that is when
$
limits(union.big)_(x' in pert(x)) "GKNN"(x')subset.eq"AGKNN"(pert(x))
$

#theorem("Soundness")[
Given a dataset $S = {(s^(i), y^(i)) | s^(i) in bb(R)^n, y^(i) in
cal(L)}$ and the perturbation $pert(x)$ of the input sample $x$, then
$
limits(union.big)_(x' in pert(x)) "GKNN"(x')subset.eq"AGKNN"(pert(x))
$
]
#proof[
Is suffice the show that the abstract precedence graph $bb(G)^A_(x)$
satisfy the condition
#block()[
  #set math.equation(numbering: "(1)")
$
 limits(union.big)_(x' in pert(x)) mono("valid_path")(bb(G)_(x_i))
 subset.eq
 mono("valid_path")(bb(G)^A_(x))
$<completeness>
]
where $mono("valid_path")(G)$ denotes the set of valid paths in
a graph G. Without loss of generality consider a valid path $p=[v_0,
v_1,dots,v_(k-1)]$ in $bb(G)_(x_i)$ for some $x_i in pert(x)$. By
definition of path in graph and $pre("", "", x: x_i)$ we have that
$
  apre(s_0, apre(s_1, apre(dots, s_(k-1))))
$
This means that $p$ is also a path in $bb(G)^A_x$. Moreover since $p$
is a valid path and, by @prop13, $forall v_i in p$
$
  bb(G)^A_(x)[s_i].mono("predecessors") subset
  bb(G)_(x_i)[s_i].mono("predecessors")
$
$p$ satisfy the conditions of being valid also for $bb(G)^A_(x)$ and
so $p in mono("valid_path")(bb(G)^A_(x))$
]

=== Incompleteness

In general the abstract classifier is sound but not _complete_ (or
_exact_). For example consider the set of samples:

- *$s_0$*: (0.75, 1.3)
- *$s_1$*: (1.0, 1.3)
- *$s_2$*: (1.25, 1.3)

and the input perturbation $pert((1,1))$ with $epsilon = 0.05$.
@incomplete-example a) shows the plot of the samples and the
perturbation region while @incomplete-example b) illustrate the
abstract graph. It easy to see that in this case the valid paths in
the abstract precedence graph are the permutations of the sequence of
vertices $[bold(v_0), bold(v_1), bold(v_2)]$ in particular:

+ $[bold(v_0), bold(v_1), bold(v_2)]$
+ $[bold(v_0), bold(v_2), bold(v_1)]$

but there is no $x'in pert(x)$ such that second path is a valid path
in $bb(G)_x'$. This is because the regions of space containing the
points closer the sample $s_0$ (i.e. the blue region) and the one
with point closer to sample $s_2$ than $s_1$ (i.e. the green region)
do not intersect.

The only case in which the abstract classifier is complete is when
$k = 1$ because in that case the vertex $v_i$ that can occur in a
valid path is the one for which there is point $x_i in pert(x)$ such
$s_i$ is the closest sample to $x_i$.

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

      plot.annotate(content((0.76,1.37), [$v_0$]))
      plot.annotate(content((1.01,1.37), [$v_1$]))
      plot.annotate(content((1.26,1.37), [$v_2$]))
      plot.annotate(content((1.02,1.05), [$x$]))

    })
  })]],
  [ #v(50pt)#align(center)[#render("
  digraph {
    v_0 -> v_1
    v_1 -> v_0
    v_0 -> v_2
    v_2 -> v_0
    v_1 -> v_2
    v_2 -> v_1
    {rank=same v_0, v_1}
  }"
)]],

  [a) Plot of dataset and perturbation],
  [b) Abstract precedence graph]), caption: [Example of incompleteness]
)<incomplete-example>

== Graph construction optimization

Since in the abstract case the query is the perturbation of the input
rather the a single point, the algorithm to reduce the set of sample
used for the precedence graph construction needs to be changed. The
only difference with the concrete counterpart is the step 4) because,
in order to ensure the soundness of the abstract classifier, the
hypershpere must contain all the $k$ closest sample of each point in
the perturbation.

In order to find the minimum radius $r$ of the hypershpere consider
the $k$ closest sample $A = {s_0, s_1, dots, s_(k-1)}$ to the input
$x$ and let $s_k$ be the furthest sample from $x$ with distance $d$.
Now consider a generic point $x' in pert(x)$ and the hypershpere
$H_x'$ centered in $x'$ and radius the distance between $x'$ and
$s_x' = limits("argmax")_(s_i in A) ||x'- s_i||_p$. Surely the
set of samples in $H_x'$ is $A union B$ where B is the set (possibly
empty) of samples closer to $x'$ than any sample in $A$. So the
enclosing hypershpere $H$ of all the hyperspheres $H_x'$ for every
$x' in pert(x)$ is the one that surely contains all the $k$ closest
sample of each point in the perturbation.

Notice that given a points $y in bb(R)^n$ and  $x'in pert(x)$
$
  ||x' - y||_p <= ||x - x'||_p + ||x - y||_p
$
due to the triangular inequality property of norms. So this means that
for every $x'in pert(x)$
$
  ||x' - s_x'||_p  <= ||x - x'||_p + ||x -  s_x'||_p <=
  sqrt(n) dot epsilon + d
$
where $s_x' = limits("argmax")_(s_i in A) ||x'- s_i||_p$.

So the hypershpere of interest $H$ is centered in the input $x$ and
has radius $2epsilon sqrt(N) + d$.

// #figure([#align(center)[#cetz.canvas({
//     import cetz.draw: *
//     import cetz.plot
//     import cetz.palette

//     set-style(axes:(tick: (minor-length: 5pt)))
//     grid((0,0), (10, 10), help-lines:true, step: .5)
//     rect((4.5, 4.5), (5.5, 5.5), fill: rgb(0,0,0,50), stroke: gray)
//     circle((5,5), radius: 0.08, fill: red, stroke: none)
//     content((5.2, 5.2), [$x$])
//     circle((7,7), radius: 0.05, fill: black)
//     content((7.3, 7.3), [$s_k$])

//     circle((6,4), radius: 0.05, fill: black)
//     circle((5.3,4.9), radius: 0.05, fill: black)

//   })]], caption: [hypershpere radius])<hypersphere>


= A better abstract classifier

One issue with the naive abstract classifier is that there are cases
in which is not efficient. For example consider the case in which
there are $n$ samples equidistant from the perturbation $pert(x)$
then in this case the abstract classifier contains at least
$
  n! / (n-k)!
$
valid paths which for just $n=10$ and $k=7$ is already over $10^6$
making the naive abstract classifier quite inefficient. The problem
with the naive abstract classifier approach is that it explicitly
enumerate all the possible paths before classifying the input but is
not necessary do so. Notice that the classification of the input does
not depend on the order of the $k$ closest samples but only on the
number of occurrences of each label. This means that paths can be
also be represented as set of vertices rather than a sequence.
Moreover samples with the same labels are equivalent from the
classification point of view. For example suppose in the previous
example $n=10$, $k=7$ and among the $n$ samples
- 6 samples have the label $l_1$;
- 3 samples have the label $l_2$;
- 1 samples have the label $l_3$
then is easy to see that in any valid paths made by the equidistant
samples at least 3 samples have label $l_1$ and since at most 3
samples can have label $l_2$ the possible classifications of the
input are the labels $l_1$ and $l_2$.

This observations suggests a more efficient representation for a set
of valid paths in $bb(G)^A_x$. For example consider an abstract
precedence graph $bb(G)^A_x = ({v_0, v_1,v_2, v_3}, E)$ such
that:

 - $V_emptyset = {v_0, v_1}$

 - $V_({v_0}) = {v_2, v_3}$

where $V_B = {v in V | v.mono("predecessors") = B}$. With this setup
the set of valid paths of length 2 contains the following paths:

 - $P_1 = {v_0, v_2, v_1}$
 - $P_2 = {v_0, v_1, v_3}$
 - $P_3 = {v_0, v_2, v_3}$

Now suppose the tuple $(B, R, n) in cal(P)(V)times cal(P)(V)times
bb(N^+)$ where $R subset.eq B$ and $|R| <= n <= |B|$ denotes the set
of subsets of $B$ of size $n$ containing the set $R$ then the set
$
  A_p_(12) = {A_0 union A_1 | (A_0, A_1) in (V_emptyset, {v_0}, 2)
                  times (V_({v_0}), emptyset, 1)}
$
contains exactly the path $P_1$ and $P_2$ since:

- $(V_emptyset, {v_0}, 2) = {{v_0, v_1}}$

- $(V_({v_0}), emptyset, 1) = {{v_2}, {v_3}}$

Similarly the set
$
  A_p_(3) =  {A_0 union A_1 | (A_0, A_1) in (V_emptyset, {v_0}, 1)
                  times (V_({v_0}), emptyset, 2)}
$
contains exactly the path $P_3$ as:

- $(V_emptyset, {v_0}, 1) = {{v_0}}$

- $(V_({v_0}), emptyset, 2) = {{v_2, v_3}}$

This example illustrates a way of representing a set of paths
more efficiently without enumerating all of them. Essentially the
idea is create sets like $A = {(B_i, R_i, n_i)}_ (i in {1,dots,n})$
containing $n$ tuples $(B_i, R_i, n_i) in cal(P)(V) times cal(P)(V)
times bb(N^+)$ such that  $sum_(i=1)^(i=n) = k$. More formally

#definition([Abstract vertex])[Given the abstract precedence graph
$bb(G)^A_x=(V, E)$ the tuple $v^A = (B, R, n) in (cal(P)(V) without
emptyset) times cal(P)(V) times bb(N^+)$ such that $R subset.eq B$
and $|R|<= n <= |B|$ is called an _abstract vertex_ and represents a
set of set of vertices, denoted with $angle.l v^A angle.r$, which is
defined as
$
  angle.l v^A angle.r =  {{v_0,v_1,dots,v_(n-1)} subset.eq B | R
  subset.eq {v_0, v_1,dots v_(n-1)} }
$
Basically $angle.l A, R, n angle.r$ denotes the set of subsets of $A$
of size $n$ containing the set $R$. ]

#definition[Given an abstract vertex $v^A = (B, R, n)$:
   - $setv(v^A)$ is the underlying set of vertices of the abstract
      vertex that is $setv(v^A) = B$.
   - $reqv(v^A)$ are the required vertices in every set of vertex in
      $angle.l v^A angle.r$ which means $reqv(v^A) = R$.
   - $lenv(v^A)$ is the size of the sets in $angle.l v^A angle.r$
      that is $lenv(v^A) = n$
]

#definition([Abstract Path])[Given the abstract precedence graph
$bb(G)^A_x=(V, E)$ the set $sans(P)^A = {v^A_i}_ (i in {1,dots,n}) in
cal(P)((cal(P)(V) without emptyset) times cal(P)(V) times bb(N^+))$
containing $n$ abstract vertices is called an _abstract path_ and
represents a set of paths in $bb(G)^A_x$, denoted with
$angle.l.double sans(P)^A angle.r.double$, which is defined as
$
  angle.l.double sans(P)^A angle.r.double = {
    limits(union.big)_(1<=i<=n) V_i | (V_1, V_2,dots, V_n) in
    angle.l v^A_1 angle.r times angle.l v^A_2 angle.r times dots
    times angle.l v^A_n angle.r
  }
$
Essentially $angle.l.double sans(P)^A angle.r.double$ contains the
sets of vertices obtained by taking the union of the sets of vertices
in the cartesian product $angle.l v^A_1 angle.r times angle.l
v^A_2 angle.r times dots times angle.l v^A_n angle.r$.]

#definition[Given an abstract path $sans(P)^A = {v^A_i}_ (i in
{1,dots,n})$
   - $setp(sans(P)^A)$ is the set containing the underlying set of
      each abstract vertex in $p^A$ that is $setp(p^A) = {setv(v^A) |
      v^A in p^A}$

   - $reqp(sans(P)^A)$ is the set comprising the required vertices of
      each abstract vertex in $p^A$ that is $reqp(p^A) = {reqv(v^A) |
      v^A in p^A}$

   - $lenp(sans(P)^A)$ is the length of the abstract path and
      represent the length the paths in $angle.l.double sans(P)^A
      angle.r.double$ that is $lenp(sans(P)^A) =
      limits(sum)_(i=0)^(i=n) lenv(v^A_i)$.

]

So following this definitions:

$A_p_(12) = lr(angle.l.double { (V_emptyset, {v_0}, 2),
             (V_({v_0}), emptyset, 1)} angle.r.double) "and"
  A_p_(3) = lr(angle.l.double { (V_emptyset, {v_0}, 1),
             (V_({v_0}), emptyset, 2)} angle.r.double)$


== Abstract paths generation

For a given abstract precedence graph $bb(G)^A_x=(V, E)$ not all
abstract paths contains exclusively paths that are also valid. To
ensure that this is the case, the set of vertices is partitioned
according to the value of the $mono("predecessors")$ attribute. So if,
given a subset $B subset.eq V$ of size $i$,
$
  V^i_B = {v in V | V.mono("predecessors") = B}
$
then partition is equal to the following set
$
  V S = {V^0_B_(01), V^1_(B_11), V^1_(B_12), dots,V^1_(B_(1i_1)),
  V^2_(B_21),dots, V^2_(B_(2i_2)),dots, V^m_(B_(m 1)),dots,
  V^m_(B_(m i_m))}
$
Afterwards the abstract paths are constructed using abstract vertices
$v^A = (A, R, n)$ such that $A in V S$ leading to the
addition of the following utility function:

- $predv(v^A)$ denotes the set of predecessors of the vertices in
  $setv(v^A)$ that is if $setv(v^A) = V^i_B$ then $predv(v^A) = B$

With this setup a valid abstract paths is defined as:

#definition([Valid abstract path])[Given the abstract precedence graph
$bb(G)^A_x=(V, E)$ an abstract path $sans(P)^A = {v^A_i}_(i in
{1,dots,n}) in cal(P)(V S times cal(P)(V) times  bb(N^+))$ is _valid_
if every path in $angle.l.double A angle.r.double$ is also valid
which occurs when for every $v_0^A in sans(P)^A$ the following
conditions are satisfied

  + $predv(v_0^A) subset.eq limits(union.big)_(v_i^A in sans(P)^A)
    setv(v_i^A)$

  + $forall v^A in sans(P)^A quad predv(v_0^A) sect setv(v^A)
     subset.eq reqv(v^A)$

The condition above essentially means that for every vertex $v$ in a
path $p in angle.l.double sans(P)^A angle.r.double$ the predecessors
of $v$ are also present in $p$.]<validpath>

Moreover, similarly to the concrete case, not every abstract vertex
$v^A$ is _safe_ for a valid abstract path $sans(P)^A$ in the sense
that it could happen that by adding $v^A$ to $sans(P)^A$ the abstract
path is no more valid. This lead to the following definition

#definition([Safe abstract vertex])[Let $sans(P)^A = {v^A_i}_ (i in
{1,dots,n})$ be a valid abstract path for a given  abstract
precedence graph $bb(G)^A_x=(V, E)$. The abstract vertex $v^A$ is
safe for $sans(P)^A$ if the following conditions are satisfied:

- $underline(setv(v^A) in setp(sans(P)^A))$: In this case let $v_0^A
  in sans(P)^A$ such that $setv(v^A) = setv(v_0^A)$ then $v^A$ is
  safe for $sans(P)^A$ if and only if $reqv(v^A) = emptyset$ and
  $lenv(v^A) + lenv(v_0^A) <= setv(v^A)$.

- $underline(setv(v^A) in.not setp(sans(P)^A))$: In this cases $v^A$
  is safe for $sans(P)^A$ if and only if the following conditions are
  satisfied:

    + $predv(v^A) subset.eq limits(union.big)_(v_i^A in sans(P)^A)
    setv(v_i^A)$

    + $ forall v_0^A in sans(P)^A quad lenv(v_0^A) >= |(reqv(v_0^A)
        union predv(v^A)) sect setv(v_0^A)| $

  Essentially together the two conditions above states it must exists
  a set in $angle.l.double sans(P)^A angle.r.double$ that contains
  $predv(v^A)$.]<safeabs>

@safeabs only states the conditions that must be satisfied so that
an abstract vertex can be added to an abstract path but after the
addition the existing elements of the abstract path needs to be
changed in order to satisfy the conditions of the @validpath.
@extend_abs_path shows how an abstract path $sans(P)^A$ is extend
with an abstract vertex $v^A$. It stars by first creating a copy, the
variable $var("new_path")$, of the abstract path $sans(P)^A$ (line
$mono(1)$) and then check whether $v^A$ is a safe vertex for
$sans(P)^A$. If it is not safe then simply return the copied path
unaltered (line $mono(2-3)$) otherwise if exists an abstract vertex
$v in var("new_path")$ such that $setv(v) =  setv(v^A)$ then increase
the size of the set of vertices in $angle.l v angle.r$ by $lenv(v^A)$
(line $mono(4-6)$). On the other hand if no abstract vertex in
$var("new_path")$ has the same underlying set as $v^A$ then for each
abstract vertex $v_i^A in var("new_path")$ adds to $reqv(v_i^A)$ the
vertices in $predv(v^A)$ that also belong to $setv(v_i^A)$ (line
$mono(7-10)$). Finally extends $var("new_path")$ with the new abstract
vertex $v^A$ before returning it (line $mono(11-12)$).

#algorithm(
  title: "extend_abs_path method",
  output: ([$sans(P)^A$ extend with $v^A$ satisfying the conditions of
            @validpath],),
  input: (
    [*$sans(P)^A$*: An abstract path,],
    [*$v^A$*: An abstract vertex],
  ))[

  $var("new_path") <- sans(P)^A$ \

  if not #func("safe", $sans(P)^A$, $v^A$) then#i\
    return #var("new_path")#d\
  end\

  if $setv(v^A) in setp(var("new_path"))$ then#i\
    $v_0^A <- v in sans(P)^A$ such that $setv(v) = setv(v^A)$\
    $lenv(v_0^A) <- lenv(v_0^A) + lenv(v^A)$#d\

  else#i\
    for $v_i^A$ in $var("new_path")$ do#i\
      $reqv(v_i^A ) <- reqv(v_i^A ) union (predv(v^A) sect
                       setv(v_i^A))$#d\
    end\
    $var("new_path") <- var("new_path") union {v^A}$#d\
  end\

  return #var("new_path")
]<extend_abs_path>

#prop[For every valid abstract path $sans(P)^A$ and abstract vertex
$v^A$, $mono("extend_path")(sans(P)^A, v^A)$ is
always a valid abstract path.]<prop41>
#proof[Let $sans(P)_1^A = mono("extend_path")(sans(P)^A, v^A)$. By
definition if $v^A$ is not a safe for $sans(P)^A$ then $sans(P)_1^A$
is simply an unaltered copy of $sans(P)^A$ which is valid by
hypothesis otherwise for every abstract vertex $v_i^A in sans(P)_1^A$:
#align(center)[$(predv(v^A) sect setv(v_i^A)) subset.eq reqv(v_i^A)$]

Since for every $v_i^A in sans(P)_1^A$ $setv(v_i^A)$ is not modified
and $reqv(v_i^A)$ is only augmented this means that the conditions of
@validpath are satisfied and so in both cases $sans(P)_1^A$ is a
valid abstract path.]

#prop[Let $sans(P)^A$ and $v^A$ be a valid abstract path and abstract
vertex respectively and let $sans(P)_1^A = mono("extend_path")(
sans(P)^A, v^A)$. If $v^A$ is not safe for $sans(P)^A$ then
$lenp(sans(P)_1^A) = lenp(sans(P)^A)$ otherwise
$lenp(sans(P)_1^A) = lenp(sans(P)^A) + lenv(v^A)$.]<prop42>
#proof[
by definition of $mono("extend_path")$ if $v^A$ is not safe for
$sans(P)^A$ then $sans(P)_1^A = sans(P)^A$ and so
$lenp(sans(P)_1^A) = lenp(sans(P)^A)$. If $v^A$ is safe then
$sans(P)_1^A = sans(P)^A union {v^A}$ and so
$
  lenp(sans(P)_1^A) = lenp(sans(P)^A) + lenv(v^A)
$
by definition of the $mono("len")^star$ function.
]

The method $mono("extend_path")$ is used for the generation of
abstract paths of length $k$. @generate_abs_paths shows how, given
an abstract precedence graph $G_x^A = (V, E)$ and the length $k$, the
abstract paths of length $k$ are generated. It make use of three
quantities:
 - The variable $n$, which denotes the length of the abstract paths
   being created.
 - The variable #var("abs_vertices") which is a set containing the
   abstract vertices that will be used to extend the abstract paths.
 - The variable #var("abs_paths") which is a set containing the
   abstract paths being generated.

The algoritm starts by initializing the variable $n$ with 0,
#var("abs_vertices") with the set containing all the abstract vertices
$v^A$ such that
  - $setv(v^A) = V_B eq.not emptyset$ where  $V_B = {v in V|
    v.mono(("predecessors") = B)}$ for some $B subset.eq V$
  - $reqv(v^A) = emptyset$
  - $lenv(v^A) = 1$
and #var("abs_paths") with a set containing the valid abstract path of
length 1 (lines $mono("1-3")$). Then repeat indefinitely the following
(lines $mono("4-17")$):

  + Increase $n$ by 1 and check wether the paths in #var("abs_paths")
    are of the desired length $k$ and if this is the case then simply
    return the set #var("abs_paths") (lines $mono("5-8")$).

  + Construct a new set of abstract paths by extending each abstract
    path in #var("abs_paths") with the safe abstract vertices in
    #var("abs_vertices") through the method $mono("extend_abs_path")$
    and afterwards assign it to #var("abs_paths")
    (lines $mono("9-16")$).

#algorithm(
  title: "generate_abstract_paths method",
  output: ([Set of abstract paths of length $k$],),
  input: (
    [*$G_x^A$*: An abstract precedence graph, ],
    [*$k$*: Required length of the abstract path],
  ))[

  $var("n") <- 0$\
  $var("abs_vertices") <- {(V_B, emptyset, 1) | B in V}  without
                          {(emptyset, emptyset, 1)}$\
  $var("abs_paths") <- {{(V_emptyset, emptyset, 1)}}$\

  while true do#i\

    $var("n") <- var("n") + 1$\
    if $var("n")$ = *k*#i\
        return #var("abs_paths")#d\
    end\

    $var("new_abs_paths") <- emptyset$\

    for #var("abs_vertex") in #var("abs_vertices") do#i\
      for #var("abs_path") in #var("abs_paths") do#i\

        $var("new_abs_path") <- func("extend_path", var("abs_path"),
                                      var("abs_vertex"))$\
        if $var("new_abs_paths") eq.not #var("abs_path")$#i\
          $var("new_abs_paths") <- var("new_abs_paths") union
                                   {var("new_abs_path")}$#d\
        end#d\
      end#d\
    end\

    $var("abs_paths") <- var("new_abs_paths")$\
    end#d\
  end
]<generate_abs_paths>

#prop[@generate_abs_paths generates all the valid abstract paths of
the desired length $k$.]
#proof[
The proposition can be proven by showing that in the $i$-th iteration
of the while loop, at line $mono(5)$ (i.e. before the check on the
length) the #var("abs_paths") contains all the valid abstract path of
length $i$. We use induction on $i$:

  - $underline((i = 1))$: In the first iteration #var("abs_paths")
    contains only the abstract path ${(V^0_emptyset, emptyset, 1)}$
    which is valid by definition. Moreover it is easy to see that is
    also the only valid path of length 1.

  - $underline((i = h+1))$: Let $H$ be the set #var("abs_paths") in
    the $h$-th iteration. So in the $h+1$-th iteration the abstract
    paths in #var("abs_paths") are obtained by extending each paths in
    $H$ with all the possible safe abstract vertices $v^A$ with
    length 1 and $reqv(v^A) = emptyset$. By induction hypothesis
    every abstract path in $H$ are valid with length $h$ and so, by
    @prop41 and @prop42 each path in #var("abs_paths") is also valid
    and has length $h+1$. This means that #var("abs_paths") contains
    all the valid abstract path of length $h+1$

So at iteration $k$ of the while the algorithm returns all the valid
abstract paths of the desired length $k$.]

#prop[Given an abstract precedence graph $G_x^A = (V, E)$ and $k in
bb(N^+)$ let $A P_k$ be the set of valid abstract paths of length $k$
(i.e. $A P_k = mono("generate_abs_paths")(G_x^A, k)$). Then the set
$
  C P_k = limits(union.big)_(P_i^A in A P_k) angle.double.l P_i^A
        angle.double.r
$
contains all the possible valid paths of length $k-1$ in $G_x^A$.
]<prop44>

#proof[The proposition can be proved using induction on the length
$k$ of the abstract paths in $A P_k$:

   - $underline((k = 1))$: In this case $A P_k = {{(V_emptyset,
     emptyset, 1)}}$ and by definition of the $angle.double.l dot
     angle.double.r$ operator
     $
      C P_k = angle.double.l {(V_emptyset, emptyset, 1)}
       angle.double.r = {{v} | v in V_emptyset} = {{v} | v in V and
                               v.mono("predecessors") = emptyset}
     $

     So $C P_k$ contains all the paths made of a single vertex $v in
     V$ such that $v.mono("predecessors") = emptyset$ which by
     definition are valid and with length $k-1$.

   - $underline((k = h + 1))$: In this case, by definition of the
     method $mono("generate_abs_paths")$ and because $A P_k =
     mono("generate_abs_paths")(G_x^A, k)$, the abstract paths in
     $A P_k$ are obtained by extending each path in $A P_h =
     mono("generate_abs_paths")(G_x^A, h)$, where $h in bb(N^+)$, with
     all the possible safe abstract vertices in the set
     $
        A V = {(V_B, emptyset, 1) | B in V}  without
              {(emptyset, emptyset, 1)}
     $

     This means that, following the definition of $angle.double.l dot
     angle.double.r$ operator and safe abstract vertex
     $
        C P_k = {sans(P) union {v} | sans(P) in C P_h and
                exists thin v^A in A V "s.t." predv(v^A) subset.eq
                sans(P) and v in angle.l v^A angle.r}
     $
     In other words $C P_k$ is obtained by adding every safe vertex
     $v in V$ to each path of $C P_h$. By induction hypothesis $C P_h$
     contains all the valid paths of length $h-1$ so it follows that
     $C P_k$ will contains all the valid paths of length $h=k-1$
]

== Classification

For the classification of the input once all the abstract path of
length $k$ are generated, it is necessary to compute all the possible
occurrences of labels in the paths represented by the abstract paths.
To do so let $mono("labels"): (cal(P)(V) without emptyset) times
cal(P)(V) times bb(N^+) -> cal(P)(cal(P)(V times bb(N^+)))$ be a
function that given an abstract vertex $v^A$ yields a set whose
elements are multisets (or bag) @MSet quantifying the occurrences of
each label found in some vertex sets within $angle.l v^A angle.r$.
To understand how the function $mono("labels")$ is defined notice
that an element $A$ of $angle.l v^A angle.r$ is the union of the set
$reqv(v^A)$ and a subset $B$ of $setv(v^A) without reqv(v^A)$ with
size $lenv(v^A) - |reqv(v^A)$|. So if $R_L$ and $B_L$ are the
multisets containing the labels in $reqv(v^A)$ and $setv(v^A) without
reqv(v^A)$ respectively then the function $mono("labels")$ is defined
as
$
  mono("labels")(v^A) = {R_L plus.circle B | &B subset.eq B_L}
$
where $plus.circle$ is the sum operation between multisets.

With the function $mono("labels")$ its easy to define the function
$mono("labels")^(star)$ that given an abstract path $sans(P)^A$
return a set of multisets each expressing the occurrences of the
labels in a path within $angle.l.double sans(P)^A angle.r.double$.
So given the abstract path $sans(P)^A = {v^A_i}_(i in {1,dots,n})$
the function $mono("labels")^(star): cal(P)(cal(P)((cal(P)(V) without
emptyset) times cal(P)(V) times bb(N^+))) -> cal(P)(cal(P)(V times
bb(N^+)))$ is defined as
$
  mono("labels")^(star)(sans(P)^A) = {A_0 plus.circle A_1 plus.circle
   dots plus.circle A_n | A_i in mono("labels")(v^A_i), i in
   {1,dots,n}}
$

Once all the multisets are generated then all the possible
classifications of the input are the most frequent labels in each
multisets.

== Abstract classifier

@abs_classifier illustrate how the abstract classifier works which
is not too much different from the naive abstract classifier. Given
as input the set of samples $S$, the input $x$ to be classified, the
degree of perturbation $epsilon$ applied to the input and the number
$k$ of neighbours to consider for the classification, the algorithm
starts by creating the abstract precedence graph $bb(G)^A_x$ (line
$mono("1")$) which is then used to generate all the possible valid
abstract paths of length $k$ (line $mono("2")$). Afterwards the set
containing all the possible classification of the input $x$ is
constructed which is then return at the end (line $mono("3-11")$).
To do so, for each abstract path generated before, the multisets
expressing all the possible occurrences of each label is computed and
then the most frequent labels are collected from each multiset (line
$mono("5-10")$).

#algorithm(
  title: "AGKNN2 algorithm",
  output: ([Set of possible classifications of the input],),
  input: (
    [*$x$*: the input sample],
    [*$epsilon$*: the degree of perturbation],
    [*$S$*: samples dataset],
    [*$k$*: number of neighbours],
  ))[

  $bb(G)^A_x <-$  #func("create_abstract_precedence_graph",
                      $S$, $x$, $epsilon$)\

  $var("abs_paths") <- func("generate_abstract_paths", bb(G)^A_x, k)$\
  $var("classifications") <- emptyset$\
  for #var("abs_path") in #var("abs_paths") do#i\
    $var("abs_path_labels")<-bold("labels"^(star))(var("abs_path"))$\
    for #var("labels") in #var("abs_path_labels") do#i\
      $var("most_frequent") <- "most frequent labels in"
                               var("labels")$\
      $var("classifications") <- var("classifications") union
                                {var("most_frequent")}$#d\
    end#d\
  end\
  return #var("classifications")
]<abs_classifier>

#theorem[Given the dataset $S = {(s^(i), y^(i)) | s^(i) in bb(R)^n,
y^(i) in cal(L)}$ and the perturbation $pert(x)$ of the input sample
$x$, AGKNN and AGKNN2 are equivalent that is for every $k in bb(N^+)$
and $epsilon in bb(R)$
$
  "AGKNN"(x, epsilon, S, k) = "AGKNN2"(x, epsilon, S, k)
$]
#proof[The equivalence derive from the fact that both AGKNN and
AGKNN2 classify the input by computing the most frequent labels in
every valid path of length $k-1$. This is valid for AGKNN because it
is an explicit part of its definition while AGKNN2 indirectly
accomplishes this due to @prop44, since the set of all abstract valid
path of length $k$ is representative of  all valid paths of length
$k-1$, therefore AGKNN2 inherently considers the full spectrum of
label frequencies found within any valid path of length $k-1$.]

== Comparison with NAVe

Some comparisons with Nave tool with perturbation $epsilon = 0.01$ and
interval domain.



#tablex(
  columns: 9,
  align: center + horizon,
  auto-vlines: false,
  repeat-header: true,
  header-rows: 2,

  /* --- header --- */
  rowspanx(2)[*Dataset*],
  colspanx(2)[*Runtime (mm:ss)*], (), (),
  rowspanx(2)[],
  colspanx(2)[*Stability*], (),
  rowspanx(2)[],
  colspanx(2)[*Robustness*], (),

  (), [*NAVe*], [*AGKNN2*], (), [*NAVe*], [*AGKNN2*],
  (), [*NAVe*], [*AGKNN2*],
  /* -------------- */
  rowspanx(5)[Fourclass],rowspanx(5)[00:01], rowspanx(5)[00:09],
  [k=1], [99.2], [99.6], [], [99.2], [99.6],
  [k=2], [98.4], [98.4], [], [98.4], [98.4],
  [k=3], [99.6], [99.6], [], [99.6], [99.6],
  [k=5], [98.4], [98.8], [], [98.4], [98.8],
  [k=7], [97.7], [98.4], [], [97.7], [98.4],
  rowspanx(5)[Pendigits],rowspanx(5)[10:16], rowspanx(5)[09:54],
  [k=1], [96.7], [97.7], [], [95.6], [96.4],
  [k=2], [94.0], [95.3], [], [93.3], [94.5],
  [k=3], [96.1], [97.8], [], [95.3], [96.6],
  [k=5], [95.7], [97.7], [], [94.9], [96.4],
  [k=7], [95.0], [97.6], [], [94.1], [96.2],
  rowspanx(5)[Letter],rowspanx(5)[37:44], rowspanx(5)[30:33],
  [k=1], [82.7], [88.6], [], [82.2], [87.8],
  [k=2], [70.4], [78.4], [], [70.4], [78.3],
  [k=3], [75.1], [85.9], [], [75.0], [85.5],
  [k=5], [69.5], [83.5], [], [69.4], [83.0],
  [k=7], [65.2], [82.1], [], [65.1], [81.7]
)


#pagebreak()
#bibliography("bibliography.bib")

# Formally verified 3D mesh intersection - trust 93 lines of spec, not 1000+ lines of AI-written code

To my knowledge, this is the first formally verified implementation of a 3D constructive solid geometry (CSG) operation: mesh intersection, implemented in Lean 4 and verified against [a concise specification](#background-and-formalization) that pins down the surface of the resulting mesh exactly and guarantees practical well-formedness conditions on the triangulation. (See also [related work](#related-work).)

This project is also an experiment in avoiding having to trust AI-generated code. A human reviewer only needs to read [93 lines of formal specification](#minimal-human-review-without-trusting-ai) and run the Lean checker [as described below](#building-and-checking) to certify the correctness of the kernel, skipping the [intricate](#special-cases) 1000+ lines of AI-written implementation. To prove correctness, AI autonomously wrote over 60,000 lines of Lean proofs, which also never have to be inspected by a human. The Lean checker guarantees conformance to the specification at compile time, with zero trust placed in any LLM. This allows us to treat the implementation and proofs as a black box. I guided the agent through the milestones described [below](#development) to arrive at the result presented here.

## Web demo

Try out the [web demo](https://schildep.github.io/verified-3d-mesh-intersection) built around the verified kernel, where you can intersect example meshes or import and intersect meshes from STL files. The compiled Lean code runs locally in your browser; no data is ever sent to a server. Note that while the kernel is formally verified, the UI and glue code are not.

Our implementation is far slower than state-of-the-art mesh intersection implementations: it takes 24 seconds to compute the exact intersection of two 70k-triangle Stanford bunnies. In this project we prioritize minimizing the effort of human review of correctness over performance. Note that this performance gap is not a fundamental limitation of formally verified software, which can in principle be as fast as conventional software. See [details](#performance).

![Intersection of Stanford bunny with Stanford bunny](readme-assets/intersection-bunny-watertight-bunny-watertight.png)

The output meshes are guaranteed to satisfy the properties described below, but the meshing may be suboptimal with respect to other criteria that we did not yet formalize; for example, it may produce a mesh that is finer than necessary.

## Background and formalization

A triangle mesh is a set of triangles, usually expected to form a closed surface that does not penetrate itself, among other well-formedness conditions we will discuss below.

Humans intuitively associate triangle meshes with a "solid", i.e. a volume in 3D space: the set of all points not on the surface but "inside" the mesh. ("Inside" can be described mathematically by signed ray intersection counting.)

![The set of points inside a mesh. Visualization of cross section and signed ray intersection test to determine if a given point is inside the solid.](readme-assets/cube-with-holes-points-inside.png)

This concept of solids allows us to understand what the output of algorithms such as a mesh intersection algorithm should look like, even when the implementation that works on the actual mesh data structure is intricate and has to treat [many geometrical special cases](#special-cases) with dedicated code.

From a mesh intersection algorithm, we expect that the set intersection of the solids of well-formed input meshes is the solid of the output mesh and that the output is a well-formed mesh again. (We also expect that the algorithm detects and reports correctly if the inputs are not well-formed.)

```lean
solid (meshIntersect M₁ M₂) = solid M₁ ∩ solid M₂
```

This [pins down](CSG/Example.lean) the surface of the resulting mesh exactly as the boundary of the intersected solids.

![Mesh intersection of a cube with holes and an approximated sphere](readme-assets/intersection-cube-with-holes-approximate-sphere.png)

![2D cross section visualization](readme-assets/intersection-cube-with-holes-approximate-sphere-cross-section.png)

Algorithms working on triangle meshes can efficiently compute meshes representing solids we have in mind, but conventional programming languages cannot express "solids" explicitly or make statements about them, since these are infinite sets. In Lean this is possible and we can for example intersect such infinite sets or prove that two infinite sets are equal. Moreover, Lean allows us to prove that a function satisfies a condition for all possible input meshes, whereas conventional programming languages only allow us to test that the function satisfies a condition for specific inputs.

We define well-formedness of meshes to capture the conditions commonly expected by real-world mesh processing tools - watertight surface, bounding a solid with multiplicity one with coherent outward orientation, no degenerate triangles, no self-intersections - with one relaxation: the surface may touch itself, not at the interiors of faces but along edges and vertices. So strict 2-manifoldness is not required. See [why an intersection algorithm that always produces manifold meshes is not possible](#why-we-cannot-have-manifold-output-meshes-in-general).

## Minimal human review without trusting AI

In order to certify correctness of the kernel, which checks the well-formedness preconditions of the inputs and computes the mesh intersection, a reviewer only needs to read 93 lines of formal specification and run the Lean checker [as described below](#building-and-checking). The reviewer can skip the intricate 1000+ lines of AI-written implementation of the algorithm. The Lean checker guarantees conformance to the specification at compile time, with zero trust assumptions on any LLM.
- It suffices to read the files [`CSG/DataStructures.lean`](CSG/DataStructures.lean), [`CSG/Def.lean`](CSG/Def.lean), [`CSG/MeshIntersectWithPreconditionCheck.lean`](CSG/MeshIntersectWithPreconditionCheck.lean) and [`CSG/WellFormedCheckMsg.lean`](CSG/WellFormedCheckMsg.lean) and run the Lean checker as described below. These are just 93 lines of code, excluding comments. Other files do not need to be read, since the theorem statements that specify `meshIntersectWithPreconditionCheck` (in the file with the same name) only rest on definitions stated in these 4 files.
- A reviewer can skip the implementation of `meshIntersectWithPreconditionCheck` that reaches over 1000 lines of code in 4 files in [`CSG/Impl/`](CSG/Impl/), since it is guaranteed by the deterministic Lean checker to conform to the human-reviewed specification.
- This works thanks to 60,000 lines of AI-written formal proofs in [`CSG/Proof/`](CSG/Proof/), which also never have to be inspected by a human.

This compression and simplification from the implementation to the specification is possible because many things the implementation has to deal with can be completely decoupled from the specification:
- The implementation has to handle [special geometrical cases](#special-cases), which make up much of the complexity of the algorithm, whereas the formal specification is short because the math can be formulated generally. The Lean checker guarantees that all special cases are handled in accordance with the specification without the specification enumerating the special cases.
- The implementation uses accelerating data structures in order to avoid quadratic runtime complexity and other optimizations. While we did not formalize runtime complexity, the Lean checker guarantees that with all these optimizations we still produce results according to the specification.

If in a future commit we for example further improve the runtime performance or the quality of the output mesh, the reviewed specification stays the same and we get correctness with respect to it, without any re-review. Also see how I [developed this project](#development) only through shaping this specification.

## Development

During development, I controlled only a small specification, leaving the proofs and detailed implementation as a black box to agents. I started with a specification that I estimated was relatively easy to implement and formally prove correct and then grew the requirements. In each of the steps listed below, I had the agent implement and formally prove the specification. This stepwise refinement allowed me to delegate large pieces of work to agents, while getting feedback that my specification is satisfiable and verifying the progress of the agents toward my end goal at each milestone. I instructed agents to first write informal proofs before formalizing.

- I started by having an agent formalize a paper that provides a mathematical framework for describing solids based on simplicial chains. This gave me a formal existence result without concrete implementation (see [`CSG/Legacy/ChainIntersectionExistence.lean`](CSG/Legacy/ChainIntersectionExistence.lean)).

  > F. R. Feito and M. Rivero, "Geometric modelling based on simplicial chains," *Computers & Graphics* **22**(5), 611–619 (1998). [doi:10.1016/S0097-8493(98)00067-3](https://doi.org/10.1016/S0097-8493(98)00067-3)

- Then I asked for an implementation with proof of correctness ([`CSG/Legacy/ChainIntersectionAlgorithm.lean`](CSG/Legacy/ChainIntersectionAlgorithm.lean)). This already satisfied a formal specification similar to my end goal. But overlapping triangles and other issues were still allowed and did occur.
- I then specified restrictions for the output mesh (similar to the current state of `WellFormedMesh`) to forbid the kind of problems from the first implementation. I also introduced a general position restriction on inputs that I later removed, to avoid the implementation having to consider a lot of special cases in this step. The stricter requirements forced a complete reimplementation, but some of the formal framework could be reused.
- I then removed the general position restrictions on inputs, which forced the agent to handle all special geometrical cases correctly.
- I then had agents optimize the implementation with bounding volume hierarchies and other optimizations. I did not formalize a requirement on runtime, but Lean verified that the optimization still satisfies the same formal spec. So in this step, I did not have to re-review anything to assure correctness.
- Finally I strengthened the specification further and made it easier to review.

This process resulted in the specification you can see in the top level of the [`CSG/`](CSG/) folder, the proof at [`CSG/Proof/`](CSG/Proof/) and the implementation at [`CSG/Impl/`](CSG/Impl/).

For most of the above steps I used Claude Opus 4.8. For some I used Fable 5 to create an initial informal proof strategy and then had Opus write formal proofs and implementation. Some of the above steps took over 24 hours of autonomous agent work.

## Comparison to vibecoding with informal specification

In contrast to regular vibecoding, combining AI with formal verification yields strict guarantees that we know will hold for all inputs and are kept enforced with each subsequent modification of the program. But like regular vibecoding, with each step the development can acquire some debt: both the implementation and the proofs that I ended up with are nowhere near as clean and do not follow a cohesive design, as they would be when controlled by a human who kept an overview of everything. Moreover, there are some constraints we did not formalize here, such as the runtime performance or the way faces of the output solid are triangulated beyond the well-formedness condition. Therefore these constraints are as hard to control as with regular vibecoding.

For comparison, I gave Opus 4.8 an informal description of the specification and asked it to implement it in C++. The length of the implementation excluding tests, glue etc. was in the same 1000+ lines range as the Lean implementation. Even though it wrote unit tests and iteratively fixed its own implementation, upon inspection by an independent agent comparing it to the formally verified Lean implementation, 3 distinct bugs were discovered in the C++ geometry kernel and reproduced on specific inputs. All of these bugs are rare and would be almost impossible to catch by black box testing. Iterated adversarial review of the code by other agents against the informal specification might have caught these bugs. But without formal verification it is not possible to know for sure that there are no more bugs in the implementation. (The C++ kernel has at least 3 distinct bugs which were reproduced: 1. In certain configurations where a vertex of a well-formed mesh lies on both an edge of another part of the mesh and a face of another well-formed mesh. 2: On well-formed input meshes when a cascade of ray intersection tests in the internal computations all happen to hit triangle edges. 3: In certain configurations where a large face was cut by several small features.)

<details>
<summary>Comparison with informal vibecoding, click to expand prompt used to produce alternative C++ implementation</summary>

> Implement an exact 3D mesh intersection algorithm. Write in C++, compile to wasm, produce an artifact I can play with. Is important that the kernel, a simple function is in a self contained separate file, the geometrical kernel separated from the all the glue. (This file only depends on a separate bignum/exact rational implementation, separate file),  This function should just take meshes as arrays of triangles with exact coordinates as inputs/outputs.
>
> This function should check the inputs are a well-formed mesh in the sense below and produce an error message otherwise. Only run the intersection if inputs are well-formed.
>
> Our definition of "well-formed mesh" captures the conditions commonly expected by real world mesh processing tools - watertight surface, bounding a solid with multiplicity one with coherent outward orientation, no degenerate triangles, no self-intersections - with one relaxation: the surface may touch itself, not at the interiors of faces but along edges and vertices (so strict 2-manifoldness is not required). This relaxation is needed so that intersection of any two well-formed meshes is again well-formed.
>
> Everything should be computed with rationals. It should treat all special cases correctly. Always producing a well-formed mesh as output if inputs are well-formed. You can intersect triangles pairwise (use bvh optimization) emitting polygons and triangulating with steiner fans.

</details>

Drawbacks of combining formal verification with vibecoding:
- It tends to produce code that is slower or disregards other practical considerations that are not captured in the specification. This stems from the difficulty of the formal verification pushing for simpler code and from the lack of formally verified practical software in the training data.
- It can take orders of magnitude more tokens and time for agents to autonomously develop formal proofs, rather than to reason informally about their implementation.
- Many practical problems do not admit a simple formal specification.

As I write this, the capability of AI agents to work on large well-defined tasks is rapidly increasing with each model release. The capability of humans to review their output and reason about it does not. I hope we can use formal verification among other methods as a lever to keep control.

## Building and checking

Requires [elan](https://github.com/leanprover/elan). The Lean version is pinned in
[`lean-toolchain`](lean-toolchain) (currently `leanprover/lean4:v4.15.0`) to simplify
the WebAssembly build; elan installs it automatically on first use.

First download the pre-built Mathlib from the community cache (without this,
the next step would compile Mathlib from source, which takes a long time):

```sh
lake exe cache get
```

> **If this aborts with a `dyld` error mentioning `SG_READ_ONLY`** (recent macOS):
> the Lean version pinned here bundles a linker with a known issue, fixed in later
> Lean releases ([lean4#6063](https://github.com/leanprover/lean4/pull/6063)).
> Relinking the cache tool with Apple's compiler works:
>
> ```sh
> rm -rf .lake/packages/mathlib/.lake/build/bin
> SDKROOT="$(xcrun --show-sdk-path)" LIBRARY_PATH="$(lean --print-prefix)/lib" LEAN_CC="$(xcrun -f clang)" lake exe cache get
> ```

Check all proofs:

```sh
lake build
```

Inspect the axioms the theorems of interest depend on (in the following example the
correctness theorems of the mesh-intersection implementation that is called in the
demo). This is important since agents could have introduced unwanted axioms into the
proofs. All theorems in this repo only depend on the trusted axioms
`[propext, Classical.choice, Quot.sound]`:

```sh
printf 'import CSG.MeshIntersectWithPreconditionCheck\n#print axioms CSG.meshIntersectWithPreconditionCheck_ok_spec\n#print axioms CSG.meshIntersectWithPreconditionCheck_ok_of_wellFormed\n#print axioms CSG.meshIntersectWithPreconditionCheck_error_sound\n#print axioms CSG.meshIntersectWithPreconditionCheck_error_of_not_wellFormed\n' | lake env lean --stdin
```

Also make sure that the theorems actually hold for the compiled functions, i.e.
that the implementation is not overridden with something else via one of the
following keywords. This search should return no matches:
```sh
rg -n 'implemented_by|extern|csimp|skipKernelTC|unsafe|partial|opaque' CSG/
```

Build the WebAssembly bundle served by the web app (requires `emscripten`, `zstd`,
and `node`/`npm`; `wasm-opt` is optional):

```sh
./build_web_demo.sh
```

## Performance

The algorithm rejects the [original Stanford bunny](https://graphics.stanford.edu/data/3Dscanrep/) since the mesh is not watertight, so I closed the holes at the bottom. The implementation takes 24 seconds to compute the exact intersection of the two 70k-triangle meshes single-threaded on an M4 Pro.

This implementation is far slower than state-of-the-art mesh intersection implementations. In this project we prioritize minimizing the effort of human review of correctness over performance.
- Most other implementations use hardware-accelerated floating-point computations. (Even exact implementations like CGAL use floats for decisions where floating-point precision is sufficient.) We don't. This is not a fundamental limitation of Lean, but using hardware-accelerated floats would require additional axioms human reviewers have to trust.
- We check all inputs at runtime against our well-formedness definition, which makes up a substantial fraction of the total runtime.

![Intersection of Stanford bunny with Stanford bunny](readme-assets/intersection-bunny-watertight-bunny-watertight.png)

## Why we cannot have manifold output meshes in general

In the following example exact rotation of the cube with holes leads to a solid whose surface is non-manifold. (See the point in front of the output where two components of the solid touch.) Set the move grid sizes of both meshes to 1/3 and rotation digits to 1 to arrange this case in the web demo. If you reset the rotation and move the cubes with holes around, you can also arrange a case where the surface of the output solid is non-manifold along an edge.

![Intersection of cube with holes with cube with holes](readme-assets/intersection-cube-with-holes-cube-with-holes.png)

If we imposed a manifoldness condition, no algorithm would be able to satisfy our specification.

## Special cases

The specification is short, but the algorithm has to deal with special geometrical cases with dedicated code in order to satisfy the specification.

Here the right faces of the two tetrahedrons overlap coplanarly with the same normal direction. The specification implicitly forces the algorithm to emit a face in the intersection of these coplanar faces. Programs that don't follow a formal specification might overlook this case and produce a hole or a double face on the surface.

![Intersection of tetrahedron with tetrahedron - coplanar overlap with same normal direction](readme-assets/intersection-tetrahedron-tetrahedron.png)

In this example tetrahedrons touch exactly, leaving zero volume between them - a coplanar overlap of faces with opposite normal direction. Our specification forces the output to be empty. Many production applications randomly produce double-membrane artifacts in cases like these. In the [example with the cubes with holes above](#why-we-cannot-have-manifold-output-meshes-in-general) you see a non-trivial example with coplanar overlaps with opposite normal direction.

![Intersection of tetrahedron with tetrahedron - coplanar overlap with opposite normal direction](readme-assets/intersection-tetrahedron-tetrahedron-opposite.png)

There are many other special cases the algorithm has to deal with. Thanks to the formal verification, we do not need to write any unit tests for any cases to ensure correctness.
- Vertices of one mesh lie on the other mesh. The algorithm must make sure to consider such vertices for creating faces on both sides of the cut.
- One or both input meshes do not satisfy one of the 4 well-formedness conditions and that must be reported correctly.
- Coplanar overlaps, which we discussed above, themselves have sub-special cases, such as edges of the overlapped faces being collinear.
- ...

There are also special cases the implementation has to get right, which are not visible from the input but occur from the geometric constructions internally in the algorithm. We would never think of testing these without reading the implementation. Our specification ensures all of this is handled correctly, without us having to think about it.
- A ray that is shot in the implementation to determine inside/outside in a subroutine exactly hits an edge or a vertex of a triangle or even coplanarly traverses a face.
- A face lies exactly on the border of a bounding box in the bounding volume hierarchy acceleration structure, requiring us to put the right inequalities in the implementation.
- The above points hold not only for the intersection but also for the well-formedness check. Getting it wrong in that part of the code might lead to meshes mistakenly being classified as non-well-formed.
- Subroutines of the algorithm can create T-junctions that it must fix again to produce a well-formed output mesh.
- ...

## Related work

- [Di Vito and Hocking (NASA Formal Methods 2021)](https://doi.org/10.1007/978-3-030-76384-8_6) verified a polygon merge algorithm in PVS, combining two overlapping simple polygons into a single outer boundary without holes.
- My earlier [verified-polygon-intersection](https://github.com/schildep/verified-polygon-intersection) verified 2D multipolygon intersection in Lean 4, relying on AI-written implementation and proof like we do here.
- Unverified exact 3D mesh booleans exist of course, e.g. [CGAL's Nef polyhedra](https://doc.cgal.org/latest/Nef_3/). Exact and robust in practice, but their correctness rests on testing and informal reasoning, not machine-checked proof.

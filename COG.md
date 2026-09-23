---
type: cog [0.1]
name: cog-build-candidate
description: "Materialize validated author source as a checked Smith package."
version: "0.1.0"
license: Apache-2.0
publisher: OpenTeams
manifest: pixi.toml
manifest_schema: openteams/cog-manifest [0.1]
---

# cog-build-candidate

This deterministic supporting Cog expands an accepted pure-code source snapshot
through cog-author's exporter, invokes Smith to create and check the package,
and returns the package, expanded evaluator input, and fingerprints. It never
authors source or runs generated tests. It is reusable wherever a checked author
snapshot must become a package, with its own collision and identity checks.

Input contains the accepted contract digest, full author request and envelope,
and caller-selected output directory. The parent must resolve inside the local
workspace. Existing destinations refuse; a matching completed materialization
receipt permits replay only while the source and package fingerprints match.
An incomplete creation with no receipt requires inspection and a fresh artifact
directory. It is not silently repaired or overwritten.

The acceptance digest records the caller's contract choice; it does not prove
who approved it. An invalid digest is refused before packaging. The output status
is packaged-not-runtime-tested, never accepted or published.

Run the supplied hand-written fixture with `pixi run run -- --bundle
examples/sample-bundle.json`. It is seam evidence, not live model authoring.

## Local host contract

This first implementation requires sibling cog-workbench, cog-author,
cog-build-evaluator and cog-smith installations. It uses the declared
`openteams/local-builder-host [0.1-draft]` extension and Workbench's local
package operations API; it does not import another Cog's task implementation.
The host path is fixed relative to this checkout, never supplied by task input.
No cloud registry portability or constrained execution environment is claimed.

Local run artifacts and declared subprocess operations are the work. There are
no protected-service reaches or external grants in this slice. Generated code
runs with the owner's ambient authority; the caller must admit that execution.
No model calls, publication, reference edits, or free-form shell commands are
supported. This Cog does not coordinate the build lifecycle; the Op does.

Install with `pixi install`; run `pixi run test`. Results use envelope v1 with
code identity, structured problems, and no model binding. Gates belong to the
Op. Only src/task_logic.py is Cog-owned; shared machinery remains Smith-owned.

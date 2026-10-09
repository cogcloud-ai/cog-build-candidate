# cog-build-candidate

Materialize validated author source as a checked Smith package.

See [COG.md](COG.md) for the work contract and local host dependency, and
[the builder Op](https://github.com/cogcloud-ai/op-cog-builder/blob/main/README.md) for the executable composition.

```sh
pixi install
pixi run test
```

This is hand-authored pipeline infrastructure, not a model-generated candidate.

## License

Copyright 2026 OpenTeams. Licensed under the [Apache License 2.0](LICENSE).
Third-party dependencies and external model services retain their own licenses
and terms. Previously published BSD-3-Clause versions remain available under
that license.

## Public preview

See the [suite guide](https://github.com/cogcloud-ai/cog-op-builder/blob/main/docs/repositories.md)
for repository roles, supported setup, and current limitations.

Candidate materialization accepts the author's durable `revision` receipt in the
full author request. The exporter validates that receipt and the scoped source
changes before any package is created; materialization still does not decide
whether to revise or accept. This is the schema companion to the public builder's
bounded revision cycle and cog-author's candidate-bound handoff.

# MTAH2027 · The Shrewdies

Our work for **More Than a Hack 2027**, in one repository.

| folder | what it holds |
|---|---|
| [`initial-challenge/`](initial-challenge/) | Per-frame team possession for BAR-ATH: code, container, tests and technical report |
| [`innovative-challenge/`](innovative-challenge/) | Reserved for the next stage of the hackathon |
| [`website/`](website/) | The team site, published with GitHub Pages: [theshrewdies.com](https://theshrewdies.com) |

Each folder is self-contained: its own README, its own build, nothing shared across folders.
The site is deployed by [`.github/workflows/pages.yml`](.github/workflows/pages.yml) whenever
`website/` changes on `main`.

Code is released under the MIT licence ([LICENSE](LICENSE)); `initial-challenge/` also carries
the organisers' original licence for the material it builds on.

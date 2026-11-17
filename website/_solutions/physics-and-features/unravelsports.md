---
title: "unravelsports"
kicker: "Physics and features"
summary: "Turns tracking into graphs, pressing intensity and formations. The shortest path from a kloppy dataset to a graph neural network."
group: physics-and-features
order: 60
chips: ["Tracking", "Graph", "Library", "MPL-2.0"]
motif: graph
motif_caption: "Each frame becomes a graph: players as nodes, distances and angles on the edges."
motif_labels: ["Player node", "Edge features", "Neighbour"]
facts:
  - { k: "Modality", v: "Tracking loaded through kloppy" }
  - { k: "Output", v: "Graph datasets; pressing and formation features" }
  - { k: "Evidence", v: "Documented open library with worked examples" }
  - { k: "Code and weights", v: "Python package; no possession model included" }
  - { k: "Licence", v: "MPL-2.0" }
verdict: { label: "Our read", text: "The practical on-ramp to football GNNs, with a pressing measure worth borrowing on its own." }
sources:
  - { title: "unravelsports: repository and documentation", url: "https://github.com/UnravelSports/unravelsports" }
related:
  - /solutions/classifiers-and-decoders/graph-network-toolkits/
  - /solutions/readers-and-formats/kloppy/
  - /solutions/direct-possession/defcon/
---
unravelsports does the unglamorous middle step of football graph learning. It takes tracking loaded through [kloppy]({{ '/solutions/readers-and-formats/kloppy/' | relative_url }}) and builds, frame by frame, the graphs a network trains on: players as nodes with position and velocity features, edges with distances and angles, a label attached to each graph.

Around that converter it ships tactical models that need no training: a pressing-intensity measure and formation detection.

## Where it wins

- It removes the data wrangling between tracking files and a graph framework.
- Pressing intensity is a physically meaningful pressure signal between defenders and attackers.
- It is built on kloppy, so every provider kloppy reads is supported.
- MPL-2.0: usable inside permissive projects, with changes to its own files staying open.

## What it costs

- It prepares graphs and trains nothing for you. A possession model still needs labels and a network.
- Pressing and formation describe behaviour around the ball. They do not say who has it.
- Graph features assume one node per player per frame. Missing players need a policy.

## How it plugs into possession

In two places. As preprocessing for a supervised graph model of possession, it is the bridge between readers and the [graph frameworks]({{ '/solutions/classifiers-and-decoders/graph-network-toolkits/' | relative_url }}).

As a feature source, pressing intensity is a decent soft cue: the team applying pressure is rarely the team in possession. It is a correlate, and should be weighted as one.

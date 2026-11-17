---
title: "kloppy"
kicker: "Readers and formats"
summary: "One loader for every provider. Tracking and event files in, a single standardised model out, with coordinates, orientation and time handled once."
group: readers-and-formats
order: 10
chips: ["Tracking + events", "Reader", "No training", "BSD-3-Clause"]
motif: pipeline
motif_caption: "Whatever the provider, the file leaves the loader in one model with one set of conventions."
motif_labels: ["Provider file", "Parser", "One model", "Coordinates", "Dataframe"]
facts:
  - { k: "Modality", v: "Tracking and event files from many providers" }
  - { k: "Output", v: "Standardised datasets, exportable to dataframes" }
  - { k: "Evidence", v: "Established PySport project, used in provider docs" }
  - { k: "Code and weights", v: "Python package" }
  - { k: "Licence", v: "BSD-3-Clause" }
verdict: { label: "Our read", text: "The standard reader. Use it wherever data crosses a provider boundary. Its discipline about coordinates is worth more than its convenience." }
sources:
  - { title: "kloppy: standardizing soccer tracking and event data (repository)", url: "https://github.com/PySport/kloppy" }
  - { title: "kloppy documentation", url: "https://kloppy.pysport.org/" }
related:
  - /solutions/readers-and-formats/databallpy/
  - /solutions/physics-and-features/floodlight/
  - /solutions/physics-and-features/unravelsports/
  - /datasets/dfl-idsse/
---
Every tracking provider invented its own file format, its own coordinate system and its own idea of which way a team attacks. kloppy is the community's answer: one library that reads them into one data model.

There is a loader for each provider and data type. Whatever the source, the result is a dataset of frames or events with typed metadata: teams, players, periods, frame rate, pitch dimensions. Transformations then remove the classic bugs. Coordinate systems convert between provider conventions. Orientation can be normalised so that a team always attacks the same way. Pitch dimensions rescale between normalised and metric units.

## Where it wins

- It removes the least interesting source of errors in football analytics: flipped axes, swapped halves, mismatched units.
- One code path for many providers. A possession method written against kloppy runs on open DFL data and on Metrica-format data alike.
- It preserves provider metadata, and carries it in typed fields.
- BSD-3-Clause and actively maintained.

## What it costs

- An object model per frame is heavier than raw arrays. For numerical work, convert once and stay in arrays.
- Standardising formats does not standardise meaning. Two providers' possession flags follow different rules, and kloppy faithfully carries both.
- It is a dependency with its own release rhythm, in a place where a pinned, minimal build may prefer a short parser of its own.

## How it plugs into possession

At the front door. It is how external labelled data, the open DFL matches above all, gets into the same shape as the data a method runs on, so that one evaluation harness serves both.

Cross-provider validation is the only sound test of a possession method that may not train on its target match, and it starts with a loader.

The datasets it reads are catalogued under [Datasets]({{ '/datasets/' | relative_url }}). For pinning events to frames, see [DataBallPy]({{ '/solutions/readers-and-formats/databallpy/' | relative_url }}).

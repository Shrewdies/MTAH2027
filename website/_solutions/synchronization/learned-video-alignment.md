---
title: "Learned video alignment (TCC, TPL)"
kicker: "Synchronisation"
summary: "Self-supervised embeddings in which the same moment looks the same from any camera. Alignment becomes nearest-neighbour search in feature space."
group: synchronization
order: 50
chips: ["Video", "Cross-view sync", "Learned", "Research code"]
motif: sync
motif_caption: "Frames from two views are embedded so that matching moments land together."
motif_labels: ["View A", "View B", "Same moment"]
facts:
  - { k: "Modality", v: "Two or more videos of the same action" }
  - { k: "Output", v: "Frame embeddings and cross-video correspondences" }
  - { k: "Evidence", v: "CVPR 2019 (TCC); ICCV 2025 (TPL)" }
  - { k: "Code and weights", v: "Research implementations; no football-trained weights" }
  - { k: "Licence", v: "None declared in either repository" }
verdict: { label: "Our read", text: "Elegant where cameras share action but not geometry. On a calibrated pitch, positions synchronise better than embeddings." }
sources:
  - { title: "Temporal Cycle-Consistency Learning (Dwibedi et al., CVPR 2019)", url: "https://openaccess.thecvf.com/content_CVPR_2019/html/Dwibedi_Temporal_Cycle-Consistency_Learning_CVPR_2019_paper.html" }
  - { title: "TCC: a published implementation", url: "https://github.com/kln-cmu-mscv/TCC" }
  - { title: "Synchronization of Multiple Videos (Naaman et al., ICCV 2025)", url: "https://openaccess.thecvf.com/content/ICCV2025/html/Naaman_Synchronization_of_Multiple_Videos_ICCV_2025_paper.html" }
  - { title: "TPL: authors' code", url: "https://github.com/BGU-CS-VIL/TPL" }
related:
  - /solutions/synchronization/geometric-sync/
  - /solutions/events-and-replay/sn-replay-grounding/
  - /solutions/synchronization/dtw-python/
---
Two cameras filming the same passage of play share no pixels. What they share is progress: the same pass is being struck in both. Learned alignment trains an encoder so that frames at the same point of an action land close together in embedding space, whatever the viewpoint.

Temporal Cycle-Consistency learns this without labels. Take a frame in one video, find its nearest neighbour in a second video, then find that frame's nearest neighbour back in the first. If the embedding is good, the cycle returns to where it started. The training loss penalises cycles that do not close.

Temporal Prototype Learning targets the synchronisation of several videos at once. It learns a shared temporal representation that all the videos are aligned to, instead of matching them only in pairs.

## Where it wins

- No shared geometry required. Views can be on opposite sides of the pitch.
- Self-supervised. No frame-level sync labels.
- The embeddings transfer to related jobs, such as retrieving similar moments.
- A shared representation scales to many cameras.

## What it costs

- These methods are built for actions with a clear progression. Open play has no canonical timeline.
- Football repeats. Two throw-ins embed alike, so alignment needs anchors to avoid matching the wrong one.
- They need training on multi-view football footage, which is scarce.
- Neither repository declares a licence.
- Precision is bounded by how distinguishable adjacent frames are.

## How it plugs into possession

When geometry is unavailable. If two feeds can both be projected to the pitch, [synchronising them through player positions]({{ '/solutions/synchronization/geometric-sync/' | relative_url }}) is more precise and needs no training. Learned alignment earns its place when one view cannot be calibrated: tight broadcast shots, replays from unusual angles.

In a possession pipeline that makes it a recovery tool. It pulls evidence from footage that would otherwise be discarded, at a temporal precision that suits context better than boundaries.

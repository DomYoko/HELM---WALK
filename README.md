# Vessel Walkthrough

A 3D viewer for yacht crew. You walk through a model of the vessel, click any object, and see what
it is, what is wrong with it and what work is planned on it.

**Open the viewer:** https://domyoko.github.io/HELM---WALK/

The model in it today is a trial: a small house with furniture, built by the 3D designer on this
project. It is there to prove the idea works before the yacht itself is modelled.

## Where this is going

The viewer will become part of a vessel management app, first for one 36 m motor yacht and later for
other vessels. Crew use the app for safety checks, maintenance and yard work.

Today that information lives in lists and on flat deck plans. A list tells you a fire extinguisher is
due for service. It does not show you where the extinguisher is, or what is behind the panel next to
it. The 3D model does.

The aim is that every locker, hatch, valve, extinguisher, lifejacket and piece of machinery on board
is an object a crew member can walk up to and click. The click shows its details. From there they can
report a defect on it or pin a job to it, and the pin stays on the exact spot.

## Using the viewer

Open it on a computer with a mouse, in Chrome, Edge or Safari.

1. **Look around from outside.** Drag to orbit. Scroll to zoom. Right-drag to pan.
2. **Walk inside.** Press **Space**. You are now standing in the model. The mouse looks around,
   **W A S D** moves you, Shift moves faster. Press Space again to leave.
3. **Click an object.** In walk mode, aim the small orange ring at it and click. A card opens with
   the object's details. The mouse is released so you can use the card.
4. **Report a defect or pin a job.** Use the two buttons on the card. Fill in the short form and
   save. A pin appears on the spot you clicked.
5. **Close the card** with the round button at its top right. The mouse goes back to looking around.
6. **Filter by category.** The chips above the object list hide or show a whole category, for
   example Structure, to see inside the building.
7. **Work log.** The second tab on the left lists every open defect and job. Click one to go to it.
8. **Try your own file.** Use **Open .glb** or drop a `.glb` onto the view. "Model readiness" at the
   bottom left scores how well the file fits this use.

Anything you add here is saved in your own browser only. Nobody else sees it.

## What the model needs

Modelling for this is different from modelling for print or RC. A printed model wants solid, merged
shapes. This viewer wants the opposite: many separate objects, each one clickable.

**Make an item its own object if any of these is true:**

1. It has a serial number, a service date or an expiry date.
2. It opens, closes, lifts out or moves: doors, hatches, locker doors, drawers, access panels, valves.
3. It is safety equipment.
4. Something is stowed in it or hidden behind it.
5. Someone could report a defect on that one item.

Everything else can be merged per room, for example the wall linings of one cabin.

**Never merge duplicates.** Five chairs are five objects, not "chairs x5". If they are one object,
clicking one chair selects all five and they share one record.

**Name each object plainly:** `Chair 3`, `Locker starboard 2`, `Fire extinguisher galley`.

**Group by room** with parent empties: deck, then room, then the objects in it.

**Export** as glTF 2.0 (`.glb`), with Custom Properties ticked under Include, Data.

## What was changed in the trial file

The trial arrived as 12 objects. Six of them were groups of duplicates. `scripts/split_merged.py`
separated them, so the file is now 22 objects and each chair, table and window is clickable alone.
`model/House-split.blend` is that result. Open it in Blender to see the difference.

Two custom properties were added to every object:

- `id` is a permanent code the software uses to keep an object's records attached to it, even if the
  object is renamed. Leave it alone. New objects get one automatically.
- `category` puts the object in one of the groups below. Setting it in Blender is optional. It can
  also be set in the viewer.

## Categories

| Code | Category |
|---|---|
| `lsa` | Lifesaving |
| `ffe` | Fire equipment |
| `firedet` | Fire detection |
| `emg` | Emergency and medical |
| `acc` | Access and openings |
| `mec` | Propulsion and machinery |
| `ele` | Electrical |
| `pip` | Piping, valves and tanks |
| `hvc` | HVAC and refrigeration |
| `nav` | Navigation, comms and AV/IT |
| `dek` | Deck equipment, tenders and toys |
| `int` | Interior and stowage |
| `gal` | Galley |
| `str` | Structure and coatings |

## What comes next

One real space from the yacht, modelled under the rules above. A single cabin or the galley is
enough to test the whole chain on real geometry before the rest of the vessel is built.

## In this repo

| Path | What it is |
|---|---|
| `index.html` | The viewer. One file, no build step. |
| `trial.json` | The trial model as the viewer loads it. |
| `model/House-split.blend` | The trial model with duplicates separated. |
| `scripts/` | Blender scripts: inspect a file, split duplicates, stamp ids, export. |

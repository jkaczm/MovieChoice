# Catch Santa! 🎅📸

A first-person stealth game built with [three.js](https://threejs.org). It's 3 a.m. on Christmas
morning. Creep down the stairs and photograph Santa Claus before he goes back up the chimney.

## Play

The whole game is a single file, `index.html`, and needs no build step. three.js loads from a CDN,
so you need an internet connection.

```bash
cd santa-game
python -m http.server 8000   # then open http://localhost:8000
```

You can also open `index.html` directly in a modern browser on a computer, phone or tablet.

## Controls

| Key | Action |
| --- | --- |
| Mouse | Look around |
| W A S D / arrows | Move |
| Hold C | Crouch and tiptoe (quiet, harder to spot) |
| Hold Shift | Run (loud!) |
| Click / Space | Take a photo (3 shots of film) |
| Esc | Pause |

### On a phone or tablet

Touch controls switch on automatically when you start the game by tapping. It plays best in landscape.

| Touch | Action |
| --- | --- |
| Drag on the left half | Walk (virtual joystick; push further to go faster) |
| Drag on the right half | Look around |
| 📷 button | Take a photo |
| Crouch / Run buttons | Tap to toggle |
| ❚❚ button | Pause |

## The house

**Upstairs**
- **Your bedroom**: you start here. Fairy lights, a letter to Santa, toys on the floor.
- **The landing and stairs**: watch out for the creaky 4th and 9th steps.
- **The hallway**: leads to the bathroom and your parents' room.
- **Your parents' bedroom**: they're asleep, so tiptoe. Dad's camera bag on the dresser holds a
  spare roll of film. Make too much noise in here and Dad wakes up and sends you back to bed.
- **The bathroom**: tub, rubber duck, night light.

**Downstairs**
- **The living room**: the tree with a toy train, the fireplace with stockings and nutcrackers,
  cookies and milk, a bookshelf, a grandfather clock, and a cat asleep in the armchair.
- **The study** (behind the tree): desk lamp, computer, piano, globe and bookshelves.
- **The kitchen and dining room** (through the archway): Christmas dinner table, gingerbread
  house, and carrots on the counter for the reindeer.

## Difficulty

| | Easy | Normal (default) | Hard |
| --- | --- | --- | --- |
| Film | 3 | 3 | 2 |
| Santa's eyesight | narrow, 13 m | wider, 15 m | very wide, 17 m |
| Hearing range | 15 m | 18 m | 21 m |
| Max photo distance | 10 m | 8.5 m | 7 m |
| Looks over his shoulder | rarely | often | constantly |
| Comes over to check noises | no | yes | yes |
| Missed flash | makes him suspicious | very suspicious | he runs for the chimney |

## How it works

- Santa works through a to-do list: presents under the tree and in the study, the cookies and
  milk, the reindeer's carrots in the kitchen, the stockings.
  Then he heads back up the chimney. If he finishes before you get a photo, you lose.
- **Suspicion meter:** Santa sees in a forward cone, and walls, the sofa and the tree block his view.
  Walls also muffle the sound of your footsteps.
  Moving in his sight, running, missed camera flashes and footsteps all raise his suspicion.
  When he hears something he stops and turns to look, so freeze and crouch.
  If suspicion reaches 100 he runs for the chimney.
- **Creaky stairs:** the 4th and 9th steps creak if you step in the middle. Keep to the edges.
- **Scoring:** the viewfinder turns green when a shot will work. You get up to 3 stars for a close
  photo taken while Santa is unaware. Walking right up and hugging him also counts.

All models are built from three.js primitives (static ones are merged so phones draw them fast), all textures are drawn on canvases at runtime,
and all sounds are synthesized with the Web Audio API, so there are no asset files.

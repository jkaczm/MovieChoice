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

## How it works

- Santa works through a to-do list: presents under the tree, the cookies and milk, the stockings.
  Then he heads back up the chimney. If he finishes before you get a photo, you lose.
- **Suspicion meter:** Santa sees in a forward cone, and walls, the sofa and the tree block his view.
  Moving in his sight, running, missed camera flashes and footsteps all raise his suspicion.
  When he hears something he stops and turns to look, so freeze and crouch.
  If suspicion reaches 100 he runs for the chimney.
- **Creaky stairs:** the 4th and 9th steps creak if you step in the middle. Keep to the edges.
- **Scoring:** the viewfinder turns green when a shot will work. You get up to 3 stars for a close
  photo taken while Santa is unaware. Walking right up and hugging him also counts.

All models are built from three.js primitives, all textures are drawn on canvases at runtime,
and all sounds are synthesized with the Web Audio API, so there are no asset files.

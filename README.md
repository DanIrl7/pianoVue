# Virtual Piano — Industrial Sonic Grid v0.1

A brutalist-designed, web-based virtual piano with polyphonic keyboard support, chord library, and professional-grade audio synthesis powered by **Tone.js** and **Vue 3**.

**Live Demo:** [localhost:5173](http://localhost:5173)

---

## 🎹 Features

### **Two-Row Piano Keyboard (No Shift Required)**

- **61-key interactive piano** spanning octaves 3–8
- Play across **multiple octaves simultaneously** with both hands
- **Zero key conflicts** — all keys mapped to unique notes
- Visual feedback on key press with smooth transitions
- Octave transposition controls (±3 octaves)

### **Keyboard Mapping**

#### Upper Deck (Right Hand — Octaves 4 & 5)

```
Number Row (Sharps/Flats):  2  3     5  6  7     9  0     =
                          C# D#    F# G# A#    C# D#    F#

QWERTY Row (White Keys):  Q  W  E  R  T  Y  U  I  O  P  [  ]
                          C  D  E  F  G  A  B  C  D  E  F  G
```

#### Lower Deck (Left Hand — Octaves 3 & 4)

```
Home Row (Sharps/Flats):  S  D     G  H  J     L  ;
                          C# D#    F# G# A#    C# D#

Bottom Row (White Keys):  Z  X  C  V  B  N  M  ,  .  /
                          C  D  E  F  G  A  B  C  D  E
```

**Play chords like:** `Q + T + Y` = C Major chord (C4 + G4 + A4)

### **Chord Library**

- **60+ pre-built chords** (Major, Minor, 7th, Maj7, Min7)
- Browse and search by root note or chord quality
- **Pin favorite chords** for instant reference on the shelf
- Visual chord diagrams with highlighted notes
- One-click chord preview with staggered polyphonic playback

### **Audio Engine**

- **Tone.js PolySynth** for zero-latency synthesis
- **Salamander Grand Piano** acoustic soundfont (optional fallback)
- Realistic piano envelope (attack, decay, sustain, release)
- Smooth fade-out to prevent audio clicking

### **Design**

- **Brutalist industrial aesthetic** with heavy borders and raw typography
- Monospace fonts (Space Mono, JetBrains Mono, Anton)
- Color scheme: #3C1950 (deep purple) + #F0CDD2 (soft rose) on raw backgrounds
- Responsive layout with hard shadows and sharp edges

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v16+)
- **npm** or **yarn**

### Installation

1. **Clone or navigate to your project:**

```bash
cd piano-app
```

2. **Install dependencies:**

```bash
npm install
```

3. **Start the development server:**

```bash
npm run dev
```

4. **Open in browser:**
   Navigate to `http://localhost:5173`

---

## 📋 Usage

### Playing Notes

- **Click keys** on the visual piano with your mouse
- **Press keyboard keys** (QWERTY, ZXCV, etc.) to play notes
- **Hold multiple keys** to play chords polyphonically
- **Hover over keys** for visual feedback (color change + slight movement)

### Transposing Octaves

- Click **"LOWER ◄"** or **"HIGHER ►"** to shift the entire keyboard up/down by octaves
- Click **"RESET"** to return to default octave

### Using the Chord Library

1. Click **"✦ CHORD_LIBRARY"** button in the header
2. **Filter by root note** (C, D, E, F, etc.) or **chord quality** (Major, Minor, 7th)
3. **Search** for specific chords (e.g., "Cm", "F#7")
4. Click **"+ PIN"** to add chords to your pinned shelf
5. Click **"▶ PLAY SOUND"** to preview a chord
6. Click **"VIEW"** to highlight chord notes on the main keyboard

### Pinned Chords Shelf

- **Quick reference** for your most-used chords
- Displays mini piano diagrams and keyboard keys
- Click **"▶ PLAY"** to play a pinned chord
- Click **"VIEW"** to highlight notes on the main keyboard
- Click **"✕"** to remove a chord from the shelf
- Click **"CLEAR ALL"** to empty the shelf

---

## 🏗️ Architecture

### File Structure

```
src/
├── App.vue                 # Root component
├── components/
│   └── Piano.vue          # Main piano component (this file)
├── main.js                # Vue entry point
└── assets/                # Optional images/styles

public/
└── (static assets)

vite.config.js             # Vite bundler config
package.json               # Dependencies & scripts
```

### Core Components

#### **Piano Component** (`Piano.vue`)

- Renders the 61-key interactive piano
- Manages keyboard state and audio synthesis
- Handles chord library and pinning logic
- Responsive modal for chord browsing

#### **Keyboard Mapping Engine**

```javascript
const keyMap = {
  q: { name: "C", octave: 4 }, // QWERTY row
  s: { name: "C#", octave: 3 }, // Home row (sharps)
  z: { name: "C", octave: 3 }, // Bottom row
  // ... etc
};
```

#### **Chord Engine**

- Generates all possible major, minor, 7th, maj7, min7 chords
- Computes semitone intervals and note positions
- Maps keyboard shortcuts to chord notes
- Highlights active chord notes on the keyboard

#### **Audio Engine** (Tone.js)

```javascript
pianoSynth = new Tone.PolySynth(Tone.Synth, {
  oscillator: { type: "triangle8" },
  envelope: {
    attack: 0.005, // Very fast attack
    decay: 1.8, // Long decay
    sustain: 0.15, // Piano sustain
    release: 1.4, // Natural release
  },
}).toDestination();
```

---

## 🎵 Dependencies

### Core

- **Vue 3** — Reactive UI framework
- **Vite** — Lightning-fast bundler and dev server
- **Tone.js** — Web Audio API wrapper for audio synthesis

### Fonts (Imported in CSS)

- **Space Mono** — Monospace UI font
- **JetBrains Mono** — Code/label font
- **Anton** — Display font for headers

---

## 🎨 Customization

### Change Color Scheme

Edit the CSS variables in `<style scoped>`:

```css
/* Primary colors */
--primary: #3c1950; /* Deep purple */
--accent: #f8ccd1; /* Soft rose */
--black: #000;
--white: #fff;
```

### Adjust Piano Audio

Modify the `pianoSynth` envelope in `initToneAudio()`:

```javascript
envelope: {
  attack: 0.005,    // How fast note starts (in seconds)
  decay: 1.8,       // How long it takes to reach sustain
  sustain: 0.15,    // Held volume level (0–1)
  release: 1.4      // How long note fades after release
}
```

### Add More Chords

Extend the `CHORD_TYPES` array:

```javascript
const CHORD_TYPES = [
  { id: "sus2", label: "Sus2", suffix: "sus2", intervals: [0, 2, 7] },
  // ... your custom chord
];
```

### Change Keyboard Mapping

Edit the `keyMap` object to reassign keys:

```javascript
const keyMap = {
  a: { name: "C", octave: 4 }, // Now 'A' plays C4
  // ... etc
};
```

---

## 🔧 Development

### Build for Production

```bash
npm run build
```

Output files go to `/dist/` — ready to deploy to any static host.

### Preview Production Build

```bash
npm run preview
```

### Debug

- Open browser DevTools (F12)
- Check console for Tone.js warnings
- Inspect Vue component state in Vue DevTools

---

## ⚙️ Browser Compatibility

| Browser | Support | Notes                           |
| ------- | ------- | ------------------------------- |
| Chrome  | ✅ Full | Recommended                     |
| Firefox | ✅ Full | Excellent                       |
| Safari  | ✅ Full | Requires HTTPS for audio on iOS |
| Edge    | ✅ Full | Chromium-based, full support    |
| IE 11   | ❌ None | No Web Audio API                |

---

## 🎯 Keyboard Shortcuts

| Action                  | Shortcut                |
| ----------------------- | ----------------------- |
| Play C4                 | `Q`                     |
| Play C#4                | `2`                     |
| Play C3 (low)           | `Z`                     |
| Play C#3 (low)          | `S`                     |
| Transpose up            | Click "HIGHER ►" button |
| Transpose down          | Click "LOWER ◄" button  |
| Open Chord Library      | Click "✦ CHORD_LIBRARY" |
| Close Chord Library     | `ESC` or click "DONE"   |
| Play chord from library | `▶ PLAY` button         |

---

## 📱 Responsive Design

- **Desktop (1200px+):** Full layout with side-by-side controls
- **Tablet (768px–1199px):** Stacked layout, pinned chords scroll horizontally
- **Mobile (< 768px):** Optimized touch interactions, vertical scrolling

---

## 🚀 Future Enhancements

### Phase 4 (Planned)

- [ ] Volume slider with real-time control
- [ ] Waveform selector (sine, square, sawtooth, triangle)
- [ ] Recording and playback
- [ ] Preset save/load system
- [ ] MIDI file import/export
- [ ] Metronome with tempo control

### Phase 5 (Aspirational)

- [ ] Reverb and effects (via Tone.js effects)
- [ ] Multiple instrument voices (strings, synth, etc.)
- [ ] Drum pads for percussion
- [ ] Sheet music visualization
- [ ] Multiplayer jam sessions (WebSockets)
- [ ] Mobile app version (React Native)

---

## 📖 Learning Resources

- **Tone.js Documentation:** https://tonejs.github.io/
- **Vue 3 Guide:** https://vuejs.org/
- **Web Audio API:** https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- **Music Theory:** https://www.musictheory.net/

---

## 🤝 Contributing

Found a bug or have a feature request?

1. Test in the latest version
2. Check for existing issues
3. Provide clear reproduction steps
4. Submit a pull request with improvements

---

## 📄 License

This project is open-source and available under the **MIT License**.

---

## 🎵 Credits

- **Design Inspiration:** Brutalist and industrial UI principles
- **Audio Synthesis:** Tone.js by Yotam Mann
- **Piano Samples:** Salamander Grand Piano by Alexander Holm
- **Typography:** Google Fonts (Space Mono, JetBrains Mono, Anton)

---

## 🐛 Troubleshooting

### "No sound playing"

- Check browser allows audio playback (may require user interaction first)
- Ensure Tone.js has been initialized (`Tone.start()` is called on first interaction)
- Check browser console for errors
- Try a different key or chord

### "Keys not responding"

- Make sure the piano window is in focus (click on it)
- Check that your keyboard layout matches the mappings (QWERTY assumed)
- Try clicking keys with mouse instead of keyboard
- Clear pressed keys by clicking elsewhere and refocusing

### "Chord Library won't open"

- Check browser console for JS errors
- Try refreshing the page
- Ensure you have enough RAM/CPU available

### "Audio is laggy or glitchy"

- Close other browser tabs/apps consuming resources
- Try using the PolySynth instead of Sampler
- Reduce octave range if performance drops

---

## 📞 Support

For issues, questions, or feedback:

- Open an issue in your repository
- Check the Vue 3 & Tone.js documentation
- Review the code comments in `Piano.vue`

---

**Version:** 0.1.0  
**Last Updated:** September 2026  
**Status:** Active Development

Happy playing! 🎹

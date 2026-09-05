<template>
  <div class="piano-container">
    <!-- Header with status and Chord Library trigger -->
    <div class="piano-header">
      <div class="header-left">
        <div class="piano-label">MAIN-CONSOLE_A1 // DUAL_DECK_PIANO</div>
        <div class="piano-status">LAYOUT: TWO_ROW_CHORD (NO SHIFT NEEDED)</div>
      </div>
      <div class="header-right">
        <button class="open-chords-btn" @click="openChordModal = true">
          <span class="btn-icon">✦</span> CHORD_LIBRARY
          <span v-if="pinnedChords.length > 0" class="pinned-pill">{{ pinnedChords.length }}</span>
        </button>
      </div>
    </div>

    <!-- Main Piano Keyboard -->
    <div class="piano-keyboard">
      <div
        v-for="note in notes"
        :key="`${note.name}-${note.octave}`"
        class="piano-key white-key"
        :class="{
          'key-pressed': isKeyPressed(note.kbKey, note.altKey),
          'chord-highlighted': isNoteInActiveChord(note.name),
        }"
        @click="playNote(note.name, note.octave + octaveShift)"
      >
        <span class="note-name">{{ note.name }}{{ note.octave + octaveShift }}</span>
        <span class="key-label">{{ note.kbKey }}</span>

        <!-- Nested Black Key -->
        <div
          v-if="note.blackKey"
          class="black-key"
          :class="{
            'key-pressed': isKeyPressed(note.blackKey.kbKey, note.blackKey.altKey),
            'chord-highlighted': isNoteInActiveChord(note.blackKey.name),
          }"
          @click.stop="playNote(note.blackKey.name, note.blackKey.octave + octaveShift)"
        >
          <span class="note-name">{{ note.blackKey.name }}{{ note.blackKey.octave + octaveShift }}</span>
          <span class="key-label">{{ note.blackKey.kbKey }}</span>
        </div>
      </div>
    </div>

    <!-- Pinned Chords Shelf (Right Below Piano) -->
    <div class="pinned-chords-shelf">
      <div class="shelf-header">
        <div class="shelf-title-group">
          <span class="shelf-tag">PINNED_CHORDS</span>
          <span class="shelf-count">[{{ pinnedChords.length }}]</span>
          <span v-if="activeHighlightChord" class="shelf-active-hint">
            // HIGHLIGHTING: <strong>{{ activeHighlightChord.name }}</strong>
          </span>
        </div>
        <div class="shelf-actions">
          <button class="shelf-btn add-btn" @click="openChordModal = true">
            + BROWSE CHORDS
          </button>
          <button
            v-if="pinnedChords.length > 0"
            class="shelf-btn clear-btn"
            @click="clearAllPinnedChords"
          >
            CLEAR ALL
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-if="pinnedChords.length === 0"
        class="empty-shelf"
        @click="openChordModal = true"
      >
        <span class="empty-icon">⊞</span>
        <span class="empty-text">
          NO CHORDS PINNED. CLICK <strong>"CHORD_LIBRARY"</strong> TO PIN CHORDS FOR INSTANT REFERENCE.
        </span>
      </div>

      <!-- Pinned Cards Row -->
      <div v-else class="pinned-cards-grid">
        <div
          v-for="chord in pinnedChords"
          :key="chord.id"
          class="pinned-card"
          :class="{ 'card-highlighted': activeHighlightChord?.id === chord.id }"
        >
          <div class="card-top">
            <div class="card-name-wrap">
              <span class="card-chord-name">{{ chord.name }}</span>
              <span class="card-chord-type">{{ chord.typeLabel }}</span>
            </div>
            <button
              class="card-remove-btn"
              title="Remove from pinned"
              @click="unpinChord(chord.id)"
            >
              ✕
            </button>
          </div>

          <!-- Mini Keyboard Diagram -->
          <div class="card-diagram-box">
            <svg class="mini-piano-svg" viewBox="0 0 154 46">
              <!-- White Keys -->
              <rect
                v-for="wk in miniWhiteKeys"
                :key="`pw-${wk.semitone}`"
                :x="wk.x"
                y="0"
                width="11"
                height="45"
                fill="#ffffff"
                stroke="#000000"
                stroke-width="1.2"
              />
              <!-- White Key Dots -->
              <circle
                v-for="wk in miniWhiteKeys"
                :key="`pwd-${wk.semitone}`"
                v-show="chord.activeSemitones.has(wk.semitone)"
                :cx="wk.x + 5.5"
                cy="35"
                r="3"
                fill="#000000"
              />
              <!-- Black Keys -->
              <rect
                v-for="bk in miniBlackKeys"
                :key="`pb-${bk.semitone}`"
                :x="bk.x"
                y="0"
                width="7"
                height="28"
                fill="#3c1950"
                stroke="#000000"
                stroke-width="1"
              />
              <!-- Black Key Dots -->
              <circle
                v-for="bk in miniBlackKeys"
                :key="`pbd-${bk.semitone}`"
                v-show="chord.activeSemitones.has(bk.semitone)"
                :cx="bk.x + 3.5"
                cy="20"
                r="2.2"
                fill="#ffffff"
              />
            </svg>
          </div>

          <!-- Notes & Computer Keys -->
          <div class="card-meta">
            <div class="meta-row">
              <span class="meta-label">NOTES:</span>
              <span class="meta-value">{{ chord.displayNotes.join(" · ") }}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">KEYS:</span>
              <div class="key-badges">
                <span v-for="k in chord.kbKeys" :key="k" class="card-key-badge">{{ k }}</span>
              </div>
            </div>
          </div>

          <!-- Card Actions -->
          <div class="card-actions">
            <button class="action-btn play-btn" @click="playChord(chord)">
              ▶ PLAY
            </button>
            <button
              class="action-btn highlight-btn"
              :class="{ active: activeHighlightChord?.id === chord.id }"
              @click="toggleHighlightChord(chord)"
            >
              {{ activeHighlightChord?.id === chord.id ? "ACTIVE" : "VIEW" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Octave Transpose Controls -->
    <div class="controls-row">
      <div class="octave-controls">
        <button class="ctrl-btn" @click="changeOctave(-1)">◄ LOWER</button>
        <span class="octave-label">
          TRANSPOSE: {{ octaveShift > 0 ? "+" + octaveShift : octaveShift }} OCT
        </span>
        <button class="ctrl-btn" @click="changeOctave(1)">HIGHER ►</button>
        <button v-if="octaveShift !== 0" class="ctrl-btn reset-btn" @click="octaveShift = 0">
          RESET
        </button>
      </div>
    </div>

    <!-- TWO-ROW KEYBOARD MAPPINGS DISPLAY -->
    <div class="key-mappings">
      <div class="mappings-header">
        <span class="mappings-title">TWO-ROW PIANO MAPPING // ZERO SHIFT KEY CONFLICTS</span>
        <span class="mappings-hint">PLAY CHORDS & MELODIES ACROSS ROWS WITH BOTH HANDS</span>
      </div>

      <div class="two-deck-container">
        <!-- UPPER DECK (Octave 4 & 5 - Right Hand) -->
        <div class="deck-section">
          <div class="deck-title">
            <span>UPPER DECK // OCTAVES 4 & 5 (RIGHT HAND CHORDS & MELODY)</span>
          </div>
          <div class="deck-rows">
            <div class="key-row black-row">
              <span class="deck-tag">BLK [NUM]</span>
              <div class="deck-keys">
                <span class="deck-btn black" :class="{ active: pressedKeys.has('2') }">
                  <span class="k-char">2</span><span class="k-note">C#4</span>
                </span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('3') }">
                  <span class="k-char">3</span><span class="k-note">D#4</span>
                </span>
                <span class="deck-gap"></span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('5') }">
                  <span class="k-char">5</span><span class="k-note">F#4</span>
                </span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('6') }">
                  <span class="k-char">6</span><span class="k-note">G#4</span>
                </span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('7') }">
                  <span class="k-char">7</span><span class="k-note">A#4</span>
                </span>
                <span class="deck-gap"></span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('9') }">
                  <span class="k-char">9</span><span class="k-note">C#5</span>
                </span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('0') }">
                  <span class="k-char">0</span><span class="k-note">D#5</span>
                </span>
                <span class="deck-gap"></span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('=') }">
                  <span class="k-char">=</span><span class="k-note">F#5</span>
                </span>
              </div>
            </div>
            <div class="key-row white-row">
              <span class="deck-tag">WHT [QWE]</span>
              <div class="deck-keys">
                <span class="deck-btn white" :class="{ active: pressedKeys.has('q') }">
                  <span class="k-char">q</span><span class="k-note">C4</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('w') }">
                  <span class="k-char">w</span><span class="k-note">D4</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('e') }">
                  <span class="k-char">e</span><span class="k-note">E4</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('r') }">
                  <span class="k-char">r</span><span class="k-note">F4</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('t') }">
                  <span class="k-char">t</span><span class="k-note">G4</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('y') }">
                  <span class="k-char">y</span><span class="k-note">A4</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('u') }">
                  <span class="k-char">u</span><span class="k-note">B4</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('i') }">
                  <span class="k-char">i</span><span class="k-note">C5</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('o') }">
                  <span class="k-char">o</span><span class="k-note">D5</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('p') }">
                  <span class="k-char">p</span><span class="k-note">E5</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('[') }">
                  <span class="k-char">[</span><span class="k-note">F5</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has(']') }">
                  <span class="k-char">]</span><span class="k-note">G5</span>
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- LOWER DECK (Octave 3 & start of 4 - Left Hand) -->
        <div class="deck-section">
          <div class="deck-title">
            <span>LOWER DECK // OCTAVE 3 & LOW 4 (LEFT HAND BASS & CHORDS)</span>
          </div>
          <div class="deck-rows">
            <div class="key-row black-row">
              <span class="deck-tag">BLK [ASD]</span>
              <div class="deck-keys">
                <span class="deck-btn black" :class="{ active: pressedKeys.has('s') }">
                  <span class="k-char">s</span><span class="k-note">C#3</span>
                </span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('d') }">
                  <span class="k-char">d</span><span class="k-note">D#3</span>
                </span>
                <span class="deck-gap"></span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('g') }">
                  <span class="k-char">g</span><span class="k-note">F#3</span>
                </span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('h') }">
                  <span class="k-char">h</span><span class="k-note">G#3</span>
                </span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('j') }">
                  <span class="k-char">j</span><span class="k-note">A#3</span>
                </span>
                <span class="deck-gap"></span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has('l') }">
                  <span class="k-char">l</span><span class="k-note">C#4</span>
                </span>
                <span class="deck-btn black" :class="{ active: pressedKeys.has(';') }">
                  <span class="k-char">;</span><span class="k-note">D#4</span>
                </span>
              </div>
            </div>
            <div class="key-row white-row">
              <span class="deck-tag">WHT [ZXC]</span>
              <div class="deck-keys">
                <span class="deck-btn white" :class="{ active: pressedKeys.has('z') }">
                  <span class="k-char">z</span><span class="k-note">C3</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('x') }">
                  <span class="k-char">x</span><span class="k-note">D3</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('c') }">
                  <span class="k-char">c</span><span class="k-note">E3</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('v') }">
                  <span class="k-char">v</span><span class="k-note">F3</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('b') }">
                  <span class="k-char">b</span><span class="k-note">G3</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('n') }">
                  <span class="k-char">n</span><span class="k-note">A3</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('m') }">
                  <span class="k-char">m</span><span class="k-note">B3</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has(',') }">
                  <span class="k-char">,</span><span class="k-note">C4</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('.') }">
                  <span class="k-char">.</span><span class="k-note">D4</span>
                </span>
                <span class="deck-btn white" :class="{ active: pressedKeys.has('/') }">
                  <span class="k-char">/</span><span class="k-note">E4</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CHORD LIBRARY MODAL -->
    <div v-if="openChordModal" class="chord-modal-backdrop" @click.self="openChordModal = false">
      <div class="chord-modal">
        <div class="modal-header">
          <div class="modal-title-group">
            <span class="modal-tag">CHORD_INDEX_V1</span>
            <span class="modal-subtitle">MAJOR, MINOR & 7TH CHORDS (NO SHIFT KEY REQUIRED)</span>
          </div>
          <button class="modal-close-btn" @click="openChordModal = false">✕ ESC</button>
        </div>

        <!-- Filter Controls Bar -->
        <div class="modal-controls">
          <!-- Root Note Filter -->
          <div class="filter-section">
            <span class="filter-label">ROOT NOTE:</span>
            <div class="filter-buttons">
              <button
                class="filter-pill"
                :class="{ active: selectedRoot === 'ALL' }"
                @click="selectedRoot = 'ALL'"
              >
                ALL
              </button>
              <button
                v-for="r in CHORD_ROOTS"
                :key="r.name"
                class="filter-pill"
                :class="{ active: selectedRoot === r.name }"
                @click="selectedRoot = r.name"
              >
                {{ r.name }}<span v-if="r.alt" class="alt-label">/{{ r.alt }}</span>
              </button>
            </div>
          </div>

          <!-- Chord Quality Filter -->
          <div class="filter-section">
            <span class="filter-label">QUALITY:</span>
            <div class="filter-buttons">
              <button
                class="filter-pill"
                :class="{ active: selectedQuality === 'ALL' }"
                @click="selectedQuality = 'ALL'"
              >
                ALL
              </button>
              <button
                v-for="q in CHORD_TYPES"
                :key="q.id"
                class="filter-pill"
                :class="{ active: selectedQuality === q.id }"
                @click="selectedQuality = q.id"
              >
                {{ q.label }}
              </button>
            </div>
          </div>

          <!-- Search filter -->
          <div class="search-box">
            <span class="search-icon">🔍</span>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="SEARCH CHORDS (e.g. C, Cm, Abm7, F#)..."
              class="search-input"
            />
            <button v-if="searchQuery" class="clear-search" @click="searchQuery = ''">✕</button>
          </div>
        </div>

        <!-- Chords Grid -->
        <div class="modal-grid-container">
          <div v-if="filteredChords.length === 0" class="no-results">
            NO CHORDS MATCHING CURRENT FILTER.
          </div>
          <div v-else class="chords-grid">
            <div
              v-for="chord in filteredChords"
              :key="chord.id"
              class="chord-item-card"
              :class="{ pinned: isChordPinned(chord.id) }"
            >
              <div class="item-top">
                <div class="item-name-group">
                  <span class="item-chord-name">{{ chord.name }}</span>
                  <span class="item-chord-type">{{ chord.typeLabel }}</span>
                </div>
                <button
                  class="item-pin-btn"
                  :class="{ active: isChordPinned(chord.id) }"
                  @click="togglePinChord(chord)"
                >
                  {{ isChordPinned(chord.id) ? "PINNED ✓" : "+ PIN" }}
                </button>
              </div>

              <!-- Mini SVG Keyboard Diagram -->
              <div class="item-diagram">
                <svg class="mini-piano-svg" viewBox="0 0 154 46">
                  <!-- White Keys -->
                  <rect
                    v-for="wk in miniWhiteKeys"
                    :key="`mw-${chord.id}-${wk.semitone}`"
                    :x="wk.x"
                    y="0"
                    width="11"
                    height="45"
                    fill="#ffffff"
                    stroke="#000000"
                    stroke-width="1.2"
                  />
                  <!-- White Key Dots -->
                  <circle
                    v-for="wk in miniWhiteKeys"
                    :key="`mwd-${chord.id}-${wk.semitone}`"
                    v-show="chord.activeSemitones.has(wk.semitone)"
                    :cx="wk.x + 5.5"
                    cy="35"
                    r="3"
                    fill="#000000"
                  />
                  <!-- Black Keys -->
                  <rect
                    v-for="bk in miniBlackKeys"
                    :key="`mb-${chord.id}-${bk.semitone}`"
                    :x="bk.x"
                    y="0"
                    width="7"
                    height="28"
                    fill="#3c1950"
                    stroke="#000000"
                    stroke-width="1"
                  />
                  <!-- Black Key Dots -->
                  <circle
                    v-for="bk in miniBlackKeys"
                    :key="`mbd-${chord.id}-${bk.semitone}`"
                    v-show="chord.activeSemitones.has(bk.semitone)"
                    :cx="bk.x + 3.5"
                    cy="20"
                    r="2.2"
                    fill="#ffffff"
                  />
                </svg>
              </div>

              <!-- Notes & Keyboard Keys -->
              <div class="item-meta">
                <div class="meta-line">
                  <span class="label">NOTES:</span>
                  <span class="value">{{ chord.displayNotes.join(" · ") }}</span>
                </div>
                <div class="meta-line">
                  <span class="label">KEYS:</span>
                  <div class="badges">
                    <span v-for="k in chord.kbKeys" :key="k" class="card-key-badge">{{ k }}</span>
                  </div>
                </div>
              </div>

              <!-- Play preview button -->
              <button class="item-play-btn" @click="playChord(chord)">
                ▶ PLAY SOUND
              </button>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <span class="footer-info">
            SHOWING {{ filteredChords.length }} CHORDS | {{ pinnedChords.length }} PINNED
          </span>
          <button class="footer-done-btn" @click="openChordModal = false">
            DONE
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.piano-container {
  border: 3px solid #000;
  padding: 24px;
  background: #f9f9f9;
  font-family: "Space Mono", monospace;
  position: relative;
}

.piano-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  flex-wrap: wrap;
  gap: 10px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.piano-label {
  font-size: 12px;
  font-weight: 700;
  background: #000;
  color: #fff;
  padding: 4px 8px;
  letter-spacing: 1px;
}

.piano-status {
  font-size: 11px;
  font-weight: 700;
  background: #f8ccd1;
  color: #3c1950;
  border: 2px solid #000;
  padding: 3px 8px;
  letter-spacing: 1px;
}

.open-chords-btn {
  font-family: "Space Mono", monospace;
  font-size: 12px;
  font-weight: 700;
  background: #3c1950;
  color: #fff;
  border: 2.5px solid #000;
  box-shadow: 4px 4px 0 0 #000;
  padding: 6px 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s ease;
  letter-spacing: 1px;
}

.open-chords-btn:hover {
  background: #000;
  transform: translate(-1px, -1px);
  box-shadow: 5px 5px 0 0 #000;
}

.open-chords-btn:active {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 0 #000;
}

.btn-icon {
  color: #f8ccd1;
}

.pinned-pill {
  background: #f8ccd1;
  color: #000;
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  border: 1.5px solid #000;
  margin-left: 4px;
}

/* ==================== MAIN KEYBOARD ==================== */
.piano-keyboard {
  display: flex;
  position: relative;
  border: 3px solid #000;
  background: #f8ccd1;
  box-shadow: 10px 10px 0 0 #000;
  user-select: none;
}

.white-key {
  flex: 1;
  height: 210px;
  border-right: 3px solid #000;
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding-bottom: 10px;
  position: relative;
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    top 0.15s ease;
  top: 0;
}

.white-key:last-of-type {
  border-right: none;
}

.white-key:hover:not(:has(.black-key:hover)) {
  background: #f8ccd1;
  top: 5px;
}

.white-key:hover:not(:has(.black-key:hover)) .black-key {
  top: -5px;
}

.white-key:has(.black-key:hover) {
  background: #fff;
  transform: none;
}

.black-key {
  position: absolute;
  top: 0;
  right: -1.5px;
  transform: translateX(50%);
  width: 65%;
  height: 135px;
  background: #3c1950;
  border: 3px solid #000;
  border-top: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding-bottom: 6px;
  cursor: pointer;
  z-index: 10;
  transition:
    background-color 0.15s ease,
    top 0.15s ease;
}

.black-key:hover {
  background: #000;
}

/* Key text labels */
.note-name {
  font-family: "JetBrains Mono", monospace;
  font-size: 9px;
  font-weight: 500;
  color: #777;
  line-height: 1;
  margin-bottom: 3px;
}

.key-label {
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  font-weight: 700;
  color: #3c1950;
  line-height: 1;
}

.black-key .note-name {
  color: rgba(255, 255, 255, 0.5);
  font-size: 8px;
}

.black-key .key-label {
  color: #fff;
  font-size: 12px;
}

/* Active / Pressed states */
.key-pressed {
  background: #3c1950 !important;
}

.key-pressed .key-label,
.key-pressed .note-name {
  color: #fff !important;
}

.black-key.key-pressed {
  background: #000 !important;
  box-shadow: inset 0 0 10px #f8ccd1;
}

.black-key.key-pressed .key-label {
  color: #f8ccd1 !important;
}

/* Chord Highlight on main keyboard */
.white-key.chord-highlighted {
  background: #fce4e8 !important;
  box-shadow: inset 0 -12px 0 0 #3c1950 !important;
}

.white-key.chord-highlighted .key-label {
  color: #000;
  font-weight: 800;
}

.black-key.chord-highlighted {
  background: #5a2675 !important;
  border-color: #000 !important;
  box-shadow: inset 0 0 10px #f8ccd1 !important;
}

.black-key.chord-highlighted .key-label {
  color: #f8ccd1 !important;
}

/* ==================== PINNED CHORDS SHELF ==================== */
.pinned-chords-shelf {
  margin-top: 20px;
  border: 3px solid #000;
  box-shadow: 6px 6px 0 0 #000;
  background: #fff;
}

.shelf-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #000;
  color: #fff;
  padding: 8px 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  flex-wrap: wrap;
  gap: 8px;
}

.shelf-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.shelf-tag {
  background: #3c1950;
  color: #fff;
  padding: 2px 6px;
  border: 1px solid #fff;
}

.shelf-count {
  color: #f8ccd1;
}

.shelf-active-hint {
  font-size: 10px;
  color: #f8ccd1;
}

.shelf-active-hint strong {
  color: #fff;
  text-decoration: underline;
}

.shelf-actions {
  display: flex;
  gap: 6px;
}

.shelf-btn {
  font-family: "Space Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  border: 1.5px solid #000;
  padding: 4px 8px;
  cursor: pointer;
  letter-spacing: 1px;
}

.shelf-btn.add-btn {
  background: #f8ccd1;
  color: #000;
}

.shelf-btn.add-btn:hover {
  background: #fff;
}

.shelf-btn.clear-btn {
  background: #ff5555;
  color: #fff;
}

.shelf-btn.clear-btn:hover {
  background: #cc0000;
}

.empty-shelf {
  padding: 20px;
  text-align: center;
  cursor: pointer;
  background: #fdf6f7;
  border-bottom: 2px dashed #3c1950;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background 0.15s ease;
}

.empty-shelf:hover {
  background: #fce4e8;
}

.empty-icon {
  font-size: 18px;
  color: #3c1950;
}

.empty-text {
  font-size: 11px;
  font-weight: 700;
  color: #3c1950;
  letter-spacing: 0.5px;
}

.empty-text strong {
  text-decoration: underline;
}

.pinned-cards-grid {
  display: flex;
  overflow-x: auto;
  gap: 12px;
  padding: 12px;
  background: #fbfbfb;
}

.pinned-card {
  min-width: 170px;
  border: 2px solid #000;
  box-shadow: 4px 4px 0 0 #000;
  background: #fff;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.pinned-card:hover {
  transform: translateY(-2px);
  box-shadow: 5px 5px 0 0 #000;
}

.pinned-card.card-highlighted {
  border-color: #3c1950;
  background: #fff9fa;
  box-shadow: 4px 4px 0 0 #3c1950;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.card-name-wrap {
  display: flex;
  flex-direction: column;
}

.card-chord-name {
  font-size: 15px;
  font-weight: 800;
  color: #000;
  line-height: 1;
}

.card-chord-type {
  font-size: 9px;
  font-weight: 700;
  color: #777;
  letter-spacing: 0.5px;
}

.card-remove-btn {
  background: none;
  border: 1.5px solid #000;
  font-size: 10px;
  font-weight: 700;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  line-height: 1;
  transition: all 0.1s ease;
}

.card-remove-btn:hover {
  background: #000;
  color: #fff;
}

.card-diagram-box {
  background: #fff;
  border: 1.5px solid #000;
  padding: 4px;
  display: flex;
  justify-content: center;
}

.mini-piano-svg {
  width: 100%;
  max-width: 154px;
  height: auto;
  display: block;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 10px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.meta-label {
  font-size: 9px;
  font-weight: 700;
  color: #666;
}

.meta-value {
  font-family: "JetBrains Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  color: #000;
}

.key-badges {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.card-key-badge {
  font-family: "JetBrains Mono", monospace;
  font-size: 11px;
  font-weight: 700;
  background: #3c1950;
  color: #fff;
  padding: 1px 6px;
  border: 1px solid #000;
}

.card-actions {
  display: flex;
  gap: 6px;
  margin-top: 2px;
}

.action-btn {
  flex: 1;
  font-family: "Space Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  border: 1.5px solid #000;
  padding: 4px 6px;
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: all 0.15s ease;
}

.action-btn.play-btn {
  background: #000;
  color: #fff;
}

.action-btn.play-btn:hover {
  background: #3c1950;
}

.action-btn.highlight-btn {
  background: #fff;
  color: #000;
}

.action-btn.highlight-btn:hover {
  background: #f8ccd1;
}

.action-btn.highlight-btn.active {
  background: #3c1950;
  color: #f8ccd1;
}

/* ==================== OCTAVE CONTROLS ==================== */
.controls-row {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.octave-controls {
  display: inline-flex;
  align-items: center;
  border: 3px solid #000;
  box-shadow: 6px 6px 0 0 #000;
  background: #fff;
}

.ctrl-btn {
  font-family: "Space Mono", monospace;
  font-size: 12px;
  font-weight: 700;
  background: #000;
  color: #fff;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.15s ease;
  letter-spacing: 1px;
}

.ctrl-btn:hover {
  background: #3c1950;
}

.ctrl-btn:active {
  background: #f8ccd1;
  color: #000;
}

.ctrl-btn.reset-btn {
  background: #555;
  border-left: 2px solid #000;
}

.ctrl-btn.reset-btn:hover {
  background: #000;
}

.octave-label {
  font-family: "Space Mono", monospace;
  font-size: 13px;
  font-weight: 700;
  background: #f8ccd1;
  color: #000;
  padding: 8px 20px;
  border-left: 3px solid #000;
  border-right: 3px solid #000;
  letter-spacing: 1.5px;
  white-space: nowrap;
}

/* ==================== TWO-ROW KEYBOARD MAP DISPLAY ==================== */
.key-mappings {
  margin-top: 24px;
  border: 3px solid #000;
  box-shadow: 6px 6px 0 0 #000;
  background: #fff;
}

.mappings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #000;
  color: #fff;
  padding: 8px 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  flex-wrap: wrap;
  gap: 8px;
}

.mappings-hint {
  color: #f8ccd1;
  font-size: 10px;
}

.two-deck-container {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.deck-section {
  padding: 12px 16px;
  border-bottom: 2px solid #000;
}

.deck-section:last-child {
  border-bottom: none;
}

.deck-title {
  font-size: 10px;
  font-weight: 800;
  color: #3c1950;
  margin-bottom: 8px;
  letter-spacing: 1.5px;
}

.deck-rows {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.key-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.deck-tag {
  font-size: 9px;
  font-weight: 700;
  padding: 3px 6px;
  border: 1.5px solid #000;
  min-width: 75px;
  text-align: center;
}

.black-row .deck-tag {
  background: #3c1950;
  color: #fff;
}

.white-row .deck-tag {
  background: #e4e4e4;
  color: #000;
}

.deck-keys {
  display: flex;
  gap: 5px;
  align-items: center;
  flex-wrap: wrap;
}

.deck-btn {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1.5px solid #000;
  padding: 2px 6px;
  min-width: 26px;
  line-height: 1;
  transition: all 0.1s ease;
}

.deck-btn.black {
  background: #3c1950;
  color: #fff;
}

.deck-btn.black .k-note {
  color: rgba(255, 255, 255, 0.65);
}

.deck-btn.white {
  background: #fff;
  color: #000;
}

.deck-btn.white .k-note {
  color: #666;
}

.deck-btn.active {
  background: #000 !important;
  color: #f8ccd1 !important;
  transform: scale(1.1);
  box-shadow: 2px 2px 0 0 #000;
}

.deck-btn.active .k-note {
  color: #fff !important;
}

.k-char {
  font-family: "JetBrains Mono", monospace;
  font-size: 12px;
  font-weight: 800;
}

.k-note {
  font-family: "JetBrains Mono", monospace;
  font-size: 8px;
  margin-top: 2px;
}

.deck-gap {
  width: 14px;
}

/* ==================== CHORD MODAL ==================== */
.chord-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.chord-modal {
  width: 100%;
  max-width: 960px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 4px solid #000;
  box-shadow: 12px 12px 0 0 #000;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #000;
  color: #fff;
  padding: 10px 16px;
}

.modal-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-tag {
  background: #f8ccd1;
  color: #000;
  font-size: 12px;
  font-weight: 800;
  padding: 3px 8px;
  letter-spacing: 1px;
}

.modal-subtitle {
  font-size: 11px;
  color: #ccc;
  letter-spacing: 1px;
}

.modal-close-btn {
  background: #3c1950;
  color: #fff;
  border: 2px solid #fff;
  font-family: "Space Mono", monospace;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  cursor: pointer;
  transition: all 0.1s ease;
}

.modal-close-btn:hover {
  background: #ff4444;
  border-color: #ff4444;
}

.modal-controls {
  padding: 12px 16px;
  background: #fdf6f7;
  border-bottom: 3px solid #000;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-section {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-label {
  font-size: 10px;
  font-weight: 800;
  color: #3c1950;
  min-width: 80px;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.filter-pill {
  font-family: "Space Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  background: #fff;
  color: #000;
  border: 1.5px solid #000;
  padding: 3px 8px;
  cursor: pointer;
  transition: all 0.1s ease;
}

.filter-pill:hover {
  background: #fce4e8;
}

.filter-pill.active {
  background: #3c1950;
  color: #fff;
  border-color: #000;
}

.filter-pill .alt-label {
  font-size: 8px;
  opacity: 0.8;
}

.search-box {
  display: flex;
  align-items: center;
  background: #fff;
  border: 2px solid #000;
  padding: 4px 8px;
  gap: 8px;
}

.search-icon {
  font-size: 12px;
}

.search-input {
  flex: 1;
  border: none;
  font-family: "Space Mono", monospace;
  font-size: 11px;
  outline: none;
}

.clear-search {
  background: none;
  border: none;
  font-size: 12px;
  cursor: pointer;
  font-weight: bold;
}

.modal-grid-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #fbfbfb;
}

.no-results {
  text-align: center;
  padding: 40px;
  font-size: 13px;
  font-weight: 700;
  color: #888;
}

.chords-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.chord-item-card {
  border: 2px solid #000;
  box-shadow: 4px 4px 0 0 #000;
  background: #fff;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: transform 0.1s ease;
}

.chord-item-card:hover {
  transform: translateY(-2px);
  box-shadow: 5px 5px 0 0 #000;
}

.chord-item-card.pinned {
  border-color: #3c1950;
  background: #fdf6f7;
}

.item-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.item-name-group {
  display: flex;
  flex-direction: column;
}

.item-chord-name {
  font-size: 16px;
  font-weight: 800;
  color: #000;
  line-height: 1.1;
}

.item-chord-type {
  font-size: 9px;
  font-weight: 700;
  color: #666;
}

.item-pin-btn {
  font-family: "Space Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  border: 1.5px solid #000;
  background: #fff;
  color: #000;
  padding: 2px 6px;
  cursor: pointer;
  transition: all 0.1s ease;
}

.item-pin-btn:hover {
  background: #f8ccd1;
}

.item-pin-btn.active {
  background: #3c1950;
  color: #fff;
}

.item-diagram {
  background: #fff;
  border: 1.5px solid #000;
  padding: 4px;
}

.item-meta {
  display: flex;
  flex-direction: column;
  gap: 3px;
  font-size: 9px;
}

.meta-line {
  display: flex;
  align-items: center;
  gap: 6px;
}

.meta-line .label {
  font-weight: 700;
  color: #666;
}

.meta-line .value {
  font-family: "JetBrains Mono", monospace;
  font-weight: 700;
  color: #000;
}

.meta-line .badges {
  display: flex;
  gap: 3px;
  flex-wrap: wrap;
}

.item-play-btn {
  font-family: "Space Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  background: #000;
  color: #fff;
  border: 1.5px solid #000;
  padding: 5px;
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: background 0.1s ease;
}

.item-play-btn:hover {
  background: #3c1950;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f0f0f0;
  border-top: 3px solid #000;
  padding: 10px 16px;
}

.footer-info {
  font-size: 10px;
  font-weight: 700;
  color: #444;
}

.footer-done-btn {
  font-family: "Space Mono", monospace;
  font-size: 11px;
  font-weight: 700;
  background: #000;
  color: #fff;
  border: 2px solid #000;
  padding: 5px 16px;
  cursor: pointer;
}

.footer-done-btn:hover {
  background: #3c1950;
}
</style>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import * as Tone from "tone";

// ************** TWO-ROW PIANO KEYBOARD ENGINE **************
// NO SHIFT REQUIRED! Plays chords across multiple octaves with both hands!
const keyMap = {
  // Lower Deck (Octave 3 & start of 4 - Left Hand)
  // Whites (Bottom row): z x c v b n m , . /
  z: { name: "C", octave: 3 },
  x: { name: "D", octave: 3 },
  c: { name: "E", octave: 3 },
  v: { name: "F", octave: 3 },
  b: { name: "G", octave: 3 },
  n: { name: "A", octave: 3 },
  m: { name: "B", octave: 3 },
  ",": { name: "C", octave: 4 },
  ".": { name: "D", octave: 4 },
  "/": { name: "E", octave: 4 },

  // Blacks (Home row): s d   g h j   l ;
  s: { name: "C#", octave: 3 },
  d: { name: "D#", octave: 3 },
  g: { name: "F#", octave: 3 },
  h: { name: "G#", octave: 3 },
  j: { name: "A#", octave: 3 },
  l: { name: "C#", octave: 4 },
  ";": { name: "D#", octave: 4 },

  // Upper Deck (Octave 4 & 5 - Right Hand)
  // Whites (QWERTY row): q w e r t y u i o p [ ]
  q: { name: "C", octave: 4 },
  w: { name: "D", octave: 4 },
  e: { name: "E", octave: 4 },
  r: { name: "F", octave: 4 },
  t: { name: "G", octave: 4 },
  y: { name: "A", octave: 4 },
  u: { name: "B", octave: 4 },
  i: { name: "C", octave: 5 },
  o: { name: "D", octave: 5 },
  p: { name: "E", octave: 5 },
  "[": { name: "F", octave: 5 },
  "]": { name: "G", octave: 5 },

  // Blacks (Number row): 2 3   5 6 7   9 0   =
  "2": { name: "C#", octave: 4 },
  "3": { name: "D#", octave: 4 },
  "5": { name: "F#", octave: 4 },
  "6": { name: "G#", octave: 4 },
  "7": { name: "A#", octave: 4 },
  "9": { name: "C#", octave: 5 },
  "0": { name: "D#", octave: 5 },
  "=": { name: "F#", octave: 5 },
};

// 61-Key On-Screen Piano Data
const octavesData = [
  {
    octave: 3,
    whiteKeys: [
      { name: "C", key: "z" },
      { name: "D", key: "x" },
      { name: "E", key: "c" },
      { name: "F", key: "v" },
      { name: "G", key: "b" },
      { name: "A", key: "n" },
      { name: "B", key: "m" },
    ],
    blackKeys: {
      C: { name: "C#", key: "s" },
      D: { name: "D#", key: "d" },
      F: { name: "F#", key: "g" },
      G: { name: "G#", key: "h" },
      A: { name: "A#", key: "j" },
    },
  },
  {
    octave: 4,
    whiteKeys: [
      { name: "C", key: "q", altKey: "," },
      { name: "D", key: "w", altKey: "." },
      { name: "E", key: "e", altKey: "/" },
      { name: "F", key: "r" },
      { name: "G", key: "t" },
      { name: "A", key: "y" },
      { name: "B", key: "u" },
    ],
    blackKeys: {
      C: { name: "C#", key: "2", altKey: "l" },
      D: { name: "D#", key: "3", altKey: ";" },
      F: { name: "F#", key: "5" },
      G: { name: "G#", key: "6" },
      A: { name: "A#", key: "7" },
    },
  },
  {
    octave: 5,
    whiteKeys: [
      { name: "C", key: "i" },
      { name: "D", key: "o" },
      { name: "E", key: "p" },
      { name: "F", key: "[" },
      { name: "G", key: "]" },
      { name: "A", key: "" },
      { name: "B", key: "" },
    ],
    blackKeys: {
      C: { name: "C#", key: "9" },
      D: { name: "D#", key: "0" },
      F: { name: "F#", key: "=" },
      G: { name: "G#", key: "" },
      A: { name: "A#", key: "" },
    },
  },
  {
    octave: 6,
    whiteKeys: [
      { name: "C", key: "" },
      { name: "D", key: "" },
      { name: "E", key: "" },
      { name: "F", key: "" },
      { name: "G", key: "" },
      { name: "A", key: "" },
      { name: "B", key: "" },
    ],
    blackKeys: {
      C: { name: "C#", key: "" },
      D: { name: "D#", key: "" },
      F: { name: "F#", key: "" },
      G: { name: "G#", key: "" },
      A: { name: "A#", key: "" },
    },
  },
  {
    octave: 7,
    whiteKeys: [
      { name: "C", key: "" },
      { name: "D", key: "" },
      { name: "E", key: "" },
      { name: "F", key: "" },
      { name: "G", key: "" },
      { name: "A", key: "" },
      { name: "B", key: "" },
    ],
    blackKeys: {
      C: { name: "C#", key: "" },
      D: { name: "D#", key: "" },
      F: { name: "F#", key: "" },
      G: { name: "G#", key: "" },
      A: { name: "A#", key: "" },
    },
  },
];

const notes = ref([]);
const octaveShift = ref(0);
const pressedKeys = ref(new Set());

// Generate the 61-key piano
const generateNotes = () => {
  notes.value = [];

  octavesData.forEach((oct) => {
    oct.whiteKeys.forEach((w) => {
      const b = oct.blackKeys[w.name];

      notes.value.push({
        name: w.name,
        octave: oct.octave,
        kbKey: w.key,
        altKey: w.altKey || null,
        isBlack: false,
        blackKey: b
          ? {
              name: b.name,
              octave: oct.octave,
              kbKey: b.key,
              altKey: b.altKey || null,
              isBlack: true,
            }
          : null,
      });
    });
  });

  // Final C8 note
  notes.value.push({
    name: "C",
    octave: 8,
    kbKey: "",
    isBlack: false,
    blackKey: null,
  });
};

// ************** CHORD ENGINE & MAPPING **************
const CHROMATIC_SCALE = [
  "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
];

const CHORD_ROOTS = [
  { name: "C", alt: "", semitone: 0 },
  { name: "C#", alt: "Db", semitone: 1 },
  { name: "D", alt: "", semitone: 2 },
  { name: "D#", alt: "Eb", semitone: 3 },
  { name: "E", alt: "", semitone: 4 },
  { name: "F", alt: "", semitone: 5 },
  { name: "F#", alt: "Gb", semitone: 6 },
  { name: "G", alt: "", semitone: 7 },
  { name: "G#", alt: "Ab", semitone: 8 },
  { name: "A", alt: "", semitone: 9 },
  { name: "A#", alt: "Bb", semitone: 10 },
  { name: "B", alt: "", semitone: 11 },
];

const CHORD_TYPES = [
  { id: "maj", label: "Major", suffix: "", intervals: [0, 4, 7] },
  { id: "min", label: "Minor", suffix: "m", intervals: [0, 3, 7] },
  { id: "7", label: "7th", suffix: "7", intervals: [0, 4, 7, 10] },
  { id: "maj7", label: "Maj7", suffix: "maj7", intervals: [0, 4, 7, 11] },
  { id: "m7", label: "Min7", suffix: "m7", intervals: [0, 3, 7, 10] },
];

// Mini piano diagram key layout: 2 full octaves (C to B twice)
const miniWhiteKeys = [
  { semitone: 0, x: 0 },
  { semitone: 2, x: 11 },
  { semitone: 4, x: 22 },
  { semitone: 5, x: 33 },
  { semitone: 7, x: 44 },
  { semitone: 9, x: 55 },
  { semitone: 11, x: 66 },
  { semitone: 12, x: 77 },
  { semitone: 14, x: 88 },
  { semitone: 16, x: 99 },
  { semitone: 17, x: 110 },
  { semitone: 19, x: 121 },
  { semitone: 21, x: 132 },
  { semitone: 23, x: 143 },
];

const miniBlackKeys = [
  { semitone: 1, x: 7.5 },
  { semitone: 3, x: 18.5 },
  { semitone: 6, x: 40.5 },
  { semitone: 8, x: 51.5 },
  { semitone: 10, x: 62.5 },
  { semitone: 13, x: 84.5 },
  { semitone: 15, x: 95.5 },
  { semitone: 18, x: 117.5 },
  { semitone: 20, x: 128.5 },
  { semitone: 22, x: 139.5 },
];

// Map semitone 0-23 to Upper Deck (Octave 4 & 5) without Shift
// Semitone 0 = C4 ('q'), 1 = C#4 ('2'), 2 = D4 ('w'), etc.
const SEMITONE_TO_KEY = [
  // Octave 4
  "q", "2", "w", "3", "e", "r", "5", "t", "6", "y", "7", "u",
  // Octave 5
  "i", "9", "o", "0", "p", "[", "=", "]",
];

// Build comprehensive chord catalogue
const allChords = [];
CHORD_ROOTS.forEach((root) => {
  CHORD_TYPES.forEach((type) => {
    const chordName = `${root.name}${type.suffix}`;
    const activeSemitones = new Set();
    const displayNotes = [];
    const soundNotes = [];
    const kbKeys = [];

    type.intervals.forEach((interval) => {
      const semitone = root.semitone + interval;
      activeSemitones.add(semitone);

      const noteName = CHROMATIC_SCALE[semitone % 12];
      displayNotes.push(noteName);

      const noteOctave = 4 + Math.floor(semitone / 12);
      soundNotes.push({ name: noteName, octave: noteOctave });

      if (semitone < SEMITONE_TO_KEY.length && SEMITONE_TO_KEY[semitone]) {
        kbKeys.push(SEMITONE_TO_KEY[semitone]);
      }
    });

    allChords.push({
      id: chordName,
      name: chordName,
      root: root.name,
      rootAlt: root.alt,
      typeId: type.id,
      typeLabel: type.label,
      activeSemitones,
      displayNotes,
      soundNotes,
      kbKeys,
    });
  });
});

// Pinned chords & modal state
const pinnedChords = ref([
  allChords.find((c) => c.name === "C"),
  allChords.find((c) => c.name === "G"),
  allChords.find((c) => c.name === "Am"),
  allChords.find((c) => c.name === "F"),
].filter(Boolean));

const openChordModal = ref(false);
const selectedRoot = ref("ALL");
const selectedQuality = ref("ALL");
const searchQuery = ref("");
const activeHighlightChord = ref(null);

const filteredChords = computed(() => {
  return allChords.filter((chord) => {
    if (selectedRoot.value !== "ALL" && chord.root !== selectedRoot.value) {
      return false;
    }
    if (selectedQuality.value !== "ALL" && chord.typeId !== selectedQuality.value) {
      return false;
    }
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.trim().toLowerCase();
      const matchName = chord.name.toLowerCase().includes(q);
      const matchRoot = chord.root.toLowerCase().includes(q);
      const matchAlt = chord.rootAlt && chord.rootAlt.toLowerCase().includes(q);
      const matchType = chord.typeLabel.toLowerCase().includes(q);
      if (!matchName && !matchRoot && !matchAlt && !matchType) return false;
    }
    return true;
  });
});

const isChordPinned = (chordId) => {
  return pinnedChords.value.some((c) => c.id === chordId);
};

const togglePinChord = (chord) => {
  const idx = pinnedChords.value.findIndex((c) => c.id === chord.id);
  if (idx > -1) {
    pinnedChords.value.splice(idx, 1);
    if (activeHighlightChord.value?.id === chord.id) {
      activeHighlightChord.value = null;
    }
  } else {
    pinnedChords.value.push(chord);
  }
};

const unpinChord = (chordId) => {
  const idx = pinnedChords.value.findIndex((c) => c.id === chordId);
  if (idx > -1) {
    pinnedChords.value.splice(idx, 1);
    if (activeHighlightChord.value?.id === chordId) {
      activeHighlightChord.value = null;
    }
  }
};

const clearAllPinnedChords = () => {
  pinnedChords.value = [];
  activeHighlightChord.value = null;
};

const toggleHighlightChord = (chord) => {
  if (activeHighlightChord.value?.id === chord.id) {
    activeHighlightChord.value = null;
  } else {
    activeHighlightChord.value = chord;
  }
};

const isNoteInActiveChord = (noteName) => {
  if (!activeHighlightChord.value) return false;
  return activeHighlightChord.value.displayNotes.includes(noteName);
};

const playChord = (chord) => {
  initToneAudio();

  chord.soundNotes.forEach((note, index) => {
    setTimeout(() => {
      playNote(note.name, note.octave + octaveShift.value);
    }, index * 22);
  });
};

// ************** TONE.JS AUDIO ENGINE **************
let pianoSampler = null;
let pianoSynth = null;
let isToneStarted = false;

const initToneAudio = async () => {
  if (!isToneStarted) {
    await Tone.start();
    isToneStarted = true;
  }

  if (!pianoSynth) {
    // Rich polyphonic synthesizer for immediate, zero-latency response
    pianoSynth = new Tone.PolySynth(Tone.Synth, {
      volume: -4,
      oscillator: { type: "triangle8" },
      envelope: {
        attack: 0.005,
        decay: 1.8,
        sustain: 0.15,
        release: 1.4,
      },
    }).toDestination();
  }

  if (!pianoSampler) {
    // Official Tone.js Salamander Grand Piano acoustic soundfont
    pianoSampler = new Tone.Sampler({
      urls: {
        A0: "A0.mp3",
        C1: "C1.mp3",
        "D#1": "Ds1.mp3",
        "F#1": "Fs1.mp3",
        A1: "A1.mp3",
        C2: "C2.mp3",
        "D#2": "Ds2.mp3",
        "F#2": "Fs2.mp3",
        A2: "A2.mp3",
        C3: "C3.mp3",
        "D#3": "Ds3.mp3",
        "F#3": "Fs3.mp3",
        A3: "A3.mp3",
        C4: "C4.mp3",
        "D#4": "Ds4.mp3",
        "F#4": "Fs4.mp3",
        A4: "A4.mp3",
        C5: "C5.mp3",
        "D#5": "Ds5.mp3",
        "F#5": "Fs5.mp3",
        A5: "A5.mp3",
        C6: "C6.mp3",
        "D#6": "Ds6.mp3",
        "F#6": "Fs6.mp3",
        A6: "A6.mp3",
        C7: "C7.mp3",
        "D#7": "Ds7.mp3",
        "F#7": "Fs7.mp3",
        A7: "A7.mp3",
        C8: "C8.mp3",
      },
      release: 1.2,
      baseUrl: "https://tonejs.github.io/audio/salamander/",
    }).toDestination();
  }
};

const playNote = (noteName, octave) => {
  initToneAudio();

  const noteWithOctave = `${noteName}${octave}`;

  try {
    if (pianoSampler && pianoSampler.loaded) {
      pianoSampler.triggerAttackRelease(noteWithOctave, "2n");
    } else if (pianoSynth) {
      pianoSynth.triggerAttackRelease(noteWithOctave, "2n");
    }
  } catch (e) {
    console.warn("Tone audio error:", e);
  }
};

// ************** KEYBOARD LISTENER (CASE-INSENSITIVE / NO SHIFT) **************
const handleKeyDown = (event) => {
  if (event.repeat) return;

  // ESC closes chord modal
  if (event.key === "Escape" && openChordModal.value) {
    openChordModal.value = false;
    return;
  }

  const key = event.key.toLowerCase();

  if (pressedKeys.value.has(key)) return;

  const noteInfo = keyMap[key];
  if (!noteInfo) return;

  event.preventDefault();
  pressedKeys.value.add(key);

  playNote(noteInfo.name, noteInfo.octave + octaveShift.value);
};

const handleKeyUp = (event) => {
  const key = event.key.toLowerCase();
  pressedKeys.value.delete(key);
};

const isKeyPressed = (kbKey, altKey) => {
  if (!kbKey && !altKey) return false;
  return (
    (kbKey && pressedKeys.value.has(kbKey)) ||
    (altKey && pressedKeys.value.has(altKey))
  );
};

const changeOctave = (direction) => {
  const newShift = octaveShift.value + direction;
  if (newShift >= -3 && newShift <= 3) {
    octaveShift.value = newShift;
  }
};

onMounted(() => {
  generateNotes();
  initToneAudio();

  window.addEventListener("keydown", handleKeyDown);
  window.addEventListener("keyup", handleKeyUp);
  window.addEventListener("blur", () => pressedKeys.value.clear());
});

onUnmounted(() => {
  window.removeEventListener("keydown", handleKeyDown);
  window.removeEventListener("keyup", handleKeyUp);
});
</script>

# Example 1: Simple Melody Generation
"""
This example demonstrates how to programmatically generate a simple melody
using the CA Music Composer system.

Run with: python examples/example_1_simple_melody.py
"""

import numpy as np
from music21 import note, stream, clef, instrument, converter

# ============================================================================
# CONFIGURATION
# ============================================================================

# CA Parameters
GENERATIONS = 30
GRID_LENGTH = 40
NUM_STATES = 8
NEIGHBORHOOD_SIZE = 1
INITIAL_CELL = 20  # Middle of grid

# Musical Parameters
INITIAL_NOTE = 'C'
OCTAVES = [5, 6]
RHYTHMIC_VALUE = 1.0  # Quarter note
INSTRUMENT_TYPE = 'Flute'

# ============================================================================
# CELLULAR AUTOMATON FUNCTIONS
# ============================================================================

def generate_rule_matrix_deterministic(num_states):
    """Generate a deterministic rule matrix."""
    return np.array([
        [(i + j) % num_states for j in range(num_states)] 
        for i in range(num_states)
    ])


def generate_ca(rule_matrix, generations, length, num_states, 
                neighborhood_size, initial_cell):
    """Generate cellular automaton evolution."""
    ca = np.zeros((generations, length), dtype=int)
    ca[0, initial_cell] = 1
    
    for gen in range(1, generations):
        for i in range(length):
            neighbor_sum = 0
            for offset in range(-neighborhood_size, neighborhood_size + 1):
                if offset != 0:
                    neighbor_index = (i + offset) % length
                    neighbor_sum += ca[gen - 1, neighbor_index]
            
            current_state = ca[gen - 1, i]
            ca[gen, i] = rule_matrix[current_state, neighbor_sum % num_states]
    
    return ca


# ============================================================================
# MUSICAL CONVERSION FUNCTIONS
# ============================================================================

def create_note_list(initial_note, octaves):
    """Create ordered list of notes."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    start_index = notes.index(initial_note)
    reordered = notes[start_index:] + notes[:start_index]
    
    note_list = []
    for i, n in enumerate(reordered):
        octave = octaves[i % len(octaves)]
        note_list.append(f"{n}{octave}")
    
    return note_list


def ca_to_music21(ca, note_list, rhythmic_value, instrument_type):
    """Convert CA to Music21 score."""
    part = stream.Part()
    part.insert(0, clef.TrebleClef())
    part.insert(0, getattr(instrument, instrument_type)())
    
    for row in ca:
        for cell in row:
            if cell > 0:
                pitch = note_list[(cell - 1) % len(note_list)]
                new_note = note.Note(pitch)
                new_note.quarterLength = rhythmic_value
                part.append(new_note)
            else:
                new_rest = note.Rest()
                new_rest.quarterLength = rhythmic_value
                part.append(new_rest)
    
    return part


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 70)
    print("CA MUSIC COMPOSER - EXAMPLE 1: SIMPLE MELODY")
    print("=" * 70)
    print()
    
    # Step 1: Generate CA
    print("📊 Step 1: Generating Cellular Automaton...")
    rule_matrix = generate_rule_matrix_deterministic(NUM_STATES)
    ca = generate_ca(
        rule_matrix, 
        GENERATIONS, 
        GRID_LENGTH, 
        NUM_STATES,
        NEIGHBORHOOD_SIZE, 
        INITIAL_CELL
    )
    print(f"   ✓ CA generated: {GENERATIONS}x{GRID_LENGTH} grid")
    print(f"   ✓ Active cells: {np.sum(ca > 0)} / {ca.size}")
    print()
    
    # Step 2: Create note mapping
    print("🎵 Step 2: Creating musical mapping...")
    note_list = create_note_list(INITIAL_NOTE, OCTAVES)
    print(f"   ✓ Note list: {', '.join(note_list[:8])}...")
    print()
    
    # Step 3: Convert to music
    print("🎼 Step 3: Converting to musical score...")
    part = ca_to_music21(ca, note_list, RHYTHMIC_VALUE, INSTRUMENT_TYPE)
    
    # Count notes
    all_notes = list(part.flatten().notes)
    num_notes = len([n for n in all_notes if isinstance(n, note.Note)])
    num_rests = len([n for n in all_notes if isinstance(n, note.Rest)])
    
    print(f"   ✓ {num_notes} notes generated")
    print(f"   ✓ {num_rests} rests")
    print(f"   ✓ Total duration: {part.quarterLength} quarter notes")
    print()
    
    # Step 4: Create full score
    print("📝 Step 4: Creating final score...")
    score = stream.Score()
    score.insert(0, part)
    score.metadata = stream.metadata.Metadata()
    score.metadata.title = "CA Simple Melody"
    score.metadata.composer = "CA Music Composer"
    print("   ✓ Score created")
    print()
    
    # Step 5: Export
    print("💾 Step 5: Exporting...")
    
    # Export MIDI
    midi_file = "output/example_1_simple_melody.mid"
    score.write('midi', fp=midi_file)
    print(f"   ✓ MIDI saved: {midi_file}")
    
    # Export MusicXML
    xml_file = "output/example_1_simple_melody.musicxml"
    score.write('musicxml', fp=xml_file)
    print(f"   ✓ MusicXML saved: {xml_file}")
    
    print()
    print("=" * 70)
    print("✅ COMPOSITION COMPLETE!")
    print("=" * 70)
    print()
    print("📂 Files created:")
    print(f"   • {midi_file}")
    print(f"   • {xml_file}")
    print()
    print("🎵 Next steps:")
    print("   1. Open MIDI file with VLC or any MIDI player")
    print("   2. Open MusicXML in MuseScore to view/edit the score")
    print("   3. Try modifying parameters at the top of this file!")
    print()


if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)
    main()

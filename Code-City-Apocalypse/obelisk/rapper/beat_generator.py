#!/usr/bin/env python3
from mido import MidiFile, MidiTrack, Message

class BeatGenerator:
    def __init__(self, bpm=140):
        self.bpm = bpm
    
    def create_beat(self, style='trap', bars=8):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        
        pattern = []
        ticks = 384
        
        for bar in range(bars):
            offset = bar * ticks
            # Kick
            pattern.append((36, 100, offset if bar == 0 else 0))
            # Snare
            pattern.append((38, 90, ticks//2))
            # Hi-hats
            for i in range(8):
                pattern.append((42, 60, ticks//16))
        
        for note, vel, time in pattern:
            track.append(Message('note_on', channel=9, note=note, velocity=vel, time=time))
            track.append(Message('note_off', channel=9, note=note, time=96))
        
        return mid

if __name__ == '__main__':
    gen = BeatGenerator()
    beat = gen.create_beat()
    beat.save('/tmp/beat.mid')
    print("✓ Beat: /tmp/beat.mid")

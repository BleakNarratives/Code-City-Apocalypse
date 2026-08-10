# ROADMAP: Riffusion-Meta-Graph Hive-Powered Beat Engine

## Goal
Create an AI-driven, data-graph-informed beat generation system that utilizes persistent hive-state management (`Whorl`) and musical theory constraints.

## Architecture Components
1.  **Hive-State Engine (Whorl):**
    -   Stores active musical context: `[current_key, current_tempo, active_scale, active_mode]`.
    -   Provides real-time debugging: Validates generative output against musical theory graph nodes.
    -   Persistence: Extends existing `~/.whorl/whorl.db` with a new `music_hive` table.

2.  **Synthesis Pipeline (Riffusion-Meta-Graph):**
    -   Integrates with `StableDiffusion` / `Riffusion` models.
    -   Uses `Loomy` / `Neo4j` to traverse musical graph nodes (`Circle of 5ths`, `Camelot Wheel`) for latent space guidance.

3.  **Loomy Connector:**
    -   API Bridge between Neo4j and the Hive State to ensure musical consistency.

## Phase 1: Persistence Layer Setup (Immediate)
- [ ] Define SQLite schema for `music_hive` table.
- [ ] Add `[music_engine]` configuration to `~/.whorl/config.toml`.
- [ ] Implement `Whorl` wrapper to read/write musical state.

## Phase 2: Synthesis Integration (Post-Persistence)
- [ ] Implement `Riffusion` mock endpoint.
- [ ] Wire musical graph traversal from `Loomy`.
- [ ] Implement real-time debugging hook.
- [ ] Implement `AudioInterruptService` for adaptive collaboration.

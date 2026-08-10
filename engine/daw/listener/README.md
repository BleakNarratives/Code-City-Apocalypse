# Audio Listener Agent

## Overview
Monitors real-time audio input for user vocalization, triggering the interrupt protocol in the `MusicHiveService` to facilitate seamless vocal ducking.

## Integration
- **MusicHiveService:** Pushes `COLLAB_MODE` interrupt signal.
- **Async Loop:** Operates as a non-blocking asynchronous task.

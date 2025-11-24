# CLI Session Setup System - Implementation Complete

## Overview

Successfully implemented a robust CLI session-setup workflow for the Smart Training project. The system now collects athlete and training context BEFORE launching the HUD/tracking loop, and organizes all data into per-athlete, per-session folders.

## Changes Made

### 1. Roster Data (data/rosters/)
Created JSON roster files for all 7 sports:

- **football_roster.json** - Hierarchical structure with:
  - Offense: Quarterbacks (Jason Smith #4 FR, Tom Hardy #14 SO, Malik Greene #2 SR), Running Backs, Wide Receivers
  - Defense: Linebackers, Defensive Backs
- **basketball_roster.json** - Placeholder with 1 generic player
- **track_field_roster.json** - Placeholder with 1 generic player
- **soccer_roster.json** - Placeholder with 1 generic player
- **volleyball_roster.json** - Placeholder with 1 generic player
- **cross_country_roster.json** - Placeholder with 1 generic player
- **gymnastics_roster.json** - Placeholder with 1 generic player

### 2. Session Controller (backend/session_controller.py)
New module with complete CLI workflow:

**Functions:**
- `start_session_cli()` - Main entry point, returns session_info dict
- `select_sport()` - Menu for 7 sports
- `load_roster(sport)` - Loads JSON roster
- `select_player_football(roster)` - Hierarchical: Side → Position Group → Player
- `select_player_generic(roster)` - Simple selection for other sports
- `select_training_location(sport)` - Sport-specific locations
- `select_weight_room_session()` - Focus + Exercise selection
- `build_session_info()` - Creates final session_info object

**Supported Sports & Locations:**
- Football: Field, Weight Room, Other
- Basketball: Court, Weight Room, Other
- Track & Field: Track, Field, Weight Room, Other
- Soccer: Field, Weight Room, Other
- Volleyball: Court, Weight Room, Other
- Cross Country: Field, Weight Room, Other
- Gymnastics: Court, Weight Room, Other

**Weight Room Options:**
- Focus: Upper Body, Lower Body, Core, Cardio
- Exercises: Bench Press, Squat, Deadlift, Bicep Curl, Shoulder Press, Lat Pulldowns

**Input Validation:**
- Numeric validation with re-prompting
- Range checking
- Graceful keyboard interrupt handling

### 3. Session Paths (backend/session_paths.py)
New `SessionPaths` class for directory and metadata management:

**Features:**
- Creates folder structure: `data/athletes/{sport}/{player_id}/sessions/{session_id}/`
- Generates unique session IDs: `{timestamp}_{exercise/focus}`
- Writes `session_meta.json` with all context
- Creates empty `metrics.csv` with headers
- Creates `clips/` subdirectory

**Properties:**
- `session_dir` - Session folder path
- `video_path` - Full video file path
- `metrics_path` - Metrics CSV path
- `clips_dir` - Clips folder path
- `metadata_path` - Metadata JSON path

**Methods:**
- `log_metric(rep_index, metric_name, metric_value, notes)` - Append metric to CSV
- `get_clip_path(clip_number)` - Get path for numbered clip

### 4. Main Integration (backend/main.py)
Updated to run CLI before tracking loop:

**Changes:**
- Imports `start_session_cli` and `SessionPaths`
- Runs CLI first to get `session_info`
- Creates `SessionPaths` object
- Passes `session_info` to HUD overlay
- Uses session video path instead of generic output path
- Displays completion message with session folder path

### 5. HUD Overlay (backend/hud_overlay.py)
Enhanced to display session context:

**Changes:**
- Accepts optional `session_info` parameter in `__init__`
- New `_draw_session_banner()` method
- Displays banner at top center with:
  - Sport name (uppercase)
  - Exercise name (if weight room)
  - Player name, number, position
  - Example: "FOOTBALL - Bench Press - Malik Greene #2 (QB)"

## File Structure Created

After a session, the following structure is created:

```
data/athletes/
  football/
    malik_greene_2/
      profile.json
      sessions/
        2025-11-22_22-58-56_bench_press/
          session_meta.json
          metrics.csv
          clips/
```

### session_meta.json Example:

```json
{
  "sport": "football",
  "location": "weight_room",
  "focus": "upper_body",
  "exercise": "bench_press",
  "player": {
    "player_id": "malik_greene_2",
    "full_name": "Malik Greene",
    "number": 2,
    "position": "QB",
    "class_year": "SR",
    "side": "Offense",
    "position_group": "Quarterbacks"
  },
  "timestamp_start": "2025-11-22T22:58:56.123456",
  "human_readable_name": "Football - Malik Greene #2 (QB SR) - Weight Room - Bench Press",
  "session_id": "2025-11-22_22-58-56_bench_press",
  "paths": {
    "session_dir": "data/athletes/football/malik_greene_2/sessions/2025-11-22_22-58-56_bench_press",
    "video_path": "data/athletes/football/malik_greene_2/sessions/2025-11-22_22-58-56_bench_press/full_video.mp4",
    "metrics_path": "data/athletes/football/malik_greene_2/sessions/2025-11-22_22-58-56_bench_press/metrics.csv",
    "clips_dir": "data/athletes/football/malik_greene_2/sessions/2025-11-22_22-58-56_bench_press/clips"
  }
}
```

### metrics.csv Structure:

```csv
timestamp,rep_index,exercise,metric_name,metric_value,notes
```

## Usage

### Basic Flow:

1. Run: `python -m backend.main`
2. CLI prompts appear:
   - Select sport (1-7)
   - Select player (hierarchical for Football)
   - Select training location
   - If weight room: select focus and exercise
3. Session folder is created
4. HUD launches with session context displayed
5. All data saves to session folder
6. On exit, completion message shows session path

### Example Session (Football QB - Bench Press):

```
python -m backend.main

========================================================================================
  SMART TRAINING - SESSION SETUP
============================================================

SELECT SPORT:

  1) Football
  2) Basketball
  3) Track & Field
  4) Soccer
  5) Volleyball
  6) Cross Country
  7) Gymnastics

Choice #: 1

============================================================
SELECT SIDE:

  1) Offense
  2) Defense

Choice #: 1

============================================================
SELECT POSITION GROUP (Offense):

  1) Quarterbacks
  2) Running Backs
  3) Wide Receivers

Choice #: 1

============================================================
SELECT PLAYER (Quarterbacks):

  1) Jason Smith         #4   QB   (FR)
  2) Tom Hardy           #14  QB   (SO)
  3) Malik Greene        #2   QB   (SR)

Choice #: 3

============================================================
SELECT TRAINING LOCATION:

  1) Field
  2) Weight Room
  3) Other

Choice #: 2

============================================================
SELECT WEIGHT ROOM FOCUS:

  1) Upper Body
  2) Lower Body
  3) Core
  4) Cardio

Choice #: 1

============================================================
SELECT EXERCISE (Upper Body):

  1) Bench Press
  2) Squat
  3) Deadlift
  4) Bicep Curl
  5) Shoulder Press
  6) Lat Pulldowns

Choice #: 1

============================================================
SESSION SETUP COMPLETE!
============================================================

Football - Malik Greene #2 (QB SR) - Weight Room - Bench Press
Start Time: 2025-11-22T22:58:56.123456

Launching tracking system...

[Session directory created]
[HUD launches with banner: FOOTBALL - Bench Press - Malik Greene #2 (QB)]
[Tracking runs...]
[Press Q or ESC to exit]
[On exit: Session complete! Data saved to: data/athletes/football/malik_greene_2/sessions/...]
```

## Backward Compatibility

- Existing HUD/tracking functionality unchanged
- All pose detection and angle calculation logic preserved
- Old `data/processed/` directory still exists but unused when CLI is active
- Can still bypass CLI if needed (would require code modification)

## Future Extensibility

Easy to extend:

1. **Add more players**: Edit roster JSON files
2. **Add more exercises**: Update `WEIGHT_ROOM_EXERCISES` list
3. **Add sport-specific movement modes**: Add to location handling
4. **Add rep counting logic**: Use `paths.log_metric()` method
5. **Add video clip saving**: Use `paths.get_clip_path(n)` method

## Testing Recommendations

1. **Test Football full flow** (Side → Position → Player → Weight Room → Exercise)
2. **Test other sport** (simple player selection)
3. **Test invalid input handling** (letters, out-of-range numbers)
4. **Verify folder structure created** correctly
5. **Verify HUD banner displays** session context
6. **Verify video saves** to session folder

## Notes

- Removed emoji characters for Windows console compatibility
- All user input validated with error handling
- Keyboard interrupt (Ctrl+C) handled gracefully
- Session metadata includes all paths for easy access
- Metrics CSV ready for future rep/performance tracking

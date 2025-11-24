"""
Session Controller - CLI workflow for athlete and training context selection.

This module provides an interactive CLI that runs before the tracking loop starts.
It handles sport selection, roster-based player selection, training location/context,
and builds a comprehensive session_info dictionary.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


# Sport configurations with their available training locations
SPORT_LOCATIONS = {
    "football": ["Field", "Weight Room", "Other"],
    "basketball": ["Court", "Weight Room", "Other"],
    "track_field": ["Track", "Field", "Weight Room", "Other"],
    "soccer": ["Field", "Weight Room", "Other"],
    "volleyball": ["Court", "Weight Room", "Other"],
    "cross_country": ["Field", "Weight Room", "Other"],
    "gymnastics": ["Court", "Weight Room", "Other"]
}

# Weight room configuration
WEIGHT_ROOM_FOCUS = ["Upper Body", "Lower Body", "Core", "Cardio"]
WEIGHT_ROOM_EXERCISES = [
    "Bench Press",
    "Squat",
    "Deadlift",
    "Bicep Curl",
    "Shoulder Press",
    "Lat Pulldowns"
]


def clear_screen():
    """Clear console screen (works on Windows and Unix)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_valid_choice(prompt: str, max_option: int) -> int:
    """
    Get a valid numeric choice from user with validation.
    
    Args:
        prompt: The prompt message to display
        max_option: Maximum valid option number
        
    Returns:
        Valid choice as integer (1-indexed)
    """
    while True:
        try:
            choice = input(prompt)
            choice_int = int(choice)
            if 1 <= choice_int <= max_option:
                return choice_int
            else:
                print(f"[!] Invalid choice. Please enter a number between 1 and {max_option}.")
        except ValueError:
            print("[!] Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nSession setup cancelled.")
            exit(0)


def select_sport() -> str:
    """
    Display sport selection menu and return selected sport.
    
    Returns:
        Sport identifier (lowercase with underscores)
    """
    clear_screen()
    print("=" * 60)
    print("  SMART TRAINING - SESSION SETUP")
    print("=" * 60)
    print("\nSELECT SPORT:\n")
    
    sports = [
        ("Football", "football"),
        ("Basketball", "basketball"),
        ("Track & Field", "track_field"),
        ("Soccer", "soccer"),
        ("Volleyball", "volleyball"),
        ("Cross Country", "cross_country"),
        ("Gymnastics", "gymnastics")
    ]
    
    for idx, (display_name, _) in enumerate(sports, 1):
        print(f"  {idx}) {display_name}")
    
    choice = get_valid_choice("\nChoice #: ", len(sports))
    return sports[choice - 1][1]


def load_roster(sport: str) -> Dict[str, Any]:
    """
    Load roster JSON file for the selected sport.
    
    Args:
        sport: Sport identifier
        
    Returns:
        Parsed roster dictionary
        
    Raises:
        FileNotFoundError: If roster file doesn't exist
    """
    roster_dir = os.path.join("data", "rosters")
    roster_path = os.path.join(roster_dir, f"{sport}_roster.json")
    
    if not os.path.exists(roster_path):
        raise FileNotFoundError(f"Roster file not found: {roster_path}")
    
    with open(roster_path, 'r') as f:
        return json.load(f)


def select_player_football(roster: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hierarchical player selection for Football (Side → Position Group → Player).
    
    Args:
        roster: Football roster dictionary
        
    Returns:
        Player info dictionary with all details
    """
    teams = roster.get("teams", {})
    
    # Step 1: Select Side (Offense/Defense)
    print("\n" + "=" * 60)
    print("SELECT SIDE:\n")
    sides = list(teams.keys())
    for idx, side in enumerate(sides, 1):
        print(f"  {idx}) {side}")
    
    side_choice = get_valid_choice("\nChoice #: ", len(sides))
    selected_side = sides[side_choice - 1]
    
    # Step 2: Select Position Group
    print("\n" + "=" * 60)
    print(f"SELECT POSITION GROUP ({selected_side}):\n")
    position_groups = list(teams[selected_side].keys())
    for idx, group in enumerate(position_groups, 1):
        print(f"  {idx}) {group}")
    
    group_choice = get_valid_choice("\nChoice #: ", len(position_groups))
    selected_group = position_groups[group_choice - 1]
    
    # Step 3: Select Player
    print("\n" + "=" * 60)
    print(f"SELECT PLAYER ({selected_group}):\n")
    players = teams[selected_side][selected_group]
    for idx, player in enumerate(players, 1):
        print(f"  {idx}) {player['full_name']:<20} #{player['number']:<3} {player['position']:<4} ({player['class_year']})")
    
    player_choice = get_valid_choice("\nChoice #: ", len(players))
    selected_player = players[player_choice - 1].copy()
    
    # Add side and position group to player info
    selected_player['side'] = selected_side
    selected_player['position_group'] = selected_group
    
    return selected_player


def select_player_generic(roster: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simple player selection for non-Football sports.
    
    Args:
        roster: Roster dictionary
        
    Returns:
        Player info dictionary
    """
    players = roster.get("players", [])
    
    print("\n" + "=" * 60)
    print("SELECT PLAYER:\n")
    for idx, player in enumerate(players, 1):
        print(f"  {idx}) {player['full_name']:<20} #{player['number']:<3} {player.get('position', 'N/A'):<10} ({player.get('class_year', 'N/A')})")
    
    player_choice = get_valid_choice("\nChoice #: ", len(players))
    selected_player = players[player_choice - 1].copy()
    
    # Add default values for consistency
    selected_player['side'] = None
    selected_player['position_group'] = player.get('position', 'General')
    
    return selected_player


def select_training_location(sport: str) -> str:
    """
    Select training location based on sport-specific options.
    
    Args:
        sport: Sport identifier
        
    Returns:
        Location identifier (lowercase with underscores)
    """
    locations = SPORT_LOCATIONS.get(sport, ["Other"])
    
    print("\n" + "=" * 60)
    print("SELECT TRAINING LOCATION:\n")
    for idx, location in enumerate(locations, 1):
        print(f"  {idx}) {location}")
    
    location_choice = get_valid_choice("\nChoice #: ", len(locations))
    selected_location = locations[location_choice - 1]
    
    # Convert to identifier format
    return selected_location.lower().replace(" ", "_").replace("&", "and")


def select_weight_room_session() -> tuple[str, Optional[str]]:
    """
    Select weight room focus and specific exercise.
    
    Returns:
        Tuple of (focus_identifier, exercise_identifier)
    """
    # Select focus
    print("\n" + "=" * 60)
    print("SELECT WEIGHT ROOM FOCUS:\n")
    for idx, focus in enumerate(WEIGHT_ROOM_FOCUS, 1):
        print(f"  {idx}) {focus}")
    
    focus_choice = get_valid_choice("\nChoice #: ", len(WEIGHT_ROOM_FOCUS))
    selected_focus = WEIGHT_ROOM_FOCUS[focus_choice - 1]
    focus_id = selected_focus.lower().replace(" ", "_")
    
    # Select exercise (for Upper Body and Lower Body)
    if selected_focus in ["Upper Body", "Lower Body"]:
        print("\n" + "=" * 60)
        print(f"SELECT EXERCISE ({selected_focus}):\n")
        for idx, exercise in enumerate(WEIGHT_ROOM_EXERCISES, 1):
            print(f"  {idx}) {exercise}")
        
        exercise_choice = get_valid_choice("\nChoice #: ", len(WEIGHT_ROOM_EXERCISES))
        selected_exercise = WEIGHT_ROOM_EXERCISES[exercise_choice - 1]
        exercise_id = selected_exercise.lower().replace(" ", "_")
    else:
        # For Core/Cardio, use general session
        exercise_id = None
    
    return focus_id, exercise_id


def build_session_info(sport: str, player: Dict[str, Any], location: str, 
                       focus: Optional[str] = None, exercise: Optional[str] = None) -> Dict[str, Any]:
    """
    Build comprehensive session_info dictionary with all context.
    
    Args:
        sport: Sport identifier
        player: Player info dictionary
        location: Training location identifier
        focus: Weight room focus (optional)
        exercise: Specific exercise (optional)
        
    Returns:
        Complete session_info dictionary
    """
    timestamp_start = datetime.now().isoformat()
    
    # Build human-readable name
    sport_display = sport.replace("_", " ").title()
    player_name = f"{player['full_name']} #{player['number']}"
    if player.get('position'):
        player_name += f" ({player['position']} {player.get('class_year', '')})"
    
    location_display = location.replace("_", " ").title()
    
    if exercise:
        exercise_display = exercise.replace("_", " ").title()
        human_name = f"{sport_display} - {player_name} - {location_display} - {exercise_display}"
    elif focus:
        focus_display = focus.replace("_", " ").title()
        human_name = f"{sport_display} - {player_name} - {location_display} - {focus_display}"
    else:
        human_name = f"{sport_display} - {player_name} - {location_display}"
    
    return {
        "sport": sport,
        "location": location,
        "focus": focus,
        "exercise": exercise,
        "player": player,
        "timestamp_start": timestamp_start,
        "human_readable_name": human_name
    }


def start_session_cli() -> Dict[str, Any]:
    """
    Main CLI entry point - orchestrates the full session setup workflow.
    
    Returns:
        Complete session_info dictionary with all user selections
    """
    try:
        # Step 1: Select sport
        sport = select_sport()
        
        # Step 2: Load roster and select player
        roster = load_roster(sport)
        
        if sport == "football":
            player = select_player_football(roster)
        else:
            player = select_player_generic(roster)
        
        # Step 3: Select training location
        location = select_training_location(sport)
        
        # Step 4: If weight room, get focus and exercise
        focus = None
        exercise = None
        
        if location == "weight_room":
            focus, exercise = select_weight_room_session()
        elif location == "other":
            print("\nEnter custom training location description:")
            custom_location = input("   -> ")
            focus = f"custom_{custom_location.lower().replace(' ', '_')}"
        
        # Step 5: Build final session_info
        session_info = build_session_info(sport, player, location, focus, exercise)
        
        # Display summary
        print("\n" + "=" * 60)
        print("SESSION SETUP COMPLETE!")
        print("=" * 60)
        print(f"\n{session_info['human_readable_name']}")
        print(f"Start Time: {session_info['timestamp_start']}")
        print("\nLaunching tracking system...\n")
        
        return session_info
        
    except KeyboardInterrupt:
        print("\n\nSession setup cancelled.")
        exit(0)
    except Exception as e:
        print(f"\n[!] Error during session setup: {e}")
        raise


if __name__ == "__main__":
    # Test the CLI
    info = start_session_cli()
    print("\nGenerated session_info:")
    print(json.dumps(info, indent=2))

"""
Session Paths - Manages directory structure and metadata for training sessions.

This module creates per-athlete, per-session folder structures and handles
metadata/data file organization.
"""

import os
import json
import csv
from datetime import datetime
from typing import Dict, Any


class SessionPaths:
    """
    Manages file paths and directory structure for a training session.
    
    Creates organized folder structure under:
    data/athletes/{sport}/{player_id}/sessions/{session_id}/
    """
    
    def __init__(self, base_dir: str, session_info: Dict[str, Any]):
        """
        Initialize SessionPaths and create directory structure.
        
        Args:
            base_dir: Base directory for athlete data (e.g., "data/athletes")
            session_info: Session information dictionary from CLI
        """
        self.base_dir = base_dir
        self.session_info = session_info
        
        # Extract key info
        self.sport = session_info['sport']
        self.player_id = session_info['player']['player_id']
        self.player_name = session_info['player']['full_name']
        
        # Generate session ID
        self.session_id = self._generate_session_id()
        
        # Build directory paths
        self.athlete_dir = os.path.join(base_dir, self.sport, self.player_id)
        self.sessions_dir = os.path.join(self.athlete_dir, "sessions")
        self.session_dir = os.path.join(self.sessions_dir, self.session_id)
        self.clips_dir = os.path.join(self.session_dir, "clips")
        
        # Build file paths
        self.profile_path = os.path.join(self.athlete_dir, "profile.json")
        self.metadata_path = os.path.join(self.session_dir, "session_meta.json")
        self.metrics_path = os.path.join(self.session_dir, "metrics.csv")
        self.video_path = os.path.join(self.session_dir, "full_video.mp4")
        
        # Create directories and initial files
        self._create_directories()
        self._write_session_metadata()
        self._create_metrics_file()
    
    def _generate_session_id(self) -> str:
        """
        Generate unique session ID from timestamp and context.
        
        Returns:
            Session ID string (filesystem-safe)
        """
        # Parse timestamp
        timestamp = datetime.fromisoformat(self.session_info['timestamp_start'])
        date_str = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Add exercise or location context
        if self.session_info.get('exercise'):
            context = self.session_info['exercise']
        elif self.session_info.get('focus'):
            context = self.session_info['focus']
        else:
            context = self.session_info['location']
        
        return f"{date_str}_{context}"
    
    def _create_directories(self):
        """Create all required directories for the session."""
        os.makedirs(self.athlete_dir, exist_ok=True)
        os.makedirs(self.sessions_dir, exist_ok=True)
        os.makedirs(self.session_dir, exist_ok=True)
        os.makedirs(self.clips_dir, exist_ok=True)
        
        # Create profile if it doesn't exist
        if not os.path.exists(self.profile_path):
            self._create_player_profile()
    
    def _create_player_profile(self):
        """Create initial player profile JSON."""
        profile = {
            "player_id": self.player_id,
            "full_name": self.player_name,
            "sport": self.sport,
            "number": self.session_info['player'].get('number'),
            "position": self.session_info['player'].get('position'),
            "class_year": self.session_info['player'].get('class_year'),
            "created_at": datetime.now().isoformat(),
            "total_sessions": 0
        }
        
        with open(self.profile_path, 'w') as f:
            json.dump(profile, f, indent=2)
    
    def _write_session_metadata(self):
        """Write session metadata JSON file."""
        metadata = {
            **self.session_info,
            "session_id": self.session_id,
            "paths": {
                "session_dir": self.session_dir,
                "video_path": self.video_path,
                "metrics_path": self.metrics_path,
                "clips_dir": self.clips_dir,
                "metadata_path": self.metadata_path
            },
            "created_at": datetime.now().isoformat()
        }
        
        with open(self.metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📁 Session directory: {self.session_dir}")
        print(f"📄 Metadata written: {self.metadata_path}")
    
    def _create_metrics_file(self):
        """Create empty metrics CSV with headers."""
        headers = [
            'timestamp',
            'rep_index',
            'exercise',
            'metric_name',
            'metric_value',
            'notes'
        ]
        
        with open(self.metrics_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        
        print(f"📊 Metrics file created: {self.metrics_path}")
    
    def log_metric(self, rep_index: int, metric_name: str, metric_value: float, notes: str = ""):
        """
        Append a metric to the CSV file.
        
        Args:
            rep_index: Repetition/sample index
            metric_name: Name of the metric (e.g., "elbow_angle", "rom")
            metric_value: Numeric value
            notes: Optional notes
        """
        timestamp = datetime.now().isoformat()
        exercise = self.session_info.get('exercise', self.session_info.get('location', 'general'))
        
        with open(self.metrics_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, rep_index, exercise, metric_name, metric_value, notes])
    
    def get_clip_path(self, clip_number: int) -> str:
        """
        Get path for a numbered clip.
        
        Args:
            clip_number: Clip number (e.g., 1, 2, 3)
            
        Returns:
            Full path to clip file
        """
        clip_filename = f"clip_{clip_number:03d}.mp4"
        return os.path.join(self.clips_dir, clip_filename)
    
    def __repr__(self) -> str:
        """String representation of SessionPaths."""
        return f"SessionPaths(sport={self.sport}, player={self.player_id}, session={self.session_id})"

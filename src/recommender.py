from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_with_reasons(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Return the total score and a list of labeled point contributions for a song."""
        score = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            score += 1.0
            reasons.append("genre match (+1.0)")
        if song.mood == user.favorite_mood:
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_points = round(2.0 * (1 - abs(song.energy - user.target_energy)), 2)
        score += energy_points
        reasons.append(f"energy proximity (+{energy_points})")

        if user.likes_acoustic and song.acousticness >= 0.6:
            score += 0.5
            reasons.append("acoustic preference (+0.5)")
        elif not user.likes_acoustic and song.acousticness < 0.4:
            score += 0.5
            reasons.append("acoustic preference (+0.5)")

        return round(score, 2), reasons

    def _score(self, user: UserProfile, song: Song) -> float:
        """Return the numeric score for a song without the reasons breakdown."""
        score, _ = self._score_with_reasons(user, song)
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score against the given user profile."""
        scored = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string showing why a song was recommended and its total score."""
        score, reasons = self._score_with_reasons(user, song)
        breakdown = ", ".join(reasons)
        return f"\"{song.title}\" by {song.artist}: {breakdown} | total: {score}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    def score_with_reasons(song: Dict) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if song["genre"] == user_prefs.get("favorite_genre"):
            score += 1.0
            reasons.append("genre match (+1.0)")
        if song["mood"] == user_prefs.get("favorite_mood"):
            score += 1.0
            reasons.append("mood match (+1.0)")

        target_energy = user_prefs.get("target_energy", 0.5)
        energy_points = round(2.0 * (1 - abs(song["energy"] - target_energy)), 2)
        score += energy_points
        reasons.append(f"energy proximity (+{energy_points})")

        likes_acoustic = user_prefs.get("likes_acoustic", False)
        if likes_acoustic and song["acousticness"] >= 0.6:
            score += 0.5
            reasons.append("acoustic preference (+0.5)")
        elif not likes_acoustic and song["acousticness"] < 0.4:
            score += 0.5
            reasons.append("acoustic preference (+0.5)")

        return round(score, 2), reasons

    def explain_song(song: Dict, score: float, reasons: List[str]) -> str:
        breakdown = ", ".join(reasons)
        return f"\"{song['title']}\" by {song['artist']}: {breakdown} | total: {score}"

    scored = sorted(songs, key=lambda s: score_with_reasons(s)[0], reverse=True)[:k]
    result = []
    for song in scored:
        score, reasons = score_with_reasons(song)
        result.append((song, score, explain_song(song, score, reasons)))
    return result

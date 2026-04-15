"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 52)
    print(f"  Top {len(recommendations)} Recommendations")
    print(f"  Genre: {user_prefs['favorite_genre']}  |  "
          f"Mood: {user_prefs['favorite_mood']}  |  "
          f"Energy: {user_prefs['target_energy']}")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        # Parse reasons and total out of the explanation string
        # Format: '"Title" by Artist: reason1, reason2 | total: X'
        reasons_part = explanation.split(": ", 1)[1] if ": " in explanation else explanation
        reasons_str, _, _ = reasons_part.partition(" | total:")

        print(f"\n  #{rank}  {song['title']}")
        print(f"       {song['artist']}  ({song['genre']} / {song['mood']})")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {reasons_str}")

    print("\n" + "=" * 52)


if __name__ == "__main__":
    main()

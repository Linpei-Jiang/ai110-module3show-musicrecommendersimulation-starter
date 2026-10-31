"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import DEFAULT_WEIGHTS, load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95, "likes_acoustic": False},
    # Adversarial profiles
    "Conflict: sad but energetic": {"genre": "folk", "mood": "sad", "energy": 0.9, "likes_acoustic": True},
    "Missing genre: bossa nova": {"genre": "bossa nova", "mood": "relaxed", "energy": 0.3, "likes_acoustic": True},
}

# Experiment: double the importance of energy, halve the importance of genre.
SHIFTED_WEIGHTS = {**DEFAULT_WEIGHTS, "energy": DEFAULT_WEIGHTS["energy"] * 2, "genre": DEFAULT_WEIGHTS["genre"] / 2}


def show(name: str, prefs: dict, songs: list, weights: dict = None, k: int = 5) -> None:
    """Print the top k recommendations for one profile in a readable layout."""
    max_score = sum((weights or DEFAULT_WEIGHTS).values())
    print(f"=== {name} ===")
    print(f"Profile: {prefs}")
    for rank, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k, weights), start=1):
        print(f"{rank}. {song['title']} [{song['genre']}/{song['mood']}]  {score:.2f} / {max_score:.2f}")
        print(f"   {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, prefs in PROFILES.items():
        show(name, prefs, songs)

    print("##### EXPERIMENT: energy weight x2, genre weight x0.5 #####\n")
    for name in ("High-Energy Pop", "Chill Lofi", "Deep Intense Rock"):
        show(name + " (shifted weights)", PROFILES[name], songs, SHIFTED_WEIGHTS)


if __name__ == "__main__":
    main()

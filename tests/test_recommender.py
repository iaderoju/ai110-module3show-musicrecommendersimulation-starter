from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- Adversarial / edge-case profiles ---

def make_full_recommender() -> Recommender:
    """Recommender loaded with all 10 catalog songs."""
    from src.recommender import Song
    songs = [
        Song(1, "Sunrise City",        "Neon Echo",      "pop",       "happy",   0.82, 118, 0.84, 0.79, 0.18),
        Song(2, "Midnight Coding",     "LoRoom",         "lofi",      "chill",   0.42,  78, 0.56, 0.62, 0.71),
        Song(3, "Storm Runner",        "Voltline",       "rock",      "intense", 0.91, 152, 0.48, 0.66, 0.10),
        Song(4, "Library Rain",        "Paper Lanterns", "lofi",      "chill",   0.35,  72, 0.60, 0.58, 0.86),
        Song(5, "Gym Hero",            "Max Pulse",      "pop",       "intense", 0.93, 132, 0.77, 0.88, 0.05),
        Song(6, "Spacewalk Thoughts",  "Orbit Bloom",    "ambient",   "chill",   0.28,  60, 0.65, 0.41, 0.92),
        Song(7, "Coffee Shop Stories", "Slow Stereo",    "jazz",      "relaxed", 0.37,  90, 0.71, 0.54, 0.89),
        Song(8, "Night Drive Loop",    "Neon Echo",      "synthwave", "moody",   0.75, 110, 0.49, 0.73, 0.22),
        Song(9, "Focus Flow",          "LoRoom",         "lofi",      "focused", 0.40,  80, 0.59, 0.60, 0.78),
        Song(10,"Rooftop Lights",      "Indigo Parade",  "indie pop", "happy",   0.76, 124, 0.81, 0.82, 0.35),
    ]
    return Recommender(songs)


def test_contradiction_high_energy_sad_lofi():
    """lofi genre + sad mood + high energy + non-acoustic — all signals conflict."""
    user = UserProfile(
        favorite_genre="lofi",
        favorite_mood="sad",
        target_energy=0.95,
        likes_acoustic=False,
    )
    rec = make_full_recommender()
    results = rec.recommend(user, k=5)
    assert len(results) == 5
    # With genre halved (+1.0) and energy doubled (2.0x), the energy signal now
    # dominates. A high-energy non-acoustic song beats the lofi genre match,
    # proving the weight shift resolved the original contradiction.
    assert results[0].energy > 0.8


def test_ghost_profile_no_catalog_matches():
    """Genre and mood not present in catalog — ranking must fall back to energy + acoustic."""
    user = UserProfile(
        favorite_genre="country",
        favorite_mood="angry",
        target_energy=0.5,
        likes_acoustic=True,
    )
    rec = make_full_recommender()
    results = rec.recommend(user, k=5)
    assert len(results) == 5
    # No song can score genre or mood points — verify top song is not penalized on acoustic
    assert results[0].acousticness >= 0.6


def test_dead_zone_energy_0_5():
    """Jazz/relaxed profile with energy=0.5 — one clear genre+mood winner, rest nearly tied."""
    user = UserProfile(
        favorite_genre="jazz",
        favorite_mood="relaxed",
        target_energy=0.5,
        likes_acoustic=True,
    )
    rec = make_full_recommender()
    results = rec.recommend(user, k=5)
    # Song 7 (Coffee Shop Stories) is the only jazz/relaxed song — must rank #1
    assert results[0].title == "Coffee Shop Stories"


def test_acoustic_trap_synthwave_likes_acoustic():
    """Synthwave genre conflicts with likes_acoustic=True — genre match but acoustic penalty."""
    user = UserProfile(
        favorite_genre="synthwave",
        favorite_mood="moody",
        target_energy=0.75,
        likes_acoustic=True,
    )
    rec = make_full_recommender()
    results = rec.recommend(user, k=5)
    # Song 8 still wins on genre+mood double match despite missing acoustic bonus
    assert results[0].title == "Night Drive Loop"
    # And it should NOT have acousticness >= 0.6
    assert results[0].acousticness < 0.6


def test_energy_extremist_target_zero():
    """target_energy=0.0 — no song is near it, acoustic bonus becomes disproportionately powerful."""
    user = UserProfile(
        favorite_genre="ambient",
        favorite_mood="chill",
        target_energy=0.0,
        likes_acoustic=True,
    )
    rec = make_full_recommender()
    results = rec.recommend(user, k=5)
    # Song 6 (Spacewalk Thoughts) matches genre+mood and has lowest energy (0.28) + high acoustic
    assert results[0].title == "Spacewalk Thoughts"


def test_maximizer_near_perfect_score():
    """Profile engineered to hit near-max score against Sunrise City (energy=0.82)."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.82,
        likes_acoustic=False,
    )
    rec = make_full_recommender()
    results = rec.recommend(user, k=1)
    assert results[0].title == "Sunrise City"
    # Score should be very close to the 4.5 maximum
    score = rec._score(user, results[0])
    assert score >= 4.4

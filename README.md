# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

**VibeFinder 1.0** is a small, command-line music recommender. It loads an 18-song catalog from `data/songs.csv` and compares every song to a user's taste profile (favorite genre, favorite mood, target energy, and whether they like acoustic sound). Each song gets a score out of 7 points with a plain-language reason for every point. The top five songs are printed, best first. It uses only song attributes, with no data from other listeners.

---

## How The System Works

Real-world platforms like Spotify and YouTube blend two signals. **Collaborative filtering** learns from the behavior of millions of users (plays, skips, saves, playlist adds) and recommends what similar listeners enjoyed. **Content-based filtering** compares the attributes of the songs themselves to a user's taste. Collaborative filtering needs a large crowd and struggles with new songs. Content-based filtering needs no other users but can trap you in a bubble of similar songs. My version is purely content-based: it has no other users, so it compares each song's attributes to a single user's taste profile. It prioritizes **energy closeness** (up to 3 points), then **genre** (2 points), then **mood** (1 point).

### Features

**`Song`** (from `data/songs.csv`): `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`

**`UserProfile`**: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

Of the song attributes, the scoring rule uses `energy`, `mood`, `genre` and `acousticness`. The others are stored for later experiments (valence is the most promising next addition).

### Catalog and Example Profile

I expanded `data/songs.csv` from 10 to 18 songs, adding genres and moods missing from the starter: hip hop, r&b, country, metal, classical, reggae, folk and edm, with moods such as confident, romantic, nostalgic, aggressive, melancholy, uplifting and euphoric.

The example taste profile:

```python
user_prefs = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "likes_acoustic": True,
}
```

This profile can tell "chill lofi" from "intense rock". Storm Runner (rock, intense, 0.91 energy) loses on genre, mood and energy, so it scores near the bottom. The weak spot is that it's narrow: the only perfect matches are the three lofi songs, and a user who likes "chill" in any genre (ambient, jazz) is only partly served. Profiles for contrasting tastes (for example rock/intense/0.9) are worth testing too.

### Data Flow

```
INPUT                 PROCESS (loop over every row of songs.csv)         OUTPUT
user_prefs  ───►  for song in songs:                              ───►  sort by score, descending
                      score = genre + mood + energy + acoustic          return top K with reasons
```

### Scoring Rule (one song)

Numeric features reward *closeness* to the user's target, not a higher or lower value. For energy:

```
energy_score = 1 - |song.energy - user.target_energy|     # 1.0 = perfect match, 0.0 = opposite
```

A user who wants 0.4 energy gets a full score from a 0.4 song and a lower score from both a 0.9 song and a 0.1 song.

| Component | Points |
|---|---|
| Energy closeness (`1 - abs difference`) | 0 to 3.0 (`3.0 * energy_score`) |
| Genre match | +2.0 |
| Mood match | +1.0 |
| Acoustic fit (`acousticness` if `likes_acoustic`, else `1 - acousticness`) | 0 to 1.0 |

The maximum score is 7.0. This is the finalized recipe: genre is worth twice a mood match, and energy closeness can contribute the most because it is continuous and separates the catalog's two clusters. (I first considered weighting mood above genre. I'm starting with genre on top, the common default, and will compare both during evaluation.)

### Expected Biases

- **Genre over-prioritization:** with +2.0 for genre, a mediocre song in the favorite genre can outrank a great mood-and-energy match in another genre. A chill ambient track could lose to an off-vibe lofi one.
- **Sparse genres:** most genres have one song, so only lofi and pop users get more than one genre match.
- **Exact-match labels:** "chill" and "relaxed" are treated as completely different moods, though they are close in feel.
- **Unused features:** valence, tempo and danceability are ignored, so two songs with the same energy but different emotional tone (Storm Runner versus Gym Hero) can score identically.
- **Small catalog:** 18 songs means results can look reasonable even when the logic is weak.

### Ranking Rule (list of songs)

The recommender scores every song in the catalog with the scoring rule, sorts them by score from highest to lowest, and returns the top `k`. Both rules are needed. The scoring rule judges one song in isolation and can't say which songs to show. The ranking rule turns the scores into an ordered list.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default pop/happy profile:

```
Loaded songs: 18
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}

Top recommendations:

1. Sunrise City by Neon Echo  [pop/happy]
   Score: 6.76 / 7.00
   - genre match (+2.0)
   - mood match (+1.0)
   - energy 0.82 vs target 0.80 (+2.94)
   - acoustic fit (+0.82)

2. Gym Hero by Max Pulse  [pop/intense]
   Score: 5.56 / 7.00
   - genre match (+2.0)
   - energy 0.93 vs target 0.80 (+2.61)
   - acoustic fit (+0.95)

3. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 4.53 / 7.00
   - mood match (+1.0)
   - energy 0.76 vs target 0.80 (+2.88)
   - acoustic fit (+0.65)

4. Concrete Crown by Kid Meridian  [hip hop/confident]
   Score: 3.82 / 7.00
   - energy 0.78 vs target 0.80 (+2.94)
   - acoustic fit (+0.88)

5. Night Drive Loop by Neon Echo  [synthwave/moody]
   Score: 3.63 / 7.00
   - energy 0.75 vs target 0.80 (+2.85)
   - acoustic fit (+0.78)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Evaluation Output (Diverse Profiles and Experiment)

Output of `python -m src.main`: five profiles (three standard, two adversarial), then the weight-shift experiment.

```
Loaded songs: 18

=== High-Energy Pop ===
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'likes_acoustic': False}
1. Sunrise City [pop/happy]  6.58 / 7.00
   genre match (+2.0); mood match (+1.0); energy 0.82 vs target 0.90 (+2.76); acoustic fit (+0.82)
2. Gym Hero [pop/intense]  5.86 / 7.00
   genre match (+2.0); energy 0.93 vs target 0.90 (+2.91); acoustic fit (+0.95)
3. Rooftop Lights [indie pop/happy]  4.23 / 7.00
   mood match (+1.0); energy 0.76 vs target 0.90 (+2.58); acoustic fit (+0.65)
4. Storm Runner [rock/intense]  3.87 / 7.00
   energy 0.91 vs target 0.90 (+2.97); acoustic fit (+0.90)
5. Pulse Cascade [edm/euphoric]  3.82 / 7.00
   energy 0.95 vs target 0.90 (+2.85); acoustic fit (+0.97)

=== Chill Lofi ===
Profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'likes_acoustic': True}
1. Library Rain [lofi/chill]  6.71 / 7.00
   genre match (+2.0); mood match (+1.0); energy 0.35 vs target 0.40 (+2.85); acoustic fit (+0.86)
2. Midnight Coding [lofi/chill]  6.65 / 7.00
   genre match (+2.0); mood match (+1.0); energy 0.42 vs target 0.40 (+2.94); acoustic fit (+0.71)
3. Focus Flow [lofi/focused]  5.78 / 7.00
   genre match (+2.0); energy 0.40 vs target 0.40 (+3.00); acoustic fit (+0.78)
4. Spacewalk Thoughts [ambient/chill]  4.56 / 7.00
   mood match (+1.0); energy 0.28 vs target 0.40 (+2.64); acoustic fit (+0.92)
5. Coffee Shop Stories [jazz/relaxed]  3.80 / 7.00
   energy 0.37 vs target 0.40 (+2.91); acoustic fit (+0.89)

=== Deep Intense Rock ===
Profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.95, 'likes_acoustic': False}
1. Storm Runner [rock/intense]  6.78 / 7.00
   genre match (+2.0); mood match (+1.0); energy 0.91 vs target 0.95 (+2.88); acoustic fit (+0.90)
2. Gym Hero [pop/intense]  4.89 / 7.00
   mood match (+1.0); energy 0.93 vs target 0.95 (+2.94); acoustic fit (+0.95)
3. Pulse Cascade [edm/euphoric]  3.97 / 7.00
   energy 0.95 vs target 0.95 (+3.00); acoustic fit (+0.97)
4. Iron Cathedral [metal/aggressive]  3.90 / 7.00
   energy 0.97 vs target 0.95 (+2.94); acoustic fit (+0.96)
5. Sunrise City [pop/happy]  3.43 / 7.00
   energy 0.82 vs target 0.95 (+2.61); acoustic fit (+0.82)

=== Conflict: sad but energetic ===
Profile: {'genre': 'folk', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': True}
1. Autumn Letters [folk/melancholy]  4.20 / 7.00
   genre match (+2.0); energy 0.33 vs target 0.90 (+1.29); acoustic fit (+0.91)
2. Storm Runner [rock/intense]  3.07 / 7.00
   energy 0.91 vs target 0.90 (+2.97); acoustic fit (+0.10)
3. Gym Hero [pop/intense]  2.96 / 7.00
   energy 0.93 vs target 0.90 (+2.91); acoustic fit (+0.05)
4. Sunrise City [pop/happy]  2.94 / 7.00
   energy 0.82 vs target 0.90 (+2.76); acoustic fit (+0.18)
5. Rooftop Lights [indie pop/happy]  2.93 / 7.00
   energy 0.76 vs target 0.90 (+2.58); acoustic fit (+0.35)

=== Missing genre: bossa nova ===
Profile: {'genre': 'bossa nova', 'mood': 'relaxed', 'energy': 0.3, 'likes_acoustic': True}
1. Coffee Shop Stories [jazz/relaxed]  4.68 / 7.00
   mood match (+1.0); energy 0.37 vs target 0.30 (+2.79); acoustic fit (+0.89)
2. Spacewalk Thoughts [ambient/chill]  3.86 / 7.00
   energy 0.28 vs target 0.30 (+2.94); acoustic fit (+0.92)
3. Autumn Letters [folk/melancholy]  3.82 / 7.00
   energy 0.33 vs target 0.30 (+2.91); acoustic fit (+0.91)
4. Moonlit Sonata [classical/melancholy]  3.73 / 7.00
   energy 0.22 vs target 0.30 (+2.76); acoustic fit (+0.97)
5. Library Rain [lofi/chill]  3.71 / 7.00
   energy 0.35 vs target 0.30 (+2.85); acoustic fit (+0.86)

##### EXPERIMENT: energy weight x2, genre weight x0.5 #####

=== High-Energy Pop (shifted weights) ===
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'likes_acoustic': False}
1. Sunrise City [pop/happy]  8.34 / 9.00
   genre match (+1.0); mood match (+1.0); energy 0.82 vs target 0.90 (+5.52); acoustic fit (+0.82)
2. Gym Hero [pop/intense]  7.77 / 9.00
   genre match (+1.0); energy 0.93 vs target 0.90 (+5.82); acoustic fit (+0.95)
3. Storm Runner [rock/intense]  6.84 / 9.00
   energy 0.91 vs target 0.90 (+5.94); acoustic fit (+0.90)
4. Rooftop Lights [indie pop/happy]  6.81 / 9.00
   mood match (+1.0); energy 0.76 vs target 0.90 (+5.16); acoustic fit (+0.65)
5. Pulse Cascade [edm/euphoric]  6.67 / 9.00
   energy 0.95 vs target 0.90 (+5.70); acoustic fit (+0.97)

=== Chill Lofi (shifted weights) ===
Profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'likes_acoustic': True}
1. Midnight Coding [lofi/chill]  8.59 / 9.00
   genre match (+1.0); mood match (+1.0); energy 0.42 vs target 0.40 (+5.88); acoustic fit (+0.71)
2. Library Rain [lofi/chill]  8.56 / 9.00
   genre match (+1.0); mood match (+1.0); energy 0.35 vs target 0.40 (+5.70); acoustic fit (+0.86)
3. Focus Flow [lofi/focused]  7.78 / 9.00
   genre match (+1.0); energy 0.40 vs target 0.40 (+6.00); acoustic fit (+0.78)
4. Spacewalk Thoughts [ambient/chill]  7.20 / 9.00
   mood match (+1.0); energy 0.28 vs target 0.40 (+5.28); acoustic fit (+0.92)
5. Coffee Shop Stories [jazz/relaxed]  6.71 / 9.00
   energy 0.37 vs target 0.40 (+5.82); acoustic fit (+0.89)

=== Deep Intense Rock (shifted weights) ===
Profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.95, 'likes_acoustic': False}
1. Storm Runner [rock/intense]  8.66 / 9.00
   genre match (+1.0); mood match (+1.0); energy 0.91 vs target 0.95 (+5.76); acoustic fit (+0.90)
2. Gym Hero [pop/intense]  7.83 / 9.00
   mood match (+1.0); energy 0.93 vs target 0.95 (+5.88); acoustic fit (+0.95)
3. Pulse Cascade [edm/euphoric]  6.97 / 9.00
   energy 0.95 vs target 0.95 (+6.00); acoustic fit (+0.97)
4. Iron Cathedral [metal/aggressive]  6.84 / 9.00
   energy 0.97 vs target 0.95 (+5.88); acoustic fit (+0.96)
5. Sunrise City [pop/happy]  6.04 / 9.00
   energy 0.82 vs target 0.95 (+5.22); acoustic fit (+0.82)
```

## Experiments You Tried

- **Diverse profiles:** I ran High-Energy Pop, Chill Lofi and Deep Intense Rock. Each put its exact genre-and-mood match first, and the lists for pop and lofi shared no songs.
- **Adversarial profiles:** A "sad but energetic" folk fan got a quiet folk song first, because the genre bonus beat the energy request. A "bossa nova" fan (a genre not in the catalog) still got calm, acoustic songs ranked by energy and acousticness.
- **Weight shift (energy x2, genre x0.5):** Chill Lofi's top two songs swapped, and for the pop profile a rock song moved above an indie pop song. Rock was unchanged. The results were different, not clearly better.

Full output and comparisons are in the Evaluation Output section above and in the [model card](model_card.md).

---

## Limitations and Risks

- It only works on a tiny catalog of 18 songs, and most genres have just one song.
- It does not understand lyrics, language, artist, or era.
- Genre can override what the user asked for: a quiet folk song beat loud songs for a user who wanted energy 0.9.
- Moods and genres must match exactly. "Chill" gets no credit for "relaxed", and "pop" gets none for "indie pop".
- Valence, tempo and danceability are not used in the score.
- The audio numbers were written by hand, not measured.

See the [model card](model_card.md) for more.

---

## Reflection

Full reflection: [**Model Card**](model_card.md)

Building this showed me that a recommender is a set of opinions turned into numbers. Choosing 2 points for genre and 1 for mood was a judgment about taste, and changing those weights changed who got good results. I was surprised that four simple rules (genre, mood, energy closeness and acoustic fit) already felt like real recommendations, mostly because each result came with a reason.

Bias can show up even in a system this small. The genre bonus favors users whose taste is common in the catalog, and exact-match labels ignore near-misses. In a real app, the data would add more bias: whatever is popular or well-represented gets recommended more. AI tools helped me build quickly, but I had to run the code and read the output to catch problems, such as a mood label ("sad") that does not exist in the data.

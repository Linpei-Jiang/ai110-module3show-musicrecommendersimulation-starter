# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder suggests songs a user might like. It takes one taste profile: favorite genre, favorite mood, target energy, and whether they like acoustic sound. It then ranks every song in the catalog and returns the top five. It also says why each song was picked.

---

## 3. Data Used

- The catalog is `data/songs.csv`. It has 18 songs.
- I started with 10 songs and added 8 more.
- Each song has genre, mood, energy, tempo, valence, danceability and acousticness.
- Genres include lofi, pop, rock, jazz, ambient, synthwave, indie pop, hip hop, r&b, country, metal, classical, reggae, folk and edm.
- Limits: the catalog is tiny. Most genres have only one song. I wrote the numbers by hand. They are not real audio measurements. Lyrics, language, artist fame and era are missing.

---

## 4. Algorithm Summary

The recommender compares every song in the catalog to one user's taste and gives each song a score out of 7 points. A song earns 2 points if its genre matches the user's favorite and 1 point if its mood matches. It earns up to 3 points for how close its energy is to the user's target, so a song that is a little too calm and one that is a little too intense lose points equally. It earns up to 1 more point for fitting the user's preference for acoustic or electronic sound. Every point comes with a plain-language reason, such as "genre match (+2.0)". Finally, the songs are sorted from highest to lowest score and the top five are shown. It uses no data from other listeners, so it is a content-based recommender.

---

## 5. Observed Behavior / Biases

The biggest weakness I found is that categorical matches can override the energy the user asked for. In the "sad but energetic" test (folk, sad, energy 0.9), the top result was Autumn Letters, a quiet folk song with energy 0.33, because it was the only song that earned the +2.0 genre bonus; a 0.91-energy rock song scored lower. The same test exposed a vocabulary problem: no song is labeled "sad" (the catalog says "melancholy"), so the mood match could never fire. Exact-string matching also gives no credit for near-misses such as "indie pop" for "pop" or "relaxed" for "chill". Most genres have just one song, so users who like a niche genre get one genre-matched result and then a list ranked only by energy and acousticness. Finally, valence, tempo and danceability are ignored, so two songs with the same energy but very different emotional tone can score almost identically.

---

## 6. Evaluation Process

I tested five profiles and one experiment. **Profiles tested** (full terminal output is in the README): High-Energy Pop, Chill Lofi, Deep Intense Rock, plus two adversarial profiles: "sad but energetic" (folk, sad, energy 0.9) and "bossa nova" (a genre that is not in the catalog).

**Did it feel right?** The three standard profiles matched my intuition: each put its exact genre-and-mood match first (Sunrise City, Library Rain, Storm Runner) with a sensible tail. The surprise was Gym Hero ranking second for both Pop and Rock, since it is pop with intense mood and very high energy, so it sits between the two profiles. Another surprise was the sad profile, where the missing "sad" label meant the mood bonus never applied.

**Why Sunrise City ranked first for High-Energy Pop:** genre match (+2.0), mood match (+1.0), energy 0.82 vs 0.90 (+2.76), and acoustic fit (+0.82) total 6.58. The runner-up Gym Hero lost its mood point (no "happy") and gained only 0.15 back from energy.

**Pairwise comparisons**
- *High-Energy Pop vs Chill Lofi:* the lists share no songs. Pop pulls in loud, low-acousticness tracks (Gym Hero, Storm Runner, Pulse Cascade); Lofi pulls in quiet, acoustic ones (Spacewalk Thoughts, Coffee Shop Stories). That is correct, since energy and acousticness point in opposite directions in this catalog.
- *High-Energy Pop vs Deep Intense Rock:* both rank high-energy songs, so Gym Hero, Pulse Cascade and Sunrise City appear in both. The difference is the top spot (a pop/happy song versus Storm Runner) and rock's tail moving toward Iron Cathedral, because mood "intense" matches Gym Hero instead of Rooftop Lights. This makes sense because the profiles are close in energy and differ mainly in genre and mood.
- *Chill Lofi vs Deep Intense Rock:* opposite ends of the energy scale, with no overlap, as expected.
- *Sad-but-energetic vs the others:* conflicting preferences produce a split list. One quiet folk song wins on genre, then ranks 2-5 are loud songs that match energy only. The system cannot satisfy both preferences, and it favors the genre bonus.
- *Bossa nova vs Chill Lofi:* with no genre match available, the list is ranked entirely by energy, acousticness and mood. It still returns reasonable calm, acoustic songs (Coffee Shop Stories, Spacewalk Thoughts), which suggests the numeric features are carrying real signal.

**Experiment: energy weight x2, genre weight x0.5.** The maximum score becomes 9.0, so scores are not comparable across runs, only rankings. The math stays valid because every component is still non-negative and the maximum equals the sum of the weights. Rankings changed little: Chill Lofi's top two swapped (Midnight Coding now first, since its energy is closer), and for High-Energy Pop, Storm Runner (rock) moved above Rooftop Lights (indie pop). Rock was unchanged. The shift made the results different but not clearly more accurate: pushing a rock song above an indie-pop song for a pop fan is arguably worse, though it follows the energy request more literally.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- Classroom learning about how recommenders work.
- Exploring how scoring weights change a ranking.
- One user at a time, run from the command line.

**Not intended for:**
- A real music app or real users. The catalog is far too small.
- Judging anyone's taste. The profile is a simple guess, not a fact about a person.
- Anything where unfair results would matter, such as pay or exposure for artists. Niche genres are badly served.

---

## 8. Ideas for Improvement

1. Match moods by similarity, so "chill" gets partial credit for "relaxed". Use valence too.
2. Add diversity. Stop the top five from being all one genre or artist.
3. Grow the catalog and use real audio data. Then add listening history so the system can learn the profile.

---

## 9. Personal Reflection

**Biggest learning moment.** The "sad but energetic" test. I expected the system to struggle, but not how. A quiet folk song won because genre was worth the most points. That showed me the weights are my own opinions about taste, written as numbers.

**How AI helped, and when I checked it.** AI helped me move fast. It drafted the data, the scoring code and the docs. I still had to check it. It chose the weights, and I had to ask whether mood or genre should matter more. It also named a "sad" mood the data did not contain. Running the code and reading the printed reasons was how I caught these issues.

**What surprised me.** Four simple rules felt like real recommendations. The top results for the pop and lofi profiles looked right. The "reasons" lines made it feel smart, even though it only adds up points.

**What I would try next.** Add valence to the score. Give partial credit for similar moods. Add a diversity rule. Then compare a few weight settings to see which one feels best.

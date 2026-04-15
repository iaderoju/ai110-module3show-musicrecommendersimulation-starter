# Reflection: User Profile Testing

## Profiles Tested

Eight user profiles were run against the 10-song catalog to explore how different taste preferences
changed which songs ranked at the top. Two were standard profiles designed to confirm basic behavior;
six were adversarial edge cases built to stress-test the scoring logic.

---

## Profile Summaries and Surprises

### 1. Baseline — `pop / happy / energy=0.8 / likes_acoustic=False`
Top result: **Sunrise City** (pop/happy, energy=0.82)

This was the sanity-check profile. The genre and mood both matched Sunrise City, and its energy
was within 0.02 of the target. The acoustic penalty did not hurt it because its acousticness (0.18)
was below the 0.4 threshold. Everything worked as expected.

**Surprise:** Rooftop Lights (indie pop / happy / energy=0.76) ranked #3, not #2.
Gym Hero (pop / intense / energy=0.93) claimed #2 because its energy was closer to the
target than Rooftop Lights. The mood mismatch ("intense" vs "happy") was not enough to
drop it below an indie pop song with a full mood match. This showed that even a +1.0 mood
bonus can be outweighed by a 0.17 energy-proximity difference when energy is weighted at 2×.

---

### 2. Maximizer — `pop / happy / energy=0.82 / likes_acoustic=False`
Top result: **Sunrise City** (score ≥ 4.4 out of 4.5 maximum)

Tuning the target energy to exactly match Sunrise City's energy (0.82) brought the score
to its theoretical ceiling. The remaining gap from 4.5 came from the acoustic signal —
Sunrise City's acousticness (0.18) was low enough to earn the non-acoustic +0.5 bonus,
so the final score was 1.0 + 1.0 + 2.0 + 0.5 = **4.5 exactly**.

**Comparison with Baseline:** Shifting target energy from 0.80 to 0.82 changed only the
energy proximity term by a small amount and did not change the #1 result. However, it
*did* flip the #2 and #3 positions — Rooftop Lights edged ahead of Gym Hero once the
energy gap closed to near-zero for Sunrise City, because Gym Hero's energy distance from
0.82 grew slightly. This showed that tiny changes in the numeric target can reshuffle the
mid-tier without touching the top result.

---

### 3. Contradiction — `lofi / sad / energy=0.95 / likes_acoustic=False`
Top result: **Storm Runner** (rock/intense, energy=0.91)

Every signal in this profile fought every other signal. The user declared lofi as their genre,
but their target energy (0.95) is the opposite of what any lofi song in the catalog delivers
(lofi songs cluster between 0.35–0.42). The declared mood "sad" does not exist in the catalog
at all, so zero songs can earn a mood match point.

After the weight shift (genre halved to +1.0, energy doubled to 2×), energy proximity dominated.
Storm Runner's energy (0.91) was closer to 0.95 than any lofi song, so it won despite being
rock/intense.

**Comparison with Ghost Profile:** Both profiles score zero mood points, but for different reasons.
The contradiction profile *has* a genre in the catalog (lofi) — it just conflicts with the user's
own energy preference. The ghost profile has *no* catalog match at all. In both cases, the ranking
silently degrades into an energy sort, but the contradiction profile still awards a genre bonus to
whichever lofi song gets compared, while the ghost profile awards nothing at all.

---

### 4. Ghost — `country / angry / energy=0.5 / likes_acoustic=True`
Top result: **Coffee Shop Stories** (jazz/relaxed, energy=0.37, acousticness=0.89)

Neither "country" nor "angry" exists in the catalog, so no song can score genre or mood points.
The ranking fell back entirely to energy proximity and the acoustic bonus. Coffee Shop Stories
won because it combined a moderately close energy (0.37 vs 0.50, giving 1.74 energy points)
with a high acoustic score (0.89 ≥ 0.60 threshold, +0.5).

**Surprise:** The top result was a jazz/relaxed song for a user who declared country/angry as
their preferences. The system made a confident recommendation with no warning that it had
ignored the user's stated genre and mood entirely. In a real product this would be misleading —
the "why" explanation would only mention energy and acoustic signals, with no mention of the
fact that the user's core preferences were absent from the catalog.

**Comparison with Dead Zone:** Both profiles get a single clear winner from energy + acoustic.
The ghost profile's winner shifts whenever `likes_acoustic` changes (flipping to a low-acoustic
high-energy song instead), because acoustic is the only differentiating categorical signal.
The dead zone profile retains its #1 result regardless of acoustic preference because Coffee
Shop Stories wins on genre+mood points alone.

---

### 5. Dead Zone — `jazz / relaxed / energy=0.5 / likes_acoustic=True`
Top result: **Coffee Shop Stories** (jazz/relaxed, energy=0.37, acousticness=0.89)

This was the clearest, cleanest result of all eight profiles. Only one song in the catalog
matches both jazz and relaxed, and that song also happened to have high acousticness. The
win margin was large enough that #2 onward were nearly tied on energy proximity alone.

**Comparison with Acoustic Trap:** Both profiles prefer acoustic. Dead Zone's genre (jazz)
and the catalog's one jazz song happen to *also* be acoustic, so there is no tension.
Acoustic Trap's genre (synthwave) conflicts with acoustic preference — the one synthwave
song has low acousticness (0.22). The trap profile still correctly ranks Night Drive Loop #1
because genre+mood double match (+2.0 combined) outweighs the missing acoustic bonus (+0.5).
This demonstrated that genre+mood dominates acoustic in every head-to-head comparison under
the current weights — a useful calibration insight.

---

### 6. Acoustic Trap — `synthwave / moody / energy=0.75 / likes_acoustic=True`
Top result: **Night Drive Loop** (synthwave/moody, energy=0.75, acousticness=0.22)

The user's genre preference and acoustic preference directly conflict: the only synthwave
song in the catalog has low acousticness. The question was whether the system would rank
a wrong-genre acoustic song higher than the correct-genre non-acoustic song.

It did not. Night Drive Loop won cleanly: genre match (+1.0) + mood match (+1.0) + near-zero
energy distance (≈ +2.0) totaled approximately 4.0, far above any high-acoustic wrong-genre
competitor. The acoustic penalty (missing the +0.5 bonus) was visible in the score but did
not change the outcome.

**Comparison with Energy Extremist:** Both profiles have a situation where the declared
preference conflicts with catalog reality — the trap user can't get acoustic + synthwave,
and the extremist user can't get a song near energy=0.0. In the trap, the conflict is minor
(only loses 0.5 pts). In the extremist case, the conflict is severe (every song is far from
the target, compressing energy scores into a narrow band of roughly 1.44–1.56).

---

### 7. Energy Extremist — `ambient / chill / energy=0.0 / likes_acoustic=True`
Top result: **Spacewalk Thoughts** (ambient/chill, energy=0.28, acousticness=0.92)

No song in the catalog has energy near 0.0. The closest is Spacewalk Thoughts at 0.28.
With energy doubled to 2× weight, a large gap still hurts — but Spacewalk also has a perfect
genre+mood match and the highest acousticness in the catalog. It won on all four signals
simultaneously, which is rare.

**Surprise:** Even though Spacewalk's energy was "far" from the target (0.28 vs 0.0 = 0.28 gap),
it still scored 1.44 energy points out of a possible 2.0. The acoustic signal (+0.5) closed most
of the remaining distance. The system behaved well here because the genre/mood winner happened
to also be the energy winner — there was no conflict to expose.

---

### 8. Chill Acoustic Listener — `lofi / chill / energy=0.35 / likes_acoustic=True`
Top result: **Library Rain** (lofi/chill, energy=0.35, acousticness=0.86)

This was the profile that fit the catalog most naturally. The user's target energy (0.35)
is an exact match for Library Rain, and the genre/mood/acoustic preferences all align.
The score was at or near the 4.5 maximum.

**Comparison with Baseline:** The baseline profile (pop/happy) also hits a near-maximum score
for its top result — but the similarity ends there. The pop profile's #2 and #3 are both
wrong-mood songs fighting on energy proximity. The chill acoustic profile has *three* lofi
songs in the catalog, so the entire top-3 stays within the target genre. This directly
illustrated the lofi over-representation bias documented in the model card: a lofi listener
gets three quality candidates while a jazz or synthwave listener gets one.

---

## Summary Observation

The profiles that worked best were those whose declared genre appeared multiple times in the
catalog (lofi) and whose target energy aligned with catalog values. The profiles that degraded
most were the ghost profile (genre absent entirely) and the energy extremist (energy target
outside catalog range). Both produced results that *looked* confident but were essentially
arbitrary — exactly the failure mode a real recommender system should warn users about.

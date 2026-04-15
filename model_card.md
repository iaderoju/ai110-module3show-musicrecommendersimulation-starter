# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
TuneMaster
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Music listeners that are trying to expand their musical horizon!


---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Genre, mood, energy, acousticness is all things considered in scoring. The system takes all of these features into account
and grades it by points to see if a song matches the user's taste based on those features.


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

In `data/songs.csv`, there are 10 songs. No songs were added or removed from the original catalog.
Lofi takes 30% and Pop takes 20% of the catalog along with Rock, Ambient, Jazz, Synthwave and Indie pop taking the rest equally.
The catalog skews toward mid-tempo, electronically-influenced, low-stress listening.
---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The recommender felt right when it ranked "Night Drive Loop" as #1 as it helped define the user's taste correctly in accordance with
the genre and mood. The system can be verified easily by a user to debug.
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  


Many genres are left out I noticed and it goes by a one-size-fits all taste shape.
It always goes by highest energy songs in the catalog. The unfairness yet again falls on the favoritism to a single genre.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

-Inspected the baseline profile by running the main script, performed recommender tests, and conducted weight shift experiments.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

-Could add tempo range
-Expand the data set and add a no match warning
-User feedback loop
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

-Im honestly surprised how well the scoring system worked.
Building this made me think about how I was introduced to new music through my use of spotify and how I can replicate that process
here. I still believe that human judgement will matter because models don't have the artistic and creative mindset humans possess.
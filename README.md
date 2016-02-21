# Seng 474 Data mining project
## Team
Alastair Beaumont
Kolby Chapman
Graeme Nathan
Cole Peterson

### Data We Have
---
- Home team *(str)*
- Away team *(str)*
- Home team's score *(int >= 0)*
- Away team's score *(int >= 0)*
- Match winner *(str)*:
    - H: home team
    - A: away team
    - D: draw
- Date of match *(date - dd/mm/yy)*

</br>


### Data We Want
---
- Relegation score *(float in (0, 1))*

</br>

### Relegation Score
---
This is calculated as **1 - (pts/team_max)**. It is a ratio in the range (0, 1) where the higher a team's score the closer they are to being relegated. 

The **team_max** is 3 times the number of games that time has played, representing the theoretical maximum score the team could have at that point in time.

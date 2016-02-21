# Seng 474 Data Mining Project
## Team

- Alastair Beaumont
- Kolby Chapman
- Graeme Nathan
- Cole Peterson

</br>

## Data
### Data We Have
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
- Relegation score *(float in (0, 1))*

</br>

### Relegation Score
This is calculated as **1 - (pts/team_max)**. It is a ratio in the range (0, 1) where the higher a team's score the closer they are to being relegated. 

The **team_max** is 3 times the number of games that time has played, representing the theoretical maximum score the team could have at that point in time.

</br>

## Plan
We will create 	a random algorithm to use as a baseline comparison against a machine-learning approach.

#### Random Algorithm
Our random algorithm will chose one of the teams randomly and predict them as the winner of the match.

#### Machine Learning
We will take two similar approaches in this area.

First, we will use our data without the relegation score. Second, we will repeat the process with the relegation score. In both cases, we will use one season as training data and another season as testing data.

#### General Idea
We will investigate whether or not a machine learning approach is any better than randomly guessing the outcome. Additionally, we are going to check whether or not a team's closeness to relegation has an impact on their playing. Should we find that such an affect does appear to occur, we will investigate the threshold where the affect starts.

</br>

## To Do
- Redefine our closeness to relegations stat to include the theoretical remaining points a team could achieve so we can measure the closeness to relegation more accurately.
	- thinking is that, if you only have a few more chances to make up enough points to leave the relegation set, then you are closer to relegation.
- Define what measures to use when checking if a team is playing 'better'; is it simply number of goals scored?


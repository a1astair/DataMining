from season import Season

class Predictor:
    def __init__(self):
        self.correct = 0
        self.false = 0
    
    def test(self, s, home, away, date, res):
        if self.predict(s, home, away, date) == res:
            self.correct += 1
        else:
            self.false += 1
        return (self.correct, self.false)

   
    def accuracy(self):
        denom = self.correct+self.false
        if denom == 0:
            return 0
        return float(self.correct)/denom

   

class HighPointsPredictor(Predictor):
    def predict(self, s, home, away, date):
        home_pts = s.points_on_date(home,date)
        away_pts = s.points_on_date(away,date)
        diff = abs(home_pts - away_pts)
        if diff < 3:
            return 'D'
        else:
            if home_pts > away_pts:
                return 'H'
            else :
                return 'A'

class HomeTeamPredictor(Predictor):
    def predict(self, s, home, away, date):
        return 'H'

class AwayTeamPredictor(Predictor):
    def predict(self, s, home, away, date):
        return 'A'


sea = Season("14-15.csv")
hpp = HighPointsPredictor()
htp = HomeTeamPredictor()
atp = AwayTeamPredictor()

for date,home,away,res in sea.matches:
    hpp.test(sea,home,away,date,res)
    htp.test(sea,home,away,date,res)
    atp.test(sea,home,away,date,res)

print 'High Points Accuracy:', hpp.accuracy()
print 'Home Team Accuracy:', htp.accuracy()
print 'Away Team Accuracy:', atp.accuracy()


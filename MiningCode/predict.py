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

class LastGamePredictor(Predictor):
    def predict(self, s, home, away, date):
        hlast = s.lastGame(home,date)
        alast = s.lastGame(away,date)
        if hlast=='N' or alast=='N':
            return 'H'
        if hlast == 'W' and (not alast == 'W'):
            return 'H'
        if alast == 'W' and (not hlast == 'W'):
            return 'A'
        if hlast == alast:
            return 'D'
        return 'H' #default behaviour

csv_files = ['11-12.csv','12-13.csv','13-14.csv','14-15.csv','15-16.csv']
hpp_tot = 0
htp_tot = 0
atp_tot = 0
lgp_tot = 0

for csv in csv_files:
    sea = Season(csv)
    hpp = HighPointsPredictor()
    htp = HomeTeamPredictor()
    atp = AwayTeamPredictor()
    lgp = LastGamePredictor()
    
    for date,home,away,res in sea.matches:
        hpp.test(sea,home,away,date,res)
        htp.test(sea,home,away,date,res)
        atp.test(sea,home,away,date,res)
        lgp.test(sea,home,away,date,res)
    
    print '\nSeason: ', csv
    print '\tHigh Points Accuracy:', hpp.accuracy()
    print '\tHome Team Accuracy:', htp.accuracy()
    print '\tAway Team Accuracy:', atp.accuracy()
    print '\tLast Game Accuracy:', lgp.accuracy()

    hpp_tot += hpp.accuracy()
    htp_tot += htp.accuracy()
    atp_tot += atp.accuracy()
    lgp_tot += lgp.accuracy()

print '\nSummary statistics over ', len(csv_files),' seasons:'
print '\tHigh Points Accuracy:', hpp_tot/len(csv_files)
print '\tHome Team Accuracy:',  htp_tot/len(csv_files)
print '\tAway Team Accuracy:', atp_tot/len(csv_files)
print '\tLast Game Accuracy:', lgp_tot/len(csv_files)



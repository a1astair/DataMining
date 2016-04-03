from season import Season
import matplotlib.pyplot as plt
from operator import add
from sklearn import tree

class Predictor(object):
    def __init__(self):
        self.correct = 0
        self.false = 0
        self.predHist = []
    
    def test(self, s, home, away, date, res):
        if self.predict(s, home, away, date) == res:
            self.correct += 1
            self.predHist.append(1)
        else:
            self.false += 1
            self.predHist.append(0)
        return (self.correct, self.false)

   
    def accuracy(self):
        denom = self.correct+self.false
        if denom == 0:
            return 0
        return float(self.correct)/denom

    def accuracyOverTime(self):
        res = []
        for i in range(0,len(self.predHist),1):
            lastI = min(i+int(.2*len(self.predHist)),len(self.predHist))
            acc = float(sum(self.predHist[i:lastI]))/(lastI-i)
            res.append(acc)
        return res

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
    def strID(self):
        return "High Points Predictor"

class HomeTeamPredictor(Predictor):
    def predict(self, s, home, away, date):
        return 'H'
    def strID(self):
        return "Home Team Predictor"

class AwayTeamPredictor(Predictor):
    def predict(self, s, home, away, date):
        return 'A'
    def strID(self):
        return "Away Team Predictor"

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
    def strID(self):
        return "Last Game Predictor"

class BettingOddsPredictor(Predictor):
    def predict(self, s, home, away, date):
        for dateM,homeM,awayM,res,bet in s.matches:
            if date == dateM and home == homeM and away == awayM:
                return bet
        print "something has gone horribly wrong!"

    def strID(self):
        return "Betting Odds Predictor"

class DecisionTreePredictor(Predictor):
    def __init__(self, trainingData):
        super(self.__class__,self).__init__()
        data = []
        target = []
        self.c2i = {}
        self.i2c = {}
        def mutual_map(a,b):
            self.c2i[a] = b
            self.i2c[b] = a
        mutual_map('H',0)
        mutual_map('D',1)
        mutual_map('A',2)
        self.c2i['W'] = 0
        self.c2i['D'] = 1
        self.c2i['L'] = 2
        self.c2i['N'] = 3
        for sea in trainingData:
            for date, home, away, res, bet in sea.matches:
                home_standing, home_remain = sea.standing(home,date)
                away_standing, away_remain = sea.standing(away,date)
                data.append( [ home_standing, self.c2i[sea.lastGame(home,date)], away_standing, self.c2i[sea.lastGame(away,date)], sea.points_on_date(home,date)-sea.points_on_date(away,date) ] )
                feature_names = ['Home standing','Home last game', 'Away standing','Away last game','Point difference']
                target.append(self.c2i[res])
        self.clf = tree.DecisionTreeClassifier(max_depth = 3)
        self.clf = self.clf.fit(data, target)

    def predict(self, s, home, away, date):
        home_standing, home_remain = sea.standing(home,date)
        away_standing, away_remain = sea.standing(away,date)
        return self.i2c[self.clf.predict([[ home_standing, self.c2i[sea.lastGame(home,date)], away_standing, self.c2i[sea.lastGame(away,date)], sea.points_on_date(home,date)-sea.points_on_date(away,date) ]])[0]]

    def strID(self):
        return "Decision Tree Predictor"

csv_files = ['11-12.csv','12-13.csv','13-14.csv','14-15.csv','15-16.csv']
number_predictors = 6
number_games = 380
tot_acc = [0]*number_predictors
acc_OT  = [[0]*number_games]*number_predictors
totalMarginOfVic = [0]*10

for csv in csv_files:
    sea = Season(csv)
    trainingData = []
    for train_csv in list(set(csv_files) - set([csv])):
        trainingData.append(Season(csv))
    predictors = [HighPointsPredictor(),HomeTeamPredictor(),AwayTeamPredictor(),LastGamePredictor(),BettingOddsPredictor(),DecisionTreePredictor(trainingData)]

    for date,home,away,res,bet in sea.matches:
        for pred in predictors:
            pred.test(sea,home,away,date,res)
        #hpp.test(sea,home,away,date,res)
        #htp.test(sea,home,away,date,res)
        #atp.test(sea,home,away,date,res)
        #lgp.test(sea,home,away,date,res)
        #bop.test(sea,home,away,date,res)
        #dct.test(sea,home,away,date,res)
 
    print '\nSeason: ', csv
    for pred in predictors:
        print '\t', pred.strID(), "Accuracy:", pred.accuracy()

    for i in range(len(predictors)):
        tot_acc[i] += predictors[i].accuracy()
        accOT = predictors[i].accuracyOverTime()
        if len(accOT) == number_games:
            acc_OT[i] = map(add,acc_OT[i],accOT)
    
    totalMarginOfVic = map(add,totalMarginOfVic,sea.marginOfVictory)

print '\nSummary statistics over ', len(csv_files),' seasons:'
for i in range(number_predictors):
    print '\t',predictors[i].strID(),'Accuracy:', tot_acc[i]/len(csv_files)
    plt.plot(map(lambda x: x/4,acc_OT[i]), label=predictors[i].strID())
plt.ylabel("Accuracy over 20 game window")
plt.title("Predictor Accuracy Over a Season")
ax = plt.axes()
ax.axes.get_xaxis().set_visible(False)
plt.legend()
plt.show()


#plt.bar(range(len(totalMarginOfVic)),totalMarginOfVic)
#plt.title('Margin of Victory in EPL games')
#plt.ylabel('Number of games')
#plt.xlabel('Margin of Victory')
#plt.show()
#


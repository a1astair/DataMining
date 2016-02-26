from sklearn import tree
from sklearn.naive_bayes import MultinomialNB
from season import Season

c2i = {}
i2c = {}

def mutual_map(a,b):
    c2i[a] = b
    i2c[b] = a

mutual_map('H',0)
mutual_map('D',1)
mutual_map('A',2)

#this overrides the previous reverse values, but it doesn't matter because we're not interpreting those values yet. 
mutual_map('N',-1)
mutual_map('W',0)
mutual_map('L',2)

scores = []

csv_files = ['11-12.csv','12-13.csv','13-14.csv','14-15.csv','15-16.csv']
for test_sea in csv_files:
    test_data = []
    test_target = []
    data = []
    target = []
    loocv = set(csv_files) - set([test_sea])
    sea = Season(test_sea)
    for date,home,away,res in sea.matches:
         home_standing, home_remain = sea.standing(home,date)
         away_standing, away_remain = sea.standing(away,date)
         #data.append( [ home_standing, home_remain, c2i[sea.lastGame(home,date)], away_standing, away_remain, c2i[sea.lastGame(away,date)], sea.points_on_date(home,date)-sea.points_on_date(away,date) ] )
         test_data.append( [ home_standing, c2i[sea.lastGame(home,date)], away_standing, c2i[sea.lastGame(away,date)], sea.points_on_date(home,date)-sea.points_on_date(away,date) ] )
         feature_names = ['Home standing','Home last game', 'Away standing','Away last game','Point difference']
         test_target.append(c2i[res])
    for csv in loocv:
        sea = Season(csv)
        for date,home,away,res in sea.matches:
             home_standing, home_remain = sea.standing(home,date)
             away_standing, away_remain = sea.standing(away,date)
             #data.append( [ home_standing, home_remain, c2i[sea.lastGame(home,date)], away_standing, away_remain, c2i[sea.lastGame(away,date)], sea.points_on_date(home,date)-sea.points_on_date(away,date) ] )
             data.append( [ home_standing, c2i[sea.lastGame(home,date)], away_standing, c2i[sea.lastGame(away,date)], sea.points_on_date(home,date)-sea.points_on_date(away,date) ] )
             feature_names = ['Home standing','Home last game', 'Away standing','Away last game','Point difference']
             target.append(c2i[res])
    clf = tree.DecisionTreeClassifier(max_depth=3)
    clf = clf.fit(data,target)
    print 'Testing on ',test_sea
    scores.append(clf.score(test_data,test_target))
    print 'Score: ',scores[-1]

print '\n\nAverage Score: ', sum(scores)/len(scores)      


#from IPython.display import Image
#from sklearn.externals.six import StringIO
#import pydot
#dot_data = StringIO()
#with open('tree.dot','w') as f:
#    f = tree.export_graphviz(clf,out_file=f,feature_names=feature_names)
#tree.export_graphviz(clf,out_file=dot_data,feature_names=feature_names,filled=True,rounded=True)
#graph = pydot.graph_from_dot_data(dot_data.getvalue())
#Image(graph.create_png())



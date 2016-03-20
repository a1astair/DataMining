import pandas as pd
import time
    
class Season:
    def __init__(self,filename):
        self.dates = []
        self.matches = []
        self.record = {}
        self.points = {}
        self.teams = []
        self.max_points = 3 * 38 
        data = pd.read_csv(filename)
        for index, row in data.iterrows():
            home = row['HomeTeam']
            away = row['AwayTeam']
            if home not in self.teams:
                self.teams.append(home)
            res  = row['FTR']
            date = time.strptime(row['Date'],'%d/%m/%y')
            self.matches.append((date,home,away,res))
            if (self.dates):
                if(self.dates[-1] < date ):
                    self.dates.append(date)
            else:
                self.dates.append(date)
            if res == 'H':
                self.addResult(home,'W',date)
                self.addResult(away,'L',date)
            elif res == 'A':
                self.addResult(home,'L',date)
                self.addResult(away,'W',date)
            else:
                self.addResult(home,'D',date)
                self.addResult(away,'D',date)
        

    def addResult(self,team,result,date):
        pointVal = 0
        if result == 'W':
            pointVal = 3
        elif result == 'D':
            pointVal = 1
        if team in self.record:
            self.record[team].append((result,date))
            self.points[team].append((self.points[team][-1][0]+pointVal,date))
        else:
            self.record[team] = [(result,date)]
            self.points[team] = [(pointVal,date)]
    
    def win_draw_loss(self,team):
        win = 0
        loss = 0
        draw = 0
        for game in self.record[team]:
            if game == 'W':
                win += 1
            elif game == 'D':
                draw += 1
            else:
                loss += 1
        return (win,draw,loss)
    
    def points_on_date(self,team, date):
        value = 0
        for game in self.points[team]:
            if game[1] >= date:
            #if game[1] > date:
                break
            else:
                value = game[0]
        return value
    
    def standings(self,date):
        curr_points = []
        for team in self.points:
            curr_points.append((self.points_on_date(team,date),team))
        return sorted(curr_points, reverse=True)
    
    def gamesPlayed(self,team,date):
        count = 0
        for game in self.record[team]:
            if game[1] >= date:
                return count
            else:
                count += 1
        return count
    
    def standing(self,team,date):
        rank = 1
        remain_games = len(self.record[team]) - self.gamesPlayed(team,date)
        for t in self.standings(date):
            if t[1] == team:
                return (rank,remain_games)
            else:
                rank += 1
        return (rank,remain_games)

    def lastGame(self,team,date):
        last_game = 'N'
        for game in self.record[team]:
            if game[1] >= date:
                break
            else:
                last_game = game[0]
        return last_game

    def custom_points_on_date(self, team, date):
        value = 0
        for game in record[team]:
            if game[1] >= date:
                break
            else:
                #other stuff
                value += 1 #dummy holder
        return value
    
       

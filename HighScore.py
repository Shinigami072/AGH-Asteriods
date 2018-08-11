class HighScore:
    def __init__(self,name,score):
        self.name=name
        self.score=score
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "{:010d} - {:^13.13s}\n".format(self.score,self.name)

class HighScores:
    def __init__(self):
        self.scores = []
        self.highscore = 0
        self.lowscore = 0

    def read(self): #wczytanie z pliku
        self.scores = []
        F = open("files/HighScores")
        for s in F:
            s = s.split(" - ")

            self.scores.append(HighScore(s[1][0:-1].strip(),(int)(s[0])))
        F.close()

        self.scores = sorted(self.scores,key=lambda s: s.score,reverse=True )
        self.highscore = self.scores[0].score
        self.lowscore = (self.scores[len(self.scores)-1]).score

    def write(self): # zapizanie do pliku

        F = open("files/HighScores",mode="w")
        for s in  self.scores:
            F.write(s.__str__())
        F.close()
    def add(self,hiscore):
        index = len(self.scores)
        worse = None

        print(self)
        for i in range(index):
            if(hiscore.score < self.scores[i].score):
                print(i,self.scores[i-1].score,hiscore.score)
            else:
                worse = self.scores[i]
                self.scores.insert(i,hiscore)
                self.scores.pop(len(self.scores) - 1)
                print("You Beat:",worse)
                break

        self.highscore = self.scores[0].score
        self.lowscore = self.scores[len(self.scores) - 1].score
        return worse



    def __repr__(self):
        s=""
        for d in self.scores:
            s+=d.__str__()
        return s


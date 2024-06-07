def calci(Catcount, left):
    progress = [0, 0 , 0]
    Batsman = Catcount[0] + Catcount[1]
    if Batsman <= 4:
        progress[0] = (Batsman/4)*100
    else:
        progress[0] = 100
    if Catcount[2] >=1:
        progress[1] = 100
    else:
        progress[1] = 0
    Bowler = Catcount[3] + Catcount[4]
    if Bowler <= 4:
        progress[2] = (Bowler/4)*100
    else:
        progress[2] = 100
    return progress
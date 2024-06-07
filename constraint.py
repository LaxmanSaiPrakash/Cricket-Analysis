def constraint(dataset):
    Batsman = 0
    Bowler = 0
    overseas = 0
    credits = 0
    wicket_keeper = 0
    AllRounder = 0
    count = 0
    for data in dataset:
        overseas += data[1]
        credits += data[2]
        wicket_keeper += data[3]
        if data[4] == "TopOrder" or data[4] == "MiddleOrder":
            Batsman += 1
        elif data[4] == "AllRounder":
            AllRounder += 1
        else:
            Bowler += 1
    if Batsman >= 4:
        count +=1
    if Bowler >= 4:
        count += 1
    if AllRounder >=1:
        count+=1
    if overseas >=4:
        count+=1
    if wicket_keeper >=1:
        count+=1
    if count == 5:
        return [True, credits]
    else:
        return [False, credits]
def score(report, sentiment, bias):
    sum = 0
    left = 0
    right = 0
    center = 0
    difference = 0
    it = 0

    reportFin = 0
    sentFin = 0
    biasFin = 0

    for i in report:
        sum = sum + i
    
    for i in report:
        it = it + 1
        if (it <= 2):
            left = left + i
        if (it > 3):
            right = right + i
            
        if (it == 3):
            center = i
            left = left + center
            right = right + center  

    if (left > right):
        difference = left - right
    if (right > left):
        difference = right - left
    if (right == left):
        return 10

    reportRes = sum - difference
    reportQuot = reportRes/sum
    reportFin = reportQuot*10

    sentAbs = abs(sentiment)
    revSent = 1 - sentAbs
    sentFin = 10*revSent

    if (bias == "Left"):
        biasFin = 1
    if (bias == "Lean Left"):
        biasFin = 5
    if (bias == "Center"):
        biasFin = 10
    if (bias == "Lean Right"):
        biasFin = 5
    if (bias == "Right"):
        biasFin = 1

    sentFin = round(sentFin)
    reportFinn = reportFin*0.25
    sentFinn = sentFin*0.35
    biasFinn = biasFin*0.4

    fin = reportFinn + sentFinn + biasFinn

    return fin

if(__name__ == "__main__"):
    print(score([10, 20, 10, 60, 100], -0.9, "Lean Right"))
    
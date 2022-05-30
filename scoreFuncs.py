def fieldScore(gameStats, weights):
    score = 0.0
    for k, v in weights.items():
        if k != 'conceded' and k != 'saves':
            score += float(weights[k]) * int(gameStats[k])

    return score / (int(gameStats['timePlayed']['minutes']))

def goalKeeperScore(gameStats, weights):
    score = 0.0
    for k, v in weights.items():
        score += float(weights[k]) * int(gameStats[k])

    return score / (int(gameStats['timePlayed']['minutes']))



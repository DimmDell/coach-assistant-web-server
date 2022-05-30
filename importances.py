from __future__ import division, print_function

import firebase_admin
from firebase_admin import db
from firebase import ref
import warnings

warnings.filterwarnings('ignore')
# russian headres
from matplotlib import pyplot as plt
from matplotlib import rc
import pandas as pd
import numpy as np
from sklearn.ensemble._forest import RandomForestRegressor

font = {'family': 'Verdana',
        'weight': 'normal'}
rc('font', **font)


def getImportances():
    data = db.reference('dictStats').get()
    pd_data = pd.DataFrame(list(data.values()))

    # gameID,shots,shotsOnTarget,passes,missedPasses,rounds,tackles,yellowCard,redCard,assists,goals,conceded,result

    features = {
        "f1": u"assists",
        "f2": u"conceded",
        "f3": u"goals",
        "f4": u"missedPasses",
        "f5": u"passes",
        "f6": u"redCard",
        "f7": u"rounds",
        "f8": u"saves",
        "f9": u"shots",
        "f10": u"shotsOnTarget",
        "f11": u"tackles",
        "f12": u"yellowCard",
    }

    forest = RandomForestRegressor(n_estimators=1000, max_features=12, random_state=1)
    forest.fit(pd_data.drop(['gameID', 'result', 'difference,'], axis=1),
               pd_data['result'])
    importances = forest.feature_importances_

    indices = np.argsort(importances)[::-1]
    # Plot the feature importancies of the forest
    num_to_plot = 12
    feature_indices = [ind + 1 for ind in indices[:num_to_plot]]

    # Print the feature ranking
    print("Feature ranking:")

    importances_dict = {}
    for f in range(num_to_plot):
        print("%d. %s %f " % (f + 1,
                              features["f" + str(feature_indices[f])],
                              importances[indices[f]]))
        importances_dict[features["f" + str(feature_indices[f])]] = 2.0 * round(importances[indices[f]], 4)
    
    return importances_dict


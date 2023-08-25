import numpy as np
import pickle
import xgboost as xgb
import os

from sklearn.datasets import load_svmlight_file

param = {
   'alpha': 0.9,
   'max_bin': 256,
   'scale_pos_weight': 2,
   'learning_rate': 0.1,
   'subsample': 1,
   'reg_lambda': 1,
   'min_child_weight': 0,
   'max_depth': 8,
   'max_leaves': 2**8,
   'tree_method': 'hist',
   "objective": 'binary:logistic'
}

# X is a scipy csr matrix, XGBoost supports many other input types,
X, y = load_svmlight_file(os.path.join("/home/dev/data", "agaricus.txt.train"))
dtrain = xgb.DMatrix(X, y)
# validation set
X_test, y_test = load_svmlight_file(os.path.join("/home/dev/data", "agaricus.txt.test"))
dtest = xgb.DMatrix(X_test, y_test)

# specify validations set to watch performance
watchlist = [(dtest, "eval"), (dtrain, "train")]
# number of boosting rounds
num_round = 2
bst = xgb.train(param, dtrain, num_boost_round=num_round, evals=watchlist)

# run prediction
preds = bst.predict(dtest)
labels = dtest.get_label()
print(
    "error=%f"
    % (
        sum(1 for i in range(len(preds)) if int(preds[i] > 0.5) != labels[i])
        / float(len(preds))
    )
)
bst.save_model("/home/dev/output/model-0.json")
# dump model
bst.dump_model("/home/dev/output/dump.raw.txt")
# dump model with feature map
bst.dump_model("/home/dev/output/dump.nice.txt", "/home/dev/data/featmap.txt")

# save dmatrix into binary buffer
dtest.save_binary("/home/dev/output/dtest.dmatrix")
# save model
bst.save_model("/home/dev/output/model-1.json")
# load model and data in
bst2 = xgb.Booster(model_file="/home/dev/output/model-1.json")
dtest2 = xgb.DMatrix("/home/dev/output/dtest.dmatrix")
preds2 = bst2.predict(dtest2)
# assert they are the same
assert np.sum(np.abs(preds2 - preds)) == 0

# alternatively, you can pickle the booster
pks = pickle.dumps(bst2)
# load model and data in
bst3 = pickle.loads(pks)
preds3 = bst3.predict(dtest2)
# assert they are the same
assert np.sum(np.abs(preds3 - preds)) == 0

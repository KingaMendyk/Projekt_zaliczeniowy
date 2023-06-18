from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split, cross_val_score, KFold, GridSearchCV
from sklearn.exceptions import NotFittedError
import pandas as pd


class Model:
    def __init__(self, *args):
        self.db = args[0]
        self.model = GaussianNB()
        self.data = self.db.fetch_data()
        self.df = pd.DataFrame(self.data, columns=self.db.fetch_names())
        self.X_train = self.df.iloc[:, :-1].values
        self.y_train = self.df.iloc[:, -1].values
        self.X_test = self.X_train
        self.y_test = self.y_train
        self.best_model = None

    def predict(self, data_to_pred):
        df = pd.DataFrame(data_to_pred)
        try:
            prediction = self.model.predict(df)
            return prediction[0]
        except NotFittedError as e:
            return "0"

    def train(self, split, size):
        X = self.X_train
        y = self.y_train

        if split:
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=size / 100)
            self.model.fit(self.X_train, self.y_train)
        else:
            self.model.fit(X, y)
        self.evaluate_best("train")

    def check(self, tset):
        if tset == "train":
            X = self.X_train
            y = self.y_train
        elif tset == "test":
            X = self.X_test
            y = self.y_test
        return X, y

    def evaluate_best(self, tset):
        X, y = self.check(tset)

        kfold = KFold()
        scores = cross_val_score(self.model, X, y, cv=kfold, scoring="accuracy")
        avg = scores.mean()
        param_grid = {'priors': [None],
                      'var_smoothing': [1e-9, 1e-6, 1e-12]}
        grid_search = GridSearchCV(self.model, param_grid, cv=kfold)
        grid_search.fit(X, y)
        results = pd.DataFrame(grid_search.cv_results_)
        best_param = grid_search.best_params_
        best_score = grid_search.best_score_
        self.best_model = grid_search.best_estimator_

        res = {"avg": avg, "param_grid": results, "best_param": best_param, "best_score": best_score}
        return res

    def evaluate_accuracy(self, tset):
        X, y = self.check(tset)
        best_predict = self.best_model.predict(X)
        acc = accuracy_score(y, best_predict)
        return acc

    def evaluate_matrix(self, tset):
        X, y = self.check(tset)
        cm = confusion_matrix(y, self.best_model.predict(X))
        return cm

    def evaluate_report(self, tset):
        X, y = self.check(tset)
        report = classification_report(y, self.best_model.predict(X))
        return report

    def rebuild(self, database):
        self.refresh(database)
        self.model = GaussianNB()
        self.X_train = self.df.iloc[:, :-1].values
        self.y_train = self.df.iloc[:, -1].values
        self.X_test = self.X_train
        self.y_test = self.y_train
        self.best_model = None

    def refresh(self, database):
        self.db = database
        self.data = self.db.fetch_data()
        self.df = pd.DataFrame(self.data, columns=self.db.fetch_names())

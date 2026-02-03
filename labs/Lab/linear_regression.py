import numpy as np

class LinearRegression:
    def __init__(self, X, y, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.X = np.asarray(X, dtype=np.float64)
        self.y = np.asarray(y, dtype=np.float64)

        if fit_intercept:
            if self.X.ndim == 1:
                self.X = self.X.reshape(-1, 1)
            if not np.allclose(self.X[:, 0], 1):
                self.X = np.column_stack([np.ones(self.X.shape[0]), self.X])                

        self.n = self.X.shape[0]
        self.d = self.X.shape[1]

    def fit(self):
        XtX = self.X.T @ self.X
        Xty = self.X.T @ self.y
        self.beta = np.linalg.solve(XtX, Xty)
        return self.beta
    
    def residuals(self):
        return self.y - self.predict()
    
    def predict(self, X_new=None):
        if not hasattr(self, "beta"):
            raise RuntimeError("Model must be fitted before calling predict().")
        
        if X_new is None:
            return self.X @ self.beta

        X_pred = np.asarray(X_new, dtype=np.float64)
        if X_pred.ndim == 1:
            X_pred = X_pred.reshape(-1, 1)

        if self.fit_intercept:
            X_pred = np.column_stack([np.ones(X_pred.shape[0]), X_pred])

        if X_pred.shape[1] != self.beta.shape[0]:
            raise ValueError(f"X has {X_pred.shape[1]} columns, but model expects {self.beta.shape[0]}")
        
        return X_pred @ self.beta

    def sample_variance(self):
        residuals = self.residuals()
        return np.sum(residuals**2) / (self.n - self.d)
    
    def standard_deviation(self):
        return np.sqrt(self.sample_variance())
    
    def rmse(self):
        residuals = self.residuals()
        return np.sqrt(np.mean(residuals**2))
        
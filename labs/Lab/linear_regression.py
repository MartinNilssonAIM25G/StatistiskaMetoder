import numpy as np
from scipy.stats import f, t, pearsonr

class LinearRegression:
    """
    Ordinary Least Squares linear regression.
    
    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Design Matrix
    y : array-like, shape (n_samples,)
        Target values
    fit_intercept : bool, default=True
        Whether to add an intercept column to X
    """
    def __init__(self, X, y, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.X = np.asarray(X, dtype=np.float64)
        self.y = np.asarray(y, dtype=np.float64)

        if fit_intercept:
            if self.X.ndim == 1:
                self.X = self.X.reshape(-1, 1)
            # Only add intercept column if not already present
            if not np.allclose(self.X[:, 0], 1):
                self.X = np.column_stack([np.ones(self.X.shape[0]), self.X])                

        self.n = self.X.shape[0]
        self.d = self.X.shape[1]

    def fit(self):
        """Fit the model using ordinary least squares."""
        XtX = self.X.T @ self.X
        Xty = self.X.T @ self.y

        self.XtX_inv = np.linalg.inv(XtX)
        self.beta = np.linalg.solve(XtX, Xty)
        
        return self.beta
    
    def _check_fitted(self):
        if not hasattr(self, "beta") or not hasattr(self, "XtX_inv"):
            raise RuntimeError("Call fit() before requesting statistics.")
    
    def df_error(self):
        """Degrees of freedom for error (n - d)."""
        return self.n - self.d
    
    def residuals(self):
        return self.y - self.predict()
    
    def sse(self):
        return np.sum(self.residuals()**2)
    
    def ssr(self):
        y_hat = self.predict()
        return np.sum((y_hat - self.y.mean())**2)
    
    def sst(self):
        return np.sum((self.y - self.y.mean())**2)
    
    def predict(self, X_new=None):
        """
        Predict using the linear model.
        
        Parameters
        ----------
        X_new : array-like, optional
            New data to predict. If None, returns fitted values.
        """
        self._check_fitted()
        
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
        """Unbiased estimate of error variance: SSE / (n - d)."""
        return self.sse() / (self.df_error())
    
    def standard_deviation(self):
        return np.sqrt(self.sample_variance())
    
    def rmse(self):
        return np.sqrt(self.sse() / self.n)
        
    def r_squared(self):
        """Coefficient of determination (R²)."""
        sst = self.sst()
        if sst == 0:
            raise ValueError("R² is undefined when variance of y is zero")
        return 1-(self.sse()/sst)

    def regression_significance(self):
        """
        F-test for overall regression significance.
        
        Tests H₀: all slope coefficients = 0
        
        Returns
        -------
        F : float
            F-statistic
        p_value : float
            P-value
        """
        SSR =self.ssr()
        SSE = self.sse()

        df_reg = self.d - 1
        df_err = self.df_error()

        MSR = SSR / df_reg
        MSE = SSE / df_err

        F = MSR / MSE

        p_value = f.sf(F, df_reg, df_err)

        return F, p_value

    def cov_beta(self):
        """Variance-covariance matrix of coefficients: σ² (X'X)⁻¹."""
        self._check_fitted()
        return self.sample_variance() * self.XtX_inv

    def standard_errors(self):
        """Standard errors of coefficients."""
        return np.sqrt(np.diag(self.cov_beta()))

    def t_values(self):
        """T-statistics for testing H₀: βᵢ = 0."""
        self._check_fitted()
        se = self.standard_errors()
        # Avoid division by zero
        se = np.where(se == 0, np.nan, se)
        return self.beta / se

    def p_values(self):
        """P-values for two-sided t-tests on coefficients."""
        tv = self.t_values()
        # Two-sided test: 2 * P(T > |t|)
        return 2 * t.sf(np.abs(tv), self.df_error())
    
    def confidence_intervals(self, alpha = 0.05):
        """
        Confidence intervals for coefficients.
        
        Parameters
        ----------
        alpha : float, default=0.05
            Significance level (0.05 → 95% CI)
        
        Returns
        -------
        lower, upper : ndarray
            Lower and upper bounds
        """
        self._check_fitted()
        se = self.standard_errors()
        df = self.df_error()
        tcrit = t.ppf(1 - alpha/2, df)
        lower = self.beta - tcrit * se
        upper = self.beta + tcrit * se
        return lower, upper

    def pearson_matrix(self):
        """
        Pearson correlation matrix between features.
        
        Returns correlation matrix excluding intercept if present.
        """
        self._check_fitted()
        X = self.X
        if self.fit_intercept:
            X = X[:, 1:]

        d = X.shape[1]
        R = np.zeros((d, d), dtype=np.float64)

        for i in range(d):
            for j in range(d):
                r, _ = pearsonr(X[:, i], X[:, j])
                R[i, j] = r    

        return R
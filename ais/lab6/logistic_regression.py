# logistic_regression.py
import time
import numpy as np


def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


def compute_loss(X, y, theta):
    """Log loss """
    h = sigmoid(X @ theta)
    h = np.clip(h, 1e-15, 1 - 1e-15)
    return -np.mean(y * np.log(h) + (1 - y) * np.log(1 - h))


def compute_gradient(X, y, theta):
    m = len(y)
    h = sigmoid(X @ theta)
    return (X.T @ (h - y)) / m


def compute_hessian(X, theta):
    """H = (1/m) Xᵀ diag(h(1-h)) X. Для упрощённого Ньютона."""
    m = X.shape[0]
    h = sigmoid(X @ theta)
    d = h * (1 - h)
    return (X.T @ (X * d[:, None])) / m


def fit(X, y, learning_rate=0.1, n_iterations=1000,
        optimizer='gd', tol=1e-7, verbose=False):

    #Обучает логистическую регрессию.

    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n_features = X.shape[1]
    theta = np.zeros(n_features)
    history = []
    t0 = time.time()
    n_done = 0

    for it in range(n_iterations):
        loss = compute_loss(X, y, theta)
        history.append(loss)
        grad = compute_gradient(X, y, theta)

        if optimizer == 'gd':
            step = learning_rate * grad
            theta = theta - step
        elif optimizer == 'newton':
            H = compute_hessian(X, theta)
            # pinv стабильнее inv при вырожденной матрице
            step = learning_rate * (np.linalg.pinv(H) @ grad)
            theta = theta - step
        else:
            raise ValueError(f"Unknown optimizer: {optimizer}")

        n_done = it + 1
        # early stopping: если loss почти не меняется
        if len(history) >= 2 and abs(history[-2] - history[-1]) < tol:
            # добавляем финальный loss и выходим
            history.append(compute_loss(X, y, theta))
            n_done = it + 2
            break

        if verbose and (it % 100 == 0 or it == n_iterations - 1):
            print(f'  iter {it:5d}  loss={loss:.6f}')

    time_sec = time.time() - t0
    return theta, history, n_done, time_sec


def predict_proba(X, theta):
    return sigmoid(X @ theta)


def predict(X, theta, threshold=0.5):
    return (predict_proba(X, theta) >= threshold).astype(int)
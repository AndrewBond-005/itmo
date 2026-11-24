# preprocessing.py
import numpy as np
import pandas as pd

ZERO_AS_NAN_COLS = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']


def load_data(path='diabetes.csv'):
    return pd.read_csv(path)


def report_missing(df):
    """Печатает, сколько нулей в колонках, где 0 = пропуск."""
    print('\n=== Нули в колонках, где 0 = пропуск (до обработки) ===')
    for col in ZERO_AS_NAN_COLS:
        n = int((df[col] == 0).sum())
        print(f'  {col:15s}: {n:4d} ({100 * n / len(df):.1f}%)')


def fix_zeros(df):
    """Заменяет 0 на NaN в ZERO_AS_NAN_COLS."""
    df = df.copy()
    for col in ZERO_AS_NAN_COLS:
        df[col] = df[col].replace(0, np.nan)
    return df


def split_data(X, y, test_size=0.2, random_state=42):
    """Свой shuffle-split: перемешиваем индексы и режем по границе."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(y)
    rng = np.random.RandomState(random_state)
    idx = rng.permutation(n)
    n_test = int(round(n * test_size))
    test_idx = idx[:n_test]
    train_idx = idx[n_test:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def fill_zeros_with_median(X_train, X_test, feature_names):
    """
    Заполняет NaN медианой train-набора.
    X уже numpy-массивы; feature_names — список имён, чтобы знать, где NaN.
    Возвращает (X_train, X_test, medians_dict).
    """
    X_train = X_train.copy()
    X_test = X_test.copy()
    medians = {}
    for j, name in enumerate(feature_names):
        col_train = X_train[:, j]
        nan_mask = np.isnan(col_train)
        if nan_mask.any():
            med = np.nanmedian(col_train)
            medians[name] = med
            X_train[nan_mask, j] = med
        # в test тоже могут быть NaN — заполняем тем же медианным значением
        nan_mask_test = np.isnan(X_test[:, j])
        if nan_mask_test.any() and name in medians:
            X_test[nan_mask_test, j] = medians[name]
    return X_train, X_test, medians


def standardize(X_train, X_test):
    """Z-score: mean/std только на train."""
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    std[std == 0] = 1.0
    return (X_train - mean) / std, (X_test - mean) / std, mean, std


def add_bias(X):
    """Добавляет столбец единиц слева (для θ₀)."""
    return np.hstack([np.ones((X.shape[0], 1)), X])


def prepare_dataset(path='diabetes.csv', test_size=0.2, random_state=42):
    """
    Полный пайплайн: load -> report -> fix zeros -> split -> fill median -> standardize -> bias.
    Возвращает словарь со всеми нужными объектами.
    """
    df = load_data(path)
    report_missing(df)

    # сначала NaN, чтобы сплит был честный (NaN не влияют на перемешивание)
    df_fixed = fix_zeros(df)
    X = df_fixed.drop(columns=['Outcome']).values.astype(float)
    y = df_fixed['Outcome'].values.astype(float)
    feature_names = list(df_fixed.drop(columns=['Outcome']).columns)

    X_train, X_test, y_train, y_test = split_data(
        X, y, test_size=test_size, random_state=random_state
    )

    # медиана — только на train
    X_train, X_test, medians = fill_zeros_with_median(X_train, X_test, feature_names)

    X_train, X_test, mean, std = standardize(X_train, X_test)

    X_train_b = add_bias(X_train)
    X_test_b = add_bias(X_test)

    return {
        'df_raw': df,
        'df_fixed': df_fixed,
        'feature_names': feature_names,
        'X_train': X_train_b,
        'X_test': X_test_b,
        'y_train': y_train,
        'y_test': y_test,
        'medians': medians,
        'mean': mean,
        'std': std,
    }
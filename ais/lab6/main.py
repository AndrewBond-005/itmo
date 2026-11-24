# main.py
import os
import numpy as np
import pandas as pd

from preprocessing import prepare_dataset, load_data, fix_zeros
from logistic_regression import fit, predict, compute_loss
from metrics import evaluate
from stats_plots import (print_describe, plot_class_balance,
                         plot_histograms, plot_boxplots_by_class, plot_correlation)
from experiments import (run_grid, learning_rate_study, iterations_study,
                         compare_optimizers, plot_grid_heatmap)

OUT_DIR = 'plots'
DATA_PATH = 'diabetes.csv'


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---------- 1. Данные и статистики ----------
    print('=' * 70)
    print('1. Загрузка и описательные статистики')
    print('=' * 70)
    df_raw = load_data(DATA_PATH)
    print(f'Размер датасета: {df_raw.shape[0]} строк, {df_raw.shape[1]} столбцов')
    print_describe(df_raw, title='(исходные данные, до обработки нулей)')

    print('\n=== Пропуски (NaN) до обработки ===')
    print(df_raw.isna().sum())

    print('\n=== Корреляция с целевой переменной Outcome ===')
    print(df_raw.corr(numeric_only=True)['Outcome'].drop('Outcome').sort_values(ascending=False).round(3))

    plot_class_balance(df_raw['Outcome'].values, OUT_DIR)
    plot_histograms(df_raw, OUT_DIR)
    plot_boxplots_by_class(df_raw, OUT_DIR)
    plot_correlation(df_raw, OUT_DIR)

    # ---------- 2. Препроцессинг ----------
    print('\n' + '=' * 70)
    print('2. Препроцессинг')
    print('=' * 70)
    data = prepare_dataset(DATA_PATH, test_size=0.2, random_state=42)
    print(f"train: {data['X_train'].shape}, test: {data['X_test'].shape}")
    print(f"Доля класса 1 в train: {data['y_train'].mean():.3f}, в test: {data['y_test'].mean():.3f}")
    print('Медианы для заполнения нулей (по train):')
    for k, v in data['medians'].items():
        print(f'  {k}: {v:.2f}')

    df_fixed = fix_zeros(df_raw)
    print_describe(df_fixed, title='(после замены нулей на NaN; describe игнорирует NaN)')

    X_train = data['X_train']
    X_test = data['X_test']
    y_train = data['y_train']
    y_test = data['y_test']

    # ---------- 3. Базовая модель ----------
    print('\n' + '=' * 70)
    print('3. Базовая модель: GD, lr=0.1, n_iter=1000')
    print('=' * 70)
    theta, hist, n_done, t = fit(X_train, y_train,
                                 learning_rate=0.1, n_iterations=1000,
                                 optimizer='gd')
    y_pred_tr = predict(X_train, theta)
    y_pred_te = predict(X_test, theta)
    m_tr = evaluate(y_train, y_pred_tr)
    m_te = evaluate(y_test, y_pred_te)
    print(f'Итераций: {n_done}, время: {t:.3f}s')
    print(f'Train: {m_tr}')
    print(f'Test:  {m_te}')
    print(f'Train loss: {hist[-1]:.5f}')
    print(f'Test loss:  {compute_loss(X_test, y_test, theta):.5f}')
    print('\nВеса (theta):')
    names = ['bias'] + data['feature_names']
    for n, w in zip(names, theta):
        print(f'  {n:15s}: {w: .4f}')

    # ---------- 4. Grid search ----------
    print('\n' + '=' * 70)
    print('4. Grid search по гиперпараметрам')
    print('=' * 70)
    df_results = run_grid(X_train, y_train, X_test, y_test,
                          lrs=(0.001, 0.01, 0.05, 0.1, 0.5),
                          iters=(100, 500, 1000, 5000),
                          optimizers=('gd', 'newton'),
                          newton_lrs=(0.5, 1.0),   # <-- ИСПРАВЛЕНИЕ
                          newton_max_iter=100)
    df_results.to_csv('grid_results.csv', index=False)
    print('\nСохранено в grid_results.csv')
    print('\nТоп-10 по test F1:')
    print(df_results.sort_values('test_f1', ascending=False)
          .head(10)[['optimizer', 'lr', 'n_iter', 'actual_iters',
                     'test_acc', 'test_precision', 'test_recall', 'test_f1',
                     'time_sec']].to_string(index=False))

    plot_grid_heatmap(df_results, OUT_DIR)

    # ---------- 5. Learning rate study ----------
    print('\n' + '=' * 70)
    print('5. Влияние learning rate')
    print('=' * 70)
    learning_rate_study(X_train, y_train, X_test, y_test,
                        lrs=(0.001, 0.01, 0.05, 0.1, 0.5),
                        n_iterations=1000, out_dir=OUT_DIR)

    # ---------- 6. Iterations study ----------
    print('\n' + '=' * 70)
    print('6. Влияние числа итераций')
    print('=' * 70)
    iterations_study(X_train, y_train, X_test, y_test,
                     lr=0.1,
                     iterations=(10, 50, 100, 200, 500, 1000, 2000, 5000),
                     out_dir=OUT_DIR)

    # ---------- 7. GD vs Newton ----------
    print('\n' + '=' * 70)
    print('7. Сравнение GD и Newton')
    print('=' * 70)
    compare_optimizers(X_train, y_train, X_test, y_test,
                       lr=0.1, gd_iters=2000, newton_iters=100,
                       out_dir=OUT_DIR)

    # ---------- 8. Выводы ----------
    print('\n' + '=' * 70)
    print('8. Выводы')
    print('=' * 70)
    best = df_results.sort_values('test_f1', ascending=False).iloc[0]
    print(f"Лучшая комбинация по test F1: optimizer={best['optimizer']}, "
          f"lr={best['lr']}, n_iter={best['n_iter']} -> "
          f"acc={best['test_acc']:.3f}, f1={best['test_f1']:.3f}")

    gd_only = df_results[df_results['optimizer'] == 'gd']
    best_gd = gd_only.sort_values('test_f1', ascending=False).iloc[0]
    print(f"Лучший GD: lr={best_gd['lr']}, n_iter={best_gd['n_iter']} -> "
          f"acc={best_gd['test_acc']:.3f}, f1={best_gd['test_f1']:.3f}")

    newton_only = df_results[df_results['optimizer'] == 'newton']
    best_newton = newton_only.sort_values('test_f1', ascending=False).iloc[0]
    print(f"Лучший Newton: lr={best_newton['lr']}, n_iter={best_newton['n_iter']} -> "
          f"acc={best_newton['test_acc']:.3f}, f1={best_newton['test_f1']:.3f}, "
          f"iters={best_newton['actual_iters']}, time={best_newton['time_sec']:.4f}s")

    small = gd_only[gd_only['lr'] == 0.001].sort_values('n_iter')
    print(f"\nПри lr=0.001 loss на 100 итерациях: "
          f"{small.iloc[0]['train_loss']:.4f}, на 5000: "
          f"{small.iloc[-1]['train_loss']:.4f} "
          f"(маленький шаг -> медленная сходимость)")

    large = gd_only[gd_only['lr'] == 0.5]
    print(f"\nПри lr=0.5: train loss от {large['train_loss'].min():.4f} "
          f"до {large['train_loss'].max():.4f} — "
          f"сходится быстро (early stopping), выигрыша в метриках не даёт")

    print('\nГотово. Графики в папке plots/, результаты грида в grid_results.csv')


if __name__ == '__main__':
    main()
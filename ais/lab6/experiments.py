# experiments.py
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from logistic_regression import fit, predict, compute_loss
from metrics import evaluate


def run_grid(X_train, y_train, X_test, y_test,
             lrs=(0.001, 0.01, 0.05, 0.1, 0.5),
             iters=(100, 500, 1000, 5000),
             optimizers=('gd', 'newton'),
             newton_lrs=(0.5, 1.0),
             newton_max_iter=100):
    rows = []
    print('\n=== Grid search ===')
    for opt in optimizers:
        cur_lrs = newton_lrs if opt == 'newton' else lrs
        for lr in cur_lrs:
            for ni in iters:
                eff_ni = min(ni, newton_max_iter) if opt == 'newton' else ni
                theta, hist, n_done, t = fit(
                    X_train, y_train,
                    learning_rate=lr, n_iterations=eff_ni, optimizer=opt
                )
                y_pred_tr = predict(X_train, theta)
                y_pred_te = predict(X_test, theta)
                m_tr = evaluate(y_train, y_pred_tr)
                m_te = evaluate(y_test, y_pred_te)
                rows.append({
                    'optimizer': opt,
                    'lr': lr,
                    'n_iter': ni,
                    'actual_iters': n_done,
                    'train_loss': hist[-1],
                    'test_loss': compute_loss(X_test, y_test, theta),
                    'train_acc': m_tr['accuracy'],
                    'test_acc': m_te['accuracy'],
                    'test_precision': m_te['precision'],
                    'test_recall': m_te['recall'],
                    'test_f1': m_te['f1'],
                    'time_sec': t,
                })
                print(f"  {opt:6s} lr={lr:<6} n_iter={ni:<5} "
                      f"iters_done={n_done:<5} "
                      f"loss={hist[-1]:.4f} "
                      f"acc={m_te['accuracy']:.3f} "
                      f"f1={m_te['f1']:.3f} "
                      f"t={t:.3f}s")
    return pd.DataFrame(rows)


def learning_rate_study(X_train, y_train, X_test, y_test,
                        lrs=(0.001, 0.01, 0.05, 0.1, 0.5),
                        n_iterations=1000, out_dir='plots'):
    os.makedirs(out_dir, exist_ok=True)
    histories = {}
    print('\n=== Learning rate study (GD) ===')
    for lr in lrs:
        theta, hist, n_done, t = fit(X_train, y_train,
                                     learning_rate=lr,
                                     n_iterations=n_iterations,
                                     optimizer='gd')
        histories[lr] = hist
        y_pred = predict(X_test, theta)
        m = evaluate(y_test, y_pred)
        print(f'  lr={lr:<6} loss={hist[-1]:.4f} '
              f'acc={m["accuracy"]:.3f} f1={m["f1"]:.3f} '
              f'iters_done={n_done} t={t:.3f}s')

    fig, ax = plt.subplots(figsize=(9, 5))
    for lr, hist in histories.items():
        ax.plot(range(len(hist)), hist, label=f'lr={lr}')
    ax.set_xlabel('Итерация')
    ax.set_ylabel('Log loss (train)')
    ax.set_title('Влияние learning rate (GD)')
    ax.set_yscale('log')
    ax.grid(alpha=0.3, which='both')
    ax.legend()
    fig.tight_layout()
    path = os.path.join(out_dir, 'lr_study_loss.png')
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f'  saved {path}')
    return histories


def iterations_study(X_train, y_train, X_test, y_test,
                     lr=0.1, iterations=(10, 50, 100, 200, 500, 1000, 2000, 5000),
                     out_dir='plots'):
    os.makedirs(out_dir, exist_ok=True)
    print('\n=== Iterations study (GD, lr=0.1) ===')
    accs, f1s, losses = [], [], []
    for ni in iterations:
        theta, hist, n_done, t = fit(X_train, y_train,
                                     learning_rate=lr,
                                     n_iterations=ni,
                                     optimizer='gd')
        y_pred = predict(X_test, theta)
        m = evaluate(y_test, y_pred)
        accs.append(m['accuracy'])
        f1s.append(m['f1'])
        losses.append(hist[-1])
        print(f'  n_iter={ni:<5} acc={m["accuracy"]:.3f} '
              f'f1={m["f1"]:.3f} loss={hist[-1]:.4f}')

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(iterations, accs, 'o-', label='accuracy (test)', color='#4C72B0')
    ax1.plot(iterations, f1s, 's-', label='f1 (test)', color='#C44E52')
    ax1.set_xlabel('n_iterations')
    ax1.set_ylabel('Метрика')
    ax1.set_xscale('log')
    ax1.grid(alpha=0.3, which='both')
    ax1.legend(loc='lower right')

    ax2 = ax1.twinx()
    ax2.plot(iterations, losses, '^--', label='train loss', color='gray', alpha=0.7)
    ax2.set_ylabel('Log loss (train)')
    ax2.set_yscale('log')
    ax2.legend(loc='upper right')

    ax1.set_title('Влияние числа итераций (GD, lr=0.1)')
    fig.tight_layout()
    path = os.path.join(out_dir, 'iter_study.png')
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f'  saved {path}')
    return iterations, accs, f1s, losses


def compare_optimizers(X_train, y_train, X_test, y_test,
                       lr=0.1, gd_iters=2000, newton_iters=100,
                       out_dir='plots'):
    os.makedirs(out_dir, exist_ok=True)
    print('\n=== GD vs Newton ===')
    results = {}
    for opt, ni in [('gd', gd_iters), ('newton', newton_iters)]:
        theta, hist, n_done, t = fit(X_train, y_train,
                                     learning_rate=lr,
                                     n_iterations=ni,
                                     optimizer=opt)
        y_pred_tr = predict(X_train, theta)
        y_pred_te = predict(X_test, theta)
        m_tr = evaluate(y_train, y_pred_tr)
        m_te = evaluate(y_test, y_pred_te)
        results[opt] = {
            'history': hist, 'n_done': n_done, 'time': t,
            'theta': theta, 'metrics_train': m_tr, 'metrics_test': m_te,
            'final_loss': hist[-1],
        }
        print(f'  {opt:6s}: iters={n_done:<5} time={t:.3f}s '
              f'loss={hist[-1]:.5f} '
              f'test_acc={m_te["accuracy"]:.3f} test_f1={m_te["f1"]:.3f}')

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    ax = axes[0]
    for opt in ['gd', 'newton']:
        h = results[opt]['history']
        ax.plot(range(len(h)), h, label=f'{opt} (iters={results[opt]["n_done"]})')
    ax.set_xlabel('Итерация')
    ax.set_ylabel('Log loss (train)')
    ax.set_yscale('log')
    ax.set_title('Сходимость: GD vs Newton')
    ax.grid(alpha=0.3, which='both')
    ax.legend()

    ax = axes[1]
    opts = ['gd', 'newton']
    times = [results[o]['time'] for o in opts]
    iters = [results[o]['n_done'] for o in opts]
    x = np.arange(len(opts))
    w = 0.35
    ax.bar(x - w/2, times, w, label='время, с', color='#4C72B0')
    ax2 = ax.twinx()
    ax2.bar(x + w/2, iters, w, label='итераций до сходимости', color='#C44E52')
    ax.set_xticks(x)
    ax.set_xticklabels(opts)
    ax.set_ylabel('Время, с')
    ax2.set_ylabel('Число итераций')
    ax.set_title('Стоимость: GD vs Newton')
    fig.tight_layout()
    path = os.path.join(out_dir, 'optimizer_compare.png')
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f'  saved {path}')
    return results


def plot_grid_heatmap(df_results, out_dir='plots'):
    """Heatmap F1 для GD по сетке lr × n_iter."""
    os.makedirs(out_dir, exist_ok=True)
    gd = df_results[df_results['optimizer'] == 'gd']
    if gd.empty:
        return
    pivot = gd.pivot_table(index='lr', columns='n_iter', values='test_f1')
    fig, ax = plt.subplots(figsize=(9, 4.5))
    im = ax.imshow(pivot.values, cmap='viridis', aspect='auto')
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_yticks(range(len(pivot.index)))
    ax.set_xticklabels([str(c) for c in pivot.columns])
    ax.set_yticklabels([str(i) for i in pivot.index])
    ax.set_xlabel('n_iterations')
    ax.set_ylabel('learning_rate')
    ax.set_title('F1 на тесте (GD): lr × n_iter')
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            v = pivot.values[i, j]
            if not np.isnan(v):
                ax.text(j, i, f'{v:.3f}', ha='center', va='center',
                        color='white' if v < pivot.values[~np.isnan(pivot.values)].mean() else 'black',
                        fontsize=8)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    path = os.path.join(out_dir, 'grid_heatmap.png')
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f'  saved {path}')
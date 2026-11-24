# stats_plots.py
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # чтобы работало без GUI
import matplotlib.pyplot as plt


def print_describe(df, title=''):
    print(f'\n=== Описательные статистики {title} ===')
    desc = df.describe().T
    pd.set_option('display.width', 200)
    pd.set_option('display.max_columns', 20)
    print(desc[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']].round(3))


def plot_class_balance(y, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    counts = pd.Series(y).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(['0 (нет диабета)', '1 (диабет)'], counts.values,
                  color=['#4C72B0', '#C44E52'])
    for b, v in zip(bars, counts.values):
        ax.text(b.get_x() + b.get_width() / 2, v + 3, str(v),
                ha='center', fontsize=11)
    ax.set_ylabel('Количество')
    ax.set_title('Баланс классов')
    ax.set_ylim(0, counts.max() * 1.15)
    fig.tight_layout()
    path = os.path.join(out_dir, 'class_balance.png')
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f'  saved {path}')


def plot_histograms(df, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    num_cols = [c for c in num_cols if c != 'Outcome']
    n = len(num_cols)
    ncols = 3
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows))
    axes = axes.flatten()
    for i, col in enumerate(num_cols):
        ax = axes[i]
        data = df[col].dropna()
        ax.hist(data, bins=30, color='#4C72B0', edgecolor='white')
        ax.set_title(col, fontsize=10)
        ax.grid(alpha=0.3)
    for j in range(len(num_cols), len(axes)):
        axes[j].axis('off')
    fig.suptitle('Распределения признаков', fontsize=13)
    fig.tight_layout()
    path = os.path.join(out_dir, 'histograms.png')
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f'  saved {path}')


def plot_boxplots_by_class(df, out_dir):
    """Боксплоты признаков в разрезе классов — видно, какие разделяют."""
    os.makedirs(out_dir, exist_ok=True)
    num_cols = [c for c in df.select_dtypes(include=[np.number]).columns
                if c != 'Outcome']
    n = len(num_cols)
    ncols = 3
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows))
    axes = axes.flatten()
    for i, col in enumerate(num_cols):
        ax = axes[i]
        data0 = df.loc[df['Outcome'] == 0, col].dropna()
        data1 = df.loc[df['Outcome'] == 1, col].dropna()
        ax.boxplot([data0, data1], labels=['0', '1'])
        ax.set_title(col, fontsize=10)
        ax.grid(alpha=0.3)
    for j in range(len(num_cols), len(axes)):
        axes[j].axis('off')
    fig.suptitle('Признаки по классам (Outcome)', fontsize=13)
    fig.tight_layout()
    path = os.path.join(out_dir, 'boxplots_by_class.png')
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f'  saved {path}')


def plot_correlation(df, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    corr = df.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(corr.values, cmap='coolwarm', vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(corr.columns, fontsize=9)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f'{corr.values[i, j]:.2f}',
                    ha='center', va='center', fontsize=7,
                    color='black' if abs(corr.values[i, j]) < 0.6 else 'white')
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title('Корреляционная матрица')
    fig.tight_layout()
    path = os.path.join(out_dir, 'correlation.png')
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f'  saved {path}')
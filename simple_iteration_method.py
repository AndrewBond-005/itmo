def solve(m, vector, n, eps):
    mat = [[0 for j in range(n)] for i in range(n)]
    mxv = [0 for i in range(n)]
    mxi = [[] for i in range(n)]
    sumr = [0 for i in range(n)]
    ind = []
    doub_ind = []
    greaterstrict = 0

    # найти макс элем
    for i in range(0, n):
        for j in range(0, n):
            abs_val = abs(m[i][j])
            sumr[i] += abs_val
            if abs_val > mxv[i]:
                mxv[i] = abs_val
                mxi[i] = [j]
            elif abs_val == mxv[i]:
                mxi[i].append(j)
        if sumr[i] - mxv[i] < mxv[i]:
            greaterstrict += 1
        if sumr[i] - mxv[i] > mxv[i]:
            return (f"Диагонального преобладания невозможно достичь потому что "
                    f"в строке {i + 1} максимальное по модулю число меньше суммы всех остальных чисел строки по модулю")
        if len(mxi[i]) == 1:
            if mxi[i][0] in ind:
                return (f"Диагонального преобладания невозможно достичь потому что "
                        f"на месте {mxi[i][0]} должны стоять одновременно две или более строки")
            ind.append(mxi[i][0])
        else:
            doub_ind.append(mxi[i])
            ind.append(-1)
    if greaterstrict == 0:
        return (f"Диагонального преобладания невозможно достичь потому что "
                f"нет строки в которой максимальный элемент был бы строго больше суммы остальных")

    if len(doub_ind) != 0:
        size = len(doub_ind)
        k = 0
        num = 1
        while (k < size):
            k += 1
            num *= 2
        for i in range(0, num):
            comb = [0] * size
            tmp = i
            k = 0
            while (tmp > 0):
                comb[k] = (tmp % 2)
                tmp = tmp // 2
                k += 1
            ans = []
            err = 0
            for i in range(0, size):
                if doub_ind[i][comb[i]] in ans or doub_ind[i][comb[i]] in ind:
                    err = 1
                    break
                else:
                    ans.append(doub_ind[i][comb[i]])
            if err == 0:
                idx = 0
                for j in range(0, n):
                    if (ind[j] == -1):
                        ind[j] = ans[idx]
                        idx += 1
                break
    # перестановка строк
    ans = [[] for i in range(n)]
    v = vector.copy()
    for i in range(0, n):
        ans[ind[i]] = m[i]
        vector[ind[i]] = v[i]
    mx = [mxv[ind[i]] for i in range(n)]
    # матрица С
    C = [[] for i in range(n)]
    for i in range(0, n):
        for j in range(0, n):
            if i == j:
                C[i].append(0)
            else:
                C[i].append(-ans[i][j] / mx[i])

    # норма
    norm = 0
    for j in range(0, n):
        summ = 0
        for i in range(0, n):
            summ += abs(C[i][j])
        norm = max(norm, summ)
    v = [vector[i] / mx[i] for i in range(n)]
    xprev = [v[i] for i in range(n)]
    xcurr = [0 for i in range(n)]
    ans = simple_iteration_method(n, eps, v, C, xprev, xcurr)
    if type(ans) == str:
        return ans
    else:
        ans.append(norm)
        return ans


def simple_iteration_method(n, eps, v, C, xprev, xcurr):
    maxx = eps + 1
    cnt = 0
    # итерации
    while abs(maxx) >= eps and cnt <= 300:
        cnt += 1
        maxx = 0
        for i in range(0, n):
            xcurr[i] = v[i]
            for j in range(0, n):
                xcurr[i] += C[i][j] * xprev[j]
            maxx = max(abs(xcurr[i] - xprev[i]), maxx)
        if (abs(maxx) >= eps):
            xprev = xcurr.copy()
    if (cnt >= 150):
        return "Итерации расходятся"
    return [cnt, xcurr, [xcurr[i] - xprev[i] for i in range(n)]]

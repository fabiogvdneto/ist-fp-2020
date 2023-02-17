def sequencial_search(lst, e):
    for i in range(len(lst)):
        if e == lst[i]:
            return i
    return -1


# Requer que a lista seja ordenada.

def binary_search(lst, e):
    linf = 0
    lsup = len(lst) - 1

    while linf <= lsup:
        meio = (linf + lsup) // 2

        if e == lst[meio]:
            return meio
        if e > lst[meio]:
            linf = meio + 1
        else:
            lsup = meio - 1
    return -1

# BubbleSort
def bubble_sort(lst):
    limite = len(lst) - 1
    nenhuma_troca = False
    while not nenhuma_troca:
        nenhuma_troca = True
        for i in range(limite):
            if lst[i] > lst[i+1]:
                lst[i], lst[i+1] = lst[i+1], lst[i]
                nenhuma_troca = False
        limite = limite - 1
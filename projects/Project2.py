"""
Projeto: O Prado
Data: 19 out 2021 (pub) - 19 nov 2021 (entrega)
Autor: Fábio Neto (ist1104126)
Contacto: fabioneto03@hotmail.com

O segundo projeto de Fundamentos da Programação consiste em escrever um programa
em Python que simule o ecossistema de um prado em que convivem animais que se movi-
mentam, alimentam, reproduzem e morrem.
"""

from functools import reduce


#                           #
# FUNÇÕES AUXILIARES GERAIS #
#                           #

def eh_int_positivo(arg):
    """Recebe um argumento universal e retorna True apenas se este for um inteiro positivo."""
    return (type(arg) == int) and (arg > 0)


def eh_int_nao_negativo(arg):
    """Recebe um argumento universal e retorna True apenas se este for um inteiro não negativo."""
    return (type(arg) == int) and (arg >= 0)


def eh_str_nao_vazia(arg):
    """Recebe um argumento universal e retorna True apenas se este for uma cadeia de caracteres não vazia."""
    return (type(arg) == str) and (len(arg) > 0)


#             #
# TAD POSICAO #
#             #

# cria_posicao: int x int --> posicao
# cria_copia_posicao: posicao --> posicao
# obter_pos_x: posicao --> int
# obter_pos_y: posicao --> int
# eh_posicao: universal --> bool
# posicoes_iguais: posicao x posicao --> bool
# posicao_para_str: posicao --> str

def cria_posicao(x, y):
    """Recebe uma coordenada x não negativa (int) e uma coordenada y não negativa
    (int) e retorna um novo animal com estas características, gerando um ValueError
    caso os argumentos não sejam válidos."""
    if not (eh_int_nao_negativo(x) and eh_int_nao_negativo(y)):
        raise ValueError('cria_posicao: argumentos invalidos')

    # Uma posição é representada internamente por um tuplo com os seguintes elementos:
    # - coordenada x;
    # - coordenada y.
    return (x, y)


def cria_copia_posicao(pos):
    """Recebe uma posição e retorna a sua cópia, gerando um ValueError caso o
    argumento não seja válido."""
    if not eh_posicao(pos):
        raise ValueError('cria_copia_posicao: argumento invalido')

    # ints são imutáveis
    return (pos[0], pos[1])


def obter_pos_x(pos):
    """Recebe uma posição e retorna a sua componente x."""
    return pos[0]


def obter_pos_y(pos):
    """Recebe uma posição e retorna a sua componente y."""
    return pos[1]


def eh_posicao(arg):
    """Recebe um argumento universal e retorna True apenas se este for uma posição."""
    return (
        type(arg) == tuple
        and len(arg) == 2
        and all(eh_int_nao_negativo(e) for e in arg)
    )


def posicoes_iguais(pos1, pos2):
    """Retorna True apenas se pos1 e pos2 são posições e são iguais."""

    # Se pos1 for uma posição e pos1 == pos2, então pos2 também é uma posição.
    return (pos1 == pos2) and eh_posicao(pos1)


def posicao_para_str(pos):
    """
    Recebe uma posição e retorna a sua representação em str.
    A representação segue o formato '(x, y)', sendo x e y as coordenadas de pos.
    """
    return str(pos)


# Funções de alto nível (TAD posicao)

def obter_posicoes_adjacentes(pos):
    """Recebe uma posição e retorna um tuplo com as posições adjacentes a esta,
    ordenadas de acordo com o sentido horário a começar de cima."""
    res = ()
    x = obter_pos_x(pos)
    y = obter_pos_y(pos)

    if (y-1) >= 0:
        res += (cria_posicao(x, y-1),)

    res += (cria_posicao(x+1, y), cria_posicao(x, y+1))

    if (x-1) >= 0:
        res += (cria_posicao(x-1, y),)

    return res


def ordenar_posicoes(posicoes):
    """Recebe um tuplo de posições e retorna outro tuplo de igual tamanho, porém
    com as posições ordenadas de acordo com a ordem de leitura do prado."""
    return tuple(sorted(posicoes,
                        key=lambda p: (obter_pos_y(p), obter_pos_x(p))))


#            #
# TAD ANIMAL #
#            #

# cria_animal: str x int x int --> animal
# cria_copia_animal: animal --> animal
# obter_especie: animal --> str
# obter_freq_reproducao: animal --> int
# obter_freq_alimentacao: animal --> int
# obter_idade: animal --> int
# obter_fome: animal --> int
# aumenta_idade: animal --> animal
# reset_idade: animal --> animal
# aumenta_fome: animal --> animal
# reset_fome: animal --> animal
# eh_animal: universal --> bool
# eh_predador: universal --> bool
# eh_presa: universal --> bool
# animais_iguais: animal x animal --> bool
# animal_para_char: animal --> str
# animal_para_str: animal --> str

def cria_animal(esp, freq_reprod, freq_alim):
    """Recebe o nome de uma espécie (str), uma frequência de reprodução (int) e
    uma frequência de alimentação (int) e retorna um novo animal com estas
    características, gerando um ValueError caso os argumentos não sejam válidos."""
    if not (
        eh_str_nao_vazia(esp)
        and eh_int_positivo(freq_reprod)
        and eh_int_nao_negativo(freq_alim)
    ):
        raise ValueError('cria_animal: argumentos invalidos')

    # Os animais são representados internamente por um dicionário com as seguintes chaves:
    # - 'especie' com o nome da espécie (str);
    # - 'freq_reprod' com a frequência de reprodução (int);
    # - 'idade' com a idade (int).
    # Caso o animal seja um predador, as seguintes chaves também são usadas:
    # - 'freq_alim' com a frequência de alimentação (int);
    # - 'fome' com a fome (int).
    animal = {'especie': esp, 'freq_reprod': freq_reprod, 'idade': 0}

    if freq_alim > 0:
        animal.update({'freq_alim': freq_alim, 'fome': 0})

    return animal


def cria_copia_animal(animal):
    """Recebe um animal e retorna uma cópia sua, gerando um ValueError caso o
    argumento não seja válido."""
    if not eh_animal(animal):
        raise ValueError('cria_copia_animal: argumento invalido')

    # strings e integers são imutáveis.
    return animal.copy()


def obter_especie(animal):
    """Recebe um animal e retorna a str correspondente ao nome da sua espécie."""
    return animal.get('especie')


def obter_freq_reproducao(animal):
    """Recebe um animal e retorna o int correspondente à sua frequência de reprodução."""
    return animal.get('freq_reprod')


def obter_freq_alimentacao(animal):
    """Recebe um animal e retorna o int correspondente à sua frequência de
    alimentação, ou 0 se este for uma presa."""
    return animal.get('freq_alim', 0)


def obter_idade(animal):
    """Recebe um animal e retorna o int correspondente à sua idade."""
    return animal.get('idade')


def obter_fome(animal):
    """Recebe um animal e retorna o int correspondente à sua fome, ou 0 se este for uma presa."""
    return animal.get('fome', 0)


def aumenta_idade(animal):
    """Recebe um animal, incrementa a sua idade em 1 e retorna-o de seguida."""
    animal['idade'] += 1
    return animal


def reset_idade(animal):
    """Recebe um animal, redefine a sua idade para 0 e retorna-o de seguida."""
    animal['idade'] = 0
    return animal


def aumenta_fome(animal):
    """Recebe um animal, incrementa a sua idade em 1 caso este seja um predador e retorna-o de seguida."""
    if eh_predador(animal):
        animal['fome'] += 1

    return animal


def reset_fome(animal):
    """Recebe um animal, redefine a sua fome para 0 caso este seja um predador e retorna-o de seguida."""
    if eh_predador(animal):
        animal['fome'] = 0

    return animal


def eh_animal(arg):
    """Recebe um argumento universal e retorna True apenas se este for um animal."""
    return (
        type(arg) == dict
        and eh_str_nao_vazia(arg.get('especie'))
        and eh_int_nao_negativo(arg.get('idade'))
        and eh_int_positivo(arg.get('freq_reprod'))
        and (
            len(arg) == 3
            or (
                len(arg) == 5
                and eh_int_positivo(arg.get('freq_alim'))
                and eh_int_nao_negativo(arg.get('fome'))
            )
        )
    )


def eh_predador(arg):
    """Recebe um argumento universal e retorna True apenas se este for um predador."""
    return eh_animal(arg) and obter_freq_alimentacao(arg) > 0


def eh_presa(arg):
    """Recebe um argumento universal e retorna True apenas se este for uma presa."""
    return eh_animal(arg) and obter_freq_alimentacao(arg) == 0


def animais_iguais(a1, a2):
    """Retorna True apenas se a1 e a2 forem animais e forem iguais."""
    return (a1 == a2) and eh_animal(a1)


def animal_para_char(animal):
    """
    Recebe um animal e retorna o caractere que o representa (na forma de uma str).
    O caractere deverá corresponder à letra inicial do nome da espécie do animal,
    maiúscula no caso dos predadores e minúscula no caso das presas.
    """
    caractere = obter_especie(animal)[0]

    return caractere.upper() if eh_predador(animal) else caractere.lower()


def animal_para_str(animal):
    """
    Recebe um animal e retorna a respetiva representação em str.
    Formato da representação:
    - no caso das presas '{especie} [{idade}/{frequência de reprodução}]';
    - no caso dos predadores '{especie} [{idade}/{frequência de reprodução};{fome}/{frequência de alimentação}]'.
    """
    esp = obter_especie(animal)
    freq_reprod = obter_freq_reproducao(animal)
    idade = obter_idade(animal)

    if eh_presa(animal):
        return f'{esp} [{idade}/{freq_reprod}]'

    freq_alim = obter_freq_alimentacao(animal)
    fome = obter_fome(animal)

    return f'{esp} [{idade}/{freq_reprod};{fome}/{freq_alim}]'


# Funções de alto nível (TAD animal)

def eh_animal_fertil(animal):
    """Recebe um animal e retorna True apenas se este atingiu a idade de reprodução."""
    return obter_idade(animal) >= obter_freq_reproducao(animal)


def eh_animal_faminto(animal):
    """Recebe um animal e retorna True apenas se este for um predador que atingiu
    um valor de fome igual ou superior à sua frequência de alimentação."""
    return 0 < obter_freq_alimentacao(animal) <= obter_fome(animal)


def reproduz_animal(animal):
    """Recebe um animal, retornando outro da mesma espécie com idade e
    fome iguais a 0, e modificando destrutivamente o primeiro animal alterando a
    sua idade para 0, simulando assim o processo de reprodução."""
    return reset_fome(cria_copia_animal(reset_idade(animal)))


#           #
# TAD PRADO #
#           #

# cria_prado: posicao x tuple x tuple x tuple --> prado
# cria_copia_prado: prado --> prado
# obter_tamanho_x: prado --> int
# obter_tamanho_y: prado --> int
# obter_numero_predadores: prado --> int
# obter_numero_presas: prado --> int
# obter_posicao_animais: prado --> tuple
# obter_animal: prado, posicao --> animal
# eliminar_animal: prado x posicao --> prado
# mover_animal: prado x posicao x posicao --> prado
# inserir_animal: prado x animal x posicao --> prado
# eh_prado: universal --> bool
# eh_posicao_animal: prado x posicao --> bool
# eh_posicao_obstaculo: prado x posicao --> bool
# eh_posicao_livre: prado x posicao --> bool
# prados_iguais: prado x prado --> bool
# prado_para_str: prado --> str

def cria_prado(ultima_pos, rochedos_posicoes, animais, animais_posicoes):
    """Cria um prado com as características fornecidas.

    Args:
        ultima_pos (posicao): Última posição do prado, localizada no canto inferior
        direito do mapa.
        rochedos_posicoes (tuple): 0 ou mais posições correspondentes aos rochedos
        que não são as montanhas dos limites exteriores do prado.
        animais (tuple): 1 ou mais animais.
        animais_posicoes (tuple): Posições correspondentes ocupadas pelos animais.

    Raises:
        ValueError: Se os argumentos não forem válidos.

    Returns:
        animal: O prado criado.
    """
    if not (
        eh_posicao(ultima_pos)
        and type(rochedos_posicoes) == type(animais) == type(animais_posicoes) == tuple
        and len(animais) == len(animais_posicoes) > 0
        and all(eh_posicao(e) for e in rochedos_posicoes + animais_posicoes)
        and all(eh_animal(e) for e in animais)
    ):
        raise ValueError('cria_prado: argumentos invalidos')

    # Um prado é representado internamente por um tuplo com os seguintes elementos:
    # - um mapa (dicionário) que armazena todas as entidades presentes no prado,
    # em que as chaves correspondem a tuplos de duas coordenadas x e y e os valores
    # correspondem às entidades presentes nas respetivas posições (podem ser animais,
    # rochedos (representados por 'rochedo') ou montanhas (representadas por
    # 'montanha'));
    # - um tuplo de duas coordenadas x e y, correspondentes ao tamanho do prado.
    max_x = obter_pos_x(ultima_pos)
    max_y = obter_pos_y(ultima_pos)
    mapa = {}

    # É necessário transformar as posições em tuplos (x, y) pois apenas podemos
    # usar tipos imutáveis como chaves em dicionários e, sendo uma posição um
    # tipo abstrato, nós não sabemos se a estrutura de dados usada pela sua
    # implementação será mutável ou imutável.

    # Inserir montanhas em cima e em baixo (incluindo os cantos).
    for x in range(0, max_x+1):
        mapa[(x, 0)] = mapa[(x, max_y)] = 'montanha'

    # Inserir montanhas nas laterais (excluindo os cantos).
    for y in range(1, max_y):
        mapa[(0, y)] = mapa[(max_x, y)] = 'montanha'

    # Inserir os rochedos.
    for pos in rochedos_posicoes:
        x = obter_pos_x(pos)
        y = obter_pos_y(pos)

        if ((x, y) in mapa) or (x > max_x) or (y > max_y):
            raise ValueError('cria_prado: argumentos invalidos')

        mapa[(x, y)] = 'rochedo'

    # Inserir os animais.
    for e in zip(animais_posicoes, animais):
        x = obter_pos_x(e[0])
        y = obter_pos_y(e[0])

        if ((x, y) in mapa) or (x > max_x) or (y > max_y):
            raise ValueError('cria_prado: argumentos invalidos')

        mapa[(x, y)] = e[1]

    return (mapa, (max_x+1, max_y+1))


def cria_copia_prado(prado):
    """Recebe um prado e retorna uma cópia sua, gerando um ValueError se o argumento não for válido."""
    if not eh_prado(prado):
        raise ValueError('cria_copia_prado: argumento invalido')

    mapa_copia = prado[0].copy()

    for pos, entidade in mapa_copia.items():
        if eh_animal(entidade):
            mapa_copia[pos] = cria_copia_animal(entidade)

    return (mapa_copia, prado[1])


def obter_tamanho_x(prado):
    """Recebe um prado e retorna o int correspondente ao seu tamanho horizontal (x)."""
    return prado[1][0]


def obter_tamanho_y(prado):
    """Recebe um prado e retorna o int correspondente ao seu tamanho vertical (y)."""
    return prado[1][1]


def obter_numero_predadores(prado):
    """Recebe um prado e retorna o número de predadores existentes (int)."""
    # True = 1, False = 0
    return reduce(lambda res, e: res + eh_predador(e), prado[0].values(), 0)


def obter_numero_presas(prado):
    """Recebe um prado e retorna o número de presas existentes (int)."""
    # True = 1, False = 0
    return reduce(lambda res, e: res + eh_presa(e), prado[0].values(), 0)


def obter_posicao_animais(prado):
    """Recebe um prado e retorna um tuplo com todas as posições ocupadas por um animal."""
    res = tuple(
        cria_posicao(coords[0], coords[1])
        for coords, entidade in prado[0].items()
        if eh_animal(entidade)
    )

    return ordenar_posicoes(res)


def obter_animal(prado, pos):
    """Recebe um prado e uma posição e retorna o animal correspondente."""
    x = obter_pos_x(pos)
    y = obter_pos_y(pos)
    res = prado[0].get((x, y))
    return res if eh_animal(res) else None


def eliminar_animal(prado, pos):
    """Recebe um prado e uma posição, remove o animal correspondente e retorna o próprio prado."""
    x = obter_pos_x(pos)
    y = obter_pos_y(pos)
    del prado[0][(x, y)]
    return prado


def mover_animal(prado, pos_atual, pos_final):
    """
    Recebe um prado e duas posições, remove o animal da posição pos_atual e
    adiciona-o à posição pos_final (simulando movimento) e retorna o próprio prado."""
    x_atual = obter_pos_x(pos_atual)
    y_atual = obter_pos_y(pos_atual)
    x_final = obter_pos_x(pos_final)
    y_final = obter_pos_y(pos_final)
    prado[0][(x_final, y_final)] = prado[0].pop((x_atual, y_atual))
    return prado


def inserir_animal(prado, animal, pos):
    """
    Recebe um prado, um animal e uma posição, insere um prado na respetiva
    posição e retorna o próprio prado."""
    x = obter_pos_x(pos)
    y = obter_pos_y(pos)
    prado[0][(x, y)] = animal
    return prado


def eh_prado(arg):
    """Recebe um argumento universal e retorna True apenas se este for um prado."""

    def eh_mapa(arg):
        """Recebe um argumento universal e retorna True apenas se este
        corresponder a um mapa (usado na representação interna de um prado)."""
        return (
            type(arg) == dict
            and all(
                eh_animal(e)
                or e == 'rochedo'
                or e == 'montanha'
                for e in arg.values()
            )
            and all(
                type(e) == tuple
                and len(e) == 2
                and eh_int_nao_negativo(e[0])
                and eh_int_nao_negativo(e[1])
                for e in arg
            )
        )

    return (
        type(arg) == tuple
        and len(arg) == 2
        and eh_mapa(arg[0])
        and eh_posicao(arg[1])
    )


def eh_posicao_animal(prado, pos):
    """Recebe um prado e uma posição e retorna True apenas se esta for ocupada por um animal."""
    x = obter_pos_x(pos)
    y = obter_pos_y(pos)
    entidade = prado[0].get((x, y))
    return eh_animal(entidade)


def eh_posicao_obstaculo(prado, pos):
    """Recebe um prado e uma posição e retorna True apenas se esta for ocupada por obstáculo."""
    x = obter_pos_x(pos)
    y = obter_pos_y(pos)
    entidade = prado[0].get((x, y))
    return (entidade == 'montanha') or (entidade == 'rochedo')


def eh_posicao_livre(prado, pos):
    """Recebe um prado e uma posição e retorna True apenas se esta não estiver ocupada."""
    x = obter_pos_x(pos)
    y = obter_pos_y(pos)
    return (
        (x, y) not in prado[0]
        # Verificar se a posição está dentro dos limites do prado.
        and x < obter_tamanho_x(prado)
        and y < obter_tamanho_y(prado)
    )


def prados_iguais(prado1, prado2):
    """Retorna True apenas se prado1 e prado2 forem prados e forem iguais."""
    return (prado1 == prado2) and eh_prado(prado1)


def prado_para_str(prado):
    """
    Recebe um prado e retorna a respetiva representação em str.
    Os animais são representados com a letra inicial do nome da sua espécie,
    os rochedos são representados com '@', as posições vazias são representadas
    com '.' e os limites do prado, correspondentes às montanhas, são representados
    com '|' e '+'.
    """

    def posicao_para_char():
        """Retorna o caractere que representa uma determinada posição do prado."""
        if eh_posicao_livre(prado, pos):
            return '.'

        if eh_posicao_obstaculo(prado, pos):
            return '@'

        return animal_para_char(obter_animal(prado, pos))

    tam_x = obter_tamanho_x(prado)
    tam_y = obter_tamanho_y(prado)
    linha_extremo = '+' + ('-' * (tam_x - 2)) + '+'

    res = linha_extremo + '\n'

    for y in range(1, tam_y-1):
        res += '|'

        for x in range(1, tam_x-1):
            pos = cria_posicao(x, y)
            res += posicao_para_char()

        res += '|\n'

    return res + linha_extremo


# Funções de alto nível (TAD prado)

def obter_valor_numerico(prado, pos):
    """Recebe um prado e uma posição e retorna o respetivo valor numérico (int)."""
    return obter_pos_y(pos) * obter_tamanho_x(prado) + obter_pos_x(pos)


def obter_movimento(prado, pos):
    """Recebe um prado e uma posição e retorna a posição seguinte do respetivo
    animal, seguindo as regras de movimentação dos animais."""

    def calcula_indice(alts):
        """Recebe a lista de posições alternativas e retorna o índice dessa lista
        correspondente ao movimento."""
        return obter_valor_numerico(prado, pos) % len(alts)

    # alts = alternativas
    alts = obter_posicoes_adjacentes(pos)

    # Se o animal for predador, este deverá procurar por uma presa primeiro.
    if eh_predador(obter_animal(prado, pos)):
        alts_com_presas = [p for p in alts
                           if eh_posicao_animal(prado, p) and eh_presa(obter_animal(prado, p))]

        if len(alts_com_presas) > 0:
            return alts_com_presas[calcula_indice(alts_com_presas)]

    alts = [p for p in alts if eh_posicao_livre(prado, p)]

    if len(alts) == 0:
        return pos

    return pos if (len(alts) == 0) else alts[calcula_indice(alts)]


# Funções adicionais

def geracao(prado):
    """
    Recebe um prado.
    Avança 1 geração no prado, permitindo que cada animal (vivo) realize o seu
    turno de ação de acordo com regras específicas e seguindo a ordem de leitura
    do prado.
    O próprio prado é retornado.
    """
    # A cópia do prado serve para evitar que alguns animais eventualmente
    # repitam o seu turno. Isto poderia acontecer caso, por exemplo, um
    # animal se movesse para baixo, devido à ordem de leitura do prado.
    # Esta cópia não será modificada.
    prado_copia = cria_copia_prado(prado)

    for pos in ordenar_posicoes(obter_posicao_animais(prado)):
        animal = obter_animal(prado, pos)

        # Precisamos de verificar se o animal que encontrámos é o mesmo animal
        # que se encontra na cópia do prado.
        # Esta verificação é necessária pois pode ter acontecido, por exemplo,
        # de uma presa ter sido comida por um predador, e nós não queremos
        # que o predador repita o seu turno.
        if not animais_iguais(animal, obter_animal(prado_copia, pos)):
            continue

        aumenta_idade(aumenta_fome(animal))

        pos_nova = obter_movimento(prado, pos)

        if not posicoes_iguais(pos, pos_nova):
            if eh_posicao_animal(prado, pos_nova) and eh_presa(obter_animal(prado, pos_nova)):
                # Simulação de ataque por parte do predador (a presa será
                # eliminada quando o animal se mover).
                reset_fome(animal)

            mover_animal(prado, pos, pos_nova)

            if (eh_animal_fertil(animal)):
                # Simulação de reprodução.
                inserir_animal(prado, reproduz_animal(animal), pos)

        if (eh_animal_faminto(animal)):
            eliminar_animal(prado, pos_nova)  # Simulação da morte.

    return prado


def __imprimir_geracao(prado, gera):
    """Recebe um prado e um inteiro correspondente à geração atual do prado e imprime a respetiva informação."""
    presas = obter_numero_presas(prado)
    predad = obter_numero_predadores(prado)
    print(f'Predadores: {predad} vs Presas: {presas} (Gen. {gera})\n' +
          prado_para_str(prado))


def simula_ecossistema(ficheiro_nome, num_de_gera, modo_verboso):
    """Simulação de um ecossistema baseado nas informações contidas num dado ficheiro.
    Recebe o nome de um ficheiro (str), um int correspondente ao número de gerações
    a simular e um bool que indica se o modo verboso deverá ser ativado ou não e
    retorna um tuple de dois elementos com o número de predadores (int) e o número
    de presas (int) que sobraram na última geração."""
    with open(ficheiro_nome, 'r') as ficheiro:
        linha1 = eval(ficheiro.readline())
        linha2 = eval(ficheiro.readline())

        ultima_pos = cria_posicao(linha1[0], linha1[1])
        rochedos_posicoes = tuple(cria_posicao(e[0], e[1]) for e in linha2)

        animais = posicoes_animais = ()

        for linha in ficheiro.readlines():
            linha = eval(linha)
            animais += (cria_animal(linha[0], linha[1], linha[2]),)
            posicoes_animais += (cria_posicao(linha[3][0], linha[3][1]),)

        prado = cria_prado(ultima_pos, rochedos_posicoes,
                           animais, posicoes_animais)

    __imprimir_geracao(prado, 0)

    if modo_verboso:
        presas_gera_anterior = obter_numero_presas(prado)
        predad_gera_anterior = obter_numero_predadores(prado)

        for gera in range(1, num_de_gera+1):
            geracao(prado)

            presas = obter_numero_presas(prado)
            predad = obter_numero_predadores(prado)

            if (presas != presas_gera_anterior) or (predad != predad_gera_anterior):
                __imprimir_geracao(prado, gera)

            predad_gera_anterior, presas_gera_anterior = predad, presas

    else:
        for gera in range(1, num_de_gera+1):
            geracao(prado)

        __imprimir_geracao(prado, num_de_gera)

    return (obter_numero_predadores(prado), obter_numero_presas(prado))

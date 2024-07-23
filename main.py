"""
Projeto: Buggy Data Base (BDB)
Data: 15 out 2021 (pub) - 5 nov 2021 (entrega)
Autor: Fábio Neto (ist1104126)
Contacto: fabioneto03@hotmail.com

Descrição: Neste primeiro projeto de Fundamentos da Programação os alunos irão desenvolver
as funções que permitam resolver cinco tarefas independentes para identificar e corrigir
os problemas de uma base de dados (Buggy Data Base, BDB) que ficou corrompida por
causas desconhecidas. A BDB contem a informação de autenticação dos utilizadores de
um sistema e está a recusar erradamente o acesso de alguns dos utilizadores registados.
As tarefas consistirão em: 1) Correção da documentação; 2) Descoberta do PIN da
base de dados; 3) Verificação da coerência dos dados; 4) Desencriptação do conteúdo; e
5) Depuração de senhas.
"""


# Tarefa 1: Correção da documentação

# 1.2.1

def corrigir_palavra(palavra):
    """Corrige a palavra potencialmente modificada por um surto de letras.

    Args:
        palavra (str): A palavra potencialmente modificada por um surto de letras.

    Returns:
        [type]: A palavra corrigida.
    """
    if len(palavra) < 2:
        return palavra

    letras = list(palavra)

    i = 0
    while i < (len(letras) - 1):
        caractere = letras[i]

        if caractere.isalpha() and caractere.swapcase() == letras[i+1]:
            del letras[i]
            del letras[i]
            if i != 0:
                i -= 1
        else:
            i += 1

    return ''.join(letras)


# 1.2.2

def eh_anagrama(palavra, anagrama):
    """Verifica se a segunda palavra é anagrama da primeira.

    Args:
        palavra (str): Uma palavra.
        anagrama (str): Outra palavra, possível anagrama da primeira.

    Returns:
        bool: True apenas se uma palavra for anagrama da outra.
    """
    if len(palavra) != len(anagrama):
        return False

    palavra = palavra.lower()
    anagrama = anagrama.lower()

    letras = list(palavra)

    for letra in anagrama:
        if letra not in letras:
            return False

        letras.remove(letra)

    return True


# 1.2.3

def __corrigir_palavras(palavras):
    for i in range(len(palavras)-1, -1, -1):
        palavra = corrigir_palavra(palavras[i])

        if palavra == '':
            del palavras[i]
        else:
            palavras[i] = palavra


def __remover_anagramas(palavras):
    i = 0
    while i < len(palavras):
        for i1 in range(len(palavras)-1, i, -1):
            p = palavras[i].lower()
            p1 = palavras[i1].lower()
            if (p != p1) and eh_anagrama(p, p1):
                del palavras[i1]
        i += 1


def corrigir_doc(txt):
    """Corrige o texto potencialmente modificado por um surto de letras.

    Args:
        txt (str): O texto potencialmente modificado por um surto de letras.

    Raises:
        ValueError: Se o argumento fornecido for inválido.

    Returns:
        str: O texto corrigido.
    """
    if not (type(txt) == str and len(txt) > 0):
        raise ValueError('corrigir_doc: argumento invalido')

    palavras = txt.split(' ')

    if not all(e.isalpha() for e in palavras):
        raise ValueError('corrigir_doc: argumento invalido')

    __corrigir_palavras(palavras)
    __remover_anagramas(palavras)

    return ' '.join(palavras)


# Tarefa 2: Descoberta do PIN

# 2.2.1

def __mover_para_cima(pos):
    # Alternativa: return pos if pos < 4 else (pos - 3)
    return pos if pos in (1, 2, 3) else (pos - 3)


def __mover_para_baixo(pos):
    # Alternativa: return pos if pos > 6 else (pos + 3)
    return pos if pos in (7, 8, 9) else (pos + 3)


def __mover_para_esquerda(pos):
    # Alternativa: return pos if (pos - 1) % 3 == 0 else (pos - 1)
    return pos if pos in (1, 4, 7) else (pos - 1)


def __mover_para_direita(pos):
    # Alternativa: return pos if pos % 3 == 0 else (pos + 1)
    return pos if pos in (3, 6, 9) else (pos + 1)


def obter_posicao(movimento, pos):
    """Calcula a nova posição de acordo com o movimento fornecido.

    Args:
        movimento (str): O movimento (caracteres válidos: 'C', 'B', 'E' e 'D').
        pos (int): A posição a partir da qual o movimento será aplicado.

    Returns:
        int: A nova posição.
    """
    if movimento == 'C':
        return __mover_para_cima(pos)

    if movimento == 'B':
        return __mover_para_baixo(pos)

    if movimento == 'E':
        return __mover_para_esquerda(pos)

    if movimento == 'D':
        return __mover_para_direita(pos)

    return pos


# 2.2.2

def obter_digito(movimentos, pos):
    """Calcula o dígito do pin a partir dos movimentos fornecidos e iniciando na posicao fornecida.

    Args:
        movimentos (str): A sequência de movimentos a seguir (caracteres válidos: 'C', 'B', 'E' e 'D').
        pos (int): A posição a partir da qual os movimentos serão aplicados.

    Returns:
        int: O dígito (ou seja, a posicao final)
    """
    for m in movimentos:
        pos = obter_posicao(m, pos)
    return pos


# 2.2.3

def __validar_movimento(caractere):
    return caractere in ('C', 'B', 'E', 'D')


def __validar_movimentos(movimentos):
    return (
        type(movimentos) == str
        and len(movimentos) > 0
        and all(__validar_movimento(e) for e in movimentos)
    )


def __validar_sequencia_de_movimentos(sequencia_de_movimentos):
    return (
        type(sequencia_de_movimentos) == tuple
        and 3 < len(sequencia_de_movimentos) < 11
        and all(__validar_movimentos(e) for e in sequencia_de_movimentos)
    )


def obter_pin(sequencia_de_movimentos):
    """Calcula o pin a partir das sequências de movimentos fornecidas, em que cada sequência equivale a um dígito.

    Args:
        sequencia_de_movimentos (tuple): Entre 4 a 10 (inclusive) sequências de movimentos.

    Raises:
        ValueError: Se o argumento fornecido for inválido.

    Returns:
        tuple: O pin (tuplo contendo x elementos em que cada elemento corresponde a um dígito).
    """
    if not __validar_sequencia_de_movimentos(sequencia_de_movimentos):
        raise ValueError('obter_pin: argumento invalido')

    pos = 5
    pin = ()

    for m in sequencia_de_movimentos:
        pos = obter_digito(m, pos)
        pin += (pos,)

    return pin


# Tarefa 3: Verificação de dados

# 3.2.1 (e 4.2.1)

def __eh_cifra(cifra):
    return (
        type(cifra) == str
        and all(e.isalpha() and e.islower() for e in cifra.split('-'))
    )


def __eh_checksum(checksum):
    if not (
        type(checksum) == str
        and len(checksum) == 7
        and checksum.startswith('[')
        and checksum.endswith(']')
    ):
        return False

    # Remove os parênteses para que possamos validar os caracteres entre estes.
    checksum = checksum[1:6]

    return checksum.isalpha() and checksum.islower()


def __eh_sequencia_de_seguranca(sequencia):
    return (
        type(sequencia) == tuple
        and len(sequencia) > 1
        and all(type(e) == int and (e > 0) for e in sequencia)
    )


def eh_entrada(entrada):
    """Verifica se o objeto fornecido corresponde a uma entrada na BDB.

    Args:
        entrada: A possível entrada.

    Returns:
        bool: True apenas se o argumento fornecido corresponder a uma entrada na BDB.
    """
    return (
        type(entrada) == tuple
        and len(entrada) == 3
        and __eh_cifra(entrada[0])
        and __eh_checksum(entrada[1])
        and __eh_sequencia_de_seguranca(entrada[2])
    )


# 3.2.2

# As funções __obter_checksum e __obter_checksum_sem_lambda produzem um resultado equivalente, porém
# a primeira faz uso de funções lambda (para que possa usufuir da função built-in do python, sorted()).
# A segunda é uma função mais complexa pois toda a ordenação é feita manualmente, e deverá ser menos
# eficiente.
def __obter_checksum(cifra):
    letras = {}

    for caractere in cifra:
        if caractere.isalpha():
            letras[caractere] = letras.get(caractere, 0) + 1

    if len(letras) < 5:
        return None

    # Sendo e[0] um caractere e e[1] o número de ocorrências do mesmo na cifra:
    # 10 - e[1] é usado pois nós queremos ordenar do maior numero para o menor.
    # Este numero é transformado em uma string para que possa ser concatenado.
    # e[0] é adicionado para que, caso haja um empate, a ordenação possa ocorrer de forma alfabética.
    letras = sorted(letras.items(), key=lambda e: (-e[1], e[0]))

    del letras[5:]  # Apenas as primeiras 5 letras são importantes.

    letras = [e[0] for e in letras]
    letras = ''.join(letras)

    return '[' + letras + ']'


def __obter_checksum_sem_lambda(cifra):
    letras = {}  # dicionário caractere/num de ocorrencias
    palavras = cifra.split('-')
    for palavra in palavras:
        for caractere1 in palavra:
            letras[caractere1] = letras.get(caractere1, 0) + 1

    checksum = []

    for caractere, ocorrencias in letras.items():
        for i in range(len(checksum)):
            caractere1 = checksum[i]
            ocorrencias1 = letras.get(caractere1)

            if (
                (ocorrencias > ocorrencias1)
                or (ocorrencias == ocorrencias1 and caractere < caractere1)
            ):
                checksum.insert(i, caractere)
                break
        else:
            checksum.append(caractere)

    del checksum[5:]

    checksum = ''.join(checksum)

    return '[' + checksum + ']'


def validar_cifra(cifra, checksum):
    """Valida a cifra fornecida.

    Args:
        cifra (str): A cifra.
        checksum (str): O checksum correspondente.

    Returns:
        bool: True apenas se a cifra for válida.
    """
    return checksum == __obter_checksum(cifra)


# 3.2.3

def filtrar_bdb(entradas):
    """Filtra as entradas que não têm uma cifra válida.

    Args:
        entradas (list): As entradas da BDB.

    Raises:
        ValueError: Se o argumento fornecido for inválido.

    Returns:
        list: As entradas da BDB cuja cifra é inválida.
    """
    if not (
        type(entradas) == list
        and len(entradas) > 0
        and all(eh_entrada(e) for e in entradas)
    ):
        raise ValueError('filtrar_bdb: argumento invalido')

    return [e for e in entradas if not validar_cifra(e[0], e[1])]


# Tarefa 4: Desencriptação do conteúdo

# 4.2.2

def obter_num_seguranca(sequencia_de_seguranca):
    """Calcula o número de segurança.

    Args:
        sequencia_de_seguranca (tuple): A sequência de seguranca.

    Returns:
        int: O número de segurança.
    """
    num_de_seguranca = max(sequencia_de_seguranca)

    for minuendo in sequencia_de_seguranca:
        for subtraendo in sequencia_de_seguranca:
            resto = minuendo - subtraendo

            if (resto > 0) and (resto < num_de_seguranca):
                num_de_seguranca = resto

    return num_de_seguranca


# 4.2.3

def __deslocar_caractere(caractere, deslocamento):
    return chr(ord('a') + (ord(caractere) - ord('a') + deslocamento) % 26)


def decifrar_texto(txt, num_de_seguranca):
    """Decifra o texto "escondido" pela cifra de acordo com o número de segurança.

    Args:
        txt (str): A cifra.
        num_de_seguranca (int): O numero de segurança.

    Returns:
        str: O texto decifrado.
    """
    res = []

    # Existem um total de 26 letras no alfabeto (a-z ou A-Z), por isso, se
    # avançarmos um total de 27 posições será o mesmo que avançarmos apenas 1.
    num_de_seguranca %= 26

    for i in range(len(txt)):
        c = txt[i]

        if c == '-':
            c = ' '
        else:
            deslocamento = num_de_seguranca

            if i % 2 == 0:
                deslocamento += 1
            else:
                deslocamento -= 1

            c = __deslocar_caractere(c, deslocamento)

        res.append(c)

    return ''.join(res)


# 4.2.4

def decifrar_bdb(entradas):
    """Decifra todas as entradas.

    Args:
        entradas (list): As entradas da BDB.

    Raises:
        ValueError: Se o argumento fornecido nao for válido.

    Returns:
        list: Os textos decifrados correspondentes às entradas fornecidas, ordenados de igual forma.
    """
    if not (
        type(entradas) == list
        and len(entradas) > 0
        and all(eh_entrada(e) for e in entradas)
    ):
        raise ValueError('decifrar_bdb: argumento invalido')

    return [decifrar_texto(e[0], obter_num_seguranca(e[2])) for e in entradas]


# Tarefa 5: Depuração de senhas

# 5.2.1

def __eh_nome_de_usuario(name):
    return type(name) == str and len(name) > 0


def __eh_senha(psswrd):
    return type(psswrd) == str and len(psswrd) > 0


def __eh_regra(rule):
    if not (type(rule) == dict and len(rule) == 2):
        return False

    vals = rule.get('vals')

    if not (type(vals) == tuple and len(vals) == 2):
        return False

    val0, val1 = vals

    if not (type(val0) == type(val1) == int and (val1 >= val0 > 0)):
        return False

    char = rule.get('char')

    return type(char) == str and len(char) == 1 and char[0].islower()


def eh_utilizador(info):
    """Verifica se o utilizador fornecido corresponde a informação relevante de um utilizador da BDB.

    Args:
        info: A informação de um possível utilizador.

    Returns:
        bool: True apenas se o argumento fornecido corresponde a informação relevante de um utilizador da BDB.
    """
    return (
        type(info) == dict
        and len(info) == 3
        and __eh_nome_de_usuario(info.get('name'))
        and __eh_senha(info.get('pass'))
        and __eh_regra(info.get('rule'))
    )


# 5.2.2

def __contem_tres_vogais_minusculas(texto):
    codigos = (97, 101, 105, 111, 117)
    encontrado = 0

    for c in texto:
        if ord(c) in codigos:
            encontrado += 1

            if encontrado == 3:
                return True

    return False


def __contem_dois_caracteres_iguais_consecutivos(texto):
    return any(texto[i] == texto[i + 1] for i in range(len(texto) - 1))


def __contar(obj, iteravel):
    encontrado = 0

    for e in iteravel:
        if e == obj:
            encontrado += 1

    return encontrado


def eh_senha_valida(senha, regra):
    """Verifica se a senha fornecida é valida, isto é, se esta cumpre com todas as regras de definição (gerais e individual).

    Args:
        senha (str): A senha.
        regra (tuple): A regra individual.

    Returns:
        bool: True apenas se a senha fornecida é válida.
    """
    # Regras Globais
    if not (
        __contem_tres_vogais_minusculas(senha)
        and __contem_dois_caracteres_iguais_consecutivos(senha)
    ):
        return False

    # Regra individual
    vals, char = regra['vals'], regra['char']
    encontrado = __contar(char, senha)
    return vals[0] <= encontrado <= vals[1]


# 5.2.3

def filtrar_senhas(infos):
    """Filtra os utilizadores com senha errada e ordena-os alfabeticamente.

    Args:
        infos (list): As informações de utilizadores.

    Raises:
        ValueError: Se o argumento fornecido for inválido.

    Returns:
        list: Os nomes dos utilizadores cuja senha é inválida, ordenados alfabeticamente.
    """
    if not (
        type(infos) == list
        and len(infos) > 0
        and all(eh_utilizador(e) for e in infos)
    ):
        raise ValueError('filtrar_senhas: argumento invalido')

    usuarios = [e['name'] for e in infos
                if not eh_senha_valida(e['pass'], e['rule'])]
    usuarios.sort()

    return usuarios

# CONSTANTES DO SISTEMA

COMBUSTIVEL_MIN = 30  # % mínimo de combustível para pousar
VENTO_OK = 15  # vento máximo para atmosfera aceitável (m/s)
VENTO_TEMPESTADE = 25  # acima disso é tempestade severa (m/s)
PRIORIDADE_ALTA = 4  # prioridade 4 ou 5 é considerada alta
CONSUMO_ESPERA = 4  # combustível gasto ao esperar uma janela


def novo(
    codigo, tipo, prioridade, combustivel, massa, criticidade, chegada, sensores=True
):
    """Monta um módulo. Um dicionário guarda todos os atributos dele."""
    return {
        "codigo": codigo,
        "tipo": tipo,
        "prioridade": prioridade,
        "combustivel": combustivel,
        "massa": massa,
        "criticidade": criticidade,
        "chegada": chegada,
        "sensores": sensores,
    }


# DADOS DOS MÓDULOS

modulos = [
    novo("HAB-01", "Habitação", 4, 33, 8500, 4, "06:10"),
    novo("HAB-02", "Habitação", 4, 41, 7800, 4, "06:15"),
    novo("HAB-03", "Habitação", 3, 37, 6400, 3, "07:10"),
    novo("HAB-04", "Habitação", 5, 55, 7100, 5, "06:20"),
    novo("ENE-01", "Energia", 5, 62, 6200, 5, "06:25"),
    novo("ENE-02", "Energia", 4, 58, 4900, 4, "06:30"),
    novo("ENE-03", "Energia", 5, 60, 5700, 5, "06:35"),
    novo("ENE-04", "Energia", 3, 44, 8200, 4, "07:15", sensores=False),
    novo("LAB-01", "Laboratório", 2, 48, 5400, 2, "06:40", sensores=False),
    novo("LAB-02", "Laboratório", 2, 46, 5100, 2, "07:20"),
    novo("LAB-03", "Laboratório", 1, 39, 4600, 1, "07:30"),
    novo("LOG-01", "Logística", 3, 35, 9800, 3, "07:05"),
    novo("LOG-02", "Logística", 3, 34, 9200, 3, "07:00"),
    novo("LOG-03", "Logística", 4, 70, 10500, 4, "06:50"),
    novo("LOG-04", "Logística", 2, 36, 6800, 2, "07:25"),
    novo("MED-01", "Suporte médico", 4, 48, 3200, 5, "06:55"),
    novo("MED-02", "Suporte médico", 5, 52, 3600, 5, "06:45"),
    novo("MED-03", "Suporte médico", 3, 45, 2800, 4, "07:35"),
]


# ESTRUTURAS LINEARES DO SISTEMA

fila = []  # Fila de módulos aguardando autorização
espera = []  # Módulos adiados na janela atual
pousados = []  # Módulos que já pousaram
alerta = []  # Módulos com problemas
historico = []  # Pilha de registros dos eventos

for m in modulos:
    fila.append(m)


# FUNÇÕES DE BUSCA


def menor_combustivel(lista):
    """Busca o módulo com a menor quantidade de combustível."""
    menor = lista[0]

    for m in lista:
        if m["combustivel"] < menor["combustivel"]:
            menor = m

    return menor


def maior_prioridade(lista):
    """Busca o módulo com a maior prioridade."""
    maior = lista[0]

    for m in lista:
        if m["prioridade"] > maior["prioridade"]:
            maior = m

    return maior


def buscar_tipo(lista, tipo):
    """Devolve todos os módulos de um determinado tipo."""
    achados = []

    for m in lista:
        if m["tipo"] == tipo:
            achados.append(m)

    return achados


def busca_binaria(lista, horario):
    """Busca um módulo pelo horário de chegada.
    A lista precisa estar ordenada pelo horário.
    """
    inicio = 0
    fim = len(lista) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2

        if lista[meio]["chegada"] == horario:
            return lista[meio]

        elif lista[meio]["chegada"] < horario:
            inicio = meio + 1

        else:
            fim = meio - 1

    return None


# ORDENAÇÃO: INSERTION SORT


def criterio_fila(m):
    """Define a ordem de prioridade dos módulos."""
    return (
        -m["prioridade"],
        -m["criticidade"],
        m["combustivel"],
        m["chegada"],
    )


def criterio_chegada(m):
    """Define a ordenação pelo horário de chegada."""
    return m["chegada"]


def ordenar(lista, criterio):
    """Ordena a lista utilizando o algoritmo insertion sort."""
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1

        while j >= 0 and criterio(lista[j]) > criterio(atual):
            lista[j + 1] = lista[j]
            j = j - 1

        lista[j + 1] = atual


# FUNÇÕES MATEMÁTICAS


def potencia_solar(hora):
    """Calcula a potência solar disponível em determinado horário."""
    return 20 * (1 - ((hora - 12) / 6) ** 2)


def pistas_livres(hora):
    """Calcula quantos pousos a energia consegue suportar."""
    sobra = potencia_solar(hora) - 6

    if sobra <= 0:
        return 0

    return int(sobra // 4)


def altura_ignicao(massa):
    """Calcula a altura de acionamento do retrofoguete."""
    a = 60000 / massa - 3.71

    return (80**2 - 2**2) / (2 * a)


# LÓGICA BOOLEANA


def pouso_normal(A, C, D, S):
    """N = C AND A AND D AND S"""
    return bool(C and A and D and S)


def pouso_emergencia(C, PA, T, D, S):
    """E = PA AND NOT C AND D AND S AND NOT T"""
    return bool(PA and (not C) and D and S and (not T))


def pouso_autorizado(A, C, PA, T, D, S):
    """P = N OR E"""
    return pouso_normal(A, C, D, S) or pouso_emergencia(C, PA, T, D, S)


def em_alerta(P, S, C):
    """ALERTA = NOT P AND (NOT S OR NOT C)"""
    return bool((not P) and ((not S) or (not C)))


def adiado(P, S, C):
    """ADIADO = NOT P AND S AND C"""
    return bool((not P) and S and C)


def decidir(m, vento, pistas):
    """Analisa os dados do módulo e decide se o pouso é autorizado."""

    C = m["combustivel"] >= COMBUSTIVEL_MIN
    A = vento <= VENTO_OK
    T = vento > VENTO_TEMPESTADE
    D = pistas > 0
    S = m["sensores"]
    PA = m["prioridade"] >= PRIORIDADE_ALTA

    P = pouso_autorizado(A, C, PA, T, D, S)

    if P:
        if pouso_normal(A, C, D, S):
            return "AUTORIZADO", "pouso normal"

        return "AUTORIZADO", "emergência (combustível baixo)"

    if em_alerta(P, S, C):
        if not S:
            return "ALERTA", "falha nos sensores"

        return "ALERTA", "combustível baixo"

    if not A:
        return "ADIADO", "vento alto"

    return "ADIADO", "sem pista livre"


def nomes(lista):
    """Retorna os códigos dos módulos de uma lista."""
    return [m["codigo"] for m in lista]


# PROGRAMA PRINCIPAL

print("=== BUSCAS ===")

print("Menor combustível:", menor_combustivel(fila)["codigo"])
print("Maior prioridade :", maior_prioridade(fila)["codigo"])
print("Cargas de energia:", nomes(buscar_tipo(fila, "Energia")))


# BUSCA BINÁRIA PELO HORÁRIO

por_horario = list(fila)
ordenar(por_horario, criterio_chegada)

achado = busca_binaria(por_horario, "06:40")

print("Quem chega às 06:40:", achado["codigo"] if achado else "ninguém")


# FILA ORDENADA POR PRIORIDADE

ordenar(fila, criterio_fila)

print("\n=== FILA ORDENADA POR PRIORIDADE ===")
print(nomes(fila))


# ALTURA DE ACIONAMENTO DO RETROFOGUETE

print("\n=== ALTURA PARA LIGAR O RETROFOGUETE (3 primeiros da fila) ===")

for m in fila[:3]:
    print(
        "%s (%d kg): %.0f m"
        % (
            m["codigo"],
            m["massa"],
            altura_ignicao(m["massa"]),
        )
    )


# JANELAS DE POUSO

janelas = [(9, 10), (11, 22), (13, 28), (15, 8)]

for numero, (hora, vento) in enumerate(janelas, start=1):

    pistas = pistas_livres(hora)

    print(
        "\n=== JANELA %d | %02d:00 | vento %d m/s | pistas livres: %d ==="
        % (numero, hora, vento, pistas)
    )

    ordenar(fila, criterio_fila)

    # Processa todos os módulos da fila
    while len(fila) > 0:

        m = fila.pop(0)

        decisao, motivo = decidir(m, vento, pistas)

        if decisao == "AUTORIZADO":
            pistas = pistas - 1
            pousados.append(m)

        elif decisao == "ALERTA":
            alerta.append(m)

        else:
            espera.append(m)

        historico.append("Janela %d: %s -> %s" % (numero, m["codigo"], decisao))

        print(
            "  %s  comb=%d%%  %s - %s"
            % (
                m["codigo"],
                m["combustivel"],
                decisao,
                motivo,
            )
        )

    # Módulos adiados gastam combustível e voltam para a fila
    for m in espera:
        m["combustivel"] = max(0, m["combustivel"] - CONSUMO_ESPERA)
        fila.append(m)

    espera.clear()

    # Módulos em alerta também gastam combustível
    for m in alerta:
        m["combustivel"] = max(0, m["combustivel"] - CONSUMO_ESPERA)


# RESULTADO FINAL

print("\n=== RESULTADO FINAL ===")

print(
    "Pousaram (%d de %d):" % (len(pousados), len(modulos)),
    nomes(pousados),
)

print("Seguem na fila:", nomes(fila))

print("Em alerta (precisam de atenção):", nomes(alerta))


# ÚLTIMOS EVENTOS DO HISTÓRICO

print("\nÚltimos 3 eventos da pilha (do mais recente para o mais antigo):")

for _ in range(min(3, len(historico))):
    print("  ", historico.pop())

# depositar valores positivos
# sacar valores positivos com limite de 3 saques diarios e limite maximo de R$500, registrar no extrato
# exibir o extrato com saldo

# NOVO DESAFIO
# Estabelecer um limite de 10 transações diárias para uma conta
# Se o usuário tentar fazer uma transação após atingir o limite, deve ser informado que ele excedeu o número de transações permitidas para aquele dia.
# Mostre no extrato, a data e hora de todas as transações.

import datetime as dt

saldo_atual = 2000
transacoes_diarias = 10
limite = 500
historico_transacoes = []
hora_atual = dt.datetime.now().strftime("%d/%m/%Y %H:%M")


def menu():
    global opcao
    opcao = int(
        input(
            f"""{"MENU".center(32, "=")}
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
=> """
        )
    )


def depositar(saldo, valor, max_transacoes, hora_transacao):
    if valor > 0 and max_transacoes > 0:
        historico_transacoes.append(f"+R${valor:.2f} - {hora_transacao}")
        saldo += valor
        print(
            f"\nDeposito de R${valor:.2f} realizado com sucesso.\nSaldo atual: R${saldo:.2f}"
        )
        global transacoes_diarias
        transacoes_diarias -= 1
        return valor
    elif max_transacoes == 0:
        print(f"\nERRO: Limite de transações diarias atingido.")
        return 0
    else:
        print("ERRO: Quantia invalida, tente novamente.\n")
        return 0


def sacar(saldo, valor, limite, max_transacoes, hora_transacao):
    if max_transacoes > 0 and valor <= limite and valor <= saldo and valor > 0:
        historico_transacoes.append(f"-R${valor:.2f} - {hora_transacao}")
        saldo -= valor
        print(
            f"\nSaque de R${valor:.2f} realizado com sucesso.\nSaldo atual: R${saldo:.2f}"
        )
        global transacoes_diarias
        transacoes_diarias -= 1
        return valor

    elif valor > saldo:
        print(f"\nERRO: Saldo insuficiente.")
        return 0
    elif valor > limite:
        print(f"\nERRO: Valor limite de saque de R${limite:.2f} excedido.")
        return 0
    elif max_transacoes == 0:
        print(f"\nERRO: Limite de transações diarias atingido.")
        return 0
    else:
        print("\nERRO: Quantia invalida, tente novamente.")
        return 0


def extrato(extrato):
    for transacao in extrato:
        print(transacao)
    print(f"\nSaldo atual: R${saldo_atual:.2f}")


while True:

    menu()

    match opcao:

        case 1:  # depositar
            valor = float(
                input(
                    f"{"DEPOSITO".center(32, "=")}\nDigite o valor a ser depositado: R$"
                )
            )
            deposito = depositar(saldo_atual, valor, transacoes_diarias, hora_atual)
            saldo_atual += deposito

        case 2:  # sacar
            valor = float(
                input(f"{"SAQUE".center(32, "=")}\nDigite o valor a ser sacado: R$")
            )
            saque = sacar(saldo_atual, valor, limite, transacoes_diarias, hora_atual)
            saldo_atual -= saque

        case 3:  # extrato
            print(f"{"EXTRATO".center(32, "=")}")
            extrato(historico_transacoes)
        case 0:  # sair
            print(
                f"""
{"SAIR".center(32, "=")}
Obrigado por utilizar nosso sistema.
Tenha um bom dia!
"""
            )
            break
        case _:  # opcao invalida
            print("\nERRO: Opcao invalida, tente novamente.")

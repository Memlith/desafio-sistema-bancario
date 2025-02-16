# depositar valores positivos
# sacar valores positivos com limite de 3 saques diarios e limite maximo de R$500, registrar no extrato
# exibir o extrato com saldo
saldo_atual = 2000
limite_saques = 3
limite = 500
extrato = []


def depositar(saldo, valor):
    if valor > 0:
        extrato.append(f"+R${valor:.2f}")
        saldo += valor
        print(
            f"\nDeposito de R${valor:.2f} realizado com sucesso.\nSaldo atual: R${saldo:.2f}"
        )
        return valor

    else:
        print("ERRO: Quantia invalida, tente novamente.\n")
        return 0


def sacar(saldo, valor, limite, max_saques):
    if max_saques > 0 and valor <= limite and valor <= saldo and valor > 0:
        extrato.append(f"-R${valor:.2f}")
        saldo -= valor
        print(
            f"\nSaque de R${valor:.2f} realizado com sucesso.\nSaldo atual: R${saldo:.2f}"
        )
        global limite_saques
        limite_saques -= 1
        return valor

    elif valor > saldo:
        print(f"\nERRO: Saldo insuficiente.")
        return 0
    elif valor > limite:
        print(f"\nERRO: Valor limite de saque de R${limite:.2f} excedido.")
        return 0
    elif max_saques == 0:
        print(f"\nERRO: Limite de saques diarios atingido.")
        return 0
    else:
        print("\nERRO: Quantia invalida, tente novamente.")
        return 0


while True:

    opcao = int(
        input(
            """================ MENU ================
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
=> """
        )
    )

    match opcao:

        case 1:  # depositar
            valor = float(
                input(
                    """
================ DEPOSITO ================
Digite o valor a ser depositado: R$"""
                )
            )
            deposito = depositar(saldo_atual, valor)
            saldo_atual += deposito

        case 2:  # sacar
            valor = float(
                input(
                    """
================ SAQUE ================
Digite o valor a ser sacado: R$"""
                )
            )
            saque = sacar(saldo_atual, valor, limite, limite_saques)
            saldo_atual -= saque

        case 3:  # extrato
            print(
                f"""
================ EXTRATO ================
Extrato: {extrato}
Saldo atual: R${saldo_atual:.2f}"""
            )

        case 0:  # sair
            print(
                """
================ SAIR ================
Obrigado por utilizar nosso sistema.
Tenha um bom dia!
"""
            )
            break
        case _:  # opcao invalida
            print("\nERRO: Opcao invalida, tente novamente.")

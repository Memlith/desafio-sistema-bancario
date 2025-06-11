from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = "1229"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self.saldo and valor < 0:
            print(
                f"\n{" Erro ao sacar, valor de saque excede saldo da conta. ".center(48, "*")}"
            )

        elif valor > 0:
            self._saldo -= valor
            print(
                f"\n{f" Saque de R$ {valor:.2f} feito com sucesso! ".center(48, "=")}"
            )
            return True

        else:
            print(f"\n{" Erro ao depositar, valor invalido. ".center(48, "*")}")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(
                f"\n{f" Deposito de R$ {valor:.2f} feito com sucesso! ".center(48, "=")}"
            )

        else:
            print(f"\n{" Erro ao depositar, valor invalido. ".center(48, "*")}")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, saldo, numero, limite=500, limite_saques=3):
        super().__init__(saldo, numero)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == "Saque"
            ]
        )

        if valor > self._limite:
            print(
                f"\n{" Erro ao sacar, valor excede limite da conta. ".center(48, "*")}"
            )
        elif numero_saques >= self._limite_saques:
            print(f"\n{" Erro ao sacar, limite de saques excedido. ".center(48, "*")}")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
AGÊNCIA:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
    """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
    menu = f"""\n{" MENU ".center(48, "=")}
    
[d]  Depositar
[s]  Sacar
[e]  Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuario
[q]  Sair
=> """
    return input(menu)


def filtrar_cliente(cpf, clientes):
    filtra_cliente = [cliente for cliente in clientes if cliente.cpf == cpf]
    return filtra_cliente[0] if filtra_cliente else None


def recupera_conta_cliente(cliente):
    if not cliente.contas:
        print(f"\n{" Cliente nao cadastrado! ".center(48, "*")}")
        return
    return cliente.contas[0]


def depositar(clientes):
    print(f"\n{" DEPOSITO ".center(48, "=")}")
    cpf = input("\nDigite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print(f"\n{" Cliente nao encontrado! ".center(48, "*")}")
        return
    valor = float(input("\nDigite o valor do deposito: "))
    transacao = Deposito(valor)
    conta = recupera_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    print(f"\n{" SAQUE ".center(48, "=")}")
    cpf = input("\nDigite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print(f"\n{" Cliente nao encontrado! ".center(48, "*")}")
        return
    valor = float(input("\nDigite o valor do saque: "))
    transacao = Saque(valor)
    conta = recupera_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    print(f"\n{" EXIBIR EXTRATO ".center(48, "=")}")
    cpf = input("\nDigite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print(f"\n{" Cliente nao encontrado! ".center(48, "*")}")
        return
    conta = recupera_conta_cliente(cliente)
    if not conta:
        return
    print(f"\n{" EXTRATO ".center(48, "=")}")
    transacoes = conta.historico.transacoes
    extrato = " "
    if not transacoes:
        extrato = "\nNão existem registros de extrato!"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\n R${transacao["valor"]:.2f}"
    print(extrato)
    print(f"\nSaldo:\n R${conta.saldo:.2f}")


def criar_cliente(clientes):
    print(f"\n{" CADASTRO CLIENTE ".center(48, "=")}")
    cpf = input("\nDigite o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print(f"\n{" Cliente ja existe! ".center(48, "*")}")
        return
    nome = input("Insira seu nome completo: ")
    data_nascimento = input("Insira a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço: ")
    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
    )
    clientes.append(cliente)
    print(f"\n{" Cliente cadastrado com sucesso! ".center(48, "=")}")


def criar_conta(numero_conta, clientes, contas):
    print(f"\n{" CADASTRO CONTA ".center(48, "=")}")
    cpf = input("\nDigite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print(f"\n{" Conta cadastrada com sucesso! ".center(48, "=")}")


def listar_contas(contas):
    print(f"\n{" LISTA DE CONTAS ".center(48, "=")}")
    for conta in contas:
        print("=" * 48)
        print(str(conta))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "q":
            break
        else:
            print(f"\n{" Opcao invalida tente novamente ".center(48, "*")}")


main()

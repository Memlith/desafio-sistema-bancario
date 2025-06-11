from abc import ABC, abstractmethod, property
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        conta.append(transacao)

    def adicionar_Conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, saldo, numero, agencia):
        self._saldo = 0
        self._numero = numero
        self._agencia = "1229"
        self._cliente = Cliente
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
            print("Erro ao sacar, valor de saque excede saldo da conta.")

        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} feito com sucesso!")
            return True

        else:
            print("Erro ao sacar, valor invalido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Deposito de R$ {valor:.2f} feito com sucesso!")

        else:
            print("Erro ao depositar, valor invalido.")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, saldo, numero, agencia, limite=500, limite_saques=3):
        super().__init__(saldo, numero, agencia)
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

        if valor > self.limite:
            print("Erro ao sacar, valor excede limite da conta.")
        elif numero_saques >= self.limite_saques:
            print("Erro ao sacar, limite de saques excedido.")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
AGÊNCIA: {self.agencia}
C/C: {self.numero}
Titular: {self.nome}
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
    menu = f"""{"MENU".center(32, "=")}
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuario
[q] Sair
=> """
    return input(menu)


def filtrar_cliente(cpf, clientes):
    filtra_cliente = [cliente for cliente in clientes if cliente.cpf == cpf]
    return filtrar_cliente[0] if filtra_cliente else None


def recupera_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente nao cadastrado!")
        return
    valor = float(input("Informe o valor de deposito: "))
    transacao = Deposito(valor)

    conta = recupera_conta_cliente(cliente)


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
            extrato(clientes)
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
            print("Opcao invalida, tente novamente!")

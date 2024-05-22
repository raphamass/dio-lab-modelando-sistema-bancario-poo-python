# abstractclassmethod e abstractproperty estão depreciados em Python 3.3
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
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco) # chama construtor da classe pai
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
    
    def __str__(self):
        return f"""\
        Nome: {self.nome}
        CPF: {self.cpf}
        Data de Nascimento: {self.data_nascimento}
        Endereço: {self.endereco}
        """

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
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
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n### Saque não realizado! Saldo em conta insuficiente. ###")
        
        elif valor > 0:
            self._saldo -= valor
            print("\n<<< Saque realizado com sucesso!! >>>")
            return True
        
        else:
            print("### Saque não realizado! Valor informado inválido. ###")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n<<< Depósito realizado!! >>>")
        else:
            print("\n### Depósito não realizado! Valor informado é inválido. ###")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    # Sobrescrever método sacar, porque precisa fazer validações.
    # Validações: Limite de saques e limite de valor de saque
    def sacar(self, valor):
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao['tipo'] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("### Saque não realizado! Limite máximo de saque: " \
                  "R$ 500,00. ###")
        
        elif excedeu_saques:
            print("### Saque não realizado! Número máximo de saques " \
                  "excedido (3)! ###")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
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
               'tipo': transacao.__class__.__name__,
               'valor': transacao.valor,
               'data': datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), 
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(cls, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu_principal():
    """Exibe menu principal."""
    menu = """\n
    *********** MENU ***********
    [1]Depósito
    [2]Saque
    [3]Extrato
    [4]Criar novo cliente
    [5]Criar nova conta
    [6]Listar contas
    [7]Listar clientes
    [8]Sair
    ****************************
    Selecione uma opção:
    => """
    return int(input(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [
        cliente for cliente in clientes if cliente.cpf == cpf
    ]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n### Cliente não possui conta!")
        return
    
    # FIXME: não permite a escolha de conta pelo cliente
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Por favor, informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes) 

    if not cliente:
        print("\n### Cliente não encontrado! ###")
        return
    
    valor = float(input("Por favor, informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Por favor, informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n### Cliente não encontrado! ###")
        return
    
    valor = float(input("Por favor, informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibe_extrato(clientes):
    cpf = input("Por favor, informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n### Cliente não encontrado!")

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n============== EXTRATO ==============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Nenhuma movimentação realizada."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=====================================")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Por favor, informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n### Usuário não encontrado, não foi possível criar conta! ###")

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n<<< Conta criada com sucesso!! >>>")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))

def criar_cliente(clientes):
    cpf = input("Por favor, informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n### O CPF informado já está em uso! ###")
        return
    
    nome = input("Por favor, informe o nome completo: ")
    data_nascimento = input("Por favor, informe a data de nascimento " \
                            "(dd-mm-aaaa): ")
    endereco = input("Informe o endereço " \
                     " (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente = PessoaFisica(
        nome=nome,
        data_nascimento=data_nascimento,
        cpf=cpf,
        endereco=endereco
    )

    clientes.append(cliente)

    print("<<< Cliente criado com sucesso!! >>>")

def listar_clientes(clientes):
    for cliente in clientes:
        print("=" * 100)
        print(cliente)

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu_principal()

        if opcao == 1:
            depositar(clientes)

        elif opcao == 2:
            sacar(clientes)
            
        elif opcao == 3:
            exibe_extrato(clientes)

        elif opcao == 4:
            criar_cliente(clientes)

        elif opcao == 5:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 6:
            listar_contas(contas)

        elif opcao == 7:
            listar_clientes(clientes)

        elif opcao == 8:
            print("Operação finalizada! Obrigado por utilizar nosso sistema!\n")
            break
        
        else:
            print("Operação inválida, por favor selecione a opção desejada.")

main()


# :desktop_computer: Lab Project - Modelando o Sistema Bancário em POO com Python
## Desafio - Bootcamp DIO - Python AI Backend Developer

###  *Objetivo Geral*

Iniciar a modelagem do sistema bancário com POO.
Adicionar classes(Cliente, ContaCorrente) e classes para operações bancárias (depósito, saque).

- #### ***[Versão 1.0]***  Foram implementadas 3 operações simples:

    - Depósito
    - Saque
    - Extrato

A versão 1 do programa está disponível no repositório **[raphamass/dio-lab-sistema-bancario-python](https://github.com/raphamass/dio-lab-sistema-bancario-python)**

- #### ***[Versão 2.0]***  Foram feitas as seguintes implementações:

    - Criação de funções para as operações existentes:
        - Menu principal - `def menu_principal()`
        - sacar - `def sacar()`
        - depositar - `def depositar()`
        - extrato - `def exibe_extrato()`
    
    - Criação de 4 novas funções:
        - Cadastro de novo usuário - `def criar_usuário()`
        - Filtro de suário - `def filtrar_usuario()`
        - Criação de conta - `def criar_conta()`
        - Listagem de contas - `def listar_contas()`
        - Listagem de usuários - `def listar_usuarios()`

    - Criação de função para rodar o sistema `def main()`.  
      
A versão 2 do programa está disponível no repositório **[raphamass/dio-lab-otimizando-sistema-bancario-funcoes-python](https://github.com/raphamass/dio-lab-otimizando-sistema-bancario-funcoes-python)**

- #### ***[Versão 3.0]*** - Foram feitas as seguintes implementações:  


    - #### Classes:
        - `Cliente`: representa cliente do banco, que possui endereço e uma lista de contas.
        - `PessoaFisica`: subclasse de `Cliente` - adiciona atributos específicos como nome, data de nascimento, CPF.
        - `Conta`: representa conta bancária. Tem atributos como saldo, número de conta, agência, cliente e histórico de transações.
        - `ContaCorrente`: subclasse de `Conta` que adiciona limite de saque valor e limite de quantidade de saques.
        - `Transacao`: classe abstrata que representa as transações.
        - `Saque` e `Deposito`: subclasses de `Transacao` que representam as transações específicas de saque e depósito.
        - `Historico`: mantém um registro de todas as transações realizadas em uma conta.
    
    - #### Funções de menu e operações bancárias:
        - Funções usadas para interação com usuário/ cliente e operações bancárias:
            - `menu_principal`, `depositar`, `sacar`, ``exibe_extrato``, ``criar_conta``, ``listar_contas``, ``criar_cliente``, ``listar_clientes``

            - Função ``main``: Entrada do programa. Exibe o menu principal e permite ao usuário escolher uma das opções:

            ********** MENU **********

            [1] Depósito  
            [2] Saque  
            [3] Extrato  
            [4] Criar novo cliente  
            [5] Criar nova conta  
            [6] Listar contas  
            [7] Listar clientes  
            [8] Sair

> _Nessa versão do programa, as transações de saque e depósito passam a ser vinculadas a uma conta e titular específicos. A visualização de extrato também passa a ser específica por conta e titular, com base na identificação (CPF) do titular da conta._

### *Classe Cliente*

A classe ``Cliente`` tem um construtor ``__init__`` que recebe um argumento ``endereco`` e inicializa duas propriedades:

- ``self.endereco``: Armazena o endereço do cliente.
- ``self.contas``: Uma lista vazia para armazenar as contas associadas ao cliente.

Também possui dois métodos:

- ``realizar_transacao(self, conta, transacao)``: Registra uma transação para uma conta específica.
- ``adicionar_conta(self, conta)``: Adiciona uma conta à lista de contas do cliente.
***

### *Classe PessoaFisica (herda da classe ``Cliente``)*

A classe ``PessoaFisica`` também tem um construtor ``__init__`` que recebe os seguintes argumentos:

- ``nome``: Nome da pessoa física.
- ``data_nascimento``: Data de nascimento da pessoa.
- ``cpf``: Número de CPF da pessoa.
- ``endereco``: Endereço da pessoa.

O método ``super().__init__(endereco)`` chama o construtor da classe pai (``Cliente``) para inicializar a propriedade ``self.endereco``.

Essa classe possui um método ``__str__`` que retorna uma representação formatada da pessoa física, incluindo nome, CPF, data de nascimento e endereço.
***

### *Classe ``Conta``*

A classe ``Conta`` tem um construtor ``__init__`` que recebe dois argumentos: ``numero`` e ``cliente``.
Ela inicializa várias propriedades:
- ``self._saldo``: Inicializado com zero.
- ``self._numero``: Armazena o número da conta.
- ``self._agencia``: Sempre definido como ‘0001’.
- ``self._cliente``: Referência ao cliente associado à conta.
- ``self._historico``: Uma instância da classe Historico.

E possui os seguintes métodos:
- ``sacar(self, valor)``: Realiza um saque, verificando se o saldo é suficiente e se o valor é válido.
- ``depositar(self, valor)``: Realiza um depósito, verificando se o valor é válido.

Dentro da classe ``Conta`` temos um método de classe (``@classmethod``), ``nova_conta(cls, cliente, numero)``. Ele cria e retorna uma nova instância da classe ``Conta`` com os argumentos fornecidos (``cliente`` e ``numero``).

Ainda dentro dessa classe, temos algumas propriedades criadas com uso do decorador ``@property``. Isso nos permite acessar valores sem o uso de parênteses.

Temos as seguintes propriedades:

- ``saldo``: Retorna o valor do saldo da conta.
- ``numero``: Retorna o número da conta.
- ``agencia``: Retorna o número da agência (sempre definido como ‘0001’).
- ``cliente``: Retorna a referência ao cliente associado à conta.
- historico: Retorna a instância da classe ``Historico`` associada à conta.

Assim, ao invés de chamarmos ``conta.saldo()``, podemos simplesmente usar ``conta.saldo``

***

### *Classe ``ContaCorrente``(herda da classe ``Conta``)*

-Essa classe também tem um construtor ``__init__`` que recebe os seguintes argumentos:

- ``numero``: Número da conta corrente.
- ``cliente``: Referência ao cliente associado à conta.
- ``limite``: Limite máximo para saques (padrão é ***R$ 500,00***).
- ``limite_saques``: Número máximo de saques permitidos (padrão é ***3***).

O método ``super().__init__(numero, cliente)`` chama o construtor da classe pai (``Conta``) para inicializar as propriedades básicas.

A classe ``ContaCorrente`` sobrescreve o método ``sacar(self, valor)`` para adicionar validações específicas:

- Verifica se o valor do saque excede o limite.
- Verifica se o número de saques já atingiu o limite.

O método ``__str__(self)`` retorna uma representação formatada da conta corrente, incluindo agência, número da conta e nome do titular.
***

### *Classe ``Historico``*

É responsável por registrar as transações associadas a uma conta.

Ela tem um construtor ``__init__`` que inicializa uma lista vazia chamada ``_transacoes``.
A propriedade transacoes (decorada com ``@property``) retorna essa lista de transações.

O método ``adicionar_transacao(self, transacao)`` adiciona uma nova transação à lista ``_transacoes``. Ele registra o tipo de transação (usando ``transacao.__class__.__name__``), o valor da transação e a data e hora atual.
***

### *Classe ``Transacao`` (classe abstrata)*

A classe ``Transacao`` é uma classe abstrata (herda de ``ABC``).

Com uso do decorador ``@abstractmethod``, ela define duas propriedades abstratas (ou métodos abstratos):

- ``valor``: Representa o valor da transação.
- ``registrar(cls, conta)``: Método de classe abstrato para registrar a transação em uma conta específica.

Esses métodos **devem** ser implementados por todas as subclasses (classes filhas) de ``Transacao``, ou seja, nessa classe é definido um contrato que suas subclasses devem seguir.
***

### *Classe ``Saque``(Subclasse de ``Transacao``)*

A classe ``Saque`` representa uma transação de saque.
Ela tem um construtor que recebe o valor do saque.

A propriedade ``valor`` retorna esse valor.
O método ``registrar(self, conta)`` verifica se o saque foi bem-sucedido na conta e, se sim, adiciona a transação ao histórico da conta.
***

### *Classe ``Deposito``(Subclasse de ``Transacao``)*

Essa classe representa uma transação de depósito.

O construtor ``__init__`` recebe o valor do depósito.

A propriedade ``valor``, definida com o decorador ``@property`` retorna o valor.

Por fim, o método ``registrar(self, conta)`` verifica se o depósito foi bem-sucedido na conta e, caso positivo, adiciona essa transação ao histórico da conta.
***




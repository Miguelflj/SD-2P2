# TRABALHO DE SISTEMAS DISTRIBUIDOS - UFMT


## SISTEMA DE ARQUIVOS DISTRIBUIDOS
### Rede P2P centralizada
    Estudo de caso da tecnologia RMI (Remote Method Invocation)
### Bibliotecas

- Pyro5
- threading
- sys
- os
- datetime

#### Estrutura

> Processo Usuário

> Processo Administrador (Um obrigatório conectado ao servidor de nomes)

> Logs

#### Características
- [x] Balanceador de cargas para transferência dos arquivos (criado uma métrica de proximidade)
- [x] Gerenciador de Logs
- [x] Máximo de 50 usuários na rede
- [x] Café quente

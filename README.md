# JonatanPedro_T11

# Pedro Barbieri e Jonatan

## 📕  Descrição  

Esse é um sistema que lê um arquivo de texto que contém dados de uma eleição que insere 
pessoas, partidos e candidatos à eleição, e n arquivos de texto que contem os 
votos por urnas, dentro da pasta "entrada". Na pasta "saida", retorna 3 arquivos:
"boletimUrnaOutput.txt", "contabilizacaoOutput.txt" e "log_erros.txt"


## 🔍 Como Funciona
Como dito anteriormente, é preciso que os arquivos 
```bash
"eleicaoRS.txt" que contém os dados da votação, como: pessoa, candidato e partido 
```
e
```bash
"urnaX.txt" que contém os votos dos eleitores, separados em X arquivos
```
estejam dentro de "Files/entrada" para funcionar corretamente
desse modo na pasta "saida" serão retornados 3 arquivos

```bash
"boletimUrnaOutput.txt" contém o resultado detalhado de cada urna.
"contabilizacaoOutput.txt" apresenta a contabilização geral dos votos.
"log_erros.txt" registra qualquer erro de entrada encontrado durante a execução.
```

## 📁 Passo a passo para USO

1 passo:
```bash
     #clone o repositirio
     $ git clone https://github.com/POD-PUCRS-2024-2/JonatanPedro_T11.git
```

2 passo:
```bash
     #acesse o diretorio do projeto
     $ cd JonatanPedro_T11
```
3 passo:
```bash
     #agora execute
     $ python app.py
     #ou adicione os argumentos/nomes dos arquivos diretamente na linha de comando (mais propenso a erros)
     $ python app.py eleicaoRS.txt urna1.txt urna2.txt ... urnaX.txt
     #ou seja, copie o nome do arquivo e separe por espaços como demonstrado acima para que o programa possa 
     #indentificar multiplos arquivos diferentes
     #no caso de utilizar essa opção, ignore o 4 passo
```

4 passo:
```bash
     #na hora de inserir a entrada com os nomes dos arquivos é nescessario que seja feito dessa forma
     eleicaoRS.txt, urna1.txt, urna2.txt, urna3.txt, urna4.txt, ..., até urnaX.txt
     #ou seja, copie o nome do arquivo e separe por vírgulas para que o programa possa 
     #indentificar multiplos arquivos diferentes
```


## 🧱 Estrutura de Classes e Métodos

-  Clase partido
     - Representa um partido político participante da eleição contendo
     - Atributos:
          - nomepartido: Nome do partido (máximo 50 caracteres).
          - cnpj: CNPJ do partido (14 caracteres).
          - numero: Número do partido (2 caracteres).
- Clase pessoa
     - Representa uma pessoa, que pode ser um eleitor ou um candidato.
     - Atributos:
          - nomepartido: Nome do partido (máximo 50 caracteres).
          - cpf: CPF da pessoa (11 caracteres).
          - nascimento: Data de nascimento da pessoa.

- Classe candidato
     - Representa um candidato, herdando de Pessoa e possuindo outros atributos específicos.
     - Atributos:
          - numero: Número do candidato.
          - partido: Objeto da classe Partido.
          - proposta: Descrição das propostas do candidato.
          
     - Métodos:
          - verifica_numero_cargo(): Método abstrato implementado pelas subclasses para verificar se o número do candidato está correto. 

- Classe eleicao
     -  Gerencia os candidatos, partidos e eleitores da eleição.
     - Atributos:
          - partidos: Lista de partidos.
          - pessoas: Lista de pessoas.
          - candidatos: Lista de candidatos.
          
     - Métodos:
          - adicionar_partido(partido): Adiciona um partido à eleição.
          - adicionar_pessoa(pessoa): Adiciona uma pessoa à eleição.
          - adicionar_candidato(candidato): Adiciona um candidato à eleição.
          - buscar_partido(numero): Busca um partido pelo seu número.
          - buscar_pessoa(cpf): Busca uma pessoa pelo seu CPF.
          - buscar_candidato(numero): Busca um candidato pelo número. 

- Classe Votacao
     - Representa uma votação de um eleitor, armazenando os candidatos escolhidos para diferentes cargos.
     - Atributos:
          - id_urna: Identificador da urna.
          - id_votacao: Identificador da votação.
          - dep_estadual: Número do candidato a Deputado Estadual escolhido.
          - dep_federal: Número do candidato a Deputado Federal escolhido.
          - senador: Número do candidato a Senador escolhido.
          - governador: Número do candidato a Governador escolhido.
          - presidente: Número do candidato a Presidente escolhido.
          
     - Métodos:
          - total_votacoes(): Método de classe que conta o total de votações registradas.

- Classe Urna
     - Representa uma urna de votação que armazena e gerencia as votações de uma eleição.
     - Atributos:
          - id_urna: Identificador da urna.
          - votacoes: Lista de objetos Votacao, representando as votações registradas nessa urna.
          
     - Métodos:
          - total_votacoes(): Método de classe que conta o total de votações registradas.
          - adicionar_votacao(votacao, eleicao): Adiciona uma votação à urna, validando os candidatos escolhidos (por exemplo, verificando se os números de candidatos são válidos e se os partidos existem).
          - contar_votos_cargo(): Conta e retorna a quantidade de votos para cada cargo (Presidente, Governador, Senador, Dep. Federal e Dep. Estadual).
          - gerar_boletim_urna(candidatos_lista): Gera o boletim detalhado da urna, listando os candidatos e a quantidade de votos que cada um recebeu, e grava o resultado no arquivo boletimUrna.txt.
          - candidato_mais_votado(candidatos_lista): Determina o candidato mais votado para cada cargo e retorna um dicionário com os resultados.
          - gerar_contabilizacao(candidatos_lista): Gera a contabilização geral dos votos da urna e salva em um arquivo contabilizacao.txt, incluindo os candidatos mais votados para cada cargo.
          - \_\_add__(other): Sobrecarga do operador +, permitindo a soma de duas urnas. Essa operação combina as votações de ambas as urnas e cria uma nova urna com um identificador concatenado.

## ⁉️ Tratamentos de erros

O sistema conta com uma série de exceções personalizadas para garantir a integridade dos dados e fornecer feedback detalhado quando ocorrem erros. Todos os erros gerados são registrados no arquivo log_erros.txt, que fica na pasta Files/saida/.
* CpfInvalidoException: Aparece quando o CPF fornecido não possui exatamente 11 dígitos.
* CnpjInvalidoException: Aparece quando o CNPJ fornecido não possui exatamente 14 dígitos.
* NomePessoaInvalidoException: Aparece quando o nome da pessoa excede 50 caracteres ou contém caracteres inválidos.
* NomePartidoInvalidoException: Aparece quando o nome do partido excede 50 caracteres ou contém caracteres inválidos.
* NumeroPartidoInvalidoException: Aparece quando o número do partido contém mais de 2 dígitos ou não é numérico.
* NumeroCandidatoInvalidoException: Aparece quando o número do candidato não corresponde à quantidade de dígitos esperada para o cargo.
* ObjetoNaoEncontradoException: Aparece quando uma busca por pessoa, candidato ou partido não encontra o objeto desejado.
* ObjetoJaExisteException: Aparece quando se tenta adicionar uma pessoa, candidato ou partido que já foi previamente adicionado.

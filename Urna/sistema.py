# pacotes/módulo de sistema
from abc import ABC, abstractmethod

# ------------------------------------------------------- Tratamento de Exceções -----------------------------------------------------------
class CpfInvalidoException(Exception):
    def __init__(self, mensagem):
        self.mensagem = f"Erro ao criar Pessoa: O CPF deve ter exatamente 11 dígitos - CPF informado: {mensagem}"
        with open("Files/saida/log_erros.txt", "a") as f:
            f.write(self.mensagem + "\n")
        super().__init__(self.mensagem)
        

class CnpjInvalidoException(Exception):
    def __init__(self, mensagem):
        self.mensagem = f"Erro ao criar Partido: O CNPJ deve ter exatamente 14 dígitos - CNPJ informado: {mensagem}"
        with open("Files/saida/log_erros.txt", "a") as f:
            f.write(self.mensagem + "\n")
        super().__init__(self.mensagem)

class NomePessoaInvalidoException(Exception):
    def __init__(self, mensagem):
        self.mensagem = f"Erro ao criar Pessoa: O nome da pessoa deve ter no máximo 50 caracteres e ser composto por apenas letras e espaços - Nome informado: {mensagem}"
        with open("Files/saida/log_erros.txt", "a") as f:
            f.write(self.mensagem + "\n")
        super().__init__(self.mensagem)

class NomePartidoInvalidoException(Exception):
    def __init__(self, mensagem):
        self.mensagem = f"Erro ao criar Partido: O nome do partido deve ter no máximo 50 caracteres e ser composto por apenas letras e espaços - Nome informado: {mensagem}"
        with open("Files/saida/log_erros.txt", "a") as f:
            f.write(self.mensagem + "\n")
        super().__init__(self.mensagem)

class NumeroPartidoInvalidoException(Exception):
    def __init__(self, mensagem):
        self.mensagem = f"Erro ao criar Partido: O numero do partido deve ter no máximo 2 dígitos - Número informado: {mensagem}" 
        with open("Files/saida/log_erros.txt", "a") as f:
            f.write(self.mensagem + "\n")
        super().__init__(self.mensagem)

class NumeroCandidatoInvalidoException(Exception):
    def __init__(self, mensagem):
        self.mensagem = f"Erro ao criar candidato: Número inválido para este cargo - Número informado: {mensagem}"
        with open("Files/saida/log_erros.txt", "a") as f:
            f.write(self.mensagem + "\n")
        super().__init__(self.mensagem)

class ObjetoNaoEncontradoException(Exception):
    def __init__(self, x, mensagem):
        if x == "h":
            self.mensagem = f"Não existe ninguém com o CPF informado: {mensagem}"
        elif x == "c":
            self.mensagem = f"Não existe nenhum candidato com o número informado: {mensagem}"
        elif x == "p":
            self.mensagem = f"Não existe nenhum partido com o número informado: {mensagem}"
        super().__init__(self.mensagem)

class ObjetoJaExisteException(Exception):
    def __init__(self, x, mensagem):
        if x == "h":
            self.mensagem = f"Essa pessoa já foi adicionada: {mensagem}"
        elif x == "c":
            self.mensagem = f"Esse candidato já foi adicionado: {mensagem}"
        elif x == "p":
            self.mensagem = f"Esse partido já foi adicionado: {mensagem}"
        super().__init__(self.mensagem)


# ----------------------------------------------------- Classes ------------------------------------------------------

class Partido():
    def __init__(self,nomepartido,cnpj,numero):
        try:
            if self._valida_nomepartido(str(nomepartido)):
                raise NomePartidoInvalidoException(nomepartido)
            if self._valida_cnpj(str(cnpj)):
                raise CnpjInvalidoException(cnpj)
            if self._valida_num(str(numero)):
                raise NumeroPartidoInvalidoException(numero)

            self._nomepartido = str(nomepartido) # no máximo 50 caracteres
            self._cnpj = str(cnpj) # 14 caracteres
            self._numero = str(numero) # no máximo 2 caracteres
            self._ehvalido = True

        except (NomePartidoInvalidoException, CnpjInvalidoException, NumeroPartidoInvalidoException) as e:
            self._ehvalido = False

    def __bool__(self):
        return self._ehvalido
    
    @property
    def nomepartido(self):
        return self._nomepartido

    @property
    def cnpj(self):
        return self._cnpj

    @property
    def numero(self):
        return self._numero
    
    def _valida_nomepartido(self, nome): # verifica se 'nomepartido' > 50 caracteres
        if (len(nome)) > 50: # or not nome.replace(" ", "").isalpha(): # estava dando problema com acentuação
            return True # True para a exception
        return False # Ignora a exception
    
    def _valida_cnpj(self, cnpj): # verifica se 'cnpj' != 14 e se não é número
        if (len(cnpj)) != 14 or not cnpj.isdigit():
            return True # True para a exception
        return False # Ignora a exception
    
    def _valida_num(self, numero): # verifica se 'num' > 2 caracteres e se não é número
        if (len(numero)) > 2 or not numero.isdigit():
            return True # True para a exception
        return False # Ignora a exception

class Pessoa():
    def __init__(self,nomepessoa,cpf,nascimento):
        try:
            if self._verifica_nomepessoa(str(nomepessoa)):
                raise NomePessoaInvalidoException(nomepessoa)
            if self._verifica_cpf(str(cpf)):
                raise CpfInvalidoException(cpf)
            
            self._nomepessoa = str(nomepessoa) # no máximo 50 caracteres
            self._cpf = str(cpf) # 11 caracteres
            self._nascimento = str(nascimento)
            self._ehvalido = True
        except (NomePartidoInvalidoException, CpfInvalidoException) as e:
            self._ehvalido = False

    @property
    def nomepessoa(self):
        return self._nomepessoa

    @property
    def cpf(self):
        return self._cpf

    @property
    def nascimento(self):
        return self._nascimento

    def __bool__(self):
        return self._ehvalido

    def _verifica_nomepessoa(self, nome): # verifica se 'nomepessoa' > 50 caracteres
        if (len(nome)) > 50: # or not nome.replace(" ", "").isalpha(): # estava dando problema com acentuação
            return True # True para a exception
        return False # Ignora a exception
    
    def _verifica_cpf(self, cpf): # verifica se 'cpf' != 11 caracters
        if (len(cpf)) != 11 or not cpf.isdigit():
            return True # True para a exception
        return False # Ignora a exception

class Candidato(Pessoa, ABC):
    def __init__(self, nomepessoa, cpf, nascimento, numero, partido, proposta):
        try:
            if self.verifica_numero_cargo(str(numero)):
                raise NumeroCandidatoInvalidoException(numero)

            super().__init__(nomepessoa, cpf, nascimento)
            self._partido = partido
            self._proposta = proposta
            self.numero = str(numero)

        except NumeroCandidatoInvalidoException as e:
            pass

    @abstractmethod
    def verifica_numero_cargo(self, numero): # método que sera implementado nas subclasses
        pass

    @property
    def partido(self):  # getter
        return self._partido

    @property
    def proposta(self):  # getter
        return self._proposta
    
    @property
    def numero(self): # getter
        return self._numero
    
    @numero.setter
    def numero(self, numero):
        self._numero = numero
        
class DepFederal(Candidato):
    def verifica_numero_cargo(self, numero):
        if (len(numero) != 4) or not numero.isdigit():
            return True # True para a exception
        return False # Ignora a exception

class DepEstadual(Candidato):
    def verifica_numero_cargo(self, numero):
        if (len(numero) != 5):
            return True # True para a exception
        return False # Ignora a exception
        
class Senador(Candidato):
    def verifica_numero_cargo(self, numero):
        if (len(numero) != 3):
            return True # True para a exception
        return False # Ignora a exception
        
class Governador(Candidato):
    def verifica_numero_cargo(self, numero):
        if (len(numero) != 2):
            return True # True para a exception
        return False # Ignora a exception

class Presidente(Candidato):
    def verifica_numero_cargo(self, numero):
        if (len(numero) != 2):
            return True # True para a exception
        return False # Ignora a exception

class Eleicao():
    def __init__(self):
        self.partidos = []
        self.pessoas = []
        self.candidatos = []

    def adicionar_partido(self, partido): # adiciona um partido à eleição se já não foi adicionado
        try:
            if (partido not in self.partidos):
                self.partidos.append(partido)
            else:
                raise ObjetoJaExisteException("p", partido)
        except ObjetoJaExisteException as e:
            pass
        
    def adicionar_pessoa(self, pessoa):
        try:
            if (pessoa not in self.pessoas):
                self.pessoas.append(pessoa)
            else:
                raise ObjetoJaExisteException("h", pessoa)
        except ObjetoJaExisteException as e:
            pass
        
    def adicionar_candidato(self, candidato): # adiciona um candidato à eleição se já não foi adicionado
        try:
            if (candidato not in self.candidatos):
                self.candidatos.append(candidato)
            else:
                raise ObjetoJaExisteException("c", candidato)
        except ObjetoJaExisteException as e:
            pass
        
    def buscar_partido(self, numero): # busca por um partido pelo seu número
        try:
            for partido in self.partidos:
                if partido.numero == numero:
                    return partido
            raise ObjetoNaoEncontradoException("p", numero)
        except ObjetoNaoEncontradoException as e:
            pass
    
    def buscar_pessoa(self, cpf): # busca por uma pessoa pelo seu cpf
        try:
            for pessoa in self.pessoas:
                if pessoa.cpf == cpf:
                    return pessoa
            raise ObjetoNaoEncontradoException("h", cpf)
        except ObjetoNaoEncontradoException as e:
            pass
    
    def buscar_candidato(self, numero): # busca por um candidato pelo seu número
        try:
            for candidato in self.candidatos:
                if candidato.numero == numero:
                    return candidato
            raise ObjetoNaoEncontradoException("c", numero)
        except ObjetoNaoEncontradoException as e:
            pass
    
    # def listar_candidatos_por_cargo(self, cargo): # retorna uma lista de candidatos para x cargo

    def total_candidatos(self): # retorna o n total de candidatos
        return len(self.candidatos)
    
    def total_partidos(self): # retorna o n total de partidos
        return len(self.partidos)

class Votacao():    
    eleitores_votaram = []

    def __init__(self, id_urna, id_votacao, dep_estadual, dep_federal, senador, governador, presidente):
        self.id_urna = id_urna
        self.id_votacao = id_votacao
        self.dep_estadual = dep_estadual
        self.dep_federal = dep_federal
        self.senador = senador
        self.governador = governador
        self.presidente = presidente

        # Adiciona a votação na lista de eleitores que votaram
        Votacao.eleitores_votaram.append(self)

    def total_votacoes(cls):
        # cls refere à classe a que pertence o método, em vez de a uma instância.
        # Conta o total de votações armazenadas
        return len(cls.eleitores_votaram)

class Urna():
    def __init__(self, id_urna):
        self.id_urna = id_urna
        self.votacoes = []
        
    def adicionar_votacao(self, votacao, eleicao):
        if isinstance(votacao, Votacao):
            with open("Files/saida/log_erros.txt", "a") as f:
                governador = eleicao.buscar_partido(votacao.governador)
                if len(votacao.governador) != 2:
                    f.write(f"Erro ao adicionar votação: Número inválido para governador - Número informado: {votacao.governador}\n")
                    votacao.governador = "Nulo"

                if len(votacao.presidente) != 2:
                    f.write(f"Erro ao adicionar votação: Número inválido para presidente - Número informado: {votacao.presidente}\n")
                    votacao.presidente = "Nulo"

                if len(votacao.senador) != 3:
                    f.write(f"Erro ao adicionar votação: Número inválido para senador - Número informado: {votacao.senador}\n")
                    votacao.senador = "Nulo"

                if len(votacao.dep_federal) != 4:
                    f.write(f"Erro ao adicionar votação: Número inválido para Deputado Federal - Número informado: {votacao.dep_federal}\n")
                    votacao.dep_federal = "Nulo"

                if len(votacao.dep_estadual) != 5:
                    f.write(f"Erro ao adicionar votação: Número inválido para Deputado Estadual - Número informado: {votacao.dep_estadual}\n")
                    votacao.dep_estadual = "Nulo"

            self.votacoes.append(votacao)

        else:
            pass

    def contar_votos_cargo(self, candidatos):
        #vai contar os votos de cada cargo
        contagem_votos = {
            "Governador": {},
            "Presidente": {},
            "DepFederal": {},
            "DepEstadual": {},
            "Senador": {}
        }
        for numero, _, cargo in candidatos:
            contagem_votos[cargo][numero] = 0

        for votacao in self.votacoes:
            contagem_votos["Presidente"][votacao.presidente] = contagem_votos["Presidente"].get(votacao.presidente, 0) + 1
            contagem_votos["Governador"][votacao.governador] = contagem_votos["Governador"].get(votacao.governador, 0) + 1
            contagem_votos["Senador"][votacao.senador] = contagem_votos["Senador"].get(votacao.senador, 0) + 1
            contagem_votos["DepFederal"][votacao.dep_federal] = contagem_votos["DepFederal"].get(votacao.dep_federal, 0) + 1
            contagem_votos["DepEstadual"][votacao.dep_estadual] = contagem_votos["DepEstadual"].get(votacao.dep_estadual, 0) + 1

        return contagem_votos

    def gerar_boletim_urna(self, candidatos_lista):

        candidatos_info = {tup[2]: {numero: nome for numero, nome, cargo in candidatos_lista if cargo == tup[2]} for tup in candidatos_lista}

        repetidotemp = {}
        for numero, nome, cargo in candidatos_lista:
            nc = f"{numero}|{cargo}"
            if nc in repetidotemp:
                repetidotemp[nc].append(nome)
            else:
                repetidotemp[nc] = [nome]

        repetido = []
        for numcargo, item in repetidotemp.items():
            if len(item) >= 2:
                repetido.append((*numcargo.split("|"), item))


        contagem = self.contar_votos_cargo(candidatos_lista)
        boletim = f"-----------------BOLETIM DA URNA {self.id_urna}----------------\n"

        # Iterar sobre os cargos e votos
        for cargo, votos in contagem.items():
            boletim += f"{cargo}:\n"
            for numero, quantidade in votos.items():
                nome = candidatos_info[cargo].get(numero)
                if nome == "Desconhecido" or nome == None:
                    continue

                for repeticao in repetido:
                    if (numero, cargo) == repeticao[:2]:
                        for pessoa in repeticao[2]:
                            if pessoa != nome:
                                boletim += f"  Candidato {pessoa} (Número {numero}): {quantidade} votos\n"

                
                boletim += f"  Candidato {nome} (Número {numero}): {quantidade} votos\n"
        
        with open("Files/saida/boletimUrnaOutput.txt", "a") as arquivo:
            arquivo.write(boletim + "\n")
        
        return boletim

    def candidato_mais_votado(self, candidatos_lista):
        contagem_votos = self.contar_votos_cargo(candidatos_lista)
        candidatos_info = {tup[2]: {numero: nome for numero, nome, cargo in candidatos_lista if cargo == tup[2]} for tup in candidatos_lista}
        mais_votados = {}

        for cargo, votos in contagem_votos.items():
            contagem_votos[cargo]["Nulo"] = 0

            for numero in votos:
                if candidatos_info[cargo].get(numero) == "Desconhecido":
                    contagem_votos[cargo][numero] = 0

            if votos:
                max_votos = max(votos.values())

                for numero, cont in votos.items():
                    if cont == max_votos and candidatos_info[cargo].get(numero) != "Desconhecido":
                        if cargo in mais_votados:
                            mais_votados[cargo].append((numero, max_votos))
                        else:
                            mais_votados[cargo] = [(numero, max_votos)]
        
        # if not contagem_votos:  # Verifica se há votos
        #     return None, 0
        # mais_votado = max(contagem_votos, key=contagem_votos.get)

        return mais_votados
    
    def gerar_contabilizacao(self, candidatos_lista):
        mais_votados = self.candidato_mais_votado(candidatos_lista)
        # candidatos_info = {numero: nome for numero, nome, _ in candidatos_lista}
        candidatos_info = {tup[2]: {numero: nome for numero, nome, cargo in candidatos_lista if cargo == tup[2]} for tup in candidatos_lista}
        contabilizacao = f"RESULTADO ELEIÇÃO------------QUANTIDADE ELEITORES: {len(self.votacoes)}\n"
    	
        for cargo, candidatos in mais_votados.items():
            contabilizacao += f"Cargo: {cargo}, Candidato(s) mais votados: "

            candidatos_str = []
            i = 0
            for numero, votos in candidatos:
                nome = candidatos_info[cargo].get(numero, "Desconhecido")
                candidatos_str.append(f"{nome} N: {numero}, Votos: {votos}" )
                i += 1

            contabilizacao += ", ".join(candidatos_str) + "\n"

        with open("Files/saida/contabilizacaoOutput.txt", "w") as arquivo:
            arquivo.write(contabilizacao + "\n")

        return contabilizacao
    
    def __add__(self, other):
        # if not isinstance(other, Urna):
        #     raise ValueError("O objeto fornecido não é uma instância da classe Urna.")
        nova_id_urna = f"{self.id_urna}_{other.id_urna}"
        nova_urna = Urna(nova_id_urna)
        nova_urna.votacoes = self.votacoes + other.votacoes
        return nova_urna
        
    def __str__(self):
        return f"ID Urna: {self.id_urna} | Total de Votações: {len(self.votacoes)}"

from Urna import sistema
import sys

print("+------------------------------------------------------------------------------------+")
print("|                                 Sistema de Votação                                 |")
print("|                         feito por Jonatan e Pedro Barbieri                         |")
print("+------------------------------------------------------------------------------------+")
print()

while(True):
    if len(sys.argv) > 1:
        sys.argv.pop(0)
        comando = sys.argv
    else:
        print("Quais seriam os arquivos de texto com os dados e votos da eleição?")
        print()
        comando = list(map(lambda x : x.strip(), str(input("Entrada (-1 para sair): ")).split(","))) # exemplo: eleicaoRS.txt, urna1.txt, urna2.txt, urna3.txt, urna4.txt, urna5.txt, urna6.txt, urna7.txt
        print()

    if comando[0] == "-1":
        break

    with open("Files/saida/log_erros.txt", "w"):
        pass
    with open("Files/saida/boletimUrnaOutput.txt", "w"):
        pass

    if comando[0] == "":
        mensagem = f"Erro: Entrada vazia. Tente novamente.\n"
        print(mensagem)
        with open("Files/saida/log_erros.txt", "a") as f:
            f.write(mensagem)
        continue

    urnas = len(comando)-1

    s = sistema
    eleicao = s.Eleicao()

    candidatos_lista = []

    cont_dados = {
        "Partido": 0,
        "Pessoa": 0,
        "Candidato": 0
    }

    try:
        with open(f"Files/entrada/{comando[0]}", "r") as f: # abre o arquivo eleicaoRS.txt para leitura apenas
            for linha in f: # andar de linha em linha

                if linha.startswith("adicionar_partido"): # se a linha começa com adicionar_partido:
                    cnpj, nome, numero = linha.removeprefix("adicionar_partido: ").replace("\n", "").split(", ") # trata e limpa os dados
                    cnpj = cnpj.replace(".", "").replace("-", "").replace("/", "")

                    partido = s.Partido(nome, cnpj, numero) # cria o partido

                    if partido:
                        eleicao.adicionar_partido(partido) # adiciona o partido na eleicao
                        cont_dados["Partido"] +=1

                if linha.startswith("adicionar_pessoa"):
                    nome, cpf, nascimento = linha.removeprefix("adicionar_pessoa: ").replace("\n", "").split(", ")

                    pessoa = s.Pessoa(nome,cpf,nascimento)

                    if (pessoa):
                        eleicao.adicionar_pessoa(pessoa)
                        cont_dados["Pessoa"] +=1

                if linha.startswith("adicionar_candidato"):
                    cpf, numero, numeropartido, propostas, cargo = linha.removeprefix("adicionar_candidato: ").replace("\n", "").split(", ")

                    try:
                        if (eleicao.buscar_pessoa(cpf) == None or len(numeropartido) > 2):
                            nome = "Desconhecido"
                        else: 
                            nome = eleicao.buscar_pessoa(cpf).nomepessoa # busca o nome da pessoa anteriormente armazenada utilizando o cpf (possui erro nos dados de entrada)

                        if (eleicao.buscar_pessoa(cpf) == None):
                            nascimento = "Desconhecido"
                        else:
                            nascimento = eleicao.buscar_pessoa(cpf).nascimento # busca o nascimento da pessoa anteriormente armazenada utilizando o cpf

                        if cargo == "Presidente":
                            candidato = s.Presidente(nome,cpf,nascimento,numero,eleicao.buscar_partido(numeropartido),propostas)
                        elif cargo == "Governador":
                            candidato = s.Governador(nome,cpf,nascimento,numero,eleicao.buscar_partido(numeropartido),propostas)
                        elif cargo == "Senador":
                            candidato = s.Senador(nome,cpf,nascimento,numero,eleicao.buscar_partido(numeropartido),propostas)
                        elif cargo == "DepFederal":
                            candidato = s.DepFederal(nome,cpf,nascimento,numero,eleicao.buscar_partido(numeropartido),propostas)
                        elif cargo == "DepEstadual":
                            candidato = s.DepEstadual(nome,cpf,nascimento,numero,eleicao.buscar_partido(numeropartido),propostas)

                        if(candidato.verifica_numero_cargo(numero)):
                            raise ValueError

                        eleicao.adicionar_candidato(candidato)
                        cont_dados["Candidato"] +=1

                        candidatos_lista.append((numero, nome, cargo))

                    except ValueError:
                        pass

    except FileNotFoundError as e:
        mensagem = f"Erro: {comando[0]} não existe. Tente novamente.\n"
        print(mensagem)
        with open("Files/saida/log_erros.txt", "a") as f:
            f.write(mensagem)
        continue

    erro_dectectado = False    
    for categoria, contagem in cont_dados.items():
        if contagem == 0:
            mensagem = f"Erro: O arquivo de dados informado não adiciona pessoa ou partido ou candidato. Tente novamente.\n"
            print(mensagem)
            with open("Files/saida/log_erros.txt", "a") as f:
                f.write(mensagem)
            erro_dectectado = True
            break
    if erro_dectectado:
        continue

    print("Partidos, pessoas e candidatos adicionados!\n")

    if urnas < 1:
        mensagem = f"Erro: Não foi informado nenhuma urna. Tente novamente.\n"
        print(mensagem)
        with open("Files/saida/log_erros.txt", "a") as f:
            f.write(mensagem)
        continue

    lista_urnas = []
    ids = []

    for id in range(1,urnas+1):
        try:
            with open(f"Files/entrada/{comando[id]}", "r") as f:
                for linha in f:
                    if linha.startswith("adicionar_voto: "):
                        id_urna = linha.removeprefix("adicionar_voto: ").replace("\n", "").split(", ")
                        ids.append(int(id_urna[0]))
                        break
                    
        except FileNotFoundError as e:
            mensagem = f"Erro: {comando[id]} não existe. Avançando para o próximo arquivo...\n"
            print(mensagem)
            with open("Files/saida/log_erros.txt", "a") as f:
                f.write(mensagem)
            ids.append("Nulo")
    
    for id in range(1,urnas+1):
        try:
            with open(f"Files/entrada/{comando[id]}", "r") as f:
                try:
                    if ids[id-1] == "Nulo":
                        continue
                except IndexError:
                    continue
                urna = s.Urna(ids[id-1])
                for linha in f:
                    if linha.startswith("adicionar_voto: "):
                        id_urna, id_votacao, depEstadual, depFederal, senador, governador, presidente = linha.removeprefix("adicionar_voto: ").replace("\n", "").split(", ")
                        voto = s.Votacao(id_urna, id_votacao, depEstadual, depFederal, senador, governador, presidente)

                        urna.adicionar_votacao(voto, eleicao)
            urna.gerar_boletim_urna(candidatos_lista)
            lista_urnas.append(urna)
        except FileNotFoundError as e:
            pass

    try:    
        total_urnas = lista_urnas[0]
    except IndexError:
        mensagem = f"Erro: Não foi informado nenhuma urna que adicione votos. Tente novamente.\n"
        print(mensagem)
        with open("Files/saida/log_erros.txt", "a") as f:
            f.write(mensagem)
        continue

    print("Registro dos erros de entrada gerado com sucesso em 'Files/saida/log_erros.txt' !\n") 

    print("Boletim de cada urna gerado com sucesso em 'Files/saida/boletimUrnaOutput.txt' !\n")

    for urna in range(1, len(lista_urnas)):
        total_urnas += lista_urnas[urna]

    total_urnas.gerar_contabilizacao(candidatos_lista)
    print("Contabilização das urnas gerado com sucesso em 'Files/saida/contabilizacaoOutput.txt' !\n")
    break  






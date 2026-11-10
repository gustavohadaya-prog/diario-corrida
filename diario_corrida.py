import json    # import importa o módulo
                # modulo conjunto de ferramentas, funções, métodos(operações como o append)
                #json é um módulo ja instalado pelo python
                # é uma forma estruturada de texto para parmazenar dicionario e listas, de forma que o python consiga ler e identificar suas informações corretamente.
import datetime

import os
#################
corridas = []

# PEDIR -> CALCULAR -> FORMATAR

#Pedir
def pedir_decimal(mensagem, valor_atual=None):
    if valor_atual is not None:
        mensagem = f"{mensagem}[atual: {valor_atual}; Enter para manter: ] "    
    while True:
        try:
            numero = input(mensagem)
            if numero == "" and valor_atual is not None:
                return valor_atual
            numero = float(numero)

            if numero > 0:
                return numero
            else:
                print("Digite um valor maior que zero.")
        except ValueError:
            print("Digite um numero. Use ponto para decimais.")

def pedir_sim_não(mensagem):
    while True:
        escolha = input(mensagem).strip().lower()

        if escolha != "s" and escolha != "n":
            print("Opção inválida. Digite s ou n: ")
        else:
            return escolha

def pedir_data(mensagem, valor_atual=None):
    if valor_atual is not None:
        data_exibição = datetime.datetime.strftime(valor_atual, "%d/%m/%Y")
        mensagem = f"{mensagem}[atual: {data_exibição}; Enter para manter: ] "
    while True:
        try:
            texto = input(mensagem)
            if texto == "" and valor_atual is not None:
                return valor_atual
            else:
                texto = datetime.datetime.strptime(texto, "%d/%m/%Y")
            return texto
        except ValueError:
            print("Data inválida. Use DD/MM/AAAA.")

def pedir_numero_item(quantidade_itens, permitir_cancelar=False):
    while True:
        try:
            numero = int(input("Escolha uma opção: "))
            if permitir_cancelar == True:
                if numero == 0:
                    return 0
            if numero <= quantidade_itens and numero > 0:
                return numero
            else:
                print("Selecione uma opção válida.")
        except ValueError:
            print("Digite um numero")

def pedir_dados_corridas(corrida_atual=None):
    distancia_atual = None
    tempo_atual = None
    data_corrida_atual = None

    if corrida_atual is not None:
        distancia_atual = corrida_atual["distancia_km"]
        tempo_atual = corrida_atual["tempo_min"]
        if "data" in corrida_atual:
            data_corrida_atual = datetime.datetime.strptime(corrida_atual["data"], "%Y-%m-%d")

    
    distancia_km = pedir_decimal("Distancia em km: ", distancia_atual)
    tempo_min = pedir_decimal("Tempo em minutos: ", tempo_atual)       
    data = pedir_data("Data do treino (DD/MM/AAAA):", data_corrida_atual)
    data_texto = data.strftime("%Y-%m-%d")
    pace = calcular_pace(distancia_km,tempo_min)

    corrida = {
    "distancia_km" : distancia_km,
    "tempo_min" : tempo_min,
    "pace" : pace,
    "data" : data_texto
    }

    return corrida
##Formatar
def formatar_pace(pace):
    minutos = int(pace)
    segundos = round((pace - minutos)*60)

    if segundos == 60:
        minutos = minutos + 1
        segundos = 0
    return (f"{minutos}:{segundos:02d} min/km")

def formatar_tempo_total(tempo_total):
    if tempo_total < 60:
        return (f"Tempo total de corridas: {tempo_total} minutos")
    elif tempo_total >= 60:
        tempo_total_horas = int(tempo_total//60)
        tempo_total_minutos = int(tempo_total%60)
        tempo_total_segundos = round((tempo_total - int(tempo_total))*60)
        if tempo_total_segundos == 60:
            tempo_total_minutos = tempo_total_minutos + 1
            tempo_total_segundos = 0
        if tempo_total_minutos == 60:
            tempo_total_horas = tempo_total_horas + 1
            tempo_total_minutos = 0
    return (f"Tempo total em corridas: {tempo_total_horas:02d}:{tempo_total_minutos:02d}:{tempo_total_segundos:02d}")


### Calcular
def calcular_distancia_total(corridas):
    distancia_total = 0
    for corrida in corridas:
        distancia_total = distancia_total + corrida["distancia_km"]
    return distancia_total


def calcular_corridas(corridas):
    return len(corridas)

def calcular_pace(distancia_km, tempo_min):
    return tempo_min / distancia_km


def calcular_tempo_total(corridas):
    tempo_total = 0
    for corrida in corridas:
        tempo_total = tempo_total + corrida["tempo_min"]
    return tempo_total


def calcular_pace_medio(corridas):
    tempo_total = calcular_tempo_total(corridas)
    distancia_total = calcular_distancia_total(corridas)

    pace_medio =  tempo_total / distancia_total

    return pace_medio

def mostrar_resumo(corridas):
    if len(corridas)> 0:                        
        corridas_selecionadas = calcular_corridas(corridas)
        distancia_total_selecionada = calcular_distancia_total(corridas)
        tempo_total_selecionado = formatar_tempo_total(calcular_tempo_total(corridas))
        pace_medio_selecionado = formatar_pace(calcular_pace_medio(corridas))
                
        print(f"Corridas no período: {corridas_selecionadas}")
        print(f"Distancia total: {distancia_total_selecionada} km")
        print(tempo_total_selecionado)
        print(f"Pace médio: {pace_medio_selecionado}")                
    else:
        print("Nenhuma corrida encontrada nesse período.")

#BACKUP
def apagar_corridas(corridas, local_arquivo):
    try:        
        corridas_zerada = []
        salvar_corridas(corridas_zerada, local_arquivo)            
    except OSError:
        print("Ocorreu uma falha!")
        return corridas
    else:
        print("Corridas apagadas com sucesso!")
        return corridas_zerada


def salvar_corridas(corridas, local_arquivo):    
    arquivo_temporario = f"{local_arquivo}.tmp"
    try:
        with open(arquivo_temporario, "w", encoding="utf-8") as arquivo:
            json.dump(corridas, arquivo, indent=4)                   
        os.replace(arquivo_temporario, local_arquivo )
    except OSError:
        try:
            os.remove(arquivo_temporario)            
        except OSError:
            pass
        raise

def listar_corridas(corridas):
    if len(corridas) == 0:
        print("Sem corridas adicionadas.")
    else:
        for i in range(len(corridas)):
            texto_pace = formatar_pace(corridas[i]["pace"])
            if "data" in corridas[i]:
                data = datetime.datetime.strptime(corridas[i]["data"], "%Y-%m-%d")
                data_exibicao = data.strftime("%d/%m/%Y")
            else:
                data_exibicao = "Data não informada"

            print(f"{i+1} - {corridas[i]['distancia_km']} km | {corridas[i]['tempo_min']} min | {texto_pace} | Data: {data_exibicao}")

def listar_corrida(corrida_selecionada, numero_corrida):
    texto_pace = formatar_pace(corrida_selecionada["pace"])
    if "data" in corrida_selecionada:
        data = datetime.datetime.strptime(corrida_selecionada["data"], "%Y-%m-%d")
        data_exibicao = data.strftime("%d/%m/%Y")
    else:
        data_exibicao = "Data não informada"

    print(f"Corrida: {numero_corrida} - {corrida_selecionada['distancia_km']} km | {corrida_selecionada['tempo_min']} min | {texto_pace} | Data: {data_exibicao}")

##### Filtrar período
def filtrar_periodo(corridas, data_inicial, data_final):
    corridas_por_periodo = []
    for corrida in corridas:
        if "data" in corrida:
            data_corrida = datetime.datetime.strptime(corrida["data"], "%Y-%m-%d")
            if data_corrida >= data_inicial and data_corrida <= data_final:
                corridas_por_periodo.append(corrida)

    return corridas_por_periodo


#MENU
def mostrar_menu():
    print("1 - Adicionar corrida.")
    print("2 - Listar corridas. ")
    print("3 - Mostrar resumo das corridas")
    print("4 - Mostrar resumo por período")
    print("5 - Editar uma corrida")
    print("6 - Excluir uma corrida")
    print("7 - Zerar todas as corridas")
    print("8 - Restaurar backup")
    print("0 - Sair")

def checar_menu():
    while True:
        try:
            numero = int(input("Escolha uma opção: "))
            if numero < 9 and numero >= 0:
                return numero
            else:
                print("Selecione uma opção válida.")
        except ValueError:
            print("Digite um numero")



def carregar_corridas(local_arquivo, permitir_ausente=True):
    try:
        with open(local_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError("O arquivo deve conter uma lista de corridas")
            chaves_obrigatorias = ["distancia_km", "tempo_min", "pace"]
            for dado in dados:
                if not isinstance(dado, dict):
                    raise ValueError("Cada corrida da lista deve ser um dicionário.")  
                for chave in chaves_obrigatorias:
                    if chave not in dado:
                        raise ValueError(chave)
                    
                    valor = dado[chave]    
                    valores_permitidos = [int, float] 
                    if type(valor) not in valores_permitidos:
                        raise ValueError(f"{chave} deve ser um número.")
                    if not valor > 0:
                        raise ValueError(f"{chave} deve ser maior que zero")
                if "data" in dado:
                    if not isinstance(dado["data"], str):
                        raise ValueError("Data não esta em str")
                    try:
                        datetime.datetime.strptime(dado["data"], "%Y-%m-%d")
                    except ValueError:
                        raise ValueError("Data inválida")                    
            return dados
    except FileNotFoundError:
        if permitir_ausente == True:
            return []
        else:
            raise
    

def encontrar_backups(pasta_programa):
	nomes = os.listdir(pasta_programa)
	backups =[]
	for nome in nomes:
		caminho = os.path.join(pasta_programa, nome)	
		if nome.startswith("backup-") and nome.endswith(".json") and os.path.isfile(caminho):
			backups.append(nome)
	return backups





########################################################################################################################################################################

try:
    pasta_programa = os.path.dirname(__file__)
    local_arquivo = os.path.join(pasta_programa, "corridas.json")
    corridas = carregar_corridas(local_arquivo, permitir_ausente=True)
except json.JSONDecodeError:
    print("Não foi possível carregar as corridas. O arquivo contém um JSON inválido e o programa será encerrado.")
    raise SystemExit
except ValueError as erro:
    print(erro)
    raise SystemExit
except OSError:
    print("Não foi possível acessar o arquivo.")
    raise SystemExit



        

    
menu = -1

while menu != 0:
    mostrar_menu()
    menu = checar_menu()

     ########################            MENU 1
    if menu == 1:
        corrida = pedir_dados_corridas()

        corridas_atualizadas = corridas.copy()
        corridas_atualizadas.append(corrida)
        try:
            salvar_corridas(corridas_atualizadas, local_arquivo)            
        except OSError:
            print("Falha no salvamento. Operação cancelada.")
        else:
            corridas = corridas_atualizadas
            print("Salvo com sucesso.")
            listar_corrida(corrida, len(corridas))
            


        
    ######################################################## MENU 2
    elif menu == 2:
        listar_corridas(corridas)
    
    ############################################## MENU 3
    elif menu == 3:
        mostrar_resumo(corridas)
    ##################################################### MENU 6
    elif menu == 7:
        escolha = pedir_sim_não("Deseja zerar todas as corridas? (s/n): ")

        if escolha == "s":
            escolha_backup = pedir_sim_não("Deseja salvar um backup das corridas atuais? (s/n): ")

            if escolha_backup == "s":
                agora = datetime.datetime.now()
                nome_backup = f"backup-{agora.strftime("%Y-%m-%d_%H-%M-%S")}.json"
                caminho_backup = os.path.join(pasta_programa, nome_backup)

                try:
                    salvar_corridas(corridas, caminho_backup)
                    print(f"{nome_backup} salvo")
                except OSError:
                    print("Ocorreu um erro durante o salvamento!")
                    print("Operação cancelada.")
                else:
                    corridas = apagar_corridas(corridas, local_arquivo)

            elif escolha_backup == "n":
                escolha_sem_backup = pedir_sim_não("Deseja prosseguir sem salvar um backup? (s/n): ")

                if escolha_sem_backup == "s":
                    corridas = apagar_corridas(corridas, local_arquivo)
                else:
                    print("Operação cancelada")

        elif escolha == "n":
            print("Operação cancelada")
    ##################################################### MENU 4
    elif menu == 4:
        data_inicial = pedir_data("Data inicial (DD/MM/AAAA): ")
        data_final = pedir_data("Data final (DD/MM/AAAA): ")

        while data_inicial > data_final:
            print("Data inicial maior que data final:")
            data_inicial = pedir_data("Data inicial (DD/MM/AAAA): ")
            data_final = pedir_data("Data final (DD/MM/AAAA): ")

        selecionadas = filtrar_periodo(corridas, data_inicial, data_final)
        
        if len(selecionadas)> 0:                        
            mostrar_resumo(selecionadas)

            print("----------- Corridas no período -------------------")            
            listar_corridas(selecionadas)
        else:
            print("Nenhuma corrida encontrada nesse período.")
    ###################################################### MENU 5
    elif menu == 5:
        listar_corridas(corridas)
        if len(corridas)>0:
            numero_corrida = pedir_numero_item(len(corridas))
            indice_corrida = numero_corrida - 1 
            corrida_escolhida = corridas[indice_corrida]
            listar_corrida(corrida_escolhida, numero_corrida)
            print("Informe os novos dados da corrida: ")
            corrida_editada = pedir_dados_corridas(corrida_escolhida)
            listar_corrida(corrida_editada, numero_corrida)
            resposta = pedir_sim_não("Deseja salvar essa edição? (s/n): ")
            if resposta == "s":
                corridas_atualizadas = corridas.copy()
                corridas_atualizadas[indice_corrida] = corrida_editada
                try:
                    salvar_corridas(corridas_atualizadas, local_arquivo)            
                except OSError:
                    print("Falha no salvamento. Operação cancelada.")
                else:
                    corridas = corridas_atualizadas
                    print("Corrida editada com sucesso")
                    
            else:
                print("Operação cancelada")

    ###################################################### MENU 6
    elif menu == 6:
        listar_corridas(corridas)
        if len(corridas)>0:
            numero_corrida = pedir_numero_item(len(corridas))
            indice_corrida = numero_corrida - 1 
            corrida_escolhida = corridas[indice_corrida]
            listar_corrida(corrida_escolhida, numero_corrida)
            resposta = pedir_sim_não("Deseja excluir esta corrida? (s/n): ")
            if resposta == "s":
                corridas_atualizadas = corridas.copy()
                corridas_atualizadas.pop(indice_corrida)
                try:
                    salvar_corridas(corridas_atualizadas, local_arquivo)                    
                except OSError:
                    print("Erro. Operação cancelada.")
                else:
                    corridas = corridas_atualizadas
                    print("Exclusão confirmada")
            else:
                print("Operação cancelada")
    elif menu == 8:
        backups = encontrar_backups(pasta_programa)
        if len(backups) == 0:
            print("Nenhum backup encontrado.")
        else:
            for i in range(len(backups)):
                print(f"{i+1} - {backups[i]}")

            print("0 - Cancelar.")
            numero_backup = pedir_numero_item(len(backups), permitir_cancelar=True)
            

            if numero_backup == 0:
                print("Operação Cancelada.")
            else:
                nome_backup = backups[numero_backup - 1]
                caminho_backup = os.path.join(pasta_programa, nome_backup)
                try:
                    corridas_backup = carregar_corridas(caminho_backup, permitir_ausente=False)        
                except FileNotFoundError:
                    print("Backup não encontrado.")
                except json.JSONDecodeError:
                    print("Backup contém um json inválido.")
                except ValueError as erro:
                    print(erro)
                except OSError:
                    print("Não foi possível acessar o backup")

                else:
                    listar_corridas(corridas_backup)
                    resposta = pedir_sim_não("Restaurar este backup substituirá todas as corridas atuais. Continuar? (s/n): ")
                    if resposta == "s":
                        try:                            
                            salvar_corridas(corridas_backup, local_arquivo)
                        except OSError:
                            print("Falha na recuperação. Operação cancelada.")     
                        else:
                            corridas = corridas_backup
                            print("Backup restaurado com sucesso.")                       
                    else:
                        print("Operação cancelada.")
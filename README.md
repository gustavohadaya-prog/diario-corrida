# Diário de Corridas

Programa em Python para registrar treinos de corrida, acompanhar os resultados e consultar o histórico pelo terminal.

Projeto desenvolvido durante meus estudos de programação e fundamentos de computação.

## Funcionalidades

- Adicionar corridas com distância, tempo e data.
- Calcular o pace de cada corrida, em minutos por quilômetro.
- Listar as corridas registradas.
- Mostrar um resumo com quantidade de corridas, distância total, tempo total e pace médio.
- Filtrar corridas por um período, incluindo as datas inicial e final.
- Editar uma corrida, com a opção de pressionar Enter para manter os valores atuais.
- Excluir uma corrida após confirmação.
- Zerar todas as corridas, com a opção de criar um backup antes.
- Restaurar um backup, com prévia dos dados e confirmação da substituição.

## Tecnologias

- Python.
- Módulos da biblioteca padrão: `json`, `datetime` e `os`.
- Arquivos JSON para armazenar os dados.

O ambiente usado no desenvolvimento é Windows, Python 3.15 e VS Code. O programa não utiliza bibliotecas externas.

## Como executar

1. Abra a pasta do projeto no VS Code.
2. Abra o arquivo `diario_corrida.py`.
3. Execute esse arquivo com o interpretador Python instalado.
4. Escolha uma opção no menu do terminal. Para sair, digite `0`.

Informe as datas no formato `DD/MM/AAAA`. Para valores decimais, use ponto, como em `5.5`.

## Armazenamento dos dados

As corridas ficam em `corridas.json`, na mesma pasta de `diario_corrida.py`. Quando esse arquivo ainda não existe, o programa começa com uma lista vazia e cria o arquivo no primeiro salvamento.

O salvamento grava os dados em um arquivo temporário antes de substituir o arquivo de destino. As alterações na lista usada pelo programa são confirmadas após o salvamento bem-sucedido.

Os backups usam nomes como `backup-2026-10-30_19-18-01.json` e ficam na mesma pasta do programa. Restaurar um backup substitui a lista atual de corridas.

O `.gitignore` mantém os dados de uso, os backups e os arquivos temporários fora do histórico do Git.

## Próximas etapas

- Organizar o código e os testes.
- Separar a lógica do programa da interação com o usuário.
- Criar uma interface gráfica.
- Preparar uma versão executável para distribuição.

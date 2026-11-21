import os
import diario_corrida

pasta = os.path.dirname(__file__)
caminho = os.path.join(pasta, "corridas_teste_numero_finito.json")

try:
    corridas = diario_corrida.carregar_corridas(
        caminho, permitir_ausente=False
    )
except ValueError as erro:
    if str(erro) != "distancia_km deve ser um número finito.":
        raise AssertionError("Rejeição por outro motivo")
    print(f"Arquivo rejeitado: {erro}")
else:
    raise AssertionError("Valor infinito foi aceito indevidamente.")
    
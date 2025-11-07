import socket
import json
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import matplotlib
import matplotlib.pyplot as plt 
import threading

PORTA = 12345

def criarFrameRede(root):
    frameRede = ttk.LabelFrame(root)
    frameRede.pack(fill="x", padx=10, pady=5)

    ttk.Label(frameRede, text="IP do destino").pack(side=tk.LEFT, padx=5, pady=5)

    ipDestino = ttk.Entry(frameRede, width=40)
    ipDestino.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)

    botaoConectar = ttk.Button(frameRede, text="Conectar")
    botaoConectar.pack(side=tk.RIGHT, padx=5, pady=5)

    return {
        "ipDestino" : ipDestino,
        "botaoConectar" : botaoConectar
    }

def criarFrameMensagemOriginal(root):
    frameMensagemOriginal = ttk.LabelFrame(root)
    frameMensagemOriginal.pack(fill="x", padx=10, pady=5)

    ttk.Label(frameMensagemOriginal, text="Mensagem original").pack(side=tk.LEFT, padx=5, pady=5)

    mensagemOriginal = ttk.Entry(frameMensagemOriginal, width=40, state="disabled")
    mensagemOriginal.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)

    botaoCriptografar = ttk.Button(frameMensagemOriginal, text="Criptografar", state="disabled")
    botaoCriptografar.pack(side=tk.RIGHT, padx=5, pady=5)

    return {
        "mensagemOriginal" : mensagemOriginal,
        "botaoCriptografar" : botaoCriptografar
    }

def criarFrameMensagemCriptografada(root):
    FrameMensagemCriptografada = ttk.LabelFrame(root)
    FrameMensagemCriptografada.pack(fill="x", padx=10, pady=5)

    ttk.Label(FrameMensagemCriptografada, text="Mensagem criptografada").pack(side=tk.LEFT, padx=5, pady=5)

    mensagemCriptografada = ttk.Entry(FrameMensagemCriptografada, width=40, state="disabled")
    mensagemCriptografada.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)

    botaoBinario = ttk.Button(FrameMensagemCriptografada, text="Converter para binário", state="disabled")
    botaoBinario.pack(side=tk.RIGHT, padx=5, pady=5)

    return {
        "mensagemCriptografada" : mensagemCriptografada,
        "botaoBinario" : botaoBinario
    }

def criarFrameMensagemBinario(root):
    FrameMensagemBinario = ttk.LabelFrame(root)
    FrameMensagemBinario.pack(fill="x", padx=10, pady=5)

    ttk.Label(FrameMensagemBinario, text="Mensagem Binario").pack(side=tk.LEFT, padx=5, pady=5)

    mensagemBinario = ttk.Entry(FrameMensagemBinario, width=40, state="disabled")
    mensagemBinario.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)

    botaoAlgoritmo = ttk.Button(FrameMensagemBinario, text="Aplicar Algoritmo", state="disabled")
    botaoAlgoritmo.pack(side=tk.RIGHT, padx=5, pady=5)

    return {
        "mensagemBinario" : mensagemBinario,
        "botaoAlgoritmo" : botaoAlgoritmo
    }

def criarFrameMensagemAlgoritmo(root):
    FrameMensagemAlgoritmo = ttk.LabelFrame(root)
    FrameMensagemAlgoritmo.pack(fill="x", padx=10, pady=5)

    ttk.Label(FrameMensagemAlgoritmo, text="Binario do Algoritmo").pack(side=tk.LEFT, padx=5, pady=5)

    mensagemAlgoritmo = ttk.Entry(FrameMensagemAlgoritmo, width=40, state="disabled")
    mensagemAlgoritmo.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)

    botaoGrafico = ttk.Button(FrameMensagemAlgoritmo, text="Gerar Gráfico", state="disabled")
    botaoGrafico.pack(side=tk.RIGHT, padx=5, pady=5)

    return {
        "mensagemAlgoritmo" : mensagemAlgoritmo,
        "botaoGrafico" : botaoGrafico
    }


def onBotaoConectar(widgets):
    ipTexto = widgets["ipDestino"].get().strip()

    if not ipTexto:
        print("Ip não digitado")
        return

    threadConexao = threading.Thread(target=threadConectar, args=(widgets, ipTexto))
    threadConexao.daemon = True
    threadConexao.start()

def onBotaoCriptografar(widgets):
    print("Clicado criptografar")

    mensagemOriginal = widgets["mensagemOriginal"]
    mensagemCriptografada = widgets["mensagemCriptografada"]

    textoOriginal = mensagemOriginal.get().strip()

    if not textoOriginal:
        print("Nada para criptografar")
        return

    textoCriptografado = criptografarMensagem(textoOriginal)

    mensagemCriptografada.config(state='normal')
    mensagemCriptografada.delete(0, tk.END)
    mensagemCriptografada.insert(tk.END, textoCriptografado)

    mensagemOriginal.config(state="disabled")

    widgets["botaoCriptografar"].config(state="disabled") 
    widgets["botaoBinario"].config(state="normal")      

def onBotaoBinario(widgets):
    print("Clicado converter para binario")

    mensagemCriptografada = widgets["mensagemCriptografada"]
    mensagemBinario = widgets["mensagemBinario"]

    textoCriptografado = mensagemCriptografada.get().strip()

    if not textoCriptografado:
        print("Nada para conveter em binario")
        return

    textoBinario = converteMensagemCriptografadaEmBinario(textoCriptografado)

    mensagemBinario.config(state='normal')
    mensagemBinario.delete(0, tk.END)
    mensagemBinario.insert(tk.END, textoBinario)

    mensagemCriptografada.config(state="disabled")     
    widgets["botaoBinario"].config(state="disabled") 
    widgets["botaoAlgoritmo"].config(state="normal") 

def onBotaoAlgoritmo(widgets):
    print("clicado no botão algoritmo")

    mensagemBinarioWidget = widgets["mensagemBinario"]
    textoBinario = mensagemBinarioWidget.get().strip()

    if not textoBinario:
        print("Nada para aplicar algoritmo")
        return

    sinalCodificado = aplicarAlgoritmo(textoBinario) 

    sinalString = ",".join(map(str, sinalCodificado)) 

    mensagemAlgoritmoWidget = widgets["mensagemAlgoritmo"]
    mensagemAlgoritmoWidget.config(state='normal')
    mensagemAlgoritmoWidget.delete(0, tk.END)
    mensagemAlgoritmoWidget.insert(tk.END, sinalString)

    mensagemBinarioWidget.config(state='disabled') 
    widgets["botaoAlgoritmo"].config(state='disabled') 
    widgets["botaoGrafico"].config(state='normal') 

def onBotaoGrafico(widgets):
    print("Clicado: Gerar Gráfico")
    
    sinalString = widgets["mensagemAlgoritmo"].get().strip()
    if not sinalString:
        print("Nada para gerar o gráfico")
        return
        
    try:
        pontos = [int(p) for p in sinalString.split(',')]
        
        gerarGrafico(pontos)
        print("Gráfico 'sinal_manchester.png' salvo com sucesso!")
        
    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")
        
    widgets["mensagemAlgoritmo"].config(state='disabled')
    widgets["botaoGrafico"].config(state='disabled')

def criarInterfaceGrafica():
    root = tk.Tk()
    root.title("Codificação de Linha")
    root.geometry("1600x900")

    widgets = {}

    widgetsRede = criarFrameRede(root)
    widgets.update(widgetsRede)

    widgetsMensagemOriginal = criarFrameMensagemOriginal(root)
    widgets.update(widgetsMensagemOriginal)

    widgetsMensagemCriptografada = criarFrameMensagemCriptografada(root)
    widgets.update(widgetsMensagemCriptografada)

    widgetsMensagemBinario = criarFrameMensagemBinario(root)
    widgets.update(widgetsMensagemBinario)

    widgetsMensagemAlgoritmo = criarFrameMensagemAlgoritmo(root)
    widgets.update(widgetsMensagemAlgoritmo)

    botaoConectar = widgets["botaoConectar"]
    botaoCriptografar = widgets["botaoCriptografar"]
    botaoBinario = widgets["botaoBinario"]
    botaoAlgoritmo = widgets["botaoAlgoritmo"]
    botaoGrafico = widgets["botaoGrafico"]

    botaoConectar.config(
        command=lambda : onBotaoConectar(widgets)
    )
    
    botaoCriptografar.config(
        command=lambda : onBotaoCriptografar(widgets)
    )

    botaoBinario.config(
        command=lambda : onBotaoBinario(widgets)
    )
    
    botaoAlgoritmo.config(
        command=lambda : onBotaoAlgoritmo(widgets)
    )

    botaoGrafico.config (
        command=lambda : onBotaoGrafico(widgets)
    )

    return root

def threadConectar(widgets, ipTexto):
    clienteSocket = conectarAoServidor(ipTexto)

    if clienteSocket:
        widgets["socketCliente"] = clienteSocket
        widgets["ipDestino"].config(state="disabled")
        widgets["botaoConectar"].config(state="disabled")

        widgets["mensagemOriginal"].config(state="normal")
        widgets["botaoCriptografar"].config(state="normal")
    else:
        print("Falha na conexao.")

def conectarAoServidor(mensagem):
    print(f"Tentando conectar ao IP: {mensagem} na porta {PORTA}")
    
    try:
        clienteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clienteSocket.settimeout(5.0)
        clienteSocket.connect((mensagem, PORTA))

        print("CONECTADO COM SUCESSO")

        return clienteSocket
    except socket.timeout:
        print("Tempo esgotado")
    except socket.error as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro: {e}")

def criptografarMensagem(mensagem):
    chave = "segredo"

    bytesMensagem = mensagem.encode('latin-1')
    bytesChave = chave.encode('latin-1')

    listaBytesCriptografado = []

    for i in range(len(bytesMensagem)):
        byteMensagem = bytesMensagem[i]
        byteChave = bytesChave[i % len(bytesChave)]

        byteCriptografado = (byteMensagem + byteChave) % 256
        listaBytesCriptografado.append(byteCriptografado)
    
    textoCriptografado = bytes(listaBytesCriptografado).decode('latin-1')
    return textoCriptografado

def converteMensagemCriptografadaEmBinario(mensagemCriptografada):
    bytesMensagem = mensagemCriptografada.encode('latin-1')
    binarioMensagem = ""

    for b in bytesMensagem:
        binarioMensagem += format(b, '08b')

    return binarioMensagem

def aplicarAlgoritmo(mensagemBinaria):
    sinalCodificado = []

    for bit in mensagemBinaria:
        if bit == '0':
            sinalCodificado.extend([1, -1])
        elif bit == '1':
            sinalCodificado.extend([-1, 1])
        else:
            pass
    return sinalCodificado

def gerarGrafico(pontos):
    if not pontos:
        print("Não há pontos para gerar o gráfico.")
        return

    pontos_x = [i * 0.5 for i in range(len(pontos))]

    plt.figure(figsize=(15, 4))
    plt.plot(pontos_x, pontos, drawstyle='steps-post', color='red')

    plt.title("Sinal Manchester (Codificado)")
    plt.xlabel("Tempo (em unidades de bit)")
    plt.ylabel("Nível de Tensão")
    plt.ylim(-1.5, 1.5) 
    plt.grid(True) 
    
    bits_totais = len(pontos) // 2
    for i in range(bits_totais + 1):
        plt.axvline(i, color='gray', linestyle='--', linewidth=0.5)

    nome_arquivo = "sinal_manchester.png"
    plt.savefig(nome_arquivo)
    
    plt.close()

def main():
    root = criarInterfaceGrafica()
    root.mainloop()

if __name__ == '__main__':
    main()
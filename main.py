import socket
import json
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import matplotlib
import matplotlib.pyplot as plt 
import threading
from PIL import Image, ImageTk
import os

PORTA = 12345

def criarFrameRede(root):
    frameRede = ttk.LabelFrame(root)
    frameRede.pack(fill="x", padx=10, pady=5)

    ttk.Label(frameRede, text="IP do destino").pack(side=tk.LEFT, padx=5, pady=5)

    ipDestino = ttk.Entry(frameRede, width=40)
    ipDestino.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)


    botaoServidor = ttk.Button(frameRede, text="Iniciar Servidor")
    botaoServidor.pack(side=tk.RIGHT, padx=5, pady=5)

    botaoConectar = ttk.Button(frameRede, text="Conectar")
    botaoConectar.pack(side=tk.RIGHT, padx=5, pady=5)

    return {
        "ipDestino" : ipDestino,
        "botaoConectar" : botaoConectar,
        "botaoServidor" : botaoServidor 
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

    botaoDescriptografar = ttk.Button(FrameMensagemCriptografada, text="Descriptografar", state="disabled")
    botaoDescriptografar.pack(side=tk.RIGHT, padx=5)

    botaoBinario = ttk.Button(FrameMensagemCriptografada, text="Converter para binário", state="disabled")
    botaoBinario.pack(side=tk.RIGHT, padx=5, pady=5)

    return {
        "mensagemCriptografada" : mensagemCriptografada,
        "botaoBinario" : botaoBinario,
        "botaoDescriptografar" : botaoDescriptografar 
    }

def criarFrameMensagemBinario(root):
    FrameMensagemBinario = ttk.LabelFrame(root)
    FrameMensagemBinario.pack(fill="x", padx=10, pady=5)

    ttk.Label(FrameMensagemBinario, text="Mensagem Binario").pack(side=tk.LEFT, padx=5, pady=5)

    mensagemBinario = ttk.Entry(FrameMensagemBinario, width=40, state="disabled")
    mensagemBinario.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)

    botaoConverterTexto = ttk.Button(FrameMensagemBinario, text="Converter p/ Texto", state="disabled")
    botaoConverterTexto.pack(side=tk.RIGHT, padx=5)

    botaoAlgoritmo = ttk.Button(FrameMensagemBinario, text="Aplicar Algoritmo", state="disabled")
    botaoAlgoritmo.pack(side=tk.RIGHT, padx=5, pady=5)

    return {
        "mensagemBinario" : mensagemBinario,
        "botaoAlgoritmo" : botaoAlgoritmo,
        "botaoConverterTexto" : botaoConverterTexto 
    }

def criarFrameMensagemAlgoritmo(root):
    FrameMensagemAlgoritmo = ttk.LabelFrame(root)
    FrameMensagemAlgoritmo.pack(fill="x", padx=10, pady=5)

    ttk.Label(FrameMensagemAlgoritmo, text="Sinal Codificado").pack(side=tk.LEFT, padx=5, pady=5)

    mensagemAlgoritmo = ttk.Entry(FrameMensagemAlgoritmo, width=40, state="disabled")
    mensagemAlgoritmo.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)

    botaoDecodificarSinal = ttk.Button(FrameMensagemAlgoritmo, text="Decodificar Sinal", state="disabled")
    botaoDecodificarSinal.pack(side=tk.RIGHT, padx=5)

    botaoGrafico = ttk.Button(FrameMensagemAlgoritmo, text="Gerar Gráfico", state="disabled")
    botaoGrafico.pack(side=tk.RIGHT, padx=5, pady=5)

    return {
        "mensagemAlgoritmo" : mensagemAlgoritmo,
        "botaoGrafico" : botaoGrafico,
        "botaoDecodificarSinal" : botaoDecodificarSinal # Adicionado ao dict
    }

def criarFrameGrafico(root):
    frameGrafico = ttk.LabelFrame(root)
    frameGrafico.pack(fill="x", padx=10, pady=5)

    labelGrafico = ttk.Label(frameGrafico, anchor="center", justify="center")
    labelGrafico.pack(pady=10)

    botaoEnviarSinal = ttk.Button(frameGrafico, text="Enviar Sinal", state="disabled")
    botaoEnviarSinal.pack(pady=10)

    return {
        "labelGrafico" : labelGrafico,
        "botaoEnviarSinal" : botaoEnviarSinal
    }


def onBotaoConectar(widgets):
    ipTexto = widgets["ipDestino"].get().strip()

    if not ipTexto:
        print("Ip não digitado")
        return

    threadConexao = threading.Thread(target=threadConectar, args=(widgets, ipTexto))
    threadConexao.daemon = True
    threadConexao.start()


def onBotaoServidor(widgets):
    print("Clicado para iniciar servidor")

    widgets["botaoConectar"].config(state="disabled")
    widgets["ipDestino"].config(state="disabled")

    threadServer = threading.Thread(target=threadServidor, args=(widgets,))
    threadServer.daemon = True
    threadServer.start()    

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

    mensagemBinario = widgets["mensagemBinario"]
    textoBinario = mensagemBinario.get().strip()

    if not textoBinario:
        print("Nada para aplicar algoritmo")
        return

    sinalCodificado = aplicarAlgoritmo(textoBinario) 

    sinalString = ",".join(map(str, sinalCodificado)) 

    mensagemAlgoritmo = widgets["mensagemAlgoritmo"]
    mensagemAlgoritmo.config(state='normal')
    mensagemAlgoritmo.delete(0, tk.END)
    mensagemAlgoritmo.insert(tk.END, sinalString)

    mensagemBinario.config(state='disabled') 
    widgets["botaoAlgoritmo"].config(state='disabled') 
    widgets["botaoGrafico"].config(state='normal') 

def onBotaoGrafico(widgets):
    print("Clicado: Gerar Gráfico")
    
    sinalString = widgets["mensagemAlgoritmo"].get().strip()
    labelGrafico = widgets["labelGrafico"] 
    if not sinalString:
        print("Nada para gerar o gráfico")
        return
        
    try:
        pontos = [int(p) for p in sinalString.split(',')]
        
        nomeArquivo = "sinal_manchester.png"

        gerarGrafico(pontos, nomeArquivo)
        print("Gráfico 'sinal_manchester.png' salvo com sucesso!")

        caminhoCompleto = os.path.abspath(nomeArquivo)
        imagem = Image.open(caminhoCompleto)

        foto = ImageTk.PhotoImage(imagem)
        labelGrafico.config(image=foto)

        labelGrafico.image = foto
        
    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")
        
    widgets["mensagemAlgoritmo"].config(state='disabled')
    widgets["botaoGrafico"].config(state='disabled')
    widgets["botaoEnviarSinal"].config(state="normal")

def onBotaoEnviarSinal(widgets):
    print("Clicado para enviar sinal")

    textoSinal = widgets["mensagemAlgoritmo"].get().strip()

    if not textoSinal:
        print("Não há sinal para ser enviado")
        return

    try:
        sinalCodificado = [int(p) for p in textoSinal.split(',')]

        dadosParaEnviar = json.dumps(sinalCodificado).encode('utf-8')

        socketCliente = widgets["socketCliente"]
        socketCliente.sendall(dadosParaEnviar)
        print("Sinal enviado")
    
    except KeyError:
        print("Erro: Socket não encontrado. Conecte primeiro.")
    except socket.error as e:
        print(f"Erro ao enviar: {e}")
    except Exception as e:
        print(f"Erro ao empacotar dados: {e}")

    widgets["ipDestino"].config(state="normal")
    widgets["botaoConectar"].config(state="normal")
    
    widgets["mensagemOriginal"].config(state='disabled') 

    widgets["mensagemCriptografada"].config(state='normal')
    widgets["mensagemCriptografada"].config(state='disabled')
    
    widgets["mensagemBinario"].config(state='normal')
    widgets["mensagemBinario"].config(state='disabled')
    
    widgets["mensagemAlgoritmo"].config(state='normal')
    widgets["mensagemAlgoritmo"].config(state='disabled')

def onBotaoDecodificarSinal(widgets):
    print("Clicado: Decodificar Sinal")
    
    mensagemAlgoritmo = widgets["mensagemAlgoritmo"]
    sinalString = mensagemAlgoritmo.get().strip()

    if not sinalString: 
        return
    
    try:
        sinalCodificado = [int(p) for p in sinalString.split(',')]
        
        textoBinario = decodificarAlgoritmo(sinalCodificado)
        
        widgets["mensagemBinario"].config(state='normal')
        widgets["mensagemBinario"].delete(0, tk.END)
        widgets["mensagemBinario"].insert(0, textoBinario)

        mensagemAlgoritmo.config(state='disabled')         
        widgets["botaoConverterTexto"].config(state='normal')
        widgets["botaoDecodificarSinal"].config(state='disabled')
        
    except Exception as e:
        print(f"Erro ao decodificar: {e}")

def onBotaoConverterTexto(widgets):
    print("Clicado: Converter para Texto")
    
    mensagemBinario = widgets["mensagemBinario"]
    textoBinario = mensagemBinario.get().strip()
    if not textoBinario: 
        return
    
    textoCriptografado = converterBinarioParaMensagemCriptografada(textoBinario)
    
    widgets["mensagemCriptografada"].config(state='normal')
    widgets["mensagemCriptografada"].delete(0, tk.END)
    widgets["mensagemCriptografada"].insert(0, textoCriptografado)
    
    mensagemBinario.config(state='disabled') 
    widgets["botaoDescriptografar"].config(state='normal')
    widgets["botaoConverterTexto"].config(state='disabled')

def onBotaoDescriptografar(widgets):
    print("Clicado: Descriptografar")
    
    mensagemCriptografada = widgets["mensagemCriptografada"]
    textoCriptografado = mensagemCriptografada.get().strip()
    
    if not textoCriptografado: 
        return
    
    textoOriginal = descriptografarMensagem(textoCriptografado)
    
    widgets["mensagemOriginal"].config(state='normal')
    widgets["mensagemOriginal"].delete(0, tk.END)
    widgets["mensagemOriginal"].insert(0, textoOriginal)

    mensagemCriptografada.config(state='disabled')     
    widgets["botaoDescriptografar"].config(state='disabled')

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

    widgetsGrafico = criarFrameGrafico(root)
    widgets.update(widgetsGrafico)

    botaoConectar = widgets["botaoConectar"]
    botaoCriptografar = widgets["botaoCriptografar"]
    botaoBinario = widgets["botaoBinario"]
    botaoAlgoritmo = widgets["botaoAlgoritmo"]
    botaoGrafico = widgets["botaoGrafico"]
    botaoEnviarSinal = widgets["botaoEnviarSinal"] 
    botaoServidor = widgets["botaoServidor"]
    
    botaoDecodificarSinal = widgets["botaoDecodificarSinal"]
    botaoConverterTexto = widgets["botaoConverterTexto"]
    botaoDescriptografar = widgets["botaoDescriptografar"]

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

    botaoEnviarSinal.config (
        command=lambda : onBotaoEnviarSinal(widgets)
    )

    botaoServidor.config(
        command=lambda : onBotaoServidor(widgets)
    )

    botaoServidor.config(
        command=lambda : onBotaoServidor(widgets)
    )

    botaoDecodificarSinal.config(
        command=lambda : onBotaoDecodificarSinal(widgets)
    )

    botaoConverterTexto.config(
        command=lambda : onBotaoConverterTexto(widgets)
    )

    botaoDescriptografar.config(
        command=lambda : onBotaoDescriptografar(widgets)
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

def threadServidor(widgets):
    botaoServidor = widgets["botaoServidor"]
    botaoServidor.config(state="disabled", text="Servidor Rodando...")

    dadosRecebidos = iniciarServidor()

    if dadosRecebidos:
        print(f"Dados Recebidos: {dadosRecebidos[:50]}...")
        try:
            
            stringSinal = dadosRecebidos.decode('utf-8')
            sinalCodificado = json.loads(stringSinal)

            textoSinal = ",".join(map(str, sinalCodificado))
            
            widgets["mensagemAlgoritmo"].config(state='normal')
            widgets["mensagemAlgoritmo"].delete(0, tk.END)
            widgets["mensagemAlgoritmo"].insert(0, textoSinal)
            widgets["mensagemAlgoritmo"].config(state='disabled')

            widgets["botaoDecodificarSinal"].config(state='normal')
            
            print("Dados recebidos e inseridos na GUI. Pronto para decodificar.")

        except json.JSONDecodeError:
            print("Erro fatal: Os dados recebidos não são um JSON válido.")
        except Exception as e:
            print(f"Erro ao processar dados recebidos: {e}")
    else:
        print("Os dados não foram mandados")

    botaoServidor.config(state="normal", text="Iniciar Servidor")


def iniciarServidor():
    servidorSocket = None
    try:
        servidorSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidorSocket.bind(('0.0.0.0', PORTA))
        servidorSocket.listen(1)
        print(f"Servidor iniciado na porta {PORTA}. Esperando conexão...")

        conn, addr = servidorSocket.accept()
        
        with conn:
            print(f"Conexão recebida de {addr}")
            dadosRecebidos = conn.recv(4096)
            if dadosRecebidos:
                return dadosRecebidos
            else:
                print("Cliente conectou mas não enviou dados.")
                return None

    except Exception as e:
        print(f"Erro no servidor: {e}")
        return None
    finally:
        if servidorSocket:
            servidorSocket.close()
            print("Servidor fechado.")

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

def gerarGrafico(pontos, nomeArquivo):
    if not pontos:
        print("Não há pontos para gerar o gráfico.")
        return
    
    pontos_x = [i * 0.5 for i in range(len(pontos))]

    bits_totais = len(pontos) // 2
    pontos_x.append(bits_totais)

    pontos.append(pontos[-1])

    plt.figure(figsize=(15, 4))
    plt.plot(pontos_x, pontos, drawstyle='steps-post', color='red')

    plt.title("Sinal Manchester (Codificado)")
    plt.xlabel("Tempo (em unidades de bit)")
    plt.ylabel("Nível de Tensão")
    plt.ylim(-1.5, 1.5) 
    plt.grid(True) 
    
    for i in range(bits_totais + 1):
        plt.axvline(i, color='gray', linestyle='--', linewidth=0.5)

    plt.savefig(nomeArquivo)
    
    plt.close()

def decodificarAlgoritmo(sinalCodificado):
    mensagemBinaria = ""

    for i in range(0, len(sinalCodificado), 2):
        
        parDeNiveis = sinalCodificado[i:i+2]

        if parDeNiveis == [1, -1]:
            mensagemBinaria += "0"
        elif parDeNiveis == [-1, 1]:
            mensagemBinaria += "1"
        else:
            pass
            
    return mensagemBinaria

def converterBinarioParaMensagemCriptografada(mensagem):
    textoMensagem = ""

    for i in range(0, len(mensagem), 8):
        byteString = mensagem[i:i+8]
        if len(byteString) == 8:
            valorByte = int(byteString, 2)
            textoMensagem += chr(valorByte)

    return textoMensagem

def descriptografarMensagem(mensagemCriptografada):
    chave = "segredo"

    bytesCripto = mensagemCriptografada.encode('latin-1')
    bytesChave = chave.encode('latin-1')

    listaBytesOriginais = []

    for i in range(len(bytesCripto)):
        byteCripto = bytesCripto[i]
        byteChave = bytesChave[i % len(bytesChave)]

        byteOriginal = (byteCripto - byteChave + 256) % 256
        listaBytesOriginais.append(byteOriginal)
    
    textoOriginal = bytes(listaBytesOriginais).decode('latin-1')
    return textoOriginal

def main():
    root = criarInterfaceGrafica()
    root.mainloop()

if __name__ == '__main__':
    main()
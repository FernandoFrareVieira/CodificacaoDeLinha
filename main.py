import socket
import json
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import matplotlib

def criarFrameRede(root):
    # O layout está como o seu, apenas renomeei o botão
    frameRede = ttk.LabelFrame(root, text="FrameRede")
    frameRede.pack(fill="x", padx=10, pady=5)

    ttk.Label(frameRede, text="IP do destino").pack(side=tk.LEFT, padx=5, pady=5)

    ipDestino = ttk.Entry(frameRede, width=40)
    ipDestino.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)

    # MUDANÇA: Renomeado para 'botaoConectar' e texto atualizado
    botaoConectar = ttk.Button(frameRede, text="Conectar")
    botaoConectar.pack(side=tk.RIGHT, padx=5, pady=5)

    return {
        "ipDestino" : ipDestino,
        "botaoConectar" : botaoConectar # MUDANÇA: Chave atualizada
    }

def criarFrameEmissor(root):
    frameEmissor = ttk.LabelFrame(root, text="FrameEmissor")
    frameEmissor.pack(fill='x', padx=10, pady=5)

    frameMensagem = ttk.Frame(frameEmissor)
    frameMensagem.pack(fill='x', padx=5, pady=5)
    
    ttk.Label(frameMensagem, text="Mensagem original:").pack(side=tk.LEFT, padx=5)
    
    mensagemOriginal = scrolledtext.ScrolledText(frameMensagem, height=3, width=60)
    mensagemOriginal.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
    
    botaoMandarCriptografar = ttk.Button(frameMensagem, text="Criptografar")
    botaoMandarCriptografar.pack(side=tk.RIGHT, padx=5)

    frameCripto = ttk.Frame(frameEmissor)
    frameCripto.pack(fill='x', padx=5, pady=5)

    ttk.Label(frameCripto, text="Texto Criptografado:").pack(side=tk.LEFT, padx=5)
    
    textoCriptografado = scrolledtext.ScrolledText(frameCripto, height=3, width=60, state='disabled')
    textoCriptografado.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
    
    frameBinario = ttk.Frame(frameEmissor)
    frameBinario.pack(fill='x', padx=5, pady=5)

    ttk.Label(frameBinario, text="Sequência Binária:").pack(side=tk.LEFT, padx=5)
    
    textoBinario = scrolledtext.ScrolledText(frameBinario, height=3, width=60, state='disabled')
    textoBinario.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
    
    botaoBinario = ttk.Button(frameBinario, text="Converter")
    botaoBinario.pack(side=tk.RIGHT, padx=5)

    botaoEnviar = ttk.Button(frameEmissor, text="Enviar para destino")
    botaoEnviar.pack(pady=10)

    return {
        "mensagemOriginal" : mensagemOriginal,
        "textoCriptografado" : textoCriptografado,
        "textoBinario" : textoBinario,
        "botaoMandarCriptografar" : botaoMandarCriptografar, # MUDANÇA
        "botaoBinario" : botaoBinario,
        "botaoEnviar" : botaoEnviar
    }

def onBotaoConectar(widgets):
    """Callback para o botão 'Conectar'."""
    print("Clicado: Conectar")
    ipWidget = widgets["ipDestino"]
    ipTexto = ipWidget.get().strip()
    
    if not ipTexto:
        print("Erro: IP de destino não pode estar vazio.")
        return
        
    print(f"Tentando conectar ao IP: {ipTexto}...")

def onBotaoMandarCriptografar(widgets):
    """Lê a msg original, criptografa e põe no campo 'textoCriptografado'."""
    print("Clicado: Criptografar")

    msgWidget = widgets["mensagemOriginal"]
    criptoWidget = widgets["textoCriptografado"]

    texto = msgWidget.get("1.0", tk.END).strip()
    if not texto:
        print("Nada para criptografar.")
        return

    chave = "segredo"
    criptoTexto = "".join(chr(ord(c) ^ ord(chave[i % len(chave)])) for i, c in enumerate(texto))

    criptoWidget.config(state='normal')
    
    # --- CORREÇÃO AQUI ---
    criptoWidget.delete("1.0", tk.END) # Deve ser "1.0" e não "1.G"
    # --- FIM DA CORREÇÃO ---
    
    criptoWidget.insert(tk.END, criptoTexto)
    criptoWidget.config(state='disabled')
    
    msgWidget.delete("1.0", tk.END)
    
    msgWidget.delete("1.0", tk.END)

def onBotaoBinario(widgets):
    """Lê o texto criptografado, converte e põe no campo 'textoBinario'."""
    print("Clicado: Converter")
    criptoWidget = widgets["textoCriptografado"]
    binarioWidget = widgets["textoBinario"]

    texto = criptoWidget.get("1.0", tk.END).strip()
    if not texto:
        print("Nada para converter (campo criptografado vazio).")
        return

    try:
        binarioTexto = "".join(format(b, '08b') for b in texto.encode('latin-1'))
    except Exception as e:
        binarioTexto = f"ERRO: {e}"

    binarioWidget.config(state='normal')
    binarioWidget.delete("1.0", tk.END)
    binarioWidget.insert(tk.END, binarioTexto)
    binarioWidget.config(state='disabled')

def onBotaoEnviar(widgets):
    """Lê o IP e o texto binário final para enviar."""
    print("Clicado: Enviar")
    ipWidget = widgets["ipDestino"]
    binarioWidget = widgets["textoBinario"]

    ipTexto = ipWidget.get().strip()
    binarioTexto = binarioWidget.get("1.0", tk.END).strip()

    if not ipTexto or not binarioTexto:
        print("Erro: IP ou dados binários estão faltando.")
        return
        
    print(f"Enviando dados para: {ipTexto}")
    print(f"Dados (primeiros 50 chars): {binarioTexto[:50]}...")
        
    binarioWidget.config(state='normal')
    binarioWidget.delete("1.0", tk.END)
    binarioWidget.config(state='disabled')
    
    criptoWidget = widgets["textoCriptografado"]
    criptoWidget.config(state='normal')
    criptoWidget.delete("1.0", tk.END)
    criptoWidget.config(state='disabled')


def criarInterfaceGrafica():
    root = tk.Tk()
    root.title("Codificação de Linha")
    root.geometry("1600x900")

    widgets = {}

    widgetsRede = criarFrameRede(root)
    widgets.update(widgetsRede)

    widgetsEmissor = criarFrameEmissor(root)
    widgets.update(widgetsEmissor)

    # --- Conecta TODOS os botões ---
    widgets["botaoConectar"].config(
        command=lambda : onBotaoConectar(widgets)
    )

    widgets["botaoMandarCriptografar"].config(
        command=lambda : onBotaoMandarCriptografar(widgets)
    )
    
    widgets["botaoBinario"].config(
        command=lambda : onBotaoBinario(widgets)
    )

    widgets["botaoEnviar"].config(
        command=lambda : onBotaoEnviar(widgets)
    )

    return root

def main():
    root = criarInterfaceGrafica()
    root.mainloop()

if __name__ == '__main__':
    main()
import tkinter as tk
from tkinter import messagebox
import subprocess
import datetime
import threading
import time
import os
import re
from tkinter import ttk

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Tarefas")
        

        self.caminho_app = tk.StringVar()
        self.chave = tk.StringVar()
        self.versao = tk.StringVar()
        self.dados = []  # Lista para armazenar os dados monitorados
        self.pagina_atual = 0
        self.itens_por_pagina = 20
        self.monitorando = False
        self.processo = None
        self.tempos_execucao = []
        

        # Campos de entrada
        self.label_caminho = tk.Label(self.root, text="Caminho do Aplicativo:")
        self.entry_caminho = tk.Entry(self.root, width=50, textvariable=self.caminho_app)

        self.label_chave = tk.Label(self.root, text="Palavra/Frase Chave:")
        self.entry_chave = tk.Entry(self.root, width=50, textvariable=self.chave)

        self.label_versao = tk.Label(self.root, text="Versão do Aplicativo:")
        self.entry_versao = tk.Entry(self.root, width=20, textvariable=self.versao)


        # Botão de iniciar
        self.botao_iniciar = tk.Button(self.root, text="Iniciar Monitoramento", command=self.iniciar_monitoramento)

        # Tabela (Treeview)
        self.colunas = ("Data Início", "Identificador", "Versão do aplicativo", "Captura", "Data Fim")
        self.tabela = ttk.Treeview(self.root, columns=self.colunas, show="headings")
        for col in self.colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=150, stretch=tk.YES) # Ajustar largura e permitir expansão

        # Labels para informações de paginação
        self.label_pagina = tk.Label(self.root, text=f"Página {self.pagina_atual + 1}")
        self.botao_anterior = tk.Button(self.root, text="Anterior", command=self.pagina_anterior)
        self.botao_proximo = tk.Button(self.root, text="Próximo", command=self.pagina_proximo)

        # Botão de finalizar
        self.botao_finalizar = tk.Button(self.root, text="Finalizar Monitoramento", command=self.finalizar_monitoramento, state=tk.DISABLED)

        # Label para exibir o intervalo médio
        self.label_intervalo = tk.Label(self.root, text="Intervalo médio: Aguardando finalização...")

        # Layout (usando grid)
        self.label_caminho.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_caminho.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        self.label_chave.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_chave.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        self.label_versao.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_versao.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.botao_iniciar.grid(row=3, column=0, columnspan=4, pady=10)

        self.tabela.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        self.botao_anterior.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        self.label_pagina.grid(row=5, column=1, padx=5, pady=5)
        self.botao_proximo.grid(row=5, column=2, padx=5, pady=5, sticky="ew")
        self.botao_finalizar.grid(row=5, column=3, padx=5, pady=5, sticky="ew")

        self.label_intervalo.grid(row=6, column=0, columnspan=4, pady=10)

        # Configurar o redimensionamento da tabela com a janela
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

        # Interceptar o evento de fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_fechamento)
        


    def atualizar_tabela(self):
        # Limpar a tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Calcular os índices para a página atual
        inicio = self.pagina_atual * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        dados_pagina = self.dados[inicio:fim]

        # Inserir os dados da página atual na tabela
        for item in dados_pagina:
            self.tabela.insert("", "end", values=item)

        # Atualizar o label da página
        self.label_pagina.config(text=f"Página {self.pagina_atual + 1}")

    def pagina_anterior(self):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.atualizar_tabela()

    def pagina_proximo(self):
        total_paginas = (len(self.dados) + self.itens_por_pagina - 1) // self.itens_por_pagina
        if self.pagina_atual < total_paginas - 1:
            self.pagina_atual += 1
            self.atualizar_tabela()

    def iniciar_monitoramento(self):
        caminho_app = self.caminho_app.get()
        chave = self.chave.get()
        versao = self.versao.get()

        if not caminho_app or not chave:
            messagebox.showerror("Erro", "Por favor, preencha o caminho do aplicativo e a palavra-chave.")
            return

        self.monitorando = True
        self.entry_caminho.config(state=tk.DISABLED)
        self.entry_chave.config(state=tk.DISABLED)
        self.entry_versao.config(state=tk.DISABLED)
        self.botao_iniciar.config(state=tk.DISABLED)
        self.botao_finalizar.config(state=tk.NORMAL)
        self.dados = []
        self.tempos_execucao = []
        self.pagina_atual = 0
        self.atualizar_tabela()
        self.label_intervalo.config(text="Intervalo médio: Monitorando...")

        def monitorar():
            caminho_app = self.caminho_app.get()
            chave = self.chave.get()
            versao = self.versao.get()

            if not os.path.exists(caminho_app):
                messagebox.showerror("Erro", f"O arquivo não foi encontrado no caminho: {caminho_app}")
                self.root.after(0, self.finalizar_monitoramento_interno)
                return

            try:
                caminho_pasta_app = os.path.dirname(caminho_app) # Obtém o diretório do executável
                self.processo = subprocess.Popen([caminho_app], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=caminho_pasta_app)

                inicio_tarefa = None
                hora_inicio = None
                captura_linha = ""
                tipo_log_inicio = ""

                for linha in self.processo.stdout:
                    if not self.monitorando:
                        print("Monitoramento finalizado, interrompendo leitura da saída.")
                        break
                    linha = linha.strip()
                    print(f"Saída do executável ({versao}): {linha}")

                    if chave in linha:
                        if inicio_tarefa is None:
                            inicio_tarefa = True
                            match_inicio = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+([A-Z]+)\s*\]", linha)
                            if match_inicio:
                                hora_inicio_str = match_inicio.group(1)
                                tipo_log_inicio = match_inicio.group(2)
                                try:
                                    hora_inicio = datetime.datetime.strptime(hora_inicio_str, "%Y-%m-%d %H:%M:%S")
                                except ValueError:
                                    hora_inicio = datetime.datetime.now()
                            else:
                                hora_inicio = datetime.datetime.now()
                                tipo_log_inicio = "INF" # Valor padrão caso não encontre o padrão
                            captura_linha = linha
                    
                    if re.search(r"<s:[^>]+>", linha) and inicio_tarefa:
                        match_fim = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+[A-Z]+\s*\]", linha)
                        hora_fim = None
                        if match_fim:
                            hora_fim_str = match_fim.group(1)
                            try:
                                hora_fim = datetime.datetime.strptime(hora_fim_str, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                hora_fim = datetime.datetime.now()
                        else:
                            hora_fim = datetime.datetime.now()

                        if hora_inicio and hora_fim:
                            self.dados.append([hora_inicio.strftime("%Y-%m-%d %H:%M:%S"), chave, versao, captura_linha, hora_fim.strftime("%Y-%m-%d %H:%M:%S")])
                            if self.tempos_execucao:
                                diff = hora_fim - self.tempos_execucao[-1][1]
                                self.tempos_execucao.append((hora_inicio, hora_fim, diff.total_seconds()))
                            else:
                                self.tempos_execucao.append((hora_inicio, hora_fim, 0)) # Primeiro registro

                            self.root.after(0, self.atualizar_tabela) # Atualizar a tabela na thread principal
                        inicio_tarefa = None
                        hora_inicio = None
                        captura_linha = ""
                        tipo_log_inicio = ""

                    if not self.monitorando:
                        break

                stdout, stderr = self.processo.communicate()
                if stderr:
                    print(f"Erro no aplicativo monitorado: {stderr}")

            except FileNotFoundError as e:
                messagebox.showerror("Erro ao iniciar", f"Arquivo não encontrado: {e.filename}")
                self.root.after(0, self.finalizar_monitoramento_interno)
            except OSError as e:
                messagebox.showerror("Erro ao iniciar", f"Erro ao executar o aplicativo: {e}")
                self.root.after(0, self.finalizar_monitoramento_interno)
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
                self.root.after(0, self.finalizar_monitoramento_interno)
            finally:
                if self.monitorando: # Garante que a finalização interna só seja chamada se o monitoramento foi iniciado
                    self.root.after(0, self.finalizar_monitoramento_interno)

        threading.Thread(target=monitorar, daemon=True).start()

    def finalizar_monitoramento(self):
        print("Botão Finalizar Monitoramento clicado.")
        self.monitorando = False
        print(f"self.monitorando agora é: {self.monitorando}")
        if self.processo:
            print(f"Processo PID: {self.processo.pid}, poll: {self.processo.poll()}")
            if self.processo.poll() is None:
                print("Processo ainda está rodando, enviando terminate()...")
                self.processo.terminate()
                try:
                    print("Aguardando finalização do processo (timeout=5s)...")
                    self.processo.wait(timeout=5)
                    print("Processo finalizou.")
                except subprocess.TimeoutExpired:
                    print("Timeout expirou, enviando kill()...")
                    self.processo.kill()
                    print("Processo foi morto.")
            else:
                print("Processo já havia terminado.")
        else:
            print("Nenhum processo para finalizar.")

        if hasattr(self, 'monitor_thread'):
            print(f"Thread de monitoramento está viva? {self.monitor_thread.is_alive()}")
            if self.monitor_thread.is_alive():
                print("Aguardando a thread de monitoramento terminar...")
                self.monitor_thread.join()
                print("Thread de monitoramento terminou.")
            else:
                print("Thread de monitoramento já havia terminado.")
        else:
            print("monitor_thread não foi definida.")

        print("Chamando finalizar_monitoramento_interno.")
        self.finalizar_monitoramento_interno()

    def finalizar_monitoramento_interno(self):
        print ("Finalizando momnitoramento interno...")
        self.calcular_intervalo_medio()
        self.salvar_log()
        self.botao_iniciar.config(state=tk.NORMAL)
        self.botao_finalizar.config(state=tk.DISABLED)
        self.entry_caminho.config(state=tk.NORMAL)
        self.entry_chave.config(state=tk.NORMAL)
        self.entry_versao.config(state=tk.NORMAL)
        self.monitorando = False
        
    def confirmar_fechamento(self):
        print("Evento de fechamento da janela detectado.")
        if self.monitorando:
            print("Monitoramento está ativo.")
            resposta = messagebox.askyesno("Alerta", "O monitoramento está em andamento. Deseja realmente encerrar?")
            print(f"Resposta do messagebox: {resposta}")
            if resposta:
                print("Usuário confirmou o encerramento.")
                self.finalizar_monitoramento()
                self.root.destroy()
            else:
                print("Usuário cancelou o encerramento.")
        else:
            print("Monitoramento não está ativo, fechando a janela.")
            self.root.destroy()

    def calcular_intervalo_medio(self):
        if len(self.tempos_execucao) > 1:
            tempos_unicos = sorted(list(set(self.tempos_execucao))) # Obter timestamps únicos e ordenados
            if len(tempos_unicos) > 1:
                total_diferenca = datetime.timedelta()
                for i in range(1, len(tempos_unicos)):
                    diferenca = tempos_unicos[i] - tempos_unicos[i-1]
                    total_diferenca += diferenca

                media_segundos = total_diferenca.total_seconds() / (len(tempos_unicos) - 1)
                intervalo_delta = datetime.timedelta(seconds=media_segundos)
                intervalo_str = str(intervalo_delta).split('.')[0]
                self.label_intervalo.config(text=f"Intervalo médio: {intervalo_str}")
            else:
                self.label_intervalo.config(text="Intervalo médio: Não há dados suficientes para calcular (timestamps únicos).")
        else:
            self.label_intervalo.config(text="Intervalo médio: Não há dados suficientes para calcular.")
            
            
    # def salvar_log(self):
    #     chave = self.chave.get()
    #     if not chave:
    #         chave = "monitoramento_sem_chave"
    #     nome_pasta = chave.replace(" ", "_")
    #     pasta_monitoramento = "Monitoramento"
    #     pasta_chave = os.path.join(pasta_monitoramento, nome_pasta)

    #     os.makedirs(pasta_chave, exist_ok=True)
    #     nome_arquivo_log = os.path.join(pasta_chave, "log.txt")

    #     try:
    #         with open(nome_arquivo_log, "w") as f:
    #             f.write(f"Relatório de Monitoramento - Chave: '{chave}' - Versão: '{self.versao.get()}'\n\n")
    #             f.write("Data Início\t\tIdentificador\tVersão\t\tCaptura\t\t\t\t\t\tData Fim\n")
    #             f.write("-" * 100 + "\n")
    #             for item in self.dados:
    #                 f.write(f"{item[0]}\t{item[1]}\t\t{item[2]}\t\t{item[3]}\t\t{item[4]}\n")
    #             f.write("\nIntervalo Médio entre Execuções: " + self.label_intervalo.cget("text").replace("Intervalo médio: ", ""))
    #         messagebox.showinfo("Sucesso", f"Log salvo em: {nome_arquivo_log}")
    #     except Exception as e:
    #         messagebox.showerror("Erro ao Salvar Log", f"Ocorreu um erro ao salvar o log: {e}")
    
    
    def salvar_log(self):
        caminho_app = self.caminho_app.get()
        chave = self.chave.get()

        if not caminho_app:
            messagebox.showerror("Erro", "Caminho do aplicativo não definido para salvar o log.")
            return

        nome_aplicativo = os.path.splitext(os.path.basename(caminho_app))[0]
        nome_pasta = nome_aplicativo.replace(" ", "_")
        nome_arquivo_log = chave.replace(" ", "_") + ".log"
        pasta_aplicativo = "Monitoramento"
        pasta_final = os.path.join(pasta_aplicativo, nome_pasta)
        caminho_arquivo_log = os.path.join(pasta_final, nome_arquivo_log)

        os.makedirs(pasta_final, exist_ok=True)

        try:
            with open(caminho_arquivo_log, "w") as f:
                f.write("Data Início,Identificador,Versão do aplicativo,Captura,Data Fim\n")
                for item in self.dados:
                    f.write(",".join(map(str, item)) + "\n")
            messagebox.showinfo("Log Salvo", f"Log salvo em: {caminho_arquivo_log}")
        except Exception as e:
            messagebox.showerror("Erro ao Salvar Log", f"Ocorreu um erro ao salvar o log: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()
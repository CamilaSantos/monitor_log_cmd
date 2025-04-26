# Monitor de log de Prompt de Comando

[![Licença](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status do Projeto](https://img.shields.io/badge/Status-Concluído-brightgreen.svg)](#status-do-projeto)
[![Linguagem](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Requisitos](https://img.shields.io/badge/Dependências-Atualizadas-brightgreen.svg)](#requirements.txt)

> Aplicativo criado para captura de dados de log em tempo real executado através do prompt de comando

## Visão Geral

A criação deste aplicativo surgiu na necessidade de monitorar uma determindata tarefa de um serviço e validar se está sendo executado dentro do tempo programado. O serviço pode ser executado via prompt de comando e ser visualizada todas as tarefas que estão sendo realizadas. Com o aplicativo é possível capturar palavra ou frase de até 80 caracteres e obter a linha em que esta CHAVE (palavra ou frase) aparece. 

As linha em que contém esta CHAVE são mostradas no aplicativo com data e hora de finalização. Ao clicar em Finalizar Monitoramento e informado o calculo de tempo médio em que esta tarefa estava sendo executada e salvo um log.txt para analise futura ou utilizado como evidência.

**Principais Recursos:**

* Recurso 1: Aceita qualquer dado de entrada (Palavra, frase, números...), limitados a 80 caracteres.
* Recurso 2: Apenas informar o caminho do arquivo ao qual deseja monitorar. (Funciona apenas com executáveis com tela de prompt de comando).
* Recurso 3: Data e hora em que foi localizada a linha com CHAVE informada, capturada a linha com a CHAVE, data e hora em que finalizou.
* Recurso 4: Ao finalizar através do botão "Finalizar Monitoramento", o registro fica salvo no log.txt
* Recurso 5: É realizado o calculo médio de quanto em quanto tempo esta CHAVE apareceu.

## Tela da aplicação
Tela de entrada de dados
![alt text](image.png)

Tela 2 para executar prompt de comando, visualização do executável informado
![alt text](image-1.png)


### Pré-requisitos

Liste aqui as dependências que precisam ser instaladas antes de executar o projeto. Inclua links para download, se aplicável.

* [Python](https://www.python.org/downloads/) (versão 3.11 ou superior)
* [pip](https://pip.pypa.io/en/stable/installing/) (geralmente instalado com o Python)
* [Git](https://git-scm.com/downloads) (para clonar o repositório)

### Instalação

Passos para instalar o projeto e suas dependências.

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  Crie e ative um ambiente virtual (recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    .\venv\Scripts\activate  # No Windows
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

### Execução

Instruções sobre como executar o projeto.

```bash
python seu_script_principal.py [argumentos opcionais]
# Como Contribuir para Monitor de log Prompt de Comando

Obrigado pelo seu interesse em contribuir para Monitor de log Prompt de Comando! Valorizamos todas as formas de contribuição, desde relatar bugs e sugerir melhorias até enviar código.

Por favor, leia este guia antes de começar a contribuir.

## Código de Conduta

Este projeto segue um [Contributor Covenant](CODE_OF_CONDUCT.md). Espera-se que todos os participantes sejam abertos, respeitosos e inclusivos.

## Como Você Pode Contribuir

Existem várias maneiras de você contribuir para este projeto:

### Relatando Bugs

Se você encontrar um bug, por favor, siga estes passos:

1.  **Verifique se o bug já foi relatado** abrindo a aba [Issues](https://github.com/CamilaSantos/monitor_log_cmd.git/issues) e pesquisando por problemas semelhantes.
2.  **Se o bug ainda não foi relatado, crie uma nova Issue.**
3.  **Forneça o máximo de detalhes possível no seu relatório:**
    * Uma descrição clara e concisa do bug.
    * Passos para reproduzir o bug.
    * O comportamento esperado e o comportamento real.
    * Informações sobre seu ambiente (sistema operacional, versão do Python, etc.).
    * Quaisquer logs de erro ou screenshots relevantes.

### Sugerindo Melhorias e Novas Funcionalidades

Se você tiver ideias para melhorar o projeto ou adicionar novas funcionalidades, por favor:

1.  **Verifique se sua sugestão já foi feita** abrindo a aba [Issues](https://github.com/CamilaSantos/monitor_log_cmd.git/issues) e pesquisando por sugestões semelhantes.
2.  **Se sua sugestão ainda não foi feita, crie uma nova Issue.**
3.  **Descreva sua sugestão o mais detalhadamente possível:**
    * Explique o problema que sua sugestão resolve ou a necessidade que ela atende.
    * Descreva a funcionalidade proposta.
    * Forneça exemplos de como ela poderia ser usada.
    * Discuta quaisquer possíveis prós e contras.

### Contribuindo com Código

Se você deseja contribuir com código, siga este fluxo de trabalho:

1.  **Faça um Fork do repositório** para sua própria conta do GitHub.
2.  **Clone o seu fork** para o seu computador local:
    ```bash
    git clone [https://github.com/CamilaSantos/monitor_log_cmd.git](https://github.com/CamilaSantos/monitor_log_cmd.git)
    cd seu-repositorio
    ```
3.  **Crie uma branch para sua contribuição:**
    * Para correções de bugs: `git checkout -b bugfix/descricao-do-bug`
    * Para novas funcionalidades: `git checkout -b feature/nome-da-funcionalidade`
4.  **Faça suas alterações e faça commits:**
    * Siga as [Convenções de Commit](#convenções-de-commit) abaixo.
    * Mantenha seus commits focados em pequenas alterações lógicas.
5.  **Faça push para sua branch no seu fork:**
    ```bash
    git push origin sua-branch
    ```
6.  **Abra um Pull Request (PR)** da sua branch para a branch `dev` do repositório principal ([https://github.com/seu-usuario/seu-repositorio/pulls](https://github.com/seu-usuario/seu-repositorio/pulls)).
7.  **Descreva claramente suas alterações no Pull Request.**
8.  **Aguarde a revisão do código.** Esteja preparado para fazer alterações com base no feedback.
9.  **Após a aprovação, seu Pull Request será mesclado.**

## Convenções de Commit

Nós seguimos as seguintes convenções para mensagens de commit [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/)
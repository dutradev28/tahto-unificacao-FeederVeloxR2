##########                TEMPLATE PARA PROJETOS DE RPA UTILIZANDO EBOTS                  ##########

Utilize este projeto como um modelo para seu novo projeto de RPA.

### Environment ###

Antes de iniciar, não se esqueça de editar o arquivo 'sonar-project.properties' colocando o nome do
seu projeto (o mesmo cadastrado no EBots) e também de rodar o comando '.\create_env.ps1' (Windows) 
ou '.\create_env.sh' (Linux) na janela de terminal.

Este comando vai criar um environment (env) separado para este projeto, bem como instalar os módulos
externos necessários, como o 'commoncore.core_ebots'.

Não se esqueça de selecionar 'Sim' quando o VS Code perguntar se deseja o novo environment criado.

### AutoPilot ###

Este template está usando o modo 'AutoPilot' do EBots, onde você deve apenas executar o AutoPilot no
módulo 'main.py' (conforme este exemplo). 

No modo AutoPilot o EBots vai procurar classes derivadas da classe base 'EbotsTaskBase' para executar. 

Estas classes devem estar na pasta 'ebots_tasks' e seguir o exemplo fornecido. O EBots vai identificar
as classes automaticamente e executá-las quando necessário de acordo com as configurações do EBots.

### Debug ###

O método Run do AutoPilot recebe dois parâmetros: O nome do robô (obrigatório) e a flag de debug (opcional).

O debug é default False, e isso significa que caso haja um erro/exception, ele será capturado e logado sem
que a execução seja interrompida. Quando estiver com True, a execução será interrompida em caso de erro.

JAMAIS SUBA PARA O GIT SEU PROJETO COM DEBUG TRUE!!!!! USE SOMENTE LOCALMENTE!!!!

### .ENV ###

Para a execução do projeto em sua máquina local, deve-se criar na raiz do projeto um arquivo chamado .env
Nele setar 2 atributos abaixo:

    EBOTS_URL = https://localhost
    EBOTS_TOKEN = 1234
Esses serviços são de comunicação dom o e-BOTS.

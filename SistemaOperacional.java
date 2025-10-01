import java.util.ArrayList;

/**
 * A classe Sistema Operacional simulara . . . o sistema operacional. Logo ela que coordenara as outras classes.
 * Cabe ao sistema operacional receber a requisiçao de tarefa, que sera feita via um documento .txt com as informaçoes da tarefa, e entao chamar o Parser para extrair os dados.
 * O sistema operacional entao ira, com esses dados, criar os TCB colocalos na Fila e chamar o Escalonador.
 * Alm disso o sistema operacional tambem tera um Clock para a passagem de tick, seja em loop ou em modo debbuger, e tera um Historico para salvar o estado das tarefaz em cada momento.
 *
 * @Jade M
 * @0.2
 */
public class SistemaOperacional
{
    // instance variables - replace the example below with your own
    private Clock relogio;
    private FilaTarefas tarefasProntas;
    private FilaTarefas tarefasSuspensas;
    private FilaTarefas tarefaExecutando;
    private Escalonador escalonador;
    private Parser parser;
    private ArrayList<Integer> configuracoes;
    
    //Criar uma classe Historico, dai o SO tem um historico e a cada tick ele manda oq tem em cada FilaTarefas pro historico pra dps o Historico poder criar o grafico
    //private Historico historico; 

    /**
     * Construtora, bem generica
     */
    public SistemaOperacional()
    {
        relogio = new Clock();
        tarefasProntas = new TarefasProntas();
        tarefasSuspensas = new TarefasSuspensas();
        tarefaExecutando = new TarefaExecutando();
        escalonador = new Escalonador();
        parser = new Parser();
        configuracoes = new ArrayList<>();
        //historico = new Historico();

    }

    /**
     * Metodo que simula a passagem de tick's
     * Presume-se que sempre tera uma tarefa sendo executada at todas serem executadas. Entao esse sera o parametro para o loop
     * 
     */
    public void loopConstante()
    {
        while(!tarefaExecutando.isEmpty())
        {
        relogio.nextTick();
        }
    }
    
    /**
     * Metodo que simula a passagem de tick's no modo debugger
     * Provavelmente o ideal seria de algum modo que ele le entrada do teclado para ir pro proximo tick
     * Mas so ir chamando ela no terminal n tem problema por hora
     * 
     */
    public void loopDebbuger()
    {
        relogio.nextTick();
    }
    
    
    /**
     * Metodo que comeca tudo
     * Começa o relogio e o loop. //O loop acaba se no tiver tarefa executando, ento ele tem q ser a ultima coisa a ser chamada
     * Chama o parseConfigs para ler as configuraçes
     * !!!!Criar alguma funçao q le as configuraçoes e separa elas em arrays pra cada uma das coisas sabe, uma por objeto uma pro escalonado
     * !!!!Ou a gente pode so usar stream sla
     * !!!!Tem que ver isso
     * Passa as configuraçes para o escalonador
     * Cria as tasks
     * Poe as tasks na fila
     * 
     */
    public void comecar()
    {
        parseConfigs("caminho_da_config");
        ArrayList<Integer> PLACEHOLDER = null;
        
        
        configsEscalonador(PLACEHOLDER);
        // chama criarTasks
        loopConstante();       
        
    }
    
    /**
     * Metodo que comeca tudo
     * Começa o relogio e o loop. //O loop acaba se no tiver tarefa executando, ento ele tem q ser a ultima coisa a ser chamada
     * Chama o parseConfigs para ler as configuraçes
     * !!!!Criar alguma funçao q le as configuraçoes e separa elas em arrays pra cada uma das coisas sabe, uma por objeto uma pro escalonado
     * !!!!Ou a gente pode so usar stream sla
     * !!!!Tem que ver isso
     * Passa as configuraçes para o escalonador
     * Cria as tasks
     * Poe as tasks na fila
     * 
     */
    public void parseConfigs(String caminho_da_config)
    {
        configuracoes = parser.lerConfigs(caminho_da_config);
        // as configuraçoes serao na ordem algoritmo_escalonamento;quantum id;cor;ingresso;duracao;prioridade;lista_eventos
        // algoritmo_escalonamento e quantum vai pro escalonador
        // sao criadas TCB's com  id;cor;ingresso;duracao;prioridade;lista_eventos e cada TCB criada vai pra lista de prontas
        
        
    }
    
    public void criarTasks(ArrayList<Integer> configs)
    {
        // vai criando TCB's e mandando pro listaProntas
        //Talvez fazer uma funçao so pra mandar pro lista prontas
    }
    
    
    public void configsEscalonador(ArrayList<Integer> configs)
    {
        // Manda pro escalonador o quantum e o tipo de algoritimo
        
    }
    
    public void atualizaHistorico()
    {
        //  atualiza o historico a cada tick
        
    }
    

}

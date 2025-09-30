import java.util.ArrayList;

/**
 * Write a description of class SistemaOperacional here.
 *
 * @author (your name)
 * @version (a version number or a date)
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
    
    //private Historico historico; Criar uma classe Historico, dai o SO tem um historico e a cada tick ele manda oq tem em cada FilaTarefas pro historico pra dps o Historico poder criar o grafico 

    /**
     * Constructor for objects of class SistemaOperacional
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
     * An example of a method - replace this comment with your own
     *
     * @param  y  a sample parameter for a method
     * @return    the sum of x and y
     */
    public void loopSimulacao(int y)
    {
        while(!tarefaExecutando.isEmpty())
        {
        relogio.nextTick();
        }
    }
    
    public void comecar()
    {
        // chama a parseConfigs
        // chama cinfigsEscalonador
        // chama criarTasks
        
        
    }
    
    public void parseConfigs()
    {
        configuracoes = parser.lerConfigs();
        // as configuraçoes serao na ordem algoritmo_escalonamento;quantum id;cor;ingresso;duracao;prioridade;lista_eventos
        // algoritmo_escalonamento e quantum vai pro escalonador
        // sao criadas TCB's com  id;cor;ingresso;duracao;prioridade;lista_eventos e cada TCB criada vai pra lista de prontas
        
        
    }
    
    public void criarTasks()
    {
        // vai criando TCB's e mandando pro listaProntas
    }
    
    
    public void configsEscalonador()
    {
        // Manda pro escalonador o quantum e o tipo de algoritimo
        
    }
    
    public void atualizaHistorico()
    {
        //  atualiza o historico a cada tick
        
    }
    

}

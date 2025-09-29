
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
    private TarefasProntas tarefas;

    /**
     * Constructor for objects of class SistemaOperacional
     */
    public SistemaOperacional()
    {
        relogio = new Clock();
        tarefas = new TarefasProntas();

    }

    /**
     * An example of a method - replace this comment with your own
     *
     * @param  y  a sample parameter for a method
     * @return    the sum of x and y
     */
    public void loopSimulacao(int y)
    {
        while(!tarefas.isEmpty())
        {
        relogio.nextTick();
        }
    }
}
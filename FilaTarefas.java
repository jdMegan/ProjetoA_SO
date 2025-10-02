import java.util.ArrayList;

/**
 * Write a description of class FilaTarefas here.
 *
 * @author (your name)
 * @version (a version number or a date)
 */
public class FilaTarefas
{
    // instance variables - replace the example below with your own
    private ArrayList<TCB> listaProntas;
    private String algoritimo;

    /**
     * Constructor for objects of class FilaTarefas
     */
    public FilaTarefas()
    {
        // initialise instance variables
        listaProntas = new ArrayList<>();
        algoritimo = "FIFO";
    }

    /**
     * An example of a method - replace this comment with your own
     *
     * @param  y  a sample parameter for a method
     * @return    the sum of x and y
     */
    public void setAlgoritimo(String alg)
    {
        // put your code here
        algoritimo = alg;
    }
    public String getAlgoritimo( )
    {
        // put your code here
        return algoritimo;
    }
    public boolean isEmpty()
    {
        // put your code here
        return listaProntas.isEmpty();
    }
}

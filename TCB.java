import java.util.ArrayList;

/**
 * Write a description of class TCB here.
 *
 * @author (your name)
 * @version (a version number or a date)
 */
public class TCB
{
    // instance variables - replace the example below with your own
    private int id;
    private int cor;
    private int ingresso;
    private int duracao;
    private int prioridade;
    
    //Vamos ter q criar uma classe eventos?
    private int eventos;

    /**
     * Constructor for objects of class TCB
     */
    public TCB()
    {
        //Cria tudo null pra dps o sistema operacional preencher
        
    }

    /**
     * An example of a method - replace this comment with your own
     *
     * @param  y  a sample parameter for a method
     * @return    the sum of x and y
     */
    public void setConfigs(ArrayList<Integer> configs)
    {
        //Vai receber um array, nao o array inteiro q tem no SistemaOperacional
        //Provavelmente usa um stream la pra passar pra ca s as relevantes
        //Dai vai salvando nas variaveis certas
        
    }
    
    public int getId()
    {
        // put your code here
        return id;
    }
    public int getCor()
    {
        // put your code here
        return cor;
    }
    public int getIngresso()
    {
        // put your code here
        return ingresso;
    }
    public int getDuracao()
    {
        // put your code here
        return duracao;
    }
    public int getPrioridade()
    {
        // put your code here
        return prioridade;
    }
    public void eventos()
    {
        // Nao sei mto bem oq fazer com os eventos
        ;
    }
}

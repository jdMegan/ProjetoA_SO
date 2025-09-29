
/**
 * Write a description of class Clock here.
 *
 * @author (your name)
 * @version (a version number or a date)
 */
public class Clock
{
    // instance variables - replace the example below with your own
    private int tick;
    private int tempoAtual;

    /**
     * Constructor for objects of class Clock
     */
    public Clock()
    {
        tempoAtual = 0;
        tick = 1;
    }

    /**
     * An example of a method - replace this comment with your own
     *
     * @param  y  a sample parameter for a method
     * @return    the sum of x and y
     */
    public int getTempo()
    {
        return tempoAtual;
    }
    
    public void setTick(int tick)
    {
        this.tick = tick;
    }
    
    /**
     * An example of a method - replace this comment with your own
     *
     * @param  y  a sample parameter for a method
     * @return    the sum of x and y
     */
    public void nextTick()
    {
        tempoAtual += tick ;
    }
}
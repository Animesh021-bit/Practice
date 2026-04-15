package Animesh;
import java.util.ArrayList;
import java.util.Iterator;
public class ArrayListExample {
    public static void main(String[] args){
        ArrayList<String> list = new ArrayList<>();
        list.add("Animesh");
        list.add("swati");
        list.add("aryan");

        // Get an iterator for the ArrayList
        Iterator<String> it = list.iterator();

        // Iterate through the list using the iterator
        while(it.hasNext()){
            System.out.println(it.next());
        }


    }
    
}

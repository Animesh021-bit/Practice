package Animesh;
import java.io.*;

public class TryCatchEcample {
    public static void main(String[] args){
        try{
            FileReader file=new FileReader("NonExistentFile.txt");
        }catch(FileNotFoundException e){
            System.out.println("File not found: "+e.getMessage());
        }
    }
    
}

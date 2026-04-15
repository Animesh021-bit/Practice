package Animesh;

public class MethodOVerloading {
    static int plusMethod(int x, int y){
        return x+y;
    }
    static double plusMethod(double x, double y){
        return x+y;
    }
    public static void main(String args[]){
        System.out.println("The sum of two integres is: "+plusMethod(5,8));
        System.out.println("The sum of double is: "+plusMethod(9.4,7.6));
    
}}
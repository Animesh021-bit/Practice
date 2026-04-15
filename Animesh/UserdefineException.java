package Animesh;
//user define exception
class InvalidAge extends Exception{
    public InvalidAge(String message) {
        super(message);
    }
}

public class UserdefineException {
    public static void main(String[] args){
        int age = 15;
        try{
            checkAge(age);
        }catch(InvalidAge e){
            System.out.println(e.getMessage());
        }
        }
    
    
    public static void checkAge(int age) throws InvalidAge{
        if (age<18){
            throw new InvalidAge("you are not eligible");
        }
        System.out.println("You are eligible" );
    }
}

//interface
interface Animal{
    public void animalSound();
    public void sleep();
}

//Pig "implements" the Animal interface
class Pig implements Animal{
    public void animalSound(){
        System.out.println("The Pig says: wee wee");
    }
    public void sleep(){
        System.out.println("Zzzzz");
    }
}

class Main {
    public static void main(String[] args){
        Pig myPig=new Pig();
        myPig.animalSound();
        myPig.sleep();
    }
}
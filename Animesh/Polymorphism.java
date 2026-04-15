package Animesh;

class Animal{
    public void animalSound(){
        System.out.println("The Animal makes a sound.");
    }
}
class Dog extends Animal{
    public void animalSound(){
        System.out.println("The Dog barks.");
    }
}
class Cat extends Animal{
    public void animalSound(){
        System.out.println("the Cat meows.");
    }
}

public class Polymorphism {
    public static void main(String args[]){
    Animal myAnimal=new Animal();
    Animal myDog = new Dog(); // Create a Dog object
    Animal myCat = new Cat(); // Create a Cat object
    myDog.animalSound();
    myCat.animalSound();
    myAnimal.animalSound();
}
}
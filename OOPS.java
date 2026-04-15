
class student {
    String name;
    int age;

    public void Info(){
        System.out.println(this.name);
        System.out.println(this.age);
    }

    student(student s2){
        this.name=s2.name;
        this.age=s2.age;
    }
    student(){
        
    }
}
public class OOPS{
    public static void main(String args[]){
        student s1=new student();

        s1.name="Animesh";
        s1.age=21;

        student s2=new student(s1);

        s2.Info();       
    }
}
class student {
    String name;
    int age;
    double marks;

    public void Info(){
        System.out.println(this.name);
        System.out.println(this.age);
        System.out.println(this.marks);
    }

    student(student s2){
        this.name=s2.name;
        this.age=s2.age;
        this.marks=s2.marks;
    }
    student(){

    }    
}
public class OOPS2{
    public static void main(String args[]){
        student s1=new student();

        s1.name="Animesh";
        s1.age=22;
        s1.marks=68.78;

        student s2=new student(s1);

        s2.Info();

    }
}

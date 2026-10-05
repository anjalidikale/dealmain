class Empolyee{
    void calculateSalary() {
        System.out.printn("General employee salary");    }
}
class Manager extends Employee {
    void calculateSalary1(){
        System.out.println("Manager salary = 80000")    }
}
class Developer extends Employee {

    void calculateSalary2() {
        System.out.println("Developer salary = 60000");  }}
        public class Main{
            public static void main(String[] args) {
                Manager m=new Manager();
                Developer d=mew Developer();
                m.calculateSalary1();
                d.developerSalary2();
            }
        }

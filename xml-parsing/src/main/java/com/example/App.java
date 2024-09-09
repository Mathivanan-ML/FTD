package com.example;

import jakarta.xml.bind.JAXBContext;
import jakarta.xml.bind.JAXBException;
import jakarta.xml.bind.Marshaller;
import jakarta.xml.bind.Unmarshaller;

import java.io.File;

public class App {
    public static void main(String[] args) throws JAXBException {
        
        object_to_xml();
        xml_to_object();
    }
    public static void object_to_xml()throws JAXBException{
        Employeesss employees = new Employeesss();

        
        Employee emp1 = new Employee(1, "Mathi", "M", 50000);
        Employee emp2 = new Employee(2, "Mohan", "P", 40000);
        employees.getEmployees().add(emp1);
        employees.getEmployees().add(emp2);

        
        JAXBContext jaxbContext = JAXBContext.newInstance(Employeesss.class);
        Marshaller jaxbMarshaller = jaxbContext.createMarshaller();

        jaxbMarshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);

        
        jaxbMarshaller.marshal(employees, System.out);

        
        jaxbMarshaller.marshal(employees, new File("out.xml"));
    }

    public static void xml_to_object()throws JAXBException{
        JAXBContext jaxbContext = JAXBContext.newInstance(Employeesss.class);
        Unmarshaller jaxbUnmarshaller = jaxbContext.createUnmarshaller();


    Employeesss emps = (Employeesss) jaxbUnmarshaller.unmarshal(new File("out.xml"));

    for (Employee emp : emps.getEmployees()) {

        System.out.println(emp.getId());
        System.out.println(emp.getFirstName());
    }
    }
}

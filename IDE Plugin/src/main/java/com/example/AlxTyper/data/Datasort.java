package com.example.AlxTyper.data;

public class Datasort {
    public static String method_split(Notedata notedata){
         String partial_code = notedata.getContent();
         String new_partial_code = partial_code+"Hello_Java";
         return new_partial_code;
    }
}

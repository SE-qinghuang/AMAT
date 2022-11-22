package com.example.AlxTyper.data;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class DataConvert {
    public static String[] convert(Notedata notedata){
        String[] raw = new String[4];
        raw[0] = notedata.getContent();
        raw[1] = notedata.getFileName();
        raw[2] = notedata.getSimple_Name();
        raw[3] = notedata.getFull_Name();
        return raw;
    }
    public static String main(String code,String Simple_Name,String fileName) {
        // 这里想办法如何到前端
//        String executer = "C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\python.exe";
//        String file_path = "F:\\wu-system\\project-wys\\Interface_TypeInference\\Type_Inference.py";


        String file_path = "D:\\Interface_TypeInference\\Type_Inference.py";
//        String file_path = "E:\\apply\\Interface_TypeInference\\Type_Inference.py";
        String executer = "D:\\Anaconda\\python.exe";
//        String file_path = "F:\\wu-system\\project-wys\\Interface_TypeInference\\main2.py";


        String newcode = code.replace('\n','\t');
        String[] command_line = new String[]{executer,file_path,newcode,Simple_Name,fileName};
//        String[] command_line = new String[]{executer,file_path,newcode,Simple_Name};
        String Code = null;
        try {
            Process pr = Runtime.getRuntime().exec(command_line);
            InputStreamReader inputStreamReader = new InputStreamReader(pr.getInputStream());
            BufferedReader in = new BufferedReader(inputStreamReader);
            Code = in.readLine();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        //C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\python.exe F:\\wu-system\\project-wys\\main.py
        return Code;

    }
}

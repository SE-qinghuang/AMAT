package com.example.AlxTyper.data;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class pythonDemo {
    public static void main() {
        try {
            System.out.println("Start");
            Process pr = Runtime.getRuntime().exec("python F:/wu-system/project-wys/main.py");

            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            pr.waitFor();
            System.out.println("end");
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}



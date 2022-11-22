package com.example.AlxTyper.data;

public class Notedata {

    private String content;
    private String fileName;

    private String Code;

    private String Simple_Name;

    private String Full_Name;
    public Notedata(String content, String fileName,String Simple_Name, String Full_Name) {
        this.content = content;
        this.fileName = fileName;
        this.Simple_Name = Simple_Name;
        this.Full_Name = Full_Name;
    }


    public String getCode() {
        return Code;
    }

    public void setCode(String code) {
        this.Code = Code;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getSimple_Name(){
        return  Simple_Name;
    }

    public void setSimple_Name(String Simple_Name){
        this.Simple_Name = Simple_Name;
    }


    public String getFull_Name(){
        return  Full_Name;
    }

    public void setFull_Name(String Full_Name){
        this.Full_Name = Full_Name;
    }
    @Override
    public String toString() {
        return "Notedata{" +
                ", content='" + content + '\'' +
                ", fileName='" + fileName + '\'' +
                '}';
    }
}

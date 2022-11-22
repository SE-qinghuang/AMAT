package com.example.AlxTyper.data;

import javax.swing.table.DefaultTableModel;
import java.util.LinkedList;
import java.util.List;

public class DataCenter {

    public static String CHILD_FILE_NAME;
    public static String SELECTED_TEXT; //Original_Code
    public static String FILE_NAME; //FileName of Original_Code
    public static List<Notedata> NOTE_LIST = new LinkedList<>();

    public static String[] HEAD={"Original_Code","Filename","Simple_Name","FQN"};

    public static DefaultTableModel TABLE_MODEL = new DefaultTableModel(null,HEAD);

    public static void reset(){
        NOTE_LIST.clear();
        TABLE_MODEL.setDataVector(null,HEAD);
    }
}

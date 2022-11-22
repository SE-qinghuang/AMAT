package com.example.AlxTyper.dialog;

import com.example.AlxTyper.data.DataCenter;
import com.example.AlxTyper.data.DataConvert;
import com.example.AlxTyper.data.Notedata;
import com.intellij.openapi.ui.DialogWrapper;
import com.intellij.ui.EditorTextField;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.awt.*;

public class AddNoteDialog extends DialogWrapper {
     private  EditorTextField TextSimple_Name;
     private  EditorTextField textinformation;
     public AddNoteDialog() {
        super(true);
        setTitle("AMAT");
        init();
    }

    @Override
    protected @Nullable JComponent createCenterPanel() {
         //设置面板内容元素
         JPanel panel = new JPanel(new BorderLayout());
         //BorderLayout--控制面板布局
         TextSimple_Name  = new EditorTextField("Automatically Extract Simple Name or Simple Name");
//         textinformation = new EditorTextField("Information of Note");
//         //设置边框大小
//         textinformation.setPreferredSize(new Dimension(200,100));
//
        // enter the need repair of Simple_Name
         panel.add(TextSimple_Name,BorderLayout.NORTH);
//         panel.add(textinformation,BorderLayout.CENTER);
         return panel;
    }



    @Override
    //建立有方向的按钮
    protected JComponent createSouthPanel() {
         JPanel panel = new JPanel();
         JButton button = new JButton("Complete Import Statement");
         JButton button1 = new JButton("Infer Type");

         //接收用户输入内容--可用作我们代码补全的输入部分代码
        // create the button instruction
         button.addActionListener(e -> {

             //将添加的存到List
             String filetype = DataCenter.FILE_NAME.substring(DataCenter.FILE_NAME.lastIndexOf(".")+1);
             String Selected_Code = DataCenter.SELECTED_TEXT;
             String Simple_Name = "Automatically Extract Simple Name";
             String fileName = DataCenter.FILE_NAME;
             String Full_Name = DataConvert.main(Selected_Code,Simple_Name,fileName);
             String[] all = Full_Name.split("--");
             String[] simple_name = all[0].split(",");
             String[] full_name = all[1].split(",");
             for(int i =0;i<full_name.length;i++){
                 simple_name[i] = simple_name[i].replace("[","").replace("]","").replace("'","");
                 full_name[i] = full_name[i].replace("[","").replace("]","").replace("'","");
                 Notedata notedata =  new Notedata(DataCenter.SELECTED_TEXT,DataCenter.CHILD_FILE_NAME,simple_name[i],full_name[i]);

                 DataCenter.NOTE_LIST.add(notedata);
                 // 这里接收内容返回到notedata里让然后输出出来
                 DataCenter.TABLE_MODEL.addRow(DataConvert.convert(notedata));
             }

         });
        button1.addActionListener(e -> {
            String filetype = DataCenter.FILE_NAME.substring(DataCenter.FILE_NAME.lastIndexOf(".")+1);
            String Selected_Code = DataCenter.SELECTED_TEXT;
            String fileName = DataCenter.FILE_NAME;
            String Simple_Name = TextSimple_Name.getText();
            String Full_Name = DataConvert.main(Selected_Code,Simple_Name,fileName);
            Full_Name = Full_Name.replace("[","").replace("]","").replace("'","");
            Notedata notedata =  new Notedata(DataCenter.SELECTED_TEXT,DataCenter.CHILD_FILE_NAME,Simple_Name,Full_Name);

            DataCenter.NOTE_LIST.add(notedata);
            // 这里接收内容返回到notedata里让然后输出出来
            DataCenter.TABLE_MODEL.addRow(DataConvert.convert(notedata));

        });

         panel.add(button1);
         panel.add(button);
         return panel;
    }
}






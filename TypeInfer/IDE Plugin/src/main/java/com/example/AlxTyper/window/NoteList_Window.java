package com.example.AlxTyper.window;

import com.example.AlxTyper.data.DataCenter;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.wm.ToolWindow;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class NoteList_Window {
    private JTable tbContent;
    private JButton btnCreate;
    private JButton btnClear;
    private JButton btnClose;
    private JPanel contentPanel;
    private void init(){
        tbContent.setModel(DataCenter.TABLE_MODEL);
        tbContent.setEnabled(true);
    }
    public NoteList_Window(Project project,ToolWindow toolWindow) {
        init();

        btnClose.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                toolWindow.hide(null);
            }
        });
        btnClear.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                DataCenter.reset();
            }
        });
    }

    public JPanel getContentPanel() {

        return contentPanel;
    }
}

package com.example.AlxTyper.action;

import com.example.AlxTyper.data.DataCenter;
import com.example.AlxTyper.dialog.AddNoteDialog;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.editor.SelectionModel;







public class PoppupAction extends AnAction {

    @Override
    public void actionPerformed(AnActionEvent e) {
        //接收用户选定
        Editor editor = e.getRequiredData(CommonDataKeys.EDITOR);
        SelectionModel selectionModel = editor.getSelectionModel();
        // get the text
        String selectedText = selectionModel.getSelectedText();
        // get the name of text
        String child_name = e.getRequiredData(CommonDataKeys.PSI_FILE).getViewProvider().getVirtualFile().getName();
        String name  = e.getRequiredData(CommonDataKeys.PSI_FILE).getViewProvider().getVirtualFile().getCanonicalPath().replace(child_name,"");
        DataCenter.SELECTED_TEXT = selectedText;
        DataCenter.CHILD_FILE_NAME = child_name;
        DataCenter.FILE_NAME = name;
        AddNoteDialog addNoteDialog = new AddNoteDialog();
        addNoteDialog.show();

        // TODO: insert action logic here

    }
}

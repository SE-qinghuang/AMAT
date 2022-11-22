import json

import torch
import numpy as np
from transformers import RobertaTokenizer, RobertaForMaskedLM
import torch.nn.functional as F
import subprocess
import os
import pandas as pd
import re


java_key_words = ['public','private','Public','Private','final','final','new','New','void','Void','Static','static','protected','Protected','extends']
current_path = "D:/workplace/challenge/project/Interface_TypeInference"  # current path

def Prompt_generate(code_snippet,simple_name):
    code_snippet = re.sub('''"(.*?)"''', "String", code_snippet)
    code_list = code_snippet.split(";")
    CodeSnippet_list = [' '.join(code.split()) + ';' for code in code_list]
    CodeSnippet_list[0] = " "+CodeSnippet_list[0]  # 在第一个元素前面加一个空格，方便匹配

    # simple_name = simple_name.split(".")[-1]
    SimpleName = re.sub('\(.*?\)|\<.*?\>', "", simple_name)

    code_Prompt_nn = []
    code_Prompt_mm = []

    for code_i in range(len(CodeSnippet_list)):
        if SimpleName.endswith("."): SN_regex = '[^A-Za-z0-9]' + SimpleName + '[A-Za-z]'
        else: SN_regex = '[^A-Za-z0-9]' + SimpleName + '[^A-Za-z0-9]'
        simple_name_info = re.search(SN_regex, CodeSnippet_list[code_i])
        if simple_name_info == None: continue
        before_index = simple_name_info.start()
        end_index = simple_name_info.end()

        # simple name is method
        if "." in SimpleName:
            method_mask = "<mask><mask><mask>." + SimpleName.split(".")[-1]
            Masked_code_nn = CodeSnippet_list[code_i][:before_index] + method_mask + CodeSnippet_list[code_i][end_index:]
            Masked_code_mm = CodeSnippet_list[code_i][:before_index] + "<mask><mask><mask>." + CodeSnippet_list[code_i][before_index+1:]

        # simple name is class / interface
        else:
            Masked_code_nn = CodeSnippet_list[code_i][:before_index] + "<mask><mask><mask>."+CodeSnippet_list[code_i][before_index+1:]
            Masked_code_mm = "NULL"

        if code_i >= 2 and code_i < len(CodeSnippet_list) - 2:  # 前面两行和后面两行都有
            code_Prompt_nn.append(CodeSnippet_list[code_i - 2:code_i])
            code_Prompt_nn.append([Masked_code_nn])
            code_Prompt_nn.append(CodeSnippet_list[code_i + 1:code_i + 3])
            code_list_nn = [inner for code in code_Prompt_nn for inner in code]
            code_Prompt_nn = " ".join(code_list_nn)

            code_Prompt_mm.append(CodeSnippet_list[code_i - 2:code_i])
            code_Prompt_mm.append([Masked_code_mm])
            code_Prompt_mm.append(CodeSnippet_list[code_i + 1:code_i + 3])
            code_list_mm = [inner for code in code_Prompt_mm for inner in code]
            code_Prompt_mm = " ".join(code_list_mm)
            break

        elif code_i < 2 and code_i < len(CodeSnippet_list) - 2:  # 前面两行没有, 后面两行有
            code_Prompt_nn.append(CodeSnippet_list[:code_i])
            code_Prompt_nn.append([Masked_code_nn])
            code_Prompt_nn.append(CodeSnippet_list[code_i + 1:code_i + 3])
            code_list_nn = [inner for code in code_Prompt_nn for inner in code]
            code_Prompt_nn = " ".join(code_list_nn)

            code_Prompt_mm.append(CodeSnippet_list[:code_i])
            code_Prompt_mm.append([Masked_code_mm])
            code_Prompt_mm.append(CodeSnippet_list[code_i + 1:code_i + 3])
            code_list_mm = [inner for code in code_Prompt_mm for inner in code]
            code_Prompt_mm = " ".join(code_list_mm)
            break

        elif code_i >= 2 and code_i >= len(CodeSnippet_list) - 2:  # 前面两行有，后面两行 没有
            code_Prompt_nn.append(CodeSnippet_list[code_i - 2:code_i])
            code_Prompt_nn.append([Masked_code_nn])
            code_Prompt_nn.append(CodeSnippet_list[code_i + 1:])
            code_list_nn = [inner for code in code_Prompt_nn for inner in code]
            code_Prompt_nn = " ".join(code_list_nn)

            code_Prompt_mm.append(CodeSnippet_list[code_i - 2:code_i])
            code_Prompt_mm.append([Masked_code_mm])
            code_Prompt_mm.append(CodeSnippet_list[code_i + 1:])
            code_list_mm = [inner for code in code_Prompt_mm for inner in code]
            code_Prompt_mm = " ".join(code_list_mm)
            break

        elif len(CodeSnippet_list) <= 3:  #
            code_str = ' '.join(CodeSnippet_list)
            code_Prompt_nn = code_str.replace(CodeSnippet_list[code_i], Masked_code_nn)
            code_Prompt_mm = code_str.replace(CodeSnippet_list[code_i], Masked_code_mm)
            break

    code_Prompt = []
    code_Prompt.append(code_Prompt_nn)
    code_Prompt.append(code_Prompt_mm)
    return code_Prompt


class Itera_Pred():
    def __init__(self,code_Prompt,Inference_step,Topk,tokenizer,model):
        self.code_Prompt = code_Prompt
        self.Inference_step = Inference_step
        self.Topk = Topk
        self.tokenizer = tokenizer
        self.model = model


    def numberMaskSearch(self):
        pred_result = []
        for prompt in self.code_Prompt:
            if '<mask><mask><mask>.' not in prompt: continue
            token_list = self.tokenizer.encode(prompt, add_special_tokens=True)
            token_tensor = torch.tensor([token_list])

            scoreList = []  # 这个list当中只会存储两个元素，当前的分数，和 上一次预测所得到的分数
            Count = 0 #
            while True:
                scores, indexs = self.model_Pred(token_tensor)  # 模型的输出
                # 将 预测所得到的 TypeId 转成 字符
                pred_token_list_temp = self.tokenizer.convert_ids_to_tokens(indexs)  # token_list--['token1','token2','token3'...]
                pred_token_list = []
                for token in pred_token_list_temp:
                    token_temp = token.replace('Ġ','')
                    if token_temp not in java_key_words:  # 去除预测结果当中的 java-key-words, e.g., final
                        pred_token_list.append(token_temp)
                pred_token_str = ''.join(pred_token_list)

                scoreList.append((sum(scores.tolist()) / len(scores.tolist()),pred_token_str))  # --> [(average-score,tokens),...] 存储 top-k个
                # scoreList:[(top-1),(top-2),..]
                if len(scoreList)>self.Topk:  # 保证在进行比较之前,scoreList 当中包含self.TopK+1 个 value
                    scoreList_Topk = sorted(scoreList,reverse=True)[:self.Topk]
                    scoreList_temp = scoreList[:self.Topk]
                    if scoreList_temp == scoreList_Topk:  # 如果 scoreList 当中 topK的序列没有发生变化，则加 1
                        Count = Count + 1
                    else:
                        Count = 0
                    scoreList.sort(reverse=True)  # 将 scoreList: max_value---> min_value

                if Count >=self.Inference_step:  #  scoreList 当中连续 x 次 value 一致 则退出预测
                    pred_result.extend(scoreList[:self.Topk])  # 取前面 前 topK个value
                    break

                insertID_list = [self.tokenizer.mask_token_id]*(len(self.maskIndex_list)+1)  # 添加 <mask> ID
                insertID_tensor = torch.tensor([insertID_list])
                beforPart = token_tensor[:,0:self.maskIndex_list[0]]
                afterPart = token_tensor[:,self.maskIndex_list[-1]+1:]
                self.new_token_tensor = torch.cat([beforPart,insertID_tensor,afterPart],dim=1)  # 完成了 对新的输入的拼接
                token_tensor = self.new_token_tensor

        return sorted(pred_result,reverse=True)[:self.Topk]

    def model_Pred(self,token_tensor):
        self.maskIndex_list = [np.argwhere(token_tensor.numpy()[0] == self.tokenizer.mask_token_id)][0].transpose()[0,:].tolist() # x == y, x 和 y的维度要相等
        output = self.model(token_tensor)[0]
        cur_pred = output[:,self.maskIndex_list,:]
        scores,indexs = torch.topk(cur_pred,k=1)  # 返回 top-beamSize 的 values
        score,index = scores.view(-1).detach(),indexs.view(-1).detach()
        return score,index

class Simple_Name_Extraction():
    def __init__(self,code_snippet):
        self.code_snippet = code_snippet
        self.template_repair()
        self.deal_AST()  # simple name extraction

    def template_repair(self):
        save_path = os.path.join(current_path,"AST_file","Test.java")
        self.code_snippet = ";".join(self.code_snippet.split(';'))
        self.template = "class Test{ \n" \
                   "public static void main(String[] args){ \n" \
                   + self.code_snippet + \
                                "\n}" \
                                   "\n}"
        with open(save_path,'w',encoding='utf-8') as f:
            f.write(self.template)

        # get the corresponding AST file
        jar_package = os.path.join(current_path,"AST_generate.jar")
        cmd = "java -jar "+ jar_package + " " + save_path
        subprocess.run(cmd)


    def deal_AST(self):
        AST_files_path = os.path.join(current_path,"AST_file","Test.json")
        simple_name_list = []
        type_define = ["Invocation","VARIABLE_TYPE"] # (1) VARIABLE_TYPE --> Class variable = ... (2) TypeAccess --> Interface/class.Method, (3) Invocation --> variable.Method()
        for type in type_define:
            type_info = '''"type": "''' + type + '''"'''
            with open(AST_files_path, 'r', encoding='utf-8') as f:
                cont = f.read()
                cont = " ".join(cont.split())

            Variable_all = re.findall(type_info, cont)

            for i in range(len(Variable_all)):
                Variable_info = re.search(type_info,cont)
                if Variable_info == None: break
                before_index = Variable_info.start()
                end_index = Variable_info.end()

                # 向前遍历 得到 variable name
                simple_name = []
                Tag = False
                while True:
                    before_index = before_index - 1
                    if Tag:
                        if cont[before_index] == '''"''':
                            simple_name.reverse()
                            simple_name_str = ''.join(simple_name)
                            if simple_name_str.count(".") <2:
                                simple_name_list.append(simple_name_str)
                            break
                        simple_name.append(cont[before_index])
                    if cont[before_index] == '''"''':
                        Tag = True

                # 向后遍历, 检查这个method 是 TypeAccess.method() 还是 variable.method(). 如果是前者，则得到对应的 TypeAccess.
                if type == "Invocation":
                    left = 0
                    right = 0
                    type_name = []
                    type_info2 = []
                    while True:
                        end_index = end_index + 1
                        if cont[end_index] == "{":
                            left = left + 1
                        elif cont[end_index] == "}":
                            right = right + 1
                        elif left == right and left != 0:
                            type_info_str = "".join(type_info2)
                            break
                        if left != 0:
                            type_info2.append(cont[end_index])

                    if '''"type": "TypeAccess"''' in type_info_str:
                        type_info3 = re.search('''"type": "TypeAccess"''', type_info_str)
                        left_index = type_info3.start()

                        # 向前遍历 得到 variable name
                        simple_name_type = []
                        Tag = False
                        while True:
                            left_index = left_index - 1
                            if Tag:
                                if type_info_str[left_index] == '''"''':
                                    simple_name_type.reverse()
                                    type_name.append(''.join(simple_name_type))
                                    break
                                simple_name_type.append(type_info_str[left_index])
                            if type_info_str[left_index] == '''"''':
                                Tag = True
                        if type_name[-1].count(".")>=2: # Java.lang.System.println() 中的println() 是 invocation，java.lang.System 是 Invocation.
                            simple_name_list.pop()
                        else:
                            simple_name_list[-1] = type_name[-1]+'.' #拼接成 typeAccess.method() // +simple_name_list[-1]
                    else:
                        simple_name_list.pop()  # variable.method 这种先不处理
                cont = cont[end_index:]

        return simple_name_list


def main_func(code_snippet, sim_name, top, opt, mod):
    # download in https://huggingface.co/ZQ/Type_Inference
    model_path = "D:/workplace/challenge/project/Interface_TypeInference/model"
    tokenizer = RobertaTokenizer.from_pretrained(model_path)
    model = RobertaForMaskedLM.from_pretrained(model_path)

    result = ""
    while True:
        if opt == "1":
            FQN_list = []
            simple_name_list = Simple_Name_Extraction(code_snippet).deal_AST()
            print("Simple Name List:", simple_name_list)
            for simple_name in simple_name_list:
                code_Prompt = Prompt_generate(code_snippet, simple_name)  # get the corresponding code prompt
                pred_result = Itera_Pred(code_Prompt, Inference_step=8, Topk=1, tokenizer=tokenizer,
                                         model=model).numberMaskSearch()  # start predict
                FQN = [type[1] + "." + simple_name for type in pred_result]
                print("simpel_name:", simple_name, " Full_Qualified_name:", FQN)

                if len(FQN) == 0: continue
                if "java.lang" in FQN[0]: continue
                if simple_name.count(".") == 0:
                    FQN_list.append("import   " + FQN[0] + "; //" + simple_name)
                elif simple_name.count(".") == 1:
                    FQN_list.append("import   " + FQN[0][:-1] + "; //" + simple_name)

            print("########### Repaired Code Snippet ###########")
            FQN_list = list(set(FQN_list))
            ouput_code_snippet = "\n".join(FQN_list) + "\n"+ "***********************************************************\n"+ \
                                 Simple_Name_Extraction(code_snippet).code_snippet
            print(ouput_code_snippet)
            return ouput_code_snippet
        else:
            for simple_name in sim_name:
                code_Prompt = Prompt_generate(code_snippet, simple_name)  # get the corresponding code prompt
                pred_result = Itera_Pred(code_Prompt, Inference_step=8, Topk=int(top), tokenizer=tokenizer,
                                         model=model).numberMaskSearch()  # start predict
                FQN = [type[1] + "." + simple_name for type in pred_result]
                if mod == "popup":
                    result = result + "simpel_name: \n" + simple_name + "\n\n" + "Full_Qualified_name: \n" + "\n".join(FQN) + "\n" + "************************************************************\n"
                if mod == "context":
                    result = result + "<br/>".join(FQN)
                print("simpel_name:", simple_name, " Full_Qualified_name:", FQN)
        # result = result.replace("\n\t", "\n")
        return result








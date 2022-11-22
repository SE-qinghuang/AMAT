//获取btnInfer按钮
var btnBuildTest = document.getElementById("btnInfer");
//绑定点击事件，发送请求
btnBuildTest.onclick = function () {
    var co_area = document.getElementById("code_area").value
    var co_name = document.getElementById("sim_name").value
    var co_top = document.getElementById("top").value
    var co_all = document.getElementById("all_code").value

    if(co_area){
        chrome.extension.sendRequest({
            action: "infer",
            co_area: co_area,
            co_name: co_name,
            co_top : co_top,
            co_all : co_all,
            model: "popup"
        },
        function(f) {
             if(f.data){
            //将翻译结果显示在result中
            //      alert(f.data)
            document.getElementById("insert_div").innerHTML="<textarea class=\"contents\" >" + f.data;
          }
        });
        document.getElementById("insert_div").innerHTML="waiting..."
    }
}

$(function(){
    var models = new Array(1);
    models[0] = new Array("top-1","top-2","top-3","top-4","top-5");
    models[1] = new Array("top-1");

    $("#all_code").change(function(){
        $("#top").empty();
        var val = this.value;
        $.each(models,function(i,n){
            if(val==i){
                $.each(models[i], function(j,m) {
                    var textNode = document.createTextNode(m);
                    var opEle = document.createElement("option");
                    $(opEle).append(textNode);
                    $(opEle).appendTo($("#top"));
                });
            }
        });

    });
});
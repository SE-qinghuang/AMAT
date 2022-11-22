console.log("加载context脚本")
var px, py, sx, sy;
var list = [];
var lastbutton = null;
var lastFrame = null;
var inBtn = false;
var inFrame = false;
var isPlayAudio = false;
//注册鼠标弹起事件
if (document.body.addEventListener) {
    document.body.addEventListener("mouseup", onEventInfer, false);
} else {
    document.body.attachEvent("onmouseup", onEventInfer);
}
/**
 * 是否全部为中文
 * @param {*} a 
 */
function isAllChinese(a) {
    var b = /^[\u4e00-\u9fa5]+$/;
    if (b.test(a)) {
        return true;
    } else {
        return false;
    }
}
/**
 * 触发infer事件
 * @param {*} c 
 */
function onEventInfer(c) {
    var b = "";
    var a = c.srcelement ? c.srcelement: c.target;
    var m = c.target.localName;

    //获取到鼠标划取到的词
    if (document.getSelection) {
        b = document.getSelection();
    } else {
        if (document.selection) {
            b = document.selection.createRange().text;
        }
    }
    if (inBtn) {
        return;
    }
    if (inFrame) {
        return;
    }
    onCloseFrame();
    onClosebutton();
    b = String(b);
    b = b.replace(/^\s*/, "").replace(/\s*$/, "");
    if (b == "") {
        return;
    }
    if (a.tagName == "INPUT" || a.tagName == "IMG") {
        return;
    }
    if (b.length > 500) {
        return;
    }
    if (isAllChinese(b)) {
        return;
    }
    if (b.indexOf("<") == 1 || b.indexOf(">") == 1) {
        return;
    }
    var z = c.target.innerText;
    if (b !== "") {
        px = c.pageX;
        py = c.pageY;
        sx = c.screenX;
        sy = c.screenY;
        getInfer(b, z, c.pageX, c.pageY, c.screenX, c.screenY);
    }
}
//获取infer信息
function getInfer(d, z, b, a, e, c) {
    chrome.extension.sendRequest({
        action: "infer",
        co_area: z,
        co_name: d,
        co_top : "2",
        co_all : "0",
        model: "context"
    },
    function(f) {
        var g = f.data["pro_code"];
        createTlBtn(b, a, e, c);
        $("#InferWrapper").click(function() {
            createTlFrame(d, b, a, e, c, g);
            $(this).hide();
        });
    });
}
//创建infer悬浮框
function createTlFrame(q, c, b, e, d, s){
    var a = $("<div></div>");
    a.attr("id", "InferContainer");
    // https://docs.oracle.com/javase/8/docs/api/java/io.BufferedReader.html
    var s_url1 = "https://docs.oracle.com/javase/8/docs/api/" + s[0].replaceAll(".", "/") + ".html";
    var s_url2 = "https://docs.oracle.com/javase/8/docs/api/" + s[1].replaceAll(".", "/") + ".html";
    var h = document.createElement("div");
    h.innerHTML = '<div style="padding:13px 13px;width:257px;border:1px solid #ccc;border-radius:2px;box-shadow:0 0 5px #ccc;background:#fff;text-align:left;font-family:\'微软雅黑\';">' +
        '<div><span style="font-size:13px;display:inline-block;font-family:\'微软雅黑\';">Full_Qualified_name: </span>' +
        '<img style="float:right;" id="closeFrame" src="' + chrome.extension.getURL("imgs/close.png") + '"></div>' +
        '<a href=" '+ s_url1 +'" target="_blank">' +
        '<p id="content" style="white-space:normal;margin-top:8px;font-size:13px;font-family:\'微软雅黑\';color:#333;padding:0;line-height:18px;width:200px;">' + s[0] + '</p></a>'+
        '<a href=" '+ s_url2 +'" target="_blank">' +
        '<p id="content" style="white-space:normal;margin-top:8px;font-size:13px;font-family:\'微软雅黑\';color:#333;padding:0;line-height:18px;width:200px;">' + s[1] + '</p></a>';
    a[0].appendChild(h);
    var o = 310;
    var g = 100;
    var f = 0;
    var m = 0;
    var n = screen.availWidth;
    var r = screen.availHeight;
    if (e + o < n) {
        f = c;
    } else {
        f = c - o - 20;
    }
    a[0].style.left = f + "px";
    if (d + g + 20 < r) {
        m = b;
    } else {
        m = b - g - 20;
    }
    a[0].style.top = m + 10 + "px";
    a[0].style.position = "absolute";
    a[0].style.zIndex = 10002;
    document.body.style.position = "static";
    document.body.appendChild(a[0]);
    list.push(a);
    $("#InferContainer").mouseover(function() {
        inFrame = true;
    }).mouseout(function(){
        inFrame = false;
    });
    $("#closeFrame").hover(function() {
        $(this).attr("src", chrome.extension.getURL("imgs/close_hover.png"));
    },
    function() {
        $(this).attr("src", chrome.extension.getURL("imgs/close.png"));
    });
    if (lastFrame != null) {
        if (lastFrame.css("left") !== $button.css("left")) {
            document.body.removeChild(lastFrame[0]);
        }
    }
    lastFrame = a;
    $("#closeFrame").click(function(){
        inFrame = false;
        $("#InferContainer").hide();
    });
    $("#moreMean").click(function() {
        inFrame = false;
        $("#InferContainer").hide();
    });

}
//创建infer按钮
function createTlBtn(h, g, e, d) {
    var a = $("<div></div>");
    a.attr("id", "InferWrapper");
    a.html("AT");
    a.css({
        height: "32px",
        width: "33px",
        "font-family": "微软雅黑",
        "font-size": "14px",
        "text-align": "center",
        "line-height": "32px",
        color: "#fff",
        "background-color": "#4395FF",
        "border-radius": "2px",
        cursor: "pointer",
        "z-index": "99999"
    });
    var j = 35;
    var l = 35;
    var f = 0;
    var i = 0;
    var b = screen.availWidth;
    var c = screen.availHeight;
    var k = 10;
    if (e + j < b) {
        f = h;
    }
    a[0].style.left = f + "px";
    i = g;
    a[0].style.top = i + 10 + "px";
    a[0].style.position = "absolute";
    document.body.style.position = "static";
    document.body.appendChild(a[0]);
    $("#InferWrapper").mouseover(function() {
        inBtn = true;
    }).mouseout(function() {
        inBtn = false;
    });
    list.push(a);
    if (lastbutton !== null) {
        if (lastbutton.css("left") !== a.css("left")) {
            document.body.removeChild(lastbutton[0]);
        }
    }
    lastbutton = a;
}
//移除Frame(翻译悬浮框)框
function onCloseFrame() {
    if (inFrame) {
        return;
    }
    if (lastFrame != null) {
        while (list.length != 0) {
            document.body.removeChild(list.pop()[0]);
        }
        lastFrame = null;
        return true;
    }
    return false;
}
//移除按钮
function onClosebutton() {
    if (inBtn) {
        return;
    }
    if (lastbutton != null) {
        while (list.length != 0) {
            document.body.removeChild(list.pop()[0]);
        }
        lastbutton = null;
        return true;
    }
    return false;
}
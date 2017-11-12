
var langList = ["漢  字","諺  文","Quốc Ngữ","字  喃","中古羅馬","中古鄭張","上古鄭張"];//zgys to 汉字,汉字 to all the others,maybe 谚文 to 汉字,Chữ Quốc Ngữ to 字喃
var codeList = ["hanzi","hangul","ynpy"    ,"ynzn" ,"zgys"   ,"zgzz"   ,"sgzz"];
$(document).ready(function(){
    $("#src .dropdown-menu")
        .append("<li><a href='#'>"+langList[0]+"</a></li>")
        .append("<li><a href='#'>"+langList[4]+"</a></li>")
        .append("<li><a href='#'>"+langList[1]+"</a></li>")
        .append("<li><a href='#'>"+langList[2]+"</a></li>");
    $("#src .dropdown-menu li").click(function(){
        var sel = $(this);
        $(this).parent().siblings("#seleted:first").text(function(i,old){
            selectAlanguage($("#src #seleted"),sel,$("#src .dropdown-menu li:contains('"+old+"')"));
        });
    });
    selectAlanguage($("#src #seleted"),$("#src .dropdown-menu li").eq(1));

    $("#dst .dropdown-menu")
        .append("<li><a href='#'>"+langList[0]+"</a></li>")
        .append("<li><a href='#'>"+langList[4]+"</a></li>")
        .append("<li><a href='#'>"+langList[5]+"</a></li>")
        .append("<li><a href='#'>"+langList[6]+"</a></li>")
        .append("<li><a href='#'>"+langList[1]+"</a></li>")
        .append("<li><a href='#'>"+langList[2]+"</a></li>")
        .append("<li><a href='#'>"+langList[3]+"</a></li>");
    $("#dst .dropdown-menu li").click(function(){
        var sel = $(this);
        $(this).parent().siblings("#seleted:first").text(function(i,old){
            selectAlanguage($("#dst #seleted"),sel,$("#dst .dropdown-menu li:contains('"+old+"')"));
        });
    });
    selectAlanguage($("#dst #seleted"),$("#dst .dropdown-menu li").eq(0));

    $("#resultText").height($("#searchText").height());
});
function selectAlanguage(_top,_li,_old){
    if(_old&&_li.text()==_old.text()) return;

    _top.text(_li.text());
    _li.addClass("disabled");
    if(_old){
        _old.removeClass("disabled");
    }
}
function transCharacter(){
    var sendmsg = $("#searchText").val();
    var srcid = langList.findIndex((txt) => txt==$("#src #seleted").text());
    var dstid = langList.findIndex((txt) => txt==$("#dst #seleted").text());
    var srclang,dstlang;
    if(srcid==-1){
        //some error
        return;
    }else{
        srclang = codeList[srcid];
    }
    if(dstid==-1){
        //some error
        return;
    }else{
        dstlang = codeList[dstid];
    }
    var _data = JSON.stringify({
        text: sendmsg,
        srclang: srclang,
        dstlang: dstlang
    }, null, '\t');

    $.ajax({
        type: "POST",
        url: "/sentence",
        contentType: "application/json;charset=UTF-8",
        data: _data,
        dataType: "json",
        success: function(netdata){
            var f = $("#resultText");
            f.html('');
            for(zizu of netdata["results"]){
                f.append('<span class="dropdown parsechar"></span>');
                var fstf = f.find(".dropdown:last");
                if(zizu.length<=0){
                    fstf.append('<span class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown">??</span>');
                }else{
                    fstf.append('<span class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown">'+zizu[0]+'</span>');
                    if(zizu.length>1){
                        fstf.append('<ul class="dropdown-menu" style="max-height:200px;overflow:auto;"></ul>');
                        var secf = fstf.find("ul");
                        for(zi of zizu){
                            if(zi==zizu[0]) continue;
                            secf.append('<li><a href="#">'+zi+'</a></<li>');
                        }
                    }
                }
            }
        }
    });
}

$(document).ready(function(){
    let isLoggined = getCookie("id") != null

    let top_right_text = ''
    
    if(isLoggined){
        let id = getCookie("id")
        top_right_text = `<a href="/my?id=${id}">내정보</a> / <a style="padding-right:10px" href="#" onclick='logout();'>로그아웃</a>`
    } else {
        top_right_text = '<a href="/join">회원가입</a> / <a style="padding-right:10px" href="/login">로그인</a>'
    }

    let temp_html = `<div class="banner">
                        <div style="height: 35%; width: 100%; text-align:right">
                            ${top_right_text}
                        </div>
                        <div style="width: 100%; text-align: center;">
                            <h1 onclick=goHome()>Today's Music</h1>
                        </div>
                    </div>`
    $("body").prepend(temp_html)
})

function goHome() {
    window.location.href = window.location.protocol + "//" + window.location.host + "/main"
}

var setCookie = function(name, value, exp) {
    var date = new Date();
    date.setTime(date.getTime() + exp*24*60*60*1000);
    document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
};

var getCookie = function(name) {
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value? value[2] : null;
};

var logout = function() {
    deleteCookie("id")
    alert("로그아웃 되었습니다.")
    window.location.href = window.location.protocol + "//" + window.location.host + "/main"
}

var deleteCookie = function(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1999 00:00:10 GMT;';
}
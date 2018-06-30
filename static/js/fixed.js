$(function(){
    bindEvent();
    scrollSet();
    window.onscroll = function() {
        scrollSet();
        // setScrollLoad();
    };
    if(window.onresize === null) {
        window.onresize = function() {
            resetStatus();
            fixBottom();
        }
    }
    fixBottom();
});

// 导航栏触发事件
function bindEvent() {
    $('#toggle-menu').on('click', function(){
        slideNav($(this));
    });
    $('.nav-menu .icon-remove-sign').parent('li').on('click', function() {
        $('.nav-menu').hide('slide', 300);
    });
    $('.scrollToTop i').on('click', function() {
        $('html,body').animate({'scrollTop': 0}, 300);
    })
}

// 设置fixed头部导航
function scrollSet() {
    var $menuBox = $('#menu-box');
    if($(window).scrollTop() > 32) {
        if(!$menuBox.hasClass('shadow')){
            $menuBox.addClass('shadow');
        }
        smWidgetsFixed(1);
    } else {
        if($menuBox.hasClass('shadow')){
            $('#menu-box').removeClass('shadow');
        }
        smWidgetsFixed(0);
    }
}

// 导航栏滑动事件
function slideNav($selector) {
    var $navMenu = $selector.siblings('.nav-menu');
    if($navMenu.css('display') === "none"){
        $navMenu.show('slide', 300);
    } else {
        $navMenu.hide('slide', 300);
    }
}

// 小组件固定
function smWidgetsFixed(flag) {
    var $rightWidgets = $('.rightWidgets');
    if(flag) {
        $rightWidgets.fadeIn(500);
    } else if(flag === 0) {
        $rightWidgets.fadeOut(500);
    }
}

function resetStatus() {
    if($(window).width() > '490') {
        $('.nav-menu').css('display', 'none');
    }
}

function fixBottom() {
    if($('.transform-body').height() < '640') {
        $('#footer').addClass('footer-fix');
    } else{
        $('#footer').removeClass('footer-fix');
    }
}

function getElementTop (el) {
    var actualTop = el.offsetTop;
    var current = el.offsetParent;
    while (current !== null) {
    actualTop += current.offsetTop;
    current = current.offsetParent;
    }
    return actuanlTop
}

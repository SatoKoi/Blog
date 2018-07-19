$(function(){
    bindEvent();
    scrollSet();
    imagePreview();
    var $image = $('.entry-img');
    var finishArray = [];
    for(var _ = 0; _ < $image.length; _++) {
        finishArray.push(0);
    }
    finishArray = _imageLazyload($image, $(window), finishArray);
    imageLazyLoad(finishArray);
    $image.load(function(event){
        $(event.target).animate({opacity: 1}, 500);
    });
    $(window).load(function (){
        fixBottom();
    });
    $(window).scroll(function () {
        scrollSet();
    });
    $(window).resize(function() {
        resetStatus();
        fixBottom();
    });
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
    var $topHeader = $('#top-header');
    var topHeight;
    if($topHeader.is(':hidden')) {
        topHeight = 0;
    } else {
        topHeight = $topHeader.outerHeight();
    }
    if($(window).scrollTop() > ($menuBox.outerHeight() + topHeight)) {
        $menuBox.addClass('shadow');
        smWidgetsFixed(1);
    } else if($(window).scrollTop() <= $menuBox.outerHeight()){
        $menuBox.removeClass('shadow');
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
    if(($('#footer').offset().top + $('#footer').outerHeight()) < $(window).height()) {
        $('#footer').addClass('footer-fix');
    } else if($('body').outerHeight() > $('#footer').offset().top){
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

// 图片预览
function imagePreview() {
    var $img = $('#imageWidget');
    var $imgGallery = $('.img-gallery');
    var reader = new FileReader();
    $img.on('change', function() {
        var obj = $img[0].files[0];
        // 如果有文件对象
        if (obj) {
            reader.onload = function (event) {
                $imgGallery.attr('src', event.target.result);
            };
            reader.readAsDataURL(obj);
        } else {
            reader.readAsDataURL(new Blob());
        }
    });
}

function imageLazyLoad(finishArray) {
    var $image = $('.entry-img');
    var done = false;
    var $window = $(window);
    $window.scroll(function() {
        var sum = 0;
        if(!done){
            $image.each(function(index, item) {
                if($(item).offset().top <= $window.height() + $window.scrollTop()) {
                    if (finishArray[index] === 1) {
                        return;
                    }
                    $(item).attr("src", $(item).attr("data-src"));
                    finishArray[index] = 1;
                }
            });
            finishArray.forEach(function(item, index, array) {
                sum += item;
                if(sum === array.length) {
                    done = true;
                }
            })
        }
    })
}

function _imageLazyload($image, $window, finishArray) {
    $image.each(function(index, item) {
        if($(item).offset().top <= $window.height() + $window.scrollTop()) {
            $(item).attr("src", $(item).attr("data-src"));
            finishArray[index] = 1;
        }
    });
    return finishArray;
}

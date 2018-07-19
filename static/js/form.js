$(function() {
    $('.search').delegate('a', 'click', function(event) {
       var target = event.currentTarget;
       var oInput = $(target).prev();
       var value = oInput.val();
       if(value !== "") {
           oInput.val('');
           window.location.href = "/search?keyword=" + value;
       }
    })
    $('.search').delegate('input', 'keypress', function(event) {
        if(event.keyCode == "13") {
            event.preventDefault();
            $('.search a').trigger('click');
        }
    })
});

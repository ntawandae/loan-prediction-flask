$(document).ready(function(){
    $('.toggle').click(function(){
        $('.toggle').toggleClass('active')
        $('.navigation').toggleClass('active')
    })
});
//        for search bar
$(document).on('click', '.search', function(event){
    event.preventDefault(); // Prevent default form submission
    $('.search-bar').addClass('search-bar-active');
});
        $(document).on('click','.search-cancel',function(){
            $('.search-bar').removeClass('search-bar-active')
        });
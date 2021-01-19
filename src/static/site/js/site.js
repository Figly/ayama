(function () {
  $(window).scroll(function () {
    var top = $(document).scrollTop();
    $('.corporate-jumbo').css({
      'background-position': '0px -' + (top / 3).toFixed(2) + 'px'
    });
    if (top > 50)
      $('.navbar').removeClass('navbar-transparent');
    else
      $('.navbar').addClass('navbar-transparent');
  }).trigger('scroll');
})();

$.ajaxSetup({
  headers: {
    "X-CSRFToken": '{{csrf_token}}'
  }
});

function on() {
  document.getElementById("figly-overlay").style.display = "block";
}

function off() {
  document.getElementById("figly-overlay").style.display = "none";
}
var swiper = new Swiper(".swiper-container", {
  effect: "coverflow",
  grabCursor: true,
  centeredSlides: true,
  slidesPerView: "auto",
  coverflowEffect: {
    rotate: 50,
    stretch: 0,
    depth: 100,
    modifier: 1,
    slideShadows: true,
  },
  pagination: {
    el: ".swiper-pagination",
  },
});

swiper.on("slideChange", function () {
  // Rest the rotation attribute on all slides
  $(".swiper-slide").attr("data-y-rotation" , parseInt(0));
});

let isFlipped = false;
$(document).on('click tap', '.swiper-slide-active', function () {
    console.log("Clicked on active-slide")
    $( this).css("transition", "all 500ms ease 0s");

    if(isFlipped)
    {
      $( this).css({'transform' : 'rotateY(0deg)'});
      swiper.allowTouchMove = true;
      isFlipped = false;
    }
    else{
      $( this).css({'transform' : 'rotateY(180deg)'});
      swiper.allowTouchMove = false;
      isFlipped = true;
    }  
});




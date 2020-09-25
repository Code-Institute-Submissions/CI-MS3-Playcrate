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

updateUiWithCurrentlySelectedGame = function () {
  if ($(".swiper-slide-active").length) {
    
    if ($("#game-title").length) {
      $("#game-title").text(
        $(".swiper-slide-active").attr("data-title")
      );
    }

    if ($("#game-release_date").length) {
      $("#game-release_date").text(
        $(".swiper-slide-active").attr("data-release-date")
      );
    }

    if ($("#view-game").length) {
      $("#view-game").attr(
        "href",
        "/games/" + $(".swiper-slide-active").attr("data-title")
      );
    }

    if ($("#add-game-to-collection").length) {
      $("#add-game-to-collection").attr(
        "href",
        "/add-game-to-collection/" + $(".swiper-slide-active").attr("id")
      );
    }
    if ($("#remove-game-from-collection").length) {
      $("#remove-game-from-collection").attr(
        "href",
        "/remove-game-from-collection/" + $(".swiper-slide-active").attr("id")
      );
    }
    if ($("#add-game-to-playcrate").length) {
      $("#add-game-to-playcrate").attr(
        "href",
        "/add-game-to-playcrate/" + $(".swiper-slide-active").attr("id")
      );
    }
    if ($("#remove-game-from-playcrate").length) {
      $("#remove-game-from-playcrate").attr(
        "href",
        "/remove-game-from-playcrate/" + $(".swiper-slide-active").attr("id")
      );
    }
  }
};

updateUiWithCurrentlySelectedGame();
swiper.on("slideChange", function () {
  setTimeout(updateUiWithCurrentlySelectedGame, 100);
});

// $(document).click(function (event) {
//   console.log($(event.target));
// });

let isFlipped = false;
$(document).on("click tap", ".swiper-slide-active", function () {
  console.log("Clicked on active-slide");
  $(this).css("transition", "all 500ms ease 0s");

  if (isFlipped) {
    $(this).css({ transform: "rotateY(0deg)" });
    swiper.allowTouchMove = true;
    isFlipped = false;
  } else {
    $(this).css({ transform: "rotateY(180deg)" });
    swiper.allowTouchMove = false;
    isFlipped = true;
  }
});

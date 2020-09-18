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
  if ($("#game-title").length) {
    document.getElementById(
      "game_title"
    ).innerText = document
      .getElementsByClassName("swiper-slide-active")[0]
      .getAttribute("data-title");
  }

  if ($("#game_release_date").length) {
    document.getElementById(
      "game_release_date"
    ).innerText = document
      .getElementsByClassName("swiper-slide-active")[0]
      .getAttribute("data-release-date");
  }

  if ($("#view-game").length) {
    document
      .getElementById("view-game")
      .setAttribute(
        "href",
        "games/" +
          document
            .getElementsByClassName("swiper-slide-active")[0]
            .getAttribute("data-title")
      );
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

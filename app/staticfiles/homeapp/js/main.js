$(document).ready(function () {
    $('.customer-logos').slick({
        slidesToShow: 6,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 1500,
        arrows: false,
        dots: false,
        pauseOnHover: false,
        responsive: [{
            breakpoint: 768,
            settings: {
                slidesToShow: 3
            }
        }, {
            breakpoint: 520,
            settings: {
                slidesToShow: 2
            }
        }]
    });

    $(".team-slider").slick({
        dots: true,
        infinite: true,
        speed: 300,
        slidesToShow: 3,
        slidesToScroll: 1,
        responsive: [
          {
            breakpoint: 1024,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1,
              infinite: true,
              dots: true,
            },
          },
          {
            breakpoint: 767,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 520,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
              dots: false,
            },
          }
        ],
    });

    $('.diploms').slick({
        slidesToShow: 5,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 1500,
        arrows: false,
        dots: false,
        draggable: false,
        pauseOnHover: true,
        responsive: [{
            breakpoint: 1200,
            settings: {
                slidesToShow: 4
            }
        }, {
            breakpoint: 767,
            settings: {
                slidesToShow: 3
            }
        }, {
            breakpoint: 520,
            settings: {
                slidesToShow: 3
            }
        }],
    });

    // Находим все изображения дипломов
    const diplomaImages = document.querySelectorAll('.diploma-img');
    const modalImage = document.getElementById('diplomaModalImage');
    const modalLabel = document.getElementById('diplomaModalLabel');

    diplomaImages.forEach(function (image) {
        // Обработчик клика для каждого изображения
        image.addEventListener('click', function (image) {
            // Подставляем URL изображения в модальное окно
            modalImage.src = event.target.src;
            modalImage.alt = event.target.alt;
            modalLabel.innerHTML = event.target.alt;
        });
    });
});
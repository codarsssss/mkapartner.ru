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
                slidesToShow: 4
            }
        }, {
            breakpoint: 520,
            settings: {
                slidesToShow: 3
            }
        }]
    });

    $('.diploms').slick({
        slidesToShow: 5,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 1500,
        arrows: false,
        dots: true,
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
                dots: false,
                slidesToShow: 3
            }
        }],
    });

    console.log('тест')
    // Находим все изображения дипломов
    const diplomaImages = document.querySelectorAll('.diploma-img');
    const modalImage = document.getElementById('diplomaModalImage');
    const modalLabel = document.getElementById('diplomaModalLabel');

    diplomaImages.forEach(function (image) {
        // Обработчик клика для каждого изображения
        image.addEventListener('click', function (image) {
            console.log(image)
            // Подставляем URL изображения в модальное окно
            modalImage.src = event.target.src;
            console.log(modalImage.alt)
            modalImage.alt = event.target.alt;
            modalLabel.innerHTML = event.target.alt;
        });
    });
});
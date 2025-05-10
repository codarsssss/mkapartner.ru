$(document).ready(function () {
    // Прелоадер
    const preloader = document.querySelector('.preloader')

    setTimeout(() => {
        preloader?.classList.add('is-hidden')
    }, 1000)


    // Находим все изображения дипломов
    const diplomaImages = document.querySelectorAll('.diploma-img');
    const modalImage = document.getElementById('diplomaModalImage');
    const modalLabel = document.getElementById('diplomaModalLabel');

    diplomaImages.forEach(function (image) {
        image.addEventListener('click', function (image) {
            modalImage.src = event.target.src;
            modalImage.alt = event.target.alt;
            modalLabel.innerHTML = event.target.alt;
        });
    });


    //Burger-menu
    const burger = document.querySelector('.js-headerBurger')
    const navigation = document.querySelector('.js-headerNav')

    burger.addEventListener('click', () => {
        burger.classList.toggle('is-active')
        navigation.classList.toggle('is-show')
    })


    //Сортировка новостей
    const newsItems = document.querySelectorAll('.js-newsItem')

    if (newsItems.length > 0) {
        const filterButtons = document.querySelectorAll('.js-newsSortButton')

        filterButtons?.forEach((button) => {
            button.addEventListener('click', function () {
                filterButtons.forEach((el) => el.classList.remove('is-active'))
                this.classList.add('is-active')
                const buttonCategory = this.dataset.category
                newsItems.forEach((el) => {
                    el.style.display = 'none'
                    if (el.dataset.category.toLowerCase() === buttonCategory.toLowerCase()) el.style.display = 'block'
                    if (buttonCategory === 'all') el.style.display = 'block'
                })
            })
        })
    }
});
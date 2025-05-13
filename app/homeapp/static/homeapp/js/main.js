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


      const input = document.body.querySelector(".telmask");
      input?.addEventListener("keypress", (evt) => {
        if (evt.keyCode < 47 || evt.keyCode > 57) {
          evt.preventDefault();
        }
      });

      input?.addEventListener("focus", () => {
        if (input.value.length === 0) {
          input.value = "+7";
          input.selectionStart = input.value.length;
        }
      });

      input?.addEventListener("click", (evt) => {
        if (input.selectionStart < 2) {
          input.selectionStart = input.value.length;
        }
        if (evt.key === "Backspace" && input.value.length <= 2) {
          evt.preventDefault();
        }
      });

      input?.addEventListener("blur", () => {
        if (input.value === "+7") {
          input.value = "";
        }
      });

      input?.addEventListener("keydown", (evt) => {
        if (evt.key === "Backspace" && input.value.length <= 2) {
          evt.preventDefault();
        }
      });

      const input_1 = document.body.querySelector(".phone_mask");
      input_1?.addEventListener("keypress", (evt) => {
        if (evt.keyCode < 47 || evt.keyCode > 57) {
          evt.preventDefault();
        }
      });

      input_1?.addEventListener("focus", () => {
        if (input_1.value.length === 0) {
          input_1.value = "+7";
          input_1.selectionStart = input_1.value.length;
        }
      });

      input_1?.addEventListener("click", (evt) => {
        if (input_1.selectionStart < 2) {
          input_1.selectionStart = input_1.value.length;
        }
        if (evt.key === "Backspace" && input_1.value.length <= 2) {
          evt.preventDefault();
        }
      });

      input_1?.addEventListener("blur", () => {
        if (input_1.value === "+7") {
          input_1.value = "";
        }
      });

      input_1?.addEventListener("keydown", (evt) => {
        if (evt.key === "Backspace" && input_1.value.length <= 2) {
          evt.preventDefault();
        }
      });


      var submenus = document.querySelectorAll(
        ".dropdown-submenu .dropdown-toggle"
      );
      submenus.forEach(function (submenu) {
        var dropdownContent = submenu.nextElementSibling; // Получаем подменю, связанное с каждым элементом

        // Слушатель для открытия подменю по клику
        submenu.addEventListener("click", function (event) {
          event.stopPropagation(); // Предотвращаем всплытие события
          // Переключаем видимость подменю
          dropdownContent.style.display =
            dropdownContent.style.display === "block" ? "none" : "block";
        });
      });

      // Слушатель для закрытия всех подменю, если клик произошел вне подменю
      document.addEventListener("click", function () {
        var openDropdowns = document.querySelectorAll(
          ".dropdown-submenu .dropdown-menu"
        );
        openDropdowns.forEach(function (openDropdown) {
          if (openDropdown.style.display === "block") {
            openDropdown.style.display = "none";
          }
        });
      });
});
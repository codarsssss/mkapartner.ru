const sliders = document.querySelectorAll('.mySlider');

if (sliders.length > 0) {
  sliders.forEach((slider) => {
    const slidesCount = slider.dataset.slidesCount 
      ? parseInt(slider.dataset.slidesCount) 
      : 3;
    const slidesCountTablet = slider.dataset.slidesCountTablet 
      ? parseInt(slider.dataset.slidesCountTablet) 
      : 2;
    const slidesCountMob = slider.dataset.slidesCountMob 
      ? parseInt(slider.dataset.slidesCountMob) 
      : 1;

    const autoplaySettings = slider.hasAttribute('data-autoplay') ? {
      autoplay: {
        delay: 3000,
        pauseOnMouseEnter: true,
        disableOnInteraction: false
      }
    } : {};

    const swiper = new Swiper(slider, {
      slidesPerView: slidesCount,
      spaceBetween: 8,
      loop: true,
      ...autoplaySettings,
      breakpoints: {
        320: {
          slidesPerView: slidesCountMob,
          spaceBetween: 8
        },
        720: {
          slidesPerView: slidesCountTablet,
          spaceBetween: 8
        },
        1000: {
          slidesPerView: slidesCount,
          spaceBetween: 8
        }
      }
    });
  });
}
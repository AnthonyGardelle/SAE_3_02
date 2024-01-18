let currentIndex = 0;
const carousel = document.getElementById('carousel');
const carousel2 = document.getElementById('carousel2');
const items = document.querySelectorAll('.carousel-item');
const totalItems = items.length;

function getIndex() {
    return currentIndex;
}

function nextSlide() {
    if (currentIndex < totalItems - 1) {
        currentIndex++;
    } else {
        currentIndex = 0;
    }
    updateCarousel();
    updateCarousel2();
}

function prevSlide() {
    if (currentIndex > 0) {
        currentIndex--;
    } else {
        currentIndex = totalItems - 1;
    }
    updateCarousel();
    updateCarousel2();
}

function updateCarousel() {
    const newTransformValue = -currentIndex * 100 + '%';
    carousel.style.transform = 'translateX(' + newTransformValue + ')';
}

function updateCarousel2() {
    const newTransformValue = -currentIndex * 100 + '%';
    carousel2.style.transform = 'translateX(' + newTransformValue + ')';
}
const starContainer = document.getElementById('stars');

function createStars(count) {
    for (let i = 0; i < count; i++) {
        const star = document.createElement('div');
        star.classList.add('star');

        star.style.top = `${Math.random() * 100}vh`;
        star.style.left = `${Math.random() * 100}vw`;
        let scale = `${1 + (Math.random() * 2)}px`;
        star.style.height = scale;
        star.style.width = scale;

        star.style.animationDelay = `${Math.random() * 5}s`;

        starContainer.appendChild(star);
    }
}

createStars(500);

const submitBtn = document.getElementById("submit")

submitBtn.addEventListener("mousedown", () => {
    const URL = document.getElementById("url").value
    if (URL === "") { return }
    const type = document.getElementById("type").value

    window.location.href = `/${type}?url=${encodeURIComponent(URL)}`
})
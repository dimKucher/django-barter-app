let toast = document.getElementById("message");
    document.getElementById("close-button-message").addEventListener("click", function () {
        toast.remove()
    }
);

function fadeOutEffect(time) {
    var fadeTarget = document.getElementById("message");
    var fadeEffect = setInterval(function () {
    if (!fadeTarget.style.opacity) {
        fadeTarget.style.opacity = 1;
    }
    if (fadeTarget.style.opacity > 0) {
        fadeTarget.style.opacity -= 0.1;
    } else {
        clearInterval(fadeEffect);
    }
    }, time);
}
fadeOutEffect(800)
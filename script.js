// static/js/script.js
document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll(".nav-link");

    tabs.forEach(tab => {
        tab.addEventListener("click", function (e) {
            e.preventDefault();

            tabs.forEach(t => t.classList.remove("active"));
            this.classList.add("active");

            const contentSections = document.querySelectorAll(".tab-section");
            contentSections.forEach(section => section.style.display = "none");

            const target = this.getAttribute("href").substring(1);
            document.getElementById(target).style.display = "block";
        });
    });

    // Default tab
    document.querySelector(".nav-link.active").click();

    // Upload functionality
    const form = document.getElementById('upload-form');
    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(form);

        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        document.getElementById('result').innerText = result.message;
        if (result.generated_image_url) {
            document.getElementById('gen-image').src = result.generated_image_url;
            document.getElementById('gen-image').style.display = 'block';
        }
    });
});

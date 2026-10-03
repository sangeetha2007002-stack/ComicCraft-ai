document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("comicForm");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        loading.style.display = "block";
        result.innerHTML = "";

        const formData = new FormData(form);

        const data = {
            prompt: formData.get("prompt"),
            character: formData.get("character"),
            setting: formData.get("setting"),
            tone: formData.get("tone"),
            art_style: formData.get("art_style")
        };

        try {
            const response = await fetch("/generate-comic", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error("Failed to generate comic");
            }

            const comic = await response.json();

            displayComic(comic);

        } catch (error) {
            console.error(error);

            result.innerHTML = `
                <div class="panel">
                    <h3>Error</h3>
                    <p>Unable to generate the comic. Please try again.</p>
                </div>
            `;
        } finally {
            loading.style.display = "none";
        }
    });

    function displayComic(comic) {

        let html = "<h2>Generated Comic</h2>";

        if (comic.title) {
            html += <h3>${comic.title}</h3>;
        }

        if (comic.panels && Array.isArray(comic.panels)) {

            comic.panels.forEach((panel, index) => {

                html += `
                    <div class="panel">
                        <h3>Panel ${index + 1}</h3>
                `;

                if (panel.description) {
                    html += <p>${panel.description}</p>;
                }

                if (panel.dialogue) {
                    html += <p><strong>Dialogue:</strong> ${panel.dialogue}</p>;
                }

                if (panel.image) {
                    html += `
                        <img src="${panel.image}" alt="Comic Panel ${index + 1}">
                    `;
                }

                html += "</div>";
            });

        } else if (comic.story) {

            html += `
                <div class="panel">
                    <p>${comic.story}</p>
                </div>
            `;
        }

        result.innerHTML = html;
    }
});
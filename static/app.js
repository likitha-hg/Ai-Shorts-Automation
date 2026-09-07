console.log("app.js loaded");

// Live status polling
async function checkStatus() {
    try {
        const response = await fetch("/status");
        const data = await response.json();

        document.getElementById("status").textContent = data.step;

        if (
            data.step !== "Completed ✅" &&
            data.step !== "Failed ❌"
        ) {
            setTimeout(checkStatus, 500);
        }

    } catch (error) {
        console.error("Status check failed:", error);
    }
}

async function generateVideo() {
    const title =
        document.getElementById("title").value.trim();

    const hook =
        document.getElementById("hook").value.trim();

    const keywords =
        document.getElementById("keywords").value
            .split(",")
            .map(k => k.trim())
            .filter(k => k !== "");

    const targetAudience =
        document.getElementById("target_audience").value.trim();

    const duration =
        parseInt(
            document.getElementById("duration").value
        );

    if (!title || !hook) {
        alert("Please enter title and hook");
        return;
    }

    const loading =
        document.getElementById("loading");

    const result =
        document.getElementById("result");

    loading.style.display = "block";
    result.style.display = "none";

    // Start status polling
    checkStatus();

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                hook: hook,
                keywords: keywords,
                target_audience: targetAudience,
                duration: duration
            })
        });

        const data = await response.json();

        if (!response.ok) {
            document.getElementById("status").textContent = "Failed ❌";
            loading.style.display = "none";

            throw new Error(
                data.detail || "Generation failed"
            );
        }

        // Script
        document.getElementById("script").textContent =
            data.script || "No script generated";

        // Scenes
        const scenesContainer =
            document.getElementById("scenes");

        scenesContainer.innerHTML = "";

        if (data.scenes) {
            data.scenes.forEach(scene => {
                const li = document.createElement("li");
                li.textContent = scene;
                scenesContainer.appendChild(li);
            });
        }

        // Final video
        const video =
            document.getElementById("video");

        video.src =
            "/" + data.video + "?t=" + Date.now();

        video.load();

        // Download button
        const downloadBtn =
            document.getElementById("downloadBtn");

        downloadBtn.href =
            "/" + data.video + "?t=" + Date.now();

        result.style.display = "block";

        // Hide loading only after completion
        document.getElementById("status").textContent = "Completed ✅";
        loading.style.display = "none";

    } catch (error) {
        console.error(error);

        document.getElementById("status").textContent = "Failed ❌";
        loading.style.display = "none";

        alert(error.message || "Generation failed");
    }
}
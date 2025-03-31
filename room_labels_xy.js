(async () => {
    // Ensure a scene is active
    if (!canvas.scene) {
        ui.notifications.warn("No active scene found.");
        return;
    }

    let output = [];
    let digitPattern = /^\d/; // Regex to check if text starts with a digit

    // Loop through all drawings in the scene
    for (let drawing of canvas.scene.drawings) {
        let text = drawing.text?.trim();
        if (text && digitPattern.test(text)) {
            let x = Math.round(drawing.x);
            let y = Math.round(drawing.y);
            output.push({ text, x, y });
        }
    }

    if (output.length === 0) {
        ui.notifications.info("No matching text-containing drawings found.");
        return;
    }

    // Sort numerically based on the leading number in the text
    output.sort((a, b) => {
        let numA = parseInt(a.text.match(/^\d+/)[0], 10);
        let numB = parseInt(b.text.match(/^\d+/)[0], 10);
        return numA - numB;
    });

    // Convert sorted output to text format
    let outputText = output.map(entry => `${entry.text}: ${entry.x},${entry.y}`).join("\n");

    // Create and download the text file
    let blob = new Blob([outputText], { type: "text/plain" });
    let url = URL.createObjectURL(blob);
    let a = document.createElement("a");
    a.href = url;
    a.download = "foundry_text_drawings_filtered_sorted.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    ui.notifications.info("Filtered and sorted text file created.");
})();

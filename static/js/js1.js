document.addEventListener("DOMContentLoaded", () => {
    const generateButton = document.getElementById("generateButton");
    const textInput = document.getElementById("textInput");
    const imageContainer = document.getElementById("imageContainer");
    const progressBar = document.getElementById("progressBar");
  
    const YOUR_API_KEY = "ea9bca0737a3b3016ea6539b5a05adfeb2e3c702056a6c5cf0a948c776dc8cb5a1b0a1526038ef3411e39eca593ba791"; // Replace with your API key
  
    function animateProgressBar(duration) {
      let start = null;
  
      function step(timestamp) {
        if (!start) start = timestamp;
        const progress = Math.min(1, (timestamp - start) / duration);
        progressBar.style.width = `${progress * 100}%`;
  
        if (progress < 1) {
          requestAnimationFrame(step);
        }
      }
  
      requestAnimationFrame(step);
    }
  
    generateButton.addEventListener("click", async () => {
      const textPrompt = textInput.value.trim();
  
      if (textPrompt !== "") {
        try {
          const form = new FormData();
          form.append("prompt", textPrompt);
  
          progressBar.style.width = "0";
          progressBar.style.display = "block";
  
          animateProgressBar(8000);
  
          const response = await fetch("https://clipdrop-api.co/text-to-image/v1", {
            method: "POST",
            headers: {
              "x-api-key": YOUR_API_KEY,
            },
            body: form,
          });
  
          const buffer = await response.arrayBuffer();
          const blob = new Blob([buffer], { type: "image/jpeg" });
  
          const imageUrl = URL.createObjectURL(blob);
  
          const imageElement = document.createElement("img");
          imageElement.src = imageUrl;
  
          imageContainer.innerHTML = "";
          imageContainer.appendChild(imageElement);
  
          progressBar.style.display = "none";
        } catch (error) {
          console.error("Error:", error);
        }
      }
    });
  });
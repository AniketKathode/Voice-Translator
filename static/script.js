const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const original = document.getElementById("original");
const translated = document.getElementById("translated");
const audioElement = document.getElementById("audio");

let mediaRecorder;
let audioChunks = [];

startButton.onclick = () => {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream); // Recording audio
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const blob = new Blob(audioChunks, { type: 'audio/webm' });
            const formData = new FormData();
            formData.append("audio_data", blob);

            const response = await fetch("/transcribe", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            original.textContent = data.transcribed;
            translated.textContent = data.translated;
            audioElement.src = data.audio_url;

            // Reset buttons
            startButton.disabled = false;
            stopButton.disabled = true;
        };

        mediaRecorder.start();

        // Update UI
        startButton.disabled = true;
        stopButton.disabled = false;
    });
};

stopButton.onclick = () => {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }
};

let currentDownloadURL = "";


function formatTimestamp(input) {

    let digits = input.value.replace(/\D/g, "");

    digits = digits.substring(0, 6);

    let formatted = "";

    if (digits.length <= 2) {

        formatted = digits;

    } else if (digits.length <= 4) {

        formatted =
            digits.substring(0, 2) +
            ":" +
            digits.substring(2);

    } else {

        formatted =
            digits.substring(0, 2) +
            ":" +
            digits.substring(2, 4) +
            ":" +
            digits.substring(4, 6);

    }

    input.value = formatted;
}


function timestampToSeconds(timestamp) {

    const parts =
        timestamp.split(":").map(Number);

    if (parts.length !== 3) {
        return NaN;
    }

    return (
        parts[0] * 3600 +
        parts[1] * 60 +
        parts[2]
    );
}


function isValidTimestamp(timestamp) {

    const pattern =
        /^\d{2}:\d{2}:\d{2}$/;

    if (!pattern.test(timestamp)) {
        return false;
    }

    const parts =
        timestamp.split(":").map(Number);

    const hours = parts[0];
    const minutes = parts[1];
    const seconds = parts[2];

    if (minutes > 59) {
        return false;
    }

    if (seconds > 59) {
        return false;
    }

    if (hours > 99) {
        return false;
    }

    return true;
}


async function createClip() {

    const url =
        document.getElementById("url").value.trim();

    const start =
        document.getElementById("start").value.trim();

    const end =
        document.getElementById("end").value.trim();

    const quality =
        document.getElementById("quality").value;

    const status =
        document.getElementById("status");

    const button =
        document.getElementById("clipButton");

    const videoContainer =
        document.getElementById("videoContainer");

    const downloadButton =
        document.getElementById("downloadButton");


    status.innerText = "";

    videoContainer.innerHTML = "";

    downloadButton.style.display = "none";


    if (!url) {

        status.innerText =
            "Please enter a video URL.";

        return;
    }


    if (!isValidTimestamp(start)) {

        status.innerText =
            "Please Input a Start time";

        return;
    }


    if (!isValidTimestamp(end)) {

        status.innerText =
            "Please Input and End time";

        return;
    }


    const startSeconds =
        timestampToSeconds(start);

    const endSeconds =
        timestampToSeconds(end);


    if (startSeconds >= endSeconds) {

        status.innerText =
            "End time must be after start time.";

        return;
    }


    button.disabled = true;

    button.innerText =
        "CREATING CLIP...";

    status.innerText =
        "Downloading and processing your clip...";


    try {

        const response =
            await fetch("/clip", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    url: url,
                    start: start,
                    end: end,
                    quality: quality

                })

            });


        const data =
            await response.json();


        if (!data.success) {

            status.innerText =
                "Error: " + data.error;

            return;
        }


        currentDownloadURL =
            data.download;


        status.innerText =
            "Clip created successfully!";


        videoContainer.innerHTML = `

            <div class="video-preview">

                <h3>Preview</h3>

                <video
                    controls
                    preload="metadata"
                    src="${data.file}"
                >
                </video>

            </div>

        `;


        downloadButton.style.display =
            "block";


    } catch (error) {

        status.innerText =
            "Something went wrong: " +
            error.message;

    } finally {

        button.disabled = false;

        button.innerText =
            "CREATE CLIP";

    }

}


function downloadClip() {

    if (!currentDownloadURL) {
        return;
    }

    const link =
        document.createElement("a");

    link.href =
        currentDownloadURL;

    link.download =
        "clip.mp4";

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

}


async function clearClips() {

    const confirmed =
        confirm(
            "Are you sure you want to delete all clips?"
        );

    if (!confirmed) {
        return;
    }


    const status =
        document.getElementById("status");


    try {

        const response =
            await fetch(
                "/clear-clips",
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (data.success) {

            document.getElementById(
                "videoContainer"
            ).innerHTML = "";

            document.getElementById(
                "downloadButton"
            ).style.display = "none";

            currentDownloadURL = "";

            status.innerText =
                `${data.deleted} clip(s) deleted.`;

        }


    } catch (error) {

        status.innerText =
            "Failed to clear clips: " +
            error.message;

    }

}

/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: video conference init Js File
*/

var chatsData = [
    {

        "id": 1,
        "msg": "Good morning 😊",
        "img": "/static/images/users/avatar-5.jpg",
        "name": "Nicholas"
    },
    {

        "id": 2,
        "msg": "Hope all guys joined the meeting right?",
        "img": "/static/images/users/avatar-1.jpg",
        "name": "Jennifer"
    },
    {

        "id": 3,
        "msg": "Yes, Ma'am.",
        "img": "/static/images/users/avatar-3.jpg",
        "name": "Alyssa"
    },
    {

        "id": 4,
        "msg": "Joined",
        "img": "/static/images/users/avatar-10.jpg",
        "name": "Phillip"
    },
    {

        "id": 5,
        "msg": "Cool, Let's start the meet.",
        "img": "/static/images/users/avatar-1.jpg",
        "name": "Jennifer"
    },
];

function loadMsg(item) {
    var html = ""
    html += `<li class="chat-list left">
                    <div class="conversation-list">
                        <div class="chat-avatar">
                            <img src="${item.img}" alt="">
                        </div>
                        <div class="user-chat-content">
                            <div class="ctext-wrap">
                                <div class="ctext-wrap-content">
                                    <p class="mb-0 ctext-content">${item.msg}</p>
                                </div>
                                <div class="dropdown align-self-start message-box-drop">
                                    <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="ri-more-2-fill"></i>
                                    </a>
                                    <div class="dropdown-menu">
                                        <a class="dropdown-item" href="#"><i class="ri-reply-line me-2 text-muted align-bottom"></i>report</a>
                                        <a class="dropdown-item" href="#"><i class="ri-file-copy-line me-2 text-muted align-bottom"></i>block</a>
                                    </div>
                                </div>
                            </div>
                            <div class="conversation-name"><small class="text-muted time">${item.name}</small> <span class="text-success check-message-icon"><i class="ri-check-double-line align-bottom"></i></span></div>
                        </div>
                    </div>
                </li>`;

    document.getElementById("users-conversation").innerHTML += html;
    scrollToBottom("users-chat");
}

var msgCount = 0;
loadMsg(chatsData[msgCount]);
msgCount++;
//meeting time & date
setInterval(() => {
    // date
    var d = new Date();
    var dateOptions = { weekday: 'short', month: 'short', day: 'numeric' };
    var date = d.toLocaleDateString(undefined, dateOptions);
    // time
    var hours = d.getHours();
    var ampm = hours >= 12 ? ' PM' : ' AM';
    var hours = hours % 12;
    var time = ("0" + hours).slice(-2) + ':' + ("0" + d.getMinutes()).slice(-2) + ampm;

    document.getElementById("current-time").innerHTML = time + " - " + date;

    if (chatsData.length > msgCount) {
        loadMsg(chatsData[msgCount]);
        msgCount++;
    }
}, 1000);

// send message 
//chat form
var chatForm = document.querySelector("#chatinput-form");
var chatInput = document.querySelector("#chat-input");

if (chatForm) {
    //add an item to the List, including to local storage
    chatForm.addEventListener("submit", function (e) {
        e.preventDefault();
        var itemList = document.getElementById("users-chat").querySelector(".chat-conversation-list");
        var chatInputValue = chatInput.value

        if (chatInputValue.length !== 0) {
            var chatMsg = `<li class="chat-list left">
            <div class="conversation-list">
                <div class="chat-avatar">
                    <img src="build/images/users/avatar-1.jpg" alt="">
                </div>
                <div class="user-chat-content">
                    <div class="ctext-wrap">
                        <div class="ctext-wrap-content">
                            <p class="mb-0 ctext-content">${chatInput.value}</p>
                        </div>
                        <div class="dropdown align-self-start message-box-drop">
                            <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <i class="ri-more-2-fill"></i>
                            </a>
                            <div class="dropdown-menu">
                                <a class="dropdown-item" href="#"><i class="ri-reply-line me-2 text-muted align-bottom"></i>report</a>
                                <a class="dropdown-item" href="#"><i class="ri-file-copy-line me-2 text-muted align-bottom"></i>block</a>
                            </div>
                        </div>
                    </div>
                    <div class="conversation-name"><small class="text-muted time">Jennifer</small> <span class="text-success check-message-icon"><i class="ri-check-double-line align-bottom"></i></span></div>
                </div>
            </div>
        </li>`;

            itemList.insertAdjacentHTML(
                "beforeend",
                chatMsg
            );
            scrollToBottom("users-chat");

            //
            chatInput.value = "";
        }

    })
}

// // Scroll to Bottom
function scrollToBottom(id) {
    setTimeout(function () {
        var simpleBar = document.getElementById(id)?.querySelector(".simplebar-content-wrapper") || null;
        
        if (!simpleBar) {
            return; // Exit if simpleBar element isn't found
        }

        var offsetHeight = document.getElementById("users-conversation") ?
            document.getElementById(id)?.querySelector("#users-conversation")?.scrollHeight - window.innerHeight + 355 : 0;
            
        if (offsetHeight && simpleBar) {
            simpleBar.scrollTo({
                top: offsetHeight,
                behavior: "smooth"
            });
        }
    }, 100);
}

var chatTime = 0;
var running = false;
//Chat time counter
function increment() {
    if (running == true) {
        setTimeout(function () {
            chatTime++;
            var hours = Math.floor(chatTime / 10 / 3600);
            if (hours <= 9) {
                hours = "0" + hours;
            }
            var mins = Math.floor(chatTime / 10 / 60);
            if (mins <= 9) {
                mins = "0" + mins;
            }
            var secs = Math.floor(chatTime / 10);
            if (secs <= 9) {
                secs = "0" + secs;
            }
            document.getElementById("videoChatTime").innerHTML = hours + ":" + mins + ":" + secs;
            increment();
        }, 100);
    }
};

const startVideoCall = document.getElementById('startVideoCall');
const endVideoCall = document.getElementById('endVideoCall');
const captureVideoImgButton = document.getElementById('captureVideoImgButton'); // Get the Capture Image button
const captureCanvas = document.getElementById('captureCanvas'); // Get the hidden canvas element
let localStream, remoteStream;
let localVideo = document.getElementById('localVideo');
let remoteVideo = document.getElementById('remoteVideo');
const zoomRange = document.getElementById('zoomRange');
const zoomRangeStatus = document.getElementById('zoomRangeStatus');
var downloadButton = document.getElementById("downloadButton");

// Function to handle the user media access
async function getMediaStream() {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localVideo.srcObject = localStream;
    } catch (error) {
        alert(error);
        console.error('Error accessing user media:', error);
    }
}

// Event listener for the range slider
zoomRange.addEventListener('input', () => {
    const scale = zoomRange.value;

    // Scale the video elements using CSS transform
    localVideo.style.transform = `scale(${scale})`;
    remoteVideo.style.transform = `scale(${scale})`;
});

// Function to capture an image from the video stream
function captureImage() {
    if (!localStream) {
        console.error('Local stream not available.');
        return;
    }

    if (document.getElementById("hideImgEle")) {
        document.getElementById("hideImgEle").style.display = "none";
    }

    // Show the canvas element
    captureCanvas.style.display = 'block';

    // Set the canvas dimensions to match the video stream
    captureCanvas.width = 333;
    captureCanvas.height = 229;

    // Draw the current frame from the video onto the canvas
    const context = captureCanvas.getContext('2d');
    context.drawImage(localVideo, 0, 0, captureCanvas.width, captureCanvas.height);

    // Get the image data from the canvas as a data URL
    const imageDataURL = captureCanvas.toDataURL();
    downloadButton.classList.remove("d-none");

    // You can now use the imageDataURL to display the captured image or send it to a server.
    // For example, you can create an <img> element and set its src to the imageDataURL:
    // const capturedImage = document.createElement('img');
    // capturedImage.src = imageDataURL;
    // document.body.appendChild(capturedImage);

    // Hide the canvas again after capturing the image
    // captureCanvas.style.display = 'none';
}

function downloadPhoto() {
    const dataURL = captureCanvas.toDataURL('image/jpeg'); // Use 'image/png' for PNG format
    const link = document.createElement('a');
    link.href = dataURL;
    link.download = 'captured-photo.jpg'; // Change the filename as needed
    link.click();
}

// Function to start the video call
function startCall() {
    if (!localStream) {
        console.error('Local stream not available. Call getMediaStream() first.');
        startVideoCall.removeAttribute("disabled");
        return;
    }

    endVideoCall.removeAttribute("disabled");

    // start counting time
    running = true;
    increment();

    // show zoom options
    zoomRangeStatus.classList.remove("d-none");

    // Create the local PeerConnection
    localPeerConnection = new RTCPeerConnection();
    // Add the local stream to the PeerConnection
    localStream.getTracks().forEach(track => {
        localPeerConnection.addTrack(track, localStream);
    });

    // Set up the remote stream when it's received
    localPeerConnection.ontrack = (event) => {
        remoteVideo.srcObject = event.streams[0];
        remoteStream = event.streams[0];
    };

    // Create the offer and set it as the local description
    localPeerConnection.createOffer()
        .then(offer => localPeerConnection.setLocalDescription(offer))
        .then(() => {
            // Implement the signaling mechanism to exchange the offer with the remote user.
            // This is usually done through a signaling server, but for simplicity,
            // you can manually exchange the offer and answer between the two peers.

            // Example: send the offer to the remote user using some signaling method
            // For demonstration purposes, you can just log it to the console.

            // After receiving the remote user's answer, set it as the remote description
            // For demonstration purposes, you can just log it to the console.
            // Example: receive the remote description through signaling and set it
            // localPeerConnection.setRemoteDescription(remoteDescription);
        })
        .catch(error => {
            console.error("Error creating offer:", error);
            startVideoCall.removeAttribute("disabled");
        });
    // Implement the call initiation logic here
    // You may need a signaling server for handling call setup and negotiation.
    // Also, set up WebRTC RTCPeerConnection and RTCDataChannel for communication.
    // This is beyond the scope of a simple example.
}

// Function to end the video call
function endCall() {
    if (localPeerConnection) {
        localPeerConnection.close();
        localPeerConnection = null;

        // hide zoom options
        zoomRangeStatus.classList.add("d-none");

        //
        endVideoCall.setAttribute("disabled", true);

        // end counting
        running = false;
        setTimeout(() => {
            document.getElementById("videoChatTime").innerHTML = '00:00:00';
            chatTime = 0;
        }, 150)
    }

    // Stop the local and remote media streams
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
        localStream = null;
    }

    if (remoteStream) {
        remoteStream.getTracks().forEach(track => track.stop());
        remoteStream = null;
    }

    // Clean up the UI
    localVideo.srcObject = null;
    remoteVideo.srcObject = null;

    // Update the UI to indicate that the call has ended
    // You can do this by hiding or disabling the video elements and buttons.

    // Clean up any other resources used during the call (data channels, etc.).
    // This is beyond the scope of a simple example.
}

startVideoCall.addEventListener('click', () => {
    startVideoCall.setAttribute("disabled", true);
    getMediaStream().then(startCall);
});

endVideoCall.addEventListener('click', () => {
    startVideoCall.removeAttribute("disabled");
    endCall();
});

captureVideoImgButton.addEventListener('click', () => {
    captureImage();
});

document.getElementById('downloadButton').addEventListener('click', () => {
    downloadPhoto();
});



if (document.getElementById("meetingVolumeBtn")) {
    document.getElementById("meetingVolumeBtn").addEventListener("click", () => {
        document.getElementById("meetingVolume").classList.remove("d-none");
        setTimeout(() => {
            document.getElementById("meetingVolume").classList.add('d-none');
        }, 5000);
    })
}
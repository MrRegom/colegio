var chatsData=[{id:1,msg:"Good morning 😊",img:"/static/images/users/avatar-5.jpg",name:"Nicholas"},{id:2,msg:"Hope all guys joined the meeting right?",img:"/static/images/users/avatar-1.jpg",name:"Jennifer"},{id:3,msg:"Yes, Ma'am.",img:"/static/images/users/avatar-3.jpg",name:"Alyssa"},{id:4,msg:"Joined",img:"/static/images/users/avatar-10.jpg",name:"Phillip"},{id:5,msg:"Cool, Let's start the meet.",img:"/static/images/users/avatar-1.jpg",name:"Jennifer"}];function loadMsg(e){var t="";t+=`<li class="chat-list left">
                    <div class="conversation-list">
                        <div class="chat-avatar">
                            <img src="${e.img}" alt="">
                        </div>
                        <div class="user-chat-content">
                            <div class="ctext-wrap">
                                <div class="ctext-wrap-content">
                                    <p class="mb-0 ctext-content">${e.msg}</p>
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
                            <div class="conversation-name"><small class="text-muted time">${e.name}</small> <span class="text-success check-message-icon"><i class="ri-check-double-line align-bottom"></i></span></div>
                        </div>
                    </div>
                </li>`,document.getElementById("users-conversation").innerHTML+=t,scrollToBottom("users-chat")}var msgCount=0,chatForm=(loadMsg(chatsData[msgCount]),msgCount++,setInterval(()=>{var e=new Date,t=e.toLocaleDateString(void 0,{weekday:"short",month:"short",day:"numeric"}),a=e.getHours(),o=12<=a?" PM":" AM",a=("0"+a%12).slice(-2)+":"+("0"+e.getMinutes()).slice(-2)+o;document.getElementById("current-time").innerHTML=a+" - "+t,chatsData.length>msgCount&&(loadMsg(chatsData[msgCount]),msgCount++)},1e3),document.querySelector("#chatinput-form")),chatInput=document.querySelector("#chat-input");function scrollToBottom(a){setTimeout(function(){var e,t=document.getElementById(a)?.querySelector(".simplebar-content-wrapper")||null;t&&(e=document.getElementById("users-conversation")?document.getElementById(a)?.querySelector("#users-conversation")?.scrollHeight-window.innerHeight+355:0)&&t&&t.scrollTo({top:e,behavior:"smooth"})},100)}chatForm&&chatForm.addEventListener("submit",function(e){e.preventDefault();var t,e=document.getElementById("users-chat").querySelector(".chat-conversation-list");0!==chatInput.value.length&&(t=`<li class="chat-list left">
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
        </li>`,e.insertAdjacentHTML("beforeend",t),scrollToBottom("users-chat"),chatInput.value="")});var chatTime=0,running=!1;function increment(){1==running&&setTimeout(function(){chatTime++;var e=Math.floor(chatTime/10/3600),t=(e<=9&&(e="0"+e),Math.floor(chatTime/10/60)),a=(t<=9&&(t="0"+t),Math.floor(chatTime/10));a<=9&&(a="0"+a),document.getElementById("videoChatTime").innerHTML=e+":"+t+":"+a,increment()},100)}const startVideoCall=document.getElementById("startVideoCall"),endVideoCall=document.getElementById("endVideoCall"),captureVideoImgButton=document.getElementById("captureVideoImgButton"),captureCanvas=document.getElementById("captureCanvas");let localStream,remoteStream,localVideo=document.getElementById("localVideo"),remoteVideo=document.getElementById("remoteVideo");const zoomRange=document.getElementById("zoomRange"),zoomRangeStatus=document.getElementById("zoomRangeStatus");var downloadButton=document.getElementById("downloadButton");async function getMediaStream(){try{localStream=await navigator.mediaDevices.getUserMedia({video:!0,audio:!0}),localVideo.srcObject=localStream}catch(e){alert(e),console.error("Error accessing user media:",e)}}function captureImage(){localStream?(document.getElementById("hideImgEle")&&(document.getElementById("hideImgEle").style.display="none"),captureCanvas.style.display="block",captureCanvas.width=333,captureCanvas.height=229,captureCanvas.getContext("2d").drawImage(localVideo,0,0,captureCanvas.width,captureCanvas.height),captureCanvas.toDataURL(),downloadButton.classList.remove("d-none")):console.error("Local stream not available.")}function downloadPhoto(){var e=captureCanvas.toDataURL("image/jpeg"),t=document.createElement("a");t.href=e,t.download="captured-photo.jpg",t.click()}function startCall(){localStream?(endVideoCall.removeAttribute("disabled"),running=!0,increment(),zoomRangeStatus.classList.remove("d-none"),localPeerConnection=new RTCPeerConnection,localStream.getTracks().forEach(e=>{localPeerConnection.addTrack(e,localStream)}),localPeerConnection.ontrack=e=>{remoteVideo.srcObject=e.streams[0],remoteStream=e.streams[0]},localPeerConnection.createOffer().then(e=>localPeerConnection.setLocalDescription(e)).then(()=>{}).catch(e=>{console.error("Error creating offer:",e),startVideoCall.removeAttribute("disabled")})):(console.error("Local stream not available. Call getMediaStream() first."),startVideoCall.removeAttribute("disabled"))}function endCall(){localPeerConnection&&(localPeerConnection.close(),localPeerConnection=null,zoomRangeStatus.classList.add("d-none"),endVideoCall.setAttribute("disabled",!0),running=!1,setTimeout(()=>{document.getElementById("videoChatTime").innerHTML="00:00:00",chatTime=0},150)),localStream&&(localStream.getTracks().forEach(e=>e.stop()),localStream=null),remoteStream&&(remoteStream.getTracks().forEach(e=>e.stop()),remoteStream=null),localVideo.srcObject=null,remoteVideo.srcObject=null}zoomRange.addEventListener("input",()=>{var e=zoomRange.value;localVideo.style.transform=`scale(${e})`,remoteVideo.style.transform=`scale(${e})`}),startVideoCall.addEventListener("click",()=>{startVideoCall.setAttribute("disabled",!0),getMediaStream().then(startCall)}),endVideoCall.addEventListener("click",()=>{startVideoCall.removeAttribute("disabled"),endCall()}),captureVideoImgButton.addEventListener("click",()=>{captureImage()}),document.getElementById("downloadButton").addEventListener("click",()=>{downloadPhoto()}),document.getElementById("meetingVolumeBtn")&&document.getElementById("meetingVolumeBtn").addEventListener("click",()=>{document.getElementById("meetingVolume").classList.remove("d-none"),setTimeout(()=>{document.getElementById("meetingVolume").classList.add("d-none")},5e3)});
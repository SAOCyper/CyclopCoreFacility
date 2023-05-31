const video = document.getElementById("video");
const results = document.getElementById('results');
const snap = document.getElementById('snap');
const errorMsgElement=document.querySelector('span#errorMsg');
const constraints = {
    audio:true,
    video: {
        width: {min:1024 , ideal:1200, max:1920},
        height:{min:576,ideal:720,max:1000}
    }
}

async function startWebCam(){
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream);
    } catch(e){
        errorMsgElement.innerHTML = 'navigator.getUserMedia error:${e.toString()}';
    }
}
function handleSuccess(stream){
    window.stream = stream;
    video.srcObject= stream;
}
var context = results.getContext('2d');
snap.addEventListener("click", () => {
    context.drawImage(video,0,0,350,350);
});

startWebCam(); 


/* const webcamElement = document.getElementById('webcam');
const canvasElement = document.getElementById('canvas');
const snapSoundElement = document.getElementById('snapSound');
const webcam = new Webcam(webcamElement, 'user', canvasElement, snapSoundElement);
webcam.start()
   .then(result =>{
      console.log("webcam started");
   })
   .catch(err => {
       console.log(err);
   });
let picture = webcam.snap();
document.querySelector('#download-photo').href = picture;

$('#cameraFlip').click(function() {
    webcam.flip();
    webcam.start();  
}); */
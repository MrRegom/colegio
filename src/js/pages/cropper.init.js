/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.comom
File: cropper Init Js File
*/

//Cropper with a range of aspect ratio
window.addEventListener('DOMContentLoaded', function () {
    var image = document.querySelector('#ragbe_aspect_ratio');
    var minAspectRatio = 0.5;
    var maxAspectRatio = 1.5;
    var cropper = new Cropper(image, {
        ready: function () {
            var cropper = this.cropper;
            var containerData = cropper.getContainerData();
            var cropBoxData = cropper.getCropBoxData();
            var aspectRatio = cropBoxData.width / cropBoxData.height;
            var newCropBoxWidth;

            if (aspectRatio < minAspectRatio || aspectRatio > maxAspectRatio) {
                newCropBoxWidth = cropBoxData.height * ((minAspectRatio + maxAspectRatio) / 2);

                cropper.setCropBoxData({
                    left: (containerData.width - newCropBoxWidth) / 2,
                    width: newCropBoxWidth
                });
            }
        },

        cropmove: function () {
            var cropper = this.cropper;
            var cropBoxData = cropper.getCropBoxData();
            var aspectRatio = cropBoxData.width / cropBoxData.height;

            if (aspectRatio < minAspectRatio) {
                cropper.setCropBoxData({
                    width: cropBoxData.height * minAspectRatio
                });
            } else if (aspectRatio > maxAspectRatio) {
                cropper.setCropBoxData({
                    width: cropBoxData.height * maxAspectRatio
                });
            }
        },
    });
});

//Crop a round image
function getRoundedCanvas(sourceCanvas) {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var width = sourceCanvas.width;
    var height = sourceCanvas.height;

    canvas.width = width;
    canvas.height = height;
    context.imageSmoothingEnabled = true;
    context.drawImage(sourceCanvas, 0, 0, width, height);
    context.globalCompositeOperation = 'destination-in';
    context.beginPath();
    context.arc(width / 2, height / 2, Math.min(width, height) / 2, 0, 2 * Math.PI, true);
    context.fill();
    return canvas;
}

window.addEventListener('DOMContentLoaded', function () {
    var image = document.getElementById('crop_round_images');
    var button = document.getElementById('cropButtonResult');
    var result = document.getElementById('resultRoundImages');
    var croppable = false;
    var cropper = new Cropper(image, {
        aspectRatio: 1,
        viewMode: 1,
        ready: function () {
            croppable = true;
        },
    });

    button.onclick = function () {
        var croppedCanvas;
        var roundedCanvas;
        var roundedImage;

        if (!croppable) {
            return;
        }

        // Crop
        croppedCanvas = cropper.getCroppedCanvas();

        // Round
        roundedCanvas = getRoundedCanvas(croppedCanvas);

        // Show
        roundedImage = document.createElement('img');
        roundedImage.src = roundedCanvas.toDataURL()
        result.innerHTML = '';
        result.appendChild(roundedImage);
    };
});

//Customize preview for Cropper
function each(arr, callback) {
    var length = arr.length;
    var i;

    for (i = 0; i < length; i++) {
        callback.call(arr, arr[i], i, arr);
    }

    return arr;
}

window.addEventListener('DOMContentLoaded', function () {
    var image = document.querySelector('#customizeImages');
    var previews = document.querySelectorAll('.preview');
    var previewReady = false;
    var cropper = new Cropper(image, {
        ready: function () {
            var clone = this.cloneNode();

            clone.className = '';
            clone.style.cssText = (
                'display: block;' +
                'width: 100%;' +
                'min-width: 0;' +
                'min-height: 0;' +
                'max-width: none;' +
                'max-height: none;'
            );

            each(previews, function (elem) {
                elem.appendChild(clone.cloneNode());
            });
            previewReady = true;
        },

        crop: function (event) {
            if (!previewReady) {
                return;
            }

            var data = event.detail;
            var cropper = this.cropper;
            var imageData = cropper.getImageData();
            var previewAspectRatio = data.width / data.height;

            each(previews, function (elem) {
                var previewImage = elem.getElementsByTagName('img').item(0);
                var previewWidth = elem.offsetWidth;
                var previewHeight = previewWidth / previewAspectRatio;
                var imageScaledRatio = data.width / previewWidth;

                elem.style.height = previewHeight + 'px';
                previewImage.style.width = imageData.naturalWidth / imageScaledRatio + 'px';
                previewImage.style.height = imageData.naturalHeight / imageScaledRatio + 'px';
                previewImage.style.marginLeft = -data.x / imageScaledRatio + 'px';
                previewImage.style.marginTop = -data.y / imageScaledRatio + 'px';
            });
        },
    });
});
const textInputElements = document.querySelectorAll('.text-field input, .text-field textarea');

textInputElements.forEach( (input) => {
    input.addEventListener('input', () => {
        updateCharTyped(input)
    });
})

function updateCharTyped(elem) {
    const charTypedSpan = elem.nextElementSibling;

    const currentLength = elem.value.length;
    const maxLength = elem.getAttribute('maxlength');

    charTypedSpan.textContent = `${currentLength}/${maxLength}`;
}

// after thumbnail file chosen, show the thumbnail image in the upload button label
const thumbnailInput = document.querySelector('#id_thumbnail');
const thumbnailLabel = document.querySelector('.thumbnail-upload-label');

const videoInput = document.querySelector('#id_video_file');
const videoLabel = document.querySelector('.video-upload-label')

thumbnailInput.addEventListener('change', () => {
    const file = thumbnailInput.files[0];
    const reader = new FileReader();

    reader.onload = () => {
        // fit the image to the label even if it's not square; maintain aspect ratio
        thumbnailLabel.style.backgroundImage = `url(${reader.result})`;
        thumbnailLabel.style.backgroundRepeat = 'no-repeat';
        thumbnailLabel.style.backgroundPosition = 'center';
        thumbnailLabel.style.backgroundSize = 'contain';
        
        // hide the label text
        thumbnailLabel.innerHTML = '';

        // update styles
        thumbnailLabel.style.backgroundColor = 'black';
        thumbnailLabel.style.border = '1px solid white';
    }

    reader.readAsDataURL(file);
});


videoInput.addEventListener('change', () => {
    const file = videoInput.files[0];
    // create a video element and preview uploaded video in it; append to label element
    const video = document.createElement('video');
    const obj_url = URL.createObjectURL(file);
    video.src = obj_url;
    video.controls = true;
    video.autoplay = true;
    video.disablePictureInPicture = true;
    video.disableRemotePlayback = true;
    video.muted = true;
    // full screen, download, picture-in-picture disbaled
    // set 'nodownload', 'nofullscreen' attributes
    video.setAttribute('controlsList', 'nodownload nofullscreen');

    video.style.width = '100%';
    video.style.height = '100%';    
    video.style.borderRadius = '5px';
    video.style.boxShadow = '0 0 5px 0 rgba(0, 0, 0, 0.5)';
    video.style.zIndex = '2';


    // append video to label
    videoLabel.appendChild(video);

    // hide the upload animation box
    const uploadAnimationBox = document.querySelector('.video-upload-animation-box');
    uploadAnimationBox.style.display = 'none';
});

const subtitleInput = document.querySelector('#id_subtitle');
const subtitleLabel = document.querySelector('.subtitle-upload-label');
const doneIcon = document.querySelector('.done-icon');
const addSpan = document.querySelector('.add-span');

subtitleInput.addEventListener('change', () => {
    const file = subtitleInput.files[0];
    const reader = new FileReader();
    
    reader.onload = () => {
        // show the done icon
        doneIcon.style.display = 'block';

        // hide the ADD span
        addSpan.style.display = 'none'; 

        // update the label text
        subtitleLabel.textContent = 'File Added';
        // font size smaller
        subtitleLabel.style.fontSize = '0.68em';
        subtitleLabel.style.padding = '0';
    }

    reader.readAsDataURL(file);
});


// progress bar on form submit

const uploadForm = document.querySelector('#video-upload-form');
const progressBarContainer = document.querySelector('.progress-bar-container');
const progressBar = document.querySelector('.progress-bar');
const progressStatus = document.querySelector('.progress-status');


$(document).ready(function(){
    $("form").submit(function(e) {
        e.preventDefault();
    
        $form = $(this);
        // console.log($form[0]);
        var formData = new FormData($form[0]);

        const fileInputs = $form.find('input[type="file"]');

        // if any file input has a file, show the progress bar
        for (let i = 0; i < fileInputs.length; i++) {
            const fileInput = fileInputs[i];
            if (fileInput.files.length > 0) {
                progressBarContainer.style.display = 'block';
                progressStatus.style.display = 'block';
                break;
            }
        }
        
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: formData,
            dataType: 'json',
            contentType: false,
            cache: false,
            processData: false,
            xhr: function() {
                const xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', function(e) {
                    console.log(e);
                    if(e.lengthComputable) {
                        const percent = e.loaded / e.total * 100;
                        progressBar.style.width = `${percent}%`;
                    }
                });
                return xhr;
            },
            success: function(response) {
                progressStatus.style.display = 'none';
                
                // show success icon
                const successIcon = document.querySelector('.success-icon');
                successIcon.style.display = 'block';

                // redirect to the page sent in the response
                window.location.href = response.redirect_url;
            },
            error: function(err) {
                console.log(err);
            }
        })
    });
});

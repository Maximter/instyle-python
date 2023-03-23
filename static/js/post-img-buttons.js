const delete_button = document.getElementById('delete');
const comment = document.getElementById('comment');

delete_button.onclick = () => {
    comment.value = ""
    uploaded_image_block.style.display = "none"
    uploaded_image.src = "#"
    uploaded_image_block.innerHTML = ` <img src="#" class="uploaded-image" id="uploaded_image" >`
}
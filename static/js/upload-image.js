const input_image = document.getElementById('input_file');
const uploaded_image = document.getElementById('uploaded_image');
let vid = document.getElementById('vid');
const uploaded_image_block = document.getElementById('uploaded_image_block');

input_image.onchange = () => {
    const [file] = input_image.files
    if (file) {
        if (file.size > 1024 * 1024 * 75) {
            Swal.fire({
                title: 'Ошибка',
                text: 'Загружаемый файл слишком большой. Максимально разрешенный размер файла: 75Мб',
                icon: 'error',
                confirmButtonText: 'Хорошо'
              })
        }
        uploaded_image_block.style.display = "block"
        let source = URL.createObjectURL(file)
        if (file.type == 'video/mp4') {
            uploaded_image_block.innerHTML = `<video class="uploaded-image" controls="controls">
            <source src="${source}" type='video/mp4;' id="vid">
        </video>`
        }
        else uploaded_image_block.innerHTML = ` <img src="${source}" class="uploaded-image" id="uploaded_image" >`
    }
}
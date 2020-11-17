$(document).ready(function () {
    $("#id_original_image").change(function () {
        var selected_file = $(this).val();
        var filename = selected_file.split('\\').reverse()[0].split('.')[0];
        console.log(filename);
        $("#id_name").val(filename);
    });
    $("#id_images_zip_file").change(function () {
        var selected_file = $(this).val();
        var filename = selected_file.split('\\').reverse()[0].split('.')[0];
        console.log(filename);
        $("#id_name").val(filename);
    });
});

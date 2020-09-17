$(document).ready(function() {
  function render_tiff_image(id_field, filename) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', filename);
    xhr.responseType = 'arraybuffer';
    xhr.onload = function (e) {
      var buffer = xhr.response;
      var tiff = new Tiff({buffer: buffer});
      var dataurl = tiff.toDataURL();
      if (dataurl) {
        $("#" + id_field).attr("src", tiff.toDataURL());
      }
    };
    xhr.send();
  }

  $(".img-list-thumb").each( function (index, element) {
    if ($(element).attr("src").endsWith(".tif")) {
      render_tiff_image(
        element.id,
        $(element).attr("src"),
      );
    }
  });
});

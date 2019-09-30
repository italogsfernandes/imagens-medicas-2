$(document).ready(function() {
  var canvas = document.createElement("canvas");

  function get_image_data_obj(image_id) {
    // Get image data as array
    var data_source_img = document.getElementById(image_id);
    canvas.width = data_source_img.width;
    canvas.height = data_source_img.height;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(data_source_img, 0, 0);
    return ctx.getImageData(
      0, 0, data_source_img.width, data_source_img.height);
  }

  function generate_histogram(image_id, div_id, title, image_data) {
    image_data = image_data || get_image_data_obj(image_id);
    // Generate Histogram Trace
    var trace = {
      x: image_data.data,
      type: 'histogram',
      autobinx: false,
      xbins: {
        end: 256,
        size: 1,
        start: 0
      }
    };
    // Set data (its possible to plot more than 1)
    var data = [trace];
    // Configure title and labels
    var layout = {
      title: title,
      xaxis: {
        title: "Value"
      },
      yaxis: {
        title: "Count"
      }
    };
    // Plot
    Plotly.newPlot(div_id, data, layout);
  }

  generate_histogram(
    "output_original_image",
    "div_original_histogram_result_plot",
    "Original Histogram")
  generate_histogram(
    "output_image",
    "div_output_histogram_result_plot",
    "Output Histogram");
  $("#btn_update_image_histogram").click(function() {
    generate_histogram(
      "output_image",
      "div_output_histogram_result_plot",
      "Output Histogram");
  });


  function update_brightness_value(new_value) {
    $("#brightness_value").text(new_value);
  }
  update_brightness_value($("#range_brightness").val());
  $("#range_brightness").on('change', _.debounce(function() {
    update_brightness_value($(this).val());
  }, 250));

  function update_contrast_value(new_value) {
    $("#contrast_value").text(new_value);
  }
  update_contrast_value($("#range_contrast").val());
  $("#range_contrast").on('change', _.debounce(function() {
    update_contrast_value($(this).val());
  }, 250));


  function show_hide_original_and_histogram() {
    input_compare = document.getElementById("input_compare");
    input_histogram = document.getElementById("input_histogram");

    if (input_histogram.checked) {
      if (input_compare.checked) {
        $("#div_output_original_image").show();
        $("#div_output_original_histogram").show();
        $("#div_output_histogram").show();
      } else {
        $("#div_output_original_image").hide();
        $("#div_output_original_histogram").hide();
        $("#div_output_histogram").show();
      }
    } else {
      if (input_compare.checked) {
        $("#div_output_original_image").show();
        $("#div_output_original_histogram").hide();
        $("#div_output_histogram").hide();
      } else {
        $("#div_output_original_image").hide();
        $("#div_output_original_histogram").hide();
        $("#div_output_histogram").hide();
      }
    }
  }
  show_hide_original_and_histogram();
  $("#input_compare").change(function() {
    show_hide_original_and_histogram();
  });

  $("#input_histogram").change(function() {
    show_hide_original_and_histogram();
  });
});

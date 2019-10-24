$(document).ready(function() {
  // Setting up canvas variables
  var canvas_original = document.createElement("canvas");
  var canvas_output = document.getElementById("canvas_output_image");

  var original_image_obj = document.getElementById("output_original_image");
  canvas_original.width = original_image_obj.width;
  canvas_original.height = original_image_obj.height;
  var ctx_original = canvas_original.getContext("2d");
  ctx_original.drawImage(original_image_obj, 0, 0);
  var image_data_original = ctx_original.getImageData(
    0, 0, original_image_obj.width, original_image_obj.height
  );

  var output_image_obj = document.getElementById("output_image");
  canvas_output.width = output_image_obj.width;
  canvas_output.height = output_image_obj.height;
  var ctx_output = canvas_output.getContext("2d");
  ctx_output.drawImage(output_image_obj, 0, 0);
  var image_data_output = ctx_output.getImageData(
    0, 0, output_image_obj.width, output_image_obj.height
  );

  function get_image_data_obj(image_id) {
    // Get image data as array
    var canvas = document.createElement("canvas");
    var data_source_img = document.getElementById(image_id);
    canvas.width = data_source_img.width;
    canvas.height = data_source_img.height;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(data_source_img, 0, 0);
    return ctx.getImageData(
      0, 0, data_source_img.width, data_source_img.height);
  }

  function generate_histogram(div_id, title, image_data) {
    var r_values = [];
    var g_values = [];
    var b_values = [];
    var x = [];

    var i;
    for (i = 0; i < image_data.data.length; i += 4) {
      r_values[i] = image_data.data[i];
      g_values[i] = image_data.data[i + 1];
      b_values[i] = image_data.data[i + 2];
      x[i] = (r_values[i] + g_values[i] + b_values[i]) / 3;
    }

    // Generate Histogram Trace
    var trace = {
      x: x,
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
        range: [0, 256],
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
    "div_original_histogram_result_plot",
    "Original Histogram",
    image_data_original
  )
  generate_histogram(
    "div_output_histogram_result_plot",
    "Output Histogram",
    image_data_output
  );
  $("#btn_update_image_histogram").click(function() {
    generate_histogram(
      "div_output_histogram_result_plot",
      "Output Histogram",
      image_data_output
    );
  });


  function update_brightness_value(new_value, image_data) {
    new_value = parseInt(new_value);
    if (new_value >= 0) {
      $("#brightness_value").text("+" + new_value);
    } else {
      $("#brightness_value").text(new_value);
    }
    var i;
    for (i = 0; i < image_data.data.length; i += 4) {
      image_data_output.data[i] = new_value + image_data.data[i];
      image_data_output.data[i + 1] = new_value + image_data.data[i + 1];
      image_data_output.data[i + 2] = new_value + image_data.data[i + 2];
      image_data_output.data[i + 3] = 255;
    }
    generate_histogram(
      "div_output_histogram_result_plot",
      "Output Histogram",
      image_data_output
    );
    ctx_output.putImageData(image_data_output, 0, 0);
  }

  function update_contrast_value(new_value, image_data) {
    new_value = parseInt(new_value) / 100.00;
    $("#contrast_value").text("x"+new_value);
    var i;
    for (i = 0; i < image_data.data.length; i += 4) {
      image_data_output.data[i] = new_value * image_data.data[i];
      image_data_output.data[i + 1] = new_value * image_data.data[i + 1];
      image_data_output.data[i + 2] = new_value * image_data.data[i + 2];
      image_data_output.data[i + 3] = 255;
    }
    generate_histogram(
      "div_output_histogram_result_plot",
      "Output Histogram",
      image_data_output
    );
    ctx_output.putImageData(image_data_output, 0, 0);
  }

  function update_brightness_then_contrast(brightness_value, contrast_value) {
    update_brightness_value(brightness_value, image_data_original);
    update_contrast_value(contrast_value, image_data_output);
  }

  update_brightness_then_contrast($("#range_brightness").val(), $("#range_contrast").val());

  $("#range_brightness").on('change', _.debounce(function() {
    update_brightness_then_contrast($(this).val(), $("#range_contrast").val());
  }, 250));

  $("#range_contrast").on('change', _.debounce(function() {
    update_brightness_then_contrast($("#range_brightness").val(), $(this).val());
  }, 250));


  function show_hide_original_and_histogram() {
    input_compare = document.getElementById("input_compare");
    input_histogram = document.getElementById("input_histogram");

    if (input_histogram.checked) {
      if (input_compare.checked) {
        $("#div_output_original_image").removeClass('col-md-12').addClass('col-md-6')
        $("#div_output_image").removeClass('col-md-12').addClass('col-md-6')
        // $("#div_output_original_histogram").removeClass('col-md-12').addClass('col-md-6')
        $("#div_output_histogram").removeClass('col-md-12').addClass('col-md-6')

        $("#div_output_original_image").show();
        $("#div_output_image").show();
        $("#div_output_original_histogram").show();
        $("#div_output_histogram").show();
      } else {
        $("#div_output_original_image").removeClass('col-md-6').addClass('col-md-12')
        $("#div_output_image").removeClass('col-md-12').addClass('col-md-6')
        // $("#div_output_original_histogram").removeClass('col-md-6').addClass('col-md-12')
        $("#div_output_histogram").removeClass('col-md-12').addClass('col-md-6')

        $("#div_output_original_image").hide();
        $("#div_output_image").show();
        $("#div_output_original_histogram").hide();
        $("#div_output_histogram").show();
      }
    } else {
      if (input_compare.checked) {
        $("#div_output_original_image").removeClass('col-md-12').addClass('col-md-6')
        $("#div_output_image").removeClass('col-md-12').addClass('col-md-6')
        // $("#div_output_original_histogram").removeClass('col-md-6').addClass('col-md-12')
        $("#div_output_histogram").removeClass('col-md-6').addClass('col-md-12')


        $("#div_output_original_image").show();
        $("#div_output_image").show();
        $("#div_output_original_histogram").hide();
        $("#div_output_histogram").hide();
      } else {
        $("#div_output_original_image").removeClass('col-md-6').addClass('col-md-12')
        $("#div_output_image").removeClass('col-md-6').addClass('col-md-12')
        // $("#div_output_original_histogram").removeClass('col-md-6').addClass('col-md-12')
        $("#div_output_histogram").removeClass('col-md-6').addClass('col-md-12')

        $("#div_output_original_image").hide();
        $("#div_output_image").show();
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

  $('#trigger_see_more_options').click(function(e) {
    var div_to_show_hide = document.getElementById("show_hide_more_options");
    if (div_to_show_hide.style.display == 'none') {
      try {
        $(div_to_show_hide).slideDown('fast');
      } catch (error) {
        div_to_show_hide.style.display = 'block';
      }
      $('#id_icon_to_show_hide').addClass('fa-caret-up');
      $('#id_icon_to_show_hide').removeClass('fa-caret-down');
    } else {
      try {
        $(div_to_show_hide).slideUp('fast');
      } catch (error) {
        div_to_show_hide.style.display = 'none';
      }
      $('#id_icon_to_show_hide').addClass('fa-caret-down');
      $('#id_icon_to_show_hide').removeClass('fa-caret-up');
    }
  });


  function update_negative_modifier(image_data) {
    var i;
    for (i = 0; i < image_data.data.length; i += 4) {
      image_data_output.data[i] = 255 - image_data.data[i];
      image_data_output.data[i + 1] = 255 - image_data.data[i + 1];
      image_data_output.data[i + 2] = 255 - image_data.data[i + 2];
      image_data_output.data[i + 3] = 255;
    }
    generate_histogram(
      "div_output_histogram_result_plot",
      "Output Histogram",
      image_data_output
    );
    ctx_output.putImageData(image_data_output, 0, 0);
  }

  $("#btn_negative").click(function() {
    update_negative_modifier(image_data_output);
  });

  $("#btn_identity").click(function() {
    alert("Identity now working yet, Italo is working on it.");
  });
});

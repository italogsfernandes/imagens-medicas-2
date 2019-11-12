$(document).ready(function() {
  // Setting up canvas variables
  var canvas_original = document.createElement("canvas");
  var canvas_output = document.createElement("canvas");

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



  function update_argument_range_min_max() {
    var selected_value = $("#id_type_of_modifier").val();
    var new_step;
    var new_min;
    var new_max;
    if (selected_value == 'BRIGHTNESS'){
      new_step = 1;
      new_min = -255;
      new_max = 255;
    } else if (selected_value == 'CONTRAST'){
      new_step = 0.01;
      new_min = 0.01;
      new_max = 3;
    } else if (selected_value == 'NEGATIVE'){
      new_step = 0.01;
      new_min = 0;
      new_max = 1;
    } else if (selected_value == 'IDENTITY'){
      new_step = 0.01;
      new_min = 0;
      new_max = 1;
    } else if (selected_value == 'LOGARITHMIC'){
      new_step = 0.01;
      new_min = 0;
      new_max = 1;
    } else if (selected_value == 'EXPONENTIAL'){
      new_step = 0.1;
      new_min = 0;
      new_max = 100;
    } else if (selected_value == 'POWER'){
      new_step = 0.1;
      new_min = 0;
      new_max = 100;
    } else {
      argument_text = "Value";
    }

    $("#id_range_input_intensity_argument_value").attr("step", new_step);
    $("#id_range_input_intensity_argument_value").attr("min", new_min);
    $("#id_range_input_intensity_argument_value").attr("max", new_max);

  }


  function update_argument_value_label() {
    var selected_value = $("#id_type_of_modifier").val();
    var argument_text = "";
    var new_value = $("#id_range_input_intensity_argument_value").val();

    if (selected_value == 'BRIGHTNESS'){
      argument_text = "Shades";
    } else if (selected_value == 'CONTRAST'){
      argument_text = "Factor";
    } else if (selected_value == 'NEGATIVE'){
      argument_text = "Percentage";
    } else if (selected_value == 'IDENTITY'){
      argument_text = "Value";
    } else if (selected_value == 'LOGARITHMIC'){
      argument_text = "C";
    } else if (selected_value == 'EXPONENTIAL'){
      argument_text = "Gamma";
    } else if (selected_value == 'POWER'){
      argument_text = "Factor";
    } else {
      argument_text = "Value";
    }

    // Particular case, show hide field
    if (selected_value != 'IDENTITY'){
      $("label[for='id_argument_value']").show();
      $("#id_argument_value").show();
      $("#id_range_input_intensity_argument_value").show();
    } else {
      $("label[for='id_argument_value']").hide();
      $("#id_argument_value").hide();
      $("#id_range_input_intensity_argument_value").hide();
    }

    $("label[for='id_argument_value']").text(argument_text + ": ");
    $("#id_argument_value").val(new_value);
  }

  update_argument_range_min_max();

  update_argument_value_label();

  $("#id_type_of_modifier").change(function() {
    update_argument_range_min_max();
    update_argument_value_label();
  });

  $("#id_range_input_intensity_argument_value").on('change', _.debounce(function() {
    update_argument_value_label();
  }, 250));

  function show_images_from_response(data) {
    $("#image_history_content_section").html(data.history_content_div);
    $("#div_output_image").html(data.output_image_block_div);
    $('#messages').replaceWith(data.messages);

    // Update image data
    var timestamp = new Date().getTime();
    $('#output_image').attr('src', data.edited_image_url + '?timestamp=' + timestamp);

    var img = new window.Image();
    img.addEventListener("load", function () {
      ctx_output.clearRect(0, 0, canvas_output.width, canvas_output.height);
      ctx_output.drawImage(img, 0, 0);
      var new_image_data_output = ctx_output.getImageData(
        0, 0, img.width, img.height
      );
      generate_histogram(
        "div_output_histogram_result_plot",
        "Output Histogram",
        new_image_data_output
      );
    });
    img.setAttribute("src", data.edited_image_url + '?timestamp=' + timestamp);
  }

  $(".form_submit_using_ajax").submit(function(event) {
    // Stop form from submitting normally
    event.preventDefault();
    // Serialize data and call using ajax
    var payload = $(this).serializeArray();
    $.post($(this).attr('action'), payload, show_images_from_response, 'json');
    return false;
  });
});

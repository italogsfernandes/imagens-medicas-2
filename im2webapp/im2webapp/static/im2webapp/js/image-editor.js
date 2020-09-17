$(document).ready(function() {

  var original_image_obj = document.getElementById("output_original_image");
  var output_image_obj = document.getElementById("output_image");

  function show_tiff_image(id_field, filename, elem_id, canvas_arg, context_arg, div_histogram, title_histogram) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', filename);
    xhr.responseType = 'arraybuffer';
    xhr.onload = function (e) {
      var buffer = xhr.response;
      var tiff = new Tiff({buffer: buffer});
      var canvas = tiff.toCanvas();
      var width = tiff.width();
      var height = tiff.height();
      var dataurl = tiff.toDataURL();
      if (dataurl) {
        $("#" + id_field).attr("src", tiff.toDataURL());
      }
      if (canvas) {
        canvas_arg.width = width;
        canvas_arg.height = height;
        context_arg.drawImage(canvas, 0, 0);

        context_canvas = canvas.getContext("2d");
        var new_image_data_output = context_canvas.getImageData(
          0, 0, width, height
        );
        generate_histogram(
          div_histogram,
          title_histogram,
          new_image_data_output
        );
      }
    };
    xhr.send();
  }

  function render_tiff_image(id_field, filename) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', filename);
    xhr.responseType = 'arraybuffer';
    xhr.onload = function (e) {
      var buffer = xhr.response;
      var tiff = new Tiff({
        buffer: buffer
      });
      var dataurl = tiff.toDataURL();
      if (dataurl) {
        $("#" + id_field).attr("src", tiff.toDataURL());
      }
    };
    xhr.send();
  }

  $(".img-mini-viewer").each(function (index, element) {
    if ($(element).attr("src").endsWith(".tif")) {
      render_tiff_image(
        element.id,
        $(element).attr("src"),
      );
    }
  });


  // Setting up canvas variables
  var canvas_original = document.createElement("canvas");
  var canvas_output = document.createElement("canvas");

  var original_image_obj = document.getElementById("output_original_image");
  canvas_original.width = original_image_obj.width;
  canvas_original.height = original_image_obj.height;
  var ctx_original = canvas_original.getContext("2d");
  if (!$(original_image_obj).attr("src").endsWith(".tif")){
    ctx_original.drawImage(original_image_obj, 0, 0);
    var image_data_original = ctx_original.getImageData(
      0, 0, original_image_obj.width, original_image_obj.height
    );
    generate_histogram(
      "div_original_histogram_result_plot",
      "Original Histogram",
      image_data_original
    )
  } else {
    show_tiff_image(
      "output_original_image",
      $(original_image_obj).attr("src"),
      'original_tiff_image',
      canvas_original,
      ctx_original,
      "div_original_histogram_result_plot",
      "Original Histogram");
  }

  var output_image_obj = document.getElementById("output_image");
  canvas_output.width = output_image_obj.width;
  canvas_output.height = output_image_obj.height;
  var ctx_output = canvas_output.getContext("2d");
  if (!$(output_image_obj).attr("src").endsWith(".tif")) {
    ctx_output.drawImage(output_image_obj, 0, 0);
    var image_data_output = ctx_output.getImageData(
      0, 0, output_image_obj.width, output_image_obj.height
    );
    generate_histogram(
      "div_output_histogram_result_plot",
      "Output Histogram",
      image_data_output
    );
  } else {
    show_tiff_image(
      "output_image",
      $(output_image_obj).attr("src"),
      "output_tiff_image",
      canvas_output,
      ctx_output,
      "div_output_histogram_result_plot",
      "Output Histogram");
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

  //////////////////////////
  // Instensity Modifiers //
  //////////////////////////
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
      new_step = 0;
      new_min = 0;
      new_max = 150;
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

  //////////
  // Ajax //
  //////////
  function show_images_from_response(data) {
    $("#image_history_content_section").html(data.history_content_div);
    $("#tab_info").html(data.tab_info_content);
    $("#div_output_image").html(data.output_image_block_div);
    $('#messages').replaceWith(data.messages);
    close_messages();

    // Update image data
    var timestamp = new Date().getTime();
    var new_edited_image_url = data.edited_image_url + '?timestamp=' + timestamp;
    
    var img = new window.Image();
    $('#output_image').attr('src', new_edited_image_url);

    if (data.edited_image_url.endsWith(".tif")) {
      show_tiff_image(
        "output_image",
        new_edited_image_url,
        "output_tiff_image",
        canvas_output,
        ctx_output,
        "div_output_histogram_result_plot",
        "Output Histogram");
    } else {
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

    set_btn_undo_last_action_click();
    set_btn_reset_all_actions_click();
  }

  $(".form_submit_using_ajax").submit(function(event) {
    // Stop form from submitting normally
    event.preventDefault();
    // Serialize data and call using ajax
    var payload = $(this).serializeArray();
    $.post($(this).attr('action'), payload, show_images_from_response, 'json');
    return false;
  });

  /////////////////////
  // Noise Modifiers //
  /////////////////////

  function update_noise_arguments_range() {
    var selected_value = $("#id_noise_type").val();
    var new_amount_value = 1;
    var new_arg1_step;
    var new_arg1_min;
    var new_arg1_max;
    var new_arg2_step;
    var new_arg2_min;
    var new_arg2_max;
    var default_arg1;
    var default_arg2;

    if (selected_value == 'uniform'){
      new_arg1_step = 1;
      new_arg1_min = -255;
      new_arg1_max = 255;
      new_arg2_step = 1;
      new_arg2_min = -255;
      new_arg2_max = 255;
      default_arg1 = 0;
      default_arg2 = 80;
    } else if (selected_value == 'gaussian'){
      new_arg1_step = 0.1;
      new_arg1_min = 0;
      new_arg1_max = 255;
      new_arg2_step = 1;
      new_arg2_min = 0;
      new_arg2_max = 255;
      default_arg1 = 5;
      default_arg2 = 30;
    } else if (selected_value == 'rayleight'){
      new_arg1_step = 1;
      new_arg1_min = 0;
      new_arg1_max = 255;
      new_arg2_step = 0.1;
      new_arg2_min = 0;
      new_arg2_max = 1;
      default_arg1 = 20;
      default_arg2 = 0;
    } else if (selected_value == 'exponential'){
      new_arg1_step = 1;
      new_arg1_min = 0;
      new_arg1_max = 255;
      new_arg2_step = 0.1;
      new_arg2_min = 0;
      new_arg2_max = 1;
      default_arg1 = 5;
      default_arg2 = 0;
    } else if (selected_value == 'gamma'){
      new_arg1_step = 0,1;
      new_arg1_min = 0;
      new_arg1_max = 1;
      new_arg2_step = 1;
      new_arg2_min = 0;
      new_arg2_max = 255;
      default_arg1 = 1;
      default_arg2 = 8;
    } else if (selected_value == 'salt_and_pepper'){
      new_arg1_step = 0.01;
      new_arg1_min = 0;
      new_arg1_max = 1;
      new_arg2_step = 0.1;
      new_arg2_min = 0;
      new_arg2_max = 1;
      default_arg1 = 0.5;
      default_arg2 = 0;
    } else {
      new_arg1_step = 1;
      new_arg1_min = 0;
      new_arg1_max = 255;
      new_arg2_step = 1;
      new_arg2_min = 0;
      new_arg2_max = 255;
      default_arg1 = 0;
      default_arg2 = 0;
    }


    $("#id_range_input_noise_arg1_value").attr("step", new_arg1_step);
    $("#id_range_input_noise_arg1_value").attr("min", new_arg1_min);
    $("#id_range_input_noise_arg1_value").attr("max", new_arg1_max);
    $("#id_range_input_noise_arg1_value").val(default_arg1);

    $("#id_range_input_noise_arg2_value").attr("step", new_arg2_step);
    $("#id_range_input_noise_arg2_value").attr("min", new_arg2_min);
    $("#id_range_input_noise_arg2_value").attr("max", new_arg2_max);
    $("#id_range_input_noise_arg2_value").val(default_arg2);

    if (selected_value == 'salt_and_pepper'){
      new_amount_value = 0.04;
    }
    $("#id_range_input_noise_amount_value").val(new_amount_value);
  }

  function update_noise_arguments_value_label() {
    var selected_value = $("#id_noise_type").val();
    var argument1_text = "";
    var argument2_text = "";
    var new_arg1_value = $("#id_range_input_noise_arg1_value").val();
    var new_arg2_value = $("#id_range_input_noise_arg2_value").val();
    var new_amount_value = $("#id_range_input_noise_amount_value").val();

    if (selected_value == 'uniform'){
      argument1_text = 'low';
      argument2_text = 'high';
    } else if (selected_value == 'gaussian'){
      argument1_text = 'mean';
      argument2_text = 'std';
    } else if (selected_value == 'rayleight'){
      argument1_text = 'scale';
      argument2_text = '';
    } else if (selected_value == 'exponential'){
      argument1_text = 'scale';
      argument2_text = '';
    } else if (selected_value == 'gamma'){
      argument1_text = 'shape';
      argument2_text = 'scale';
    } else if (selected_value == 'salt_and_pepper'){
      argument1_text = 'S vs P';
      argument2_text = '';
    } else {
      argument1_text = 'Value 1';
      argument2_text = 'Value 2';
    }

    // Particular case, show hide field
    if (selected_value == 'rayleight' ||
        selected_value == 'exponential' ||
        selected_value == 'salt_and_pepper'){
      $("label[for='id_argument2_value']").hide();
      $("#id_argument2_value").hide();
      $("#id_range_input_noise_arg2_value").hide();
    } else {
      $("label[for='id_argument2_value']").show();
      $("#id_argument2_value").show();
      $("#id_range_input_noise_arg2_value").show();
    }

    $("label[for='id_argument1_value']").text(argument1_text + ": ");
    $("label[for='id_argument2_value']").text(argument2_text + ": ");
    $("#id_argument1_value").val(new_arg1_value);
    $("#id_argument2_value").val(new_arg2_value);
    $("#id_amount_value").val(new_amount_value);
  }


  update_noise_arguments_range();

  update_noise_arguments_value_label();

  $("#id_noise_type").change(function() {
    update_noise_arguments_range();
    update_noise_arguments_value_label();
  });

  $('input[id^="id_range_input_noise_"][id$="_value"]').on('change', _.debounce(function() {
    update_noise_arguments_value_label();
  }, 250));

  /////////////////////
  // Filter Modifiers //
  /////////////////////

  function update_filter_arguments_range() {
    var selected_value = $("#id_filter_type").val();
    var new_arg_step;
    var new_arg_min;
    var new_arg_max;
    var default_arg;

    if (selected_value == 'gaussian'){
      default_arg = 3;
      new_arg_step = 0.1;
      new_arg_max = 100;
      new_arg_min = 0;
    } else if (selected_value == 'uniform'){
      default_arg = 3;
      new_arg_step = 0.1;
      new_arg_max = 100;
      new_arg_min = 0;
    } else if (selected_value == 'median'){
      default_arg = 3;
      new_arg_step = 0.1;
      new_arg_max = 100;
      new_arg_min = 0;
    } else if (selected_value == 'maximum'){
      default_arg = 3;
      new_arg_step = 0.1;
      new_arg_max = 100;
      new_arg_min = 0;
    } else if (selected_value == 'minimum'){
      default_arg = 3;
      new_arg_step = 0.1;
      new_arg_max = 100;
      new_arg_min = 0;
    } else if (selected_value == 'sharpening'){
      default_arg = 30;
      new_arg_step = 0.1;
      new_arg_max = 100;
      new_arg_min = 0;
    } else if (selected_value == 'percentile'){
      default_arg = 75;
      new_arg_step = 0.1;
      new_arg_max = 100;
      new_arg_min = 0;
    } else if (selected_value == 'wiener'){
      default_arg = 0;
      new_arg_step = 0.1;
      new_arg_max = 100;
      new_arg_min = 0;
    } else if (selected_value == 'sobel'){
      default_arg = 3;
      new_arg_step = 0.1;
      new_arg_max = 100;
      new_arg_min = 0;
    } else {
      default_arg = 3;
      new_arg_step = 0.1;
      new_arg_max = 100;
      new_arg_min = 0;
    }

    $("#id_range_input_filter_arg_value").attr("step", new_arg_step);
    $("#id_range_input_filter_arg_value").attr("min", new_arg_min);
    $("#id_range_input_filter_arg_value").attr("max", new_arg_max);
    $("#id_range_input_filter_arg_value").val(default_arg);

    if (selected_value == 'sharpening'){
      $("#id_range_input_filter_size_value").attr("step", 0.1);
      $("#id_range_input_filter_size_value").attr("min", 0);
      $("#id_range_input_filter_size_value").attr("max", 10);
    } else {
      $("#id_range_input_filter_size_value").attr("step", 2);
      $("#id_range_input_filter_size_value").attr("min", 3);
      $("#id_range_input_filter_size_value").attr("max", 15);
      $("#id_range_input_filter_size_value").val(3);
    }
  }

  function update_filter_arguments_value_label() {
    var selected_value = $("#id_filter_type").val();
    var argument_text = "";
    var new_arg_value = $("#id_range_input_filter_arg_value").val();
    var new_size_value = $("#id_range_input_filter_size_value").val();

    if (selected_value == 'gaussian'){
      argument_text = 'Sigma';
      size_text = 'Size';
    } else if (selected_value == 'uniform'){
      argument_text = '';
      size_text = 'Size';
    } else if (selected_value == 'median'){
      argument_text = '';
      size_text = 'Size';
    } else if (selected_value == 'maximum'){
      argument_text = '';
      size_text = 'Size';
    } else if (selected_value == 'minimum'){
      argument_text = '';
      size_text = 'Size';
    } else if (selected_value == 'sharpening'){
      argument_text = 'Alpha';
      size_text = 'Sigma';
    } else if (selected_value == 'percentile'){
      argument_text = 'Percentile';
      size_text = 'Size';
    } else if (selected_value == 'wiener'){
      argument_text = 'Noise Power';
      size_text = 'Size';
    } else if (selected_value == 'sobel'){
      argument_text = '';
      size_text = '';
    } else {
      argument_text = 'Value 1';
      size_text = 'Size';
    }



    if (selected_value == 'sobel'){
      $("label[for='id_filter_argument_value']").hide();
      $("#id_filter_argument_value").hide();
      $("#id_range_input_filter_arg_value").hide();
      $("label[for='id_size_value']").hide();
      $("#id_size_value").hide();
      $("#id_range_input_filter_size_value").hide();
    } else {
      $("label[for='id_size_value']").show();
      $("#id_size_value").show();
      $("#id_range_input_filter_size_value").show();
      // Particular case, show hide field
      if (selected_value == 'uniform' ||
          selected_value == 'median' ||
          selected_value == 'maximum' ||
          selected_value == 'minimum'){
        $("label[for='id_filter_argument_value']").hide();
        $("#id_filter_argument_value").hide();
        $("#id_range_input_filter_arg_value").hide();
      } else {
        $("label[for='id_filter_argument_value']").show();
        $("#id_filter_argument_value").show();
        $("#id_range_input_filter_arg_value").show();
      }
    }

    $("label[for='id_filter_argument_value']").text(argument_text + ": ");
    $("label[for='id_size_value']").text(size_text + ": ");
    $("#id_filter_argument_value").val(new_arg_value);
    $("#id_size_value").val(new_size_value);
  }

  update_filter_arguments_range();

  update_filter_arguments_value_label();

  $("#id_filter_type").change(function() {
    update_filter_arguments_range();
    update_filter_arguments_value_label();
  });

  $('input[id^="id_range_input_filter_"][id$="_value"]').on('change', _.debounce(function() {
    update_filter_arguments_value_label();
  }, 250));

  function set_btn_undo_last_action_click(){
    $("#btn_undo_last_action").click(function (event) {
      event.preventDefault();
      var href = $("#btn_undo_last_action").attr("href");
      $.get(href, show_images_from_response, 'json');
      return false;
    });
  }
  set_btn_undo_last_action_click();

  function set_btn_reset_all_actions_click() {
    $("#btn_reset_all_actions").click(function (event) {
      event.preventDefault();
      var href = $("#btn_reset_all_actions").attr("href");
      $.get(href, show_images_from_response, 'json');
      return false;
    });
  }
  set_btn_reset_all_actions_click();
  
});

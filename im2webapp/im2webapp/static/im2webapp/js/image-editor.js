$(document).ready(function() {
  $("#range_brightness").blur(function() {
    var amount = $(this).val();
    amount = amount / 10;
    $("#brightness_value").text(amount);
    var img = document.getElementById('output_image');
    img.setAttribute('style',
      'filter:brightness(' +
      amount +
      '); -webkit-filter:brightness(' +
      amount +
      '); -moz-filter:brightness(' +
      amount +
      ')'
    );
  });
  $("#range_contrast").blur(function() {
    var amount = $(this).val();
    amount = amount / 10;
    $("#contrast_value").text(amount);
    var img = document.getElementById('output_image');
    img.setAttribute('style',
      'filter:contrast(' +
      amount +
      '); -webkit-filter:contrast(' +
      amount +
      '); -moz-filter:contrast(' +
      amount +
      ')'
    );
  });


  $("#input_compare").change(function() {
    if(this.checked) {
      $("#div_output_original_image").show();
      if($("#input_histogram").checked) {
        $("#div_output_original_histogram").show();
      }
    } else {
      $("#div_output_original_image").hide();
      if($("#input_histogram").checked) {
        $("#div_output_original_histogram").hide();
      }
    }
  });

  $("#input_histogram").change(function() {
    if(this.checked) {
      if($("#input_compare").checked) {
        $("#div_output_original_histogram").show();
      }
      $("#div_output_histogram").show();
    } else {
      if($("#input_compare").checked) {
        $("#div_output_original_histogram").hide();
      }
      $("#div_output_histogram").hide();
    }
  });
});

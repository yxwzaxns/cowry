$(function() {
  $('#settings').click(function() {
    $('.current').hide();
    $('.current').removeClass('current');
    $('.settings').show();
    $('.settings').addClass('current');
    // #('')
  })
  $('#dash').click(function() {
    $('.current').hide();
    $('.current').removeClass('current');
    $('.dash').show();
    $('.dash').addClass('current');
    // #('')
  })
  $('#profile').click(function() {
    $('.current').hide();
    $('.current').removeClass('current');
    $('.profile').show();
    $('.profile').addClass('current');
    // #('')
  })
  //
  $('#save').click(function () {
      var postData = $( ".settings form" ).serializeArray();
      $.ajax(
      {
          url : '/home/settings',
          type: "POST",
          data : postData,
          dataType: "json",
          success:function(data, textStatus, jqXHR)
          {
              console.log(data)
              alert(data)
          },
          error: function(jqXHR, textStatus, errorThrown)
          {
              // console.log(errorThrown)
          }
      });
  })
})

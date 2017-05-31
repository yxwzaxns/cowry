document.addEventListener("DOMContentLoaded", function(event) {
  //do work
  $.get('/api/syslog',function (data) {
    for (i = 0; i < data.length; i++) {
      row = $('<tr><td>'+data[i].id+'</td><td>'+data[i].uid+'</td><td>'+data[i].ip+'</td><td>'+data[i].event.trim()+'</td><td>'+data[i].update_time+'</td></tr>'); //create row
      $('.log').append(row);
    }
  })
});

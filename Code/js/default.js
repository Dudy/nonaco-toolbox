$('.project-overview a').click(function(e) {
  e.preventDefault();
  var data_container = $(this).parent().parent(),
    type = $(this).attr('data-type'),
    key_type = data_container.attr('data-type'),
    key = data_container.attr('data-urlsafe'),
    operation = $(this).attr('data-operation'),
    url = '/project/' + type + '?' + key_type + '-key=' + key + '&operation=' + operation;
  $.getJSON(url, function(result) {
    $('#content').html(result.html);
  });
});
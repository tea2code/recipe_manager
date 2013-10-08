$(document).ready(function() {
    // Chosen.
    $('#tags').chosen();

    // Add URLs.
    $('#manage-recipe #add-url').click(function(event)
    {
        var url_count = parseInt($('#url-counter').val());
        $('#url-counter').val(url_count + 1);
        var input = '<div>' +
                    '    <label for="url-name-'+url_count+'">Name of link '+(url_count+1)+':</label>' +
                    '    <input type="text" id="url-name-'+url_count+'" name="url-name-'+url_count+'" value="" />' +
                    '</div>' +
                    '<div>' +
                    '    <label for="url-url-'+url_count+'">Link '+(url_count+1)+':</label>' +
                    '    <input type="text" id="url-url-'+url_count+'" name="url-url-'+url_count+'" value="" />' +
                    '</div>';
        $('#manage-recipe #urls').append(input);
        event.preventDefault();
    });
});
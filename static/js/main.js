$(document).ready(function() {
    // Chosen.
    $('#tags').chosen();

    // Add Synonyms.
    $('#manage-recipe #add-synonym').click(function(event)
    {
        var synonym_count = parseInt($('#synonym-counter').val());
        $('#synonym-counter').val(synonym_count + 1);
        var input = '<div>' +
                    '    <label for="synonym-'+synonym_count+'">Synonym '+(synonym_count+1)+':</label>' +
                    '    <input type="text" id="synonym-'+synonym_count+'" name="synonym-'+synonym_count+'" value="" />' +
                    '</div>';
        $('#manage-recipe #synonyms').append(input);
        event.preventDefault();
    });

    // Add URLs.
    $('#manage-recipe #add-url').click(function(event)
    {
        var url_count = parseInt($('#url-counter').val());
        $('#url-counter').val(url_count + 1);
        var input = '<div>' +
                    '    <label for="url-name-'+url_count+'">Name of Link '+(url_count+1)+':</label>' +
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
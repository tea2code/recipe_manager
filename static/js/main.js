$(document).ready(function() {
    // Tag Groups.
    $('.tag-group').children(':not(.tag-group-legend)').hide();
    $('.tag-group-legend').click(function() 
    {
        $(this).siblings().toggle();
    });

    // Chosen.
    $('#manage-recipe #categories').chosen();
    $('#manage-recipe #tags').chosen();
    
    // Fancybox.
    $('.fancybox').fancybox();

    // Add Images.
    $('#manage-recipe #add-image').click(function(event)
    {
        var image_count = parseInt($('#new-image-counter').val());
        $('#new-image-counter').val(image_count + 1);
        var input = '<div class="input-row">' +
                    '    <label for="new-image-'+image_count+'">New Image '+(image_count+1)+':</label>' +
                    '    <input type="file" id="new-image-'+image_count+'" accept="image/gif, image/jpeg, image/png" name="new-image-'+image_count+'" />' +
                    '</div>';
        $('#manage-recipe #images').append(input);
        event.preventDefault();
    });

    // Delete Images.
    $('#manage-recipe .delete-image').click(function(event)
    {
        var image_id = $(this).data('rel');
        $('#'+image_id).remove();
        event.preventDefault();
    });

    // Add Synonyms.
    $('#manage-recipe #add-synonym').click(function(event)
    {
        var synonym_count = parseInt($('#synonym-counter').val());
        $('#synonym-counter').val(synonym_count + 1);
        var input = '<div class="input-row">' +
                    '    <label for="synonym-'+synonym_count+'">Synonym '+(synonym_count+1)+':</label>' +
                    '    <input type="text" id="synonym-'+synonym_count+'" name="synonym-'+synonym_count+'" />' +
                    '</div>';
        $('#manage-recipe #synonyms').append(input);
        event.preventDefault();
    });

    // Add URLs.
    $('#manage-recipe #add-url').click(function(event)
    {
        var url_count = parseInt($('#url-counter').val());
        $('#url-counter').val(url_count + 1);
        var input = '<div class="input-row">' +
                    '    <label for="url-name-'+url_count+'">Name of Link '+(url_count+1)+':</label>' +
                    '    <input type="text" id="url-name-'+url_count+'" name="url-name-'+url_count+'" />' +
                    '</div>' +
                    '<div class="input-row">' +
                    '    <label for="url-url-'+url_count+'">Link '+(url_count+1)+':</label>' +
                    '    <input type="text" id="url-url-'+url_count+'" name="url-url-'+url_count+'" />' +
                    '</div>';
        $('#manage-recipe #urls').append(input);
        event.preventDefault();
    });
});
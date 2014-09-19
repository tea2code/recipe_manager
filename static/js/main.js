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
    
    // Language Selection.
    $('#language-selection').change(function(event)
    {
        $.cookie('language', $(this).val(), { expires: 365, path: '/' });
        location.reload();
    });

    // Add Images.
    $('#manage-recipe #add-image').click(function(event)
    {
        var image_count = parseInt($('#new-image-counter').val());
        $('#new-image-counter').val(image_count + 1);
        var input = $('#template-add-image').html()
                    .replace(/{image_count}/g, image_count)
                    .replace(/{image_count\+1}/g, (image_count + 1));
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
        var input = $('#template-add-synonym').html()
                    .replace(/{synonym_count}/g, synonym_count)
                    .replace(/{synonym_count\+1}/g, (synonym_count + 1));
        $('#manage-recipe #synonyms').append(input);
        event.preventDefault();
    });

    // Add URLs.
    $('#manage-recipe #add-url').click(function(event)
    {
        var url_count = parseInt($('#url-counter').val());
        $('#url-counter').val(url_count + 1);
        var input = $('#template-add-url').html()
                    .replace(/{url_count}/g, url_count)
                    .replace(/{url_count\+1}/g, (url_count + 1));
        $('#manage-recipe #urls').append(input);
        event.preventDefault();
    });
});
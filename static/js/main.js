$(document).ready(function() {
    // Scroll to recipe title.
    if ($(".anchor").length > 0)
    {
        $(document).scrollTop($(".anchor").first().offset().top);  
    }

    // Chosen.
    $('#manage-recipe #categories').chosen();
    $('#manage-recipe #tags').chosen();
    
    // Custom content scroller.
    $('#images,#randoms').mCustomScrollbar({
        theme:'dark-thin'
    });
    
    // Fancybox.
    $('.fancybox').fancybox();
    
    // Language Selection.
    $('#language-selection').change(function(event)
    {
        $.cookie('language', $(this).val(), { expires: 365, path: '/' });
        location.reload();
    });
    
    // Custom file input.
    $('form').on('click', '.upload-button', function(event) 
    { 
        $('#' + $(this).data('upload')).trigger('click'); 
        event.preventDefault();        
    });
    
    $('form').on('change', '.upload-input', function(event)
    {
        $('#fake-' + $(this).attr('id')).val($(this).val());
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
    
    // Tag Groups.
    $('.tag-group').children(':not(.tag-group-legend)').hide();
    $('.tag-group-legend').click(function() 
    {
        $(this).siblings().toggle();
    });
});
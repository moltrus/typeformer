jQuery(document).ready(function () {
    var slider_mask = $('#max_words_mask');
    slider_mask.on('change mousemove', function () {
        $('#label_max_words').text('Top k words: ' + slider_mask.val());
    });

    $('#input_text').on('input', function () {
        const inputText = $(this).val().trim();
        if (inputText) {
            $.ajax({
                url: '/segcorrect',
                type: "post",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify({ "input_text": inputText }),
                beforeSend: function () {
                    console.log("beforeSend");
                    $('.overlay').show();
                },
                complete: function () {
                    $('.overlay').hide();
                }
            }).done(function (jsondata) {
                console.log(jsondata);
                const sentence = jsondata['words'].join(' ');
                $('#output_text').val(sentence);
            }).fail(function (error) {
                console.error("Error in /segcorrect:", error);
            });
        }
    });

    $('#btn-process').on('click', function () {
        const inputText = $('#mask_input_text').val().trim();
        if (inputText) {
            $.ajax({
                url: '/predict',
                type: "post",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify({
                    "input_text": inputText,
                    "top_k": slider_mask.val()
                }),
                beforeSend: function () {
                    $('.overlay').show();
                },
                complete: function () {
                    $('.overlay').hide();
                }
            }).done(function (jsondata) {
                console.log(jsondata);
                $('#mask_output_text').val('');
                sentence = ''
                jsondata.words.forEach(word => { sentence += inputText +' '+ word + '\n' });
                jsondata.words.forEach(word => { console.log(inputText +' '+ word); });
                //const sentence = jsondata['words'].join(' ');
                $('#mask_output_text').val(sentence);
            }).fail(function (error) {
                console.error("Error in /predict:", error);
            });
        }
    });
});

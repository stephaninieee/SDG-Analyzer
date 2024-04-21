function setTableData(data){
    $('#Keyword_table').DataTable().clear().destroy();
    $('#Keyword_table').DataTable({
        data: data,
        "columns":[
            {"data":"Keyword"},
            {"data":"Rate"}
        ]  
    });
}

$(document).ready(function () {
            
    $("#submit").click(function () {
        var form_data = new FormData();
        form_data.append('text',$(text.getData()).text())
        form_data.append('lang',$("#lang").val())

        $.ajax({
            type: "POST",
            url: "/get_keywords",
            data: form_data,
            contentType: false,
            processData: false,
            dataType: "json",
        }).done(function(data){
            var wordlist = [];

            wdata = data.wordsData

            for(var i=0;i<wdata.length;i++){
                wordlist[i] = wdata[i]['Keyword']
            }
            setTableData(wdata);
            $('#foo').val(wordlist);
            document.getElementById("datashow").style.display="";
        })
    });

    var clipboard = new ClipboardJS('.btn');

    clipboard.on('success', function(e) {
        console.info('Action:', e.action);
        console.info('Text:', e.text);
        console.info('Trigger:', e.trigger);

        e.clearSelection();
    });

    clipboard.on('error', function(e) {
        console.error('Action:', e.action);
        console.error('Trigger:', e.trigger);
    });

});  
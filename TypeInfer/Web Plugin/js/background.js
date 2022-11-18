chrome.extension.onRequest.addListener(function (request, sender, sendResponse) {
    console.log('request', request);
    console.log('sender', sender);
    if (request.action == 'infer') {
        $.ajax({
            url:'http://localhost:5000/login',
            method: 'POST',
            data: {
                co_area: request.co_area,
                co_name: request.co_name,
                co_top : request.co_top,
                co_all : request.co_all,
                model: request.model
            },
            asyne: true
        }).done(function (data) {
            // console.log('transData', data);
            sendResponse({
                data: data
            });
        });
    }else {
        //todo
    }
});




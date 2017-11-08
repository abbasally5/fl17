var req = function(type, url, data, success, complete) {
    $.ajax({
        url: url,
        type: type,
        datatype: "json",
        data: data,
        success: success,
        complete: complete,
    });
    return false;
};

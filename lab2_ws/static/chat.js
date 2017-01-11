$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new WebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);

    var objDiv = $("#chat-list");
    objDiv.scrollTop(objDiv.prop("scrollHeight"));

    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data)
        var chat = $("#chat-element").first().clone().appendTo("#chat-element-list").removeClass('hidden');
        var body = chat.find("#chat-element-body")
        body.text(data.message)

        var details = chat.find("#chat-element-details")
        details.text(data.handle + " " + data.timestamp)
        data.remove

        var objDiv = $("#chat-list");
        objDiv.scrollTop(objDiv.prop("scrollHeight"));
    };

    $("#chatform").on("submit", function(event) {
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
});
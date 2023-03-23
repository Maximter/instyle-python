let requestGetNewMesSent = false;

function sendMessage () {
    let message = messageInput.value;
    message = message.trim();

    if (activeConversation === undefined && idInterlocutor === undefined || message === "") return 0;

    if (message.length > 2000) {
        Swal.fire({
            position: 'top',
            icon: 'error',
            title: 'Слишком длинное сообщение. Максимально разрешённая длина символов: 2000',
            showConfirmButton: false,
            timer: 2000
        })    
      return
    }

    console.log(activeConversation, idInterlocutor) 
    if ((activeConversation === undefined || activeConversation === 'none') && idInterlocutor) socket.emit('sendFirstMessage', message, idInterlocutor);
    else {
        socket.emit('sendMessage', message, activeConversation);
        $.ajax('/chat/unread', {
            method : 'GET',
            data: { id_chat: activeConversation }
        });
    }
    let date = new Date(+new Date).toLocaleTimeString().slice(0,-3);

    messageInput.value = "";
    let htmlCode = document.createElement('li');
    htmlCode.classList.add('message', 'own');
    htmlCode.innerHTML = `<p>${message}</p>
                        <date style="font-size:12px">${date}</date>`
    outputMessage.append(htmlCode)

    const chats = document.getElementsByClassName('chat')
    for (let i = 0; i <= chats.length-1; i++) {
        if (activeConversation === chats[i].attributes.id_chat.value) {

            let lastMessage = ""
            let tempHtml = document.createElement('div');
            tempHtml.innerHTML = `${message}`;
            if (tempHtml.getElementsByClassName('bar').length > 0) lastMessage = "Пост"
            else if (tempHtml.getElementsByClassName('sticker_img').length > 0) lastMessage = "Стикер"
            else lastMessage = message
            
            if (lastMessage.length > 30) {
                lastMessage = message.substr(0, 30)
                lastMessage += '...'
            }
           
            chats[i].childNodes[5].childNodes[3].innerText = `Вы: ${lastMessage}`;
            chats[i].childNodes[7].childNodes[3].className = 'blueUnread'
            chats[i].childNodes[7].childNodes[3].innerHTML = ''

            let date = new Date(+new Date).toLocaleTimeString().slice(0,-3);
            chats[i].childNodes[7].childNodes[1].innerHTML = date

            if (i !== 0) outputChats.prepend(chats[i]);
        break;
        }
    }
    outputMessages.scrollTop = outputMessages.scrollHeight
}

function addMessages(data, id_chat) {
    outputMessage.innerHTML = "";
    for (let i = 0; i < data.length; i++) {
        
        let date;
        if (86400000 < data[i].sent_date) date = parseToShortDate(data[i].sent_date)
        else date = `${new Date(+data[i].sent_date).toLocaleTimeString().slice(0,-3)} ${parseToShortDate(data[i].sent_date)}`
        

        if (data[i].sender != undefined) {
            outputMessage.innerHTML += `<li class="message own" id_message="${data[i].id}">
                                                        <p>${data[i].content}</p>
                                                        <date style="font-size:12px; color: #000">${date}</date>
                                                    </li>`;
        } else {
            outputMessage.innerHTML += `<li class="message interlocutor" id_message="${data[i].id}">
                                                            <p>${data[i].content}</p>
                                                        <date style="font-size:12px; color: #000">${date}</date>
                                                    </li>`;
        }
    }
    outputMessages.scrollTop = outputMessages.scrollHeight
}

function clientIsTyping () {
    socket.emit('isTyping', activeConversation)
}

$('ul').on('click','li.chat',function(element){

    const username = element.currentTarget.attributes.username.value;
    chatInfoImg.style = "display: box"
    nameHref.href = `user/${username}`
    imgHref.href = `user/${username}`

    if (element.target.src || element.target.id === "onlinePoint") element.target = element.target.parentNode
    else if (element.target.id === "chatName" || element.target.id === "lastMessage" ||
               element.target.id === "read" || element.target.id === "time_last_message") element.target = element.target.parentNode.parentNode

    let id_chat = element.target.attributes.id_chat.nodeValue;
    let statusChat = element.target.attributes.online.nodeValue;
    // let isread = element.target.childNodes[7].childNodes[3];

    if (statusChat === "0") status.innerText = "В сети"
    else status.innerText = wasOnline(statusChat);
    
    // if (isread !== undefined) {
    //     if (isread.innerHTML !== '') {
    //         isread.innerHTML = ''
    //         isread.className = ''
    //     }
    // }

    
    if (element.target.getElementsByClassName('inside')[0]) {
        chatInfoName.innerText = element.target.getElementsByClassName('inside')[0].getElementsByClassName('lastSenderText')[0].innerText
        chatInfoImg.src = element.target.childNodes[1].src
    } else { 
        chatInfoName.innerText = element.target.getElementsByClassName('lastSenderText')[0].innerText
        chatInfoImg.src = "../img/smallAvatar/standard.jpg"
    }
    
    writeTo = undefined;
    activeConversation = id_chat;

    if (activeConversation === undefined) return 0;
    
    $.ajax('/chat/getMessages', {
        data: { id_chat: id_chat },
        success: data => addMessages(data, id_chat)
    });
    messageInput.click();

    $.ajax('/chat/read', {
        data: {id_chat: id_chat}
    });
    socket.emit('read', activeConversation)
    requestGetNewMesSent = false
});


$('ul').on('click','li.liSticker',function(element){
    let sticker = element.target;
    sticker.style.height = "180px"
    message.value = `${sticker.outerHTML}`;
    sticker.style.height = "88px"
    sendMessage();
    stickerMenu.style = "display: none;"
    message.value = ""
});

send.onclick = () => sendMessage();
addEventListener("keydown", function(event) {
    if (event.code === "Enter") sendMessage();
});

addEventListener('input', function (event) {
    if (event.path !== undefined && event.path[0].attributes.id.value === "message") {
        clientIsTyping();
    } else if (event.target.id !== undefined && event.target.id === "message") {
        clientIsTyping();
    }
});



outputMessages.addEventListener("scroll", function (event) {
    if (outputMessages.scrollTop == 0) {     
        let fixedScroll = outputMessages.scrollHeight
        if (!requestGetNewMesSent) {
            requestGetNewMesSent = true;
            let lastId
            if (outputMessages.childNodes[0].attributes) lastId = outputMessages.childNodes[0].attributes.id_message.value
            else lastId = outputMessages.childNodes[1].attributes.id_message.value
            
            $.ajax('/chat/getNewMessages', {
                data: { activeConversation: activeConversation, idInterlocutor : idInterlocutor, lastId : lastId },
                success: data => {
                    outputMessages.scrollTop == 1
                    for (let i = 0; i < data.length; i++) {
                        let date = data[i].sent_date;
                        if (!idInterlocutor) {
                            if (86400000 < data[i].sent_date) date = parseToShortDate(data[i].sent_date)
                            else date = `${new Date(+data[i].sent_date).toLocaleTimeString().slice(0,-3)} ${parseToShortDate(data[i].sent_date)}`
                        }
                
                        if (data[i].sender != undefined) {
                            let str =`<li class="message own" id_message="${data[i].id}">
                                            <p>${data[i].content}</p>
                                            <date style="font-size:12px; color: #000">${date}</date>
                                        </li>`;
                            outputMessage.insertAdjacentHTML( 'afterbegin', str );
                        } else {
                            let str = `<li class="message interlocutor" id_message="${data[i].id}">
                                            <p>${data[i].content}</p>
                                            <date style="font-size:12px; color: #000">${date}</date>
                                        </li>`;
                            outputMessage.insertAdjacentHTML( 'afterbegin', str );
                        }
                    }
                    outputMessages.scrollTop = outputMessages.scrollHeight - fixedScroll
                    requestGetNewMesSent = false;
                }
            });
            setTimeout(async () => requestGetNewMesSent = false, 8000);
        }
    }
})
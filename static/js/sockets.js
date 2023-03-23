let socket = io();

socket.on('getMessage', function (message, fromConversation) {  
    const chats = document.getElementsByClassName('chat')
    for (let i = 0; i < chats.length; i++) {
        if (fromConversation === chats[i].attributes.id_chat.value) {



            let time_last_message = chats[i].childNodes[7].childNodes[1]
            let date = new Date(+new Date).toLocaleTimeString().slice(0,-3);
            time_last_message.innerHTML = date

            if (activeConversation === fromConversation) {
                let htmlCode = document.createElement('li');
                htmlCode.classList.add('message', 'interlocutor');
                htmlCode.innerHTML = ` <p>${message}</p>
                <date style="font-size:12px; color: #000;">${date}</date>`
                outputMessage.append(htmlCode)

                $.ajax('/chat/read', {
                    data: {id_chat: activeConversation}
                });
                socket.emit('read', activeConversation)
                outputMessages.scrollTop = outputMessages.scrollHeight
            } else {
                if (chats[i].childNodes[7].childNodes[3].className !== 'unread') {
                    chats[i].childNodes[7].childNodes[3].className = 'unread'
                    chats[i].childNodes[7].childNodes[3].innerHTML = 1
                } else {
                    chats[i].childNodes[7].childNodes[3].innerHTML = +chats[i].childNodes[7].childNodes[3].innerHTML + 1
                }

            }

            let tempHtml = document.createElement('div');
            tempHtml.innerHTML = `${message}`;
            if (tempHtml.getElementsByClassName('bar').length > 0) lastMessage = "Пост"
            else if (tempHtml.getElementsByClassName('sticker_img').length > 0) lastMessage = "Стикер"
            else lastMessage = message

            if (lastMessage.length > 30) {
                lastMessage = message.substr(0, 30)
                lastMessage += '...'
            }

            chats[i].attributes.lastMessage.value = lastMessage
            chats[i].childNodes[5].childNodes[3].innerText = lastMessage;

            if (i !== 0) outputChats.prepend(chats[i]);
        }
    }
})

socket.on('addNewConversation', function (user, id_conversation) {
    let sender = ""
    let addClass = ""
    let addUnread = ""

    if (user.sender) {
        sender = "Вы:"
        addClass = "blueUnread"
    } else {
        addClass = "unread"
        addUnread = "1"
    }
    let style_online_point = 'none'
    if (user.online == '0') style_online_point = 'flex'
    if (user.avatar) user.avatar = `./../img/avatar/${user.id}.jpg`
    else user.avatar = `./../img/avatar/standard.jpg`

    let time_status = new Date(+new Date()).toLocaleTimeString().slice(0,-3);

    let newChat = `<li class="chat" id_chat="${id_conversation}" username="${user.username}" id="chat" online="${user.online}" lastMessage="${user.message}">
                        <img src="${user.avatar}" id_chat="${id_conversation}" class="chatAvatarImg" >
                        <div class="onlinePoint" id="onlinePoint" id_chat="${id_conversation}" style="display:${style_online_point}"></div>
                        <div>
                            <p id="chatName" id_chat="${id_conversation}" class="lastSenderText">${user.name_lastname}</p>
                            <p id="lastMessage" id_chat="${id_conversation}" class="lastMessageText">${sender} ${user.message}</p>
                        </div>
                        <div>
                            <p id="time_last_message" class="time_last_message">${time_status}</p>
                            <div id="read" class="${addClass}">${addUnread}</div>
                        </div>
                    </li>`;
    
    outputChats.prepend(new DOMParser().parseFromString(newChat, "text/html").getElementsByTagName("li")[0])

    if (user.sender) {
        const chats = document.getElementsByClassName('chat')
        for (let i = 0; i < chats.length; i++) {
            if (id_conversation === chats[i].attributes.id_chat.value && user.sender) {
                chats[i].click()
            }
        }   
    }
    
})

socket.on('getTyping', function (id_chat) {
    const chats = document.getElementsByClassName('chat')

    for (let i = 0; i < chats.length; i++) {
        if (id_chat === chats[i].attributes.id_chat.value) {
            if (activeConversation === id_chat) {
                status.style.display = 'none'
                typing.innerText = "Печатает..."
            }
            chats[i].childNodes[5].childNodes[3].innerText = "Печатает..."
            isTypingNow = true;

            setTimeout(function () {
                isTypingNow = false

                setTimeout(function () {
                    if (!isTypingNow) chats[i].childNodes[5].childNodes[3].innerText = chats[i].attributes.lastMessage.value
                    if (activeConversation === id_chat && !isTypingNow) {
                        typing.innerText = ""
                        status.style.display = 'flex'
                    }
                }, 1000);
            }, 2000);
            break;
        }
    }
})

socket.on('getRead', function (id_chat) {
    const chats = document.getElementsByClassName('chat')
    for (let i = 0; i < chats.length; i++) {
        if (id_chat === chats[i].attributes.id_chat.value) {
            if (chats[i].childNodes[7].childNodes[3].className === 'blueUnread') {
                chats[i].childNodes[7].childNodes[3].className = ''
                chats[i].childNodes[7].childNodes[3].innerHTML = ''
            }
        }
    }
})
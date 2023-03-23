const send = document.getElementById('send');
const messageBox = document.getElementById('messageBox');
const dropDown = document.getElementById('myDropdown');
const findCode = document.getElementById('findCode');
const message = document.getElementById('message');

const status = document.getElementById('status');
const chatOnlinePoint = document.getElementById('chatOnlinePoint');

const chatInfoName = document.getElementById('chatInfoName');
const chatInfo = document.getElementById('chatInfo');
const chatInfoImg = document.getElementById('chatInfoImg');
const typing = document.getElementById('typing');

const showProfileButton = document.getElementById('showProfile');
const profileBox = document.getElementById('profileBox');
const avatarImg = document.getElementById('avatarImg');

const messageInput = document.getElementById('message');
const searchInput = document.getElementById('searchInput');
const nameInput = document.getElementById('nameInput');
const lastnameInput = document.getElementById('lastnameInput');
const inputBox = document.querySelector('.inputBox');

const searchOutput = document.getElementById('searchOutput');
const conversationOutput = document.getElementById('outputConversations');
const outputMessage = document.getElementById('outputMessages');

const oldPassword = document.getElementById('oldPassword');
const newPassword = document.getElementById('newPassword');
const RepeatNewPassword = document.getElementById('RepeatNewPassword');

const changeName = document.getElementById('changeName');
const changePassword = document.getElementById('changePassword');
const read = document.getElementById('read');
const nameLastname = document.getElementById('nameLastname');
const mainAvatar = document.getElementById('mainAvatar');
const time_last_message = document.getElementById('time_last_message');
const profileNameLastname = document.getElementById('profileNameLastname');
const start_dialog = document.getElementById('start_dialog');
const imgHref = document.getElementById('imgHref');
const nameHref = document.getElementById('nameHref');
const outputChats = document.getElementById('outputChats');
const stickerButton = document.getElementById('sticker-button');
const stickerMenu = document.getElementById('sticker-menu');

let activeConversation;
let idInterlocutor;
let isTypingNow = false

let USERNAME;
let USERLASTNAME;
let USERFINDCODE;
let USERAVATAR;
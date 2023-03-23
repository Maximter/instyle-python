function parseToShortDate (ms) {
    let now = Date.parse(`${new Date()}`)
    let different = Math.floor((now - ms) / 1000 / 60);
    let time_status = "";
    let date = '';

    if (different < 60 * 24) date = new Date(+ms).toLocaleTimeString().slice(0,-3);
    else {
        time_status = String(new Date(+ms).toLocaleDateString());
        time_status = time_status.split("");
        delete time_status[time_status.length-4];
        delete time_status[time_status.length-3];
        time_status.forEach ((element) => {
            date += element;
        })
    }
    return date
}

function wasOnline (statusChat) {
    if (statusChat == '0') return 'В сети'
    let onlineTime = new Date(+statusChat);
    let onlineMs = Date.parse(`${onlineTime}`)
    let now = Date.parse(`${new Date()}`)
    let different = Math.floor((now - onlineMs) / 1000 / 60);
    let isStatus;

    if (different < 1)  isStatus = "Только что"
    else if (different < 60)  {
        switch (different) {
            case 1: case 21: case 31: case 41: case 51: {
                isStatus = `${different} минуту назад`
                break;
            }
            case 2: case 3: case 4:  case 22: case 23: case 24:
            case 32: case 33: case 34: case 42: case 43: case 44:
            case 52: case 53: case 54: {
                isStatus = `${different} минуты назад`
                break;
            }
            default:  isStatus = `${different} минут назад`
        }
    } else if (different < 1440) {
        different = Math.floor(different / 60);

        switch (different) {
            case 1:
            case 21: {
                isStatus = `${different} час назад`
                break;
            }
            case 2:
            case 3:
            case 4:
            case 22:
            case 23: {
                isStatus = `${different} часа назад`
                break;
            }
            default:
                isStatus = `${different} часов назад`
        }
    } else if (different / 24 / 24 < 30) {
        different = Math.floor(different / 60 / 24);

        switch (different) {
            case 1:
            case 21: {
                isStatus = `${different} день назад`
                break;
            }
            case 2:
            case 3:
            case 4:
            case 22:
            case 23:
            case 24: {
                isStatus = `${different} дня назад`
                break;
            }
            default:
                isStatus = `${different} дней назад`
        }
    } else if (different / 24 / 24 < 360) {
        different = Math.floor(different / 60 / 24 / 30);

        switch (different) {
            case 1: {
                isStatus = `${different} месяц назад`
                break;
            }
            case 2:
            case 3:
            case 4: {
                isStatus = `${different} месяца назад`
                break;
            }
            default:
                isStatus = `${different} месяцев назад`
        }
    } else {
        different = Math.floor(different / 60 / 24 / 30 / 12);

        switch (different) {
            case 1: {
                isStatus = `${different} год назад`
                break;
            }
            case 2:
            case 3:
            case 4: {
                isStatus = `${different} года назад`
                break;
            }
            default:
                isStatus = `${different} лет назад`
        }
    }


    return `Был(а) в сети: ${isStatus}`
}
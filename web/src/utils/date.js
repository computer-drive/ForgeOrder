
function formatDateInTime(date) {
    const hour = date.getHours().toString().padStart(2, '0');
    const minute = date.getMinutes().toString().padStart(2, '0');
    return `${hour}:${minute}`;
}

function getSub(date1, date2) {
    const diff = Math.abs(date1 - date2);
    
    if (diff < 60 * 1000) { // 判断是否小于1分钟
        return {
            hour: 0,
            minute: 0,
            second: Math.floor(diff / 1000),
        };
    } else if (diff < 60 * 60 * 1000) { // 判断是否小于1小时
        return {
            hour: Math.floor(diff / (60 * 1000)),
            minute: Math.floor((diff % (60 * 1000)) / 1000),
            second: 0,
        };
    } else {
        return {
            hour: Math.floor(diff / (60 * 60 * 1000)),
            minute: Math.floor((diff % (60 * 60 * 1000)) / (60 * 1000)),
            second: Math.floor((diff % (60 * 60 * 1000)) % (60 * 1000) / 1000)
        }
    }
}

export {
    formatDateInTime,
    getSub,
}
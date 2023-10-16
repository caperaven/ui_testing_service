export function cleanTime(time) {
    if (time == null || time.trim().length == 0) return {date: "", time: ""};

    time = time.replace(" ", "T");

    const parts = time.split("T");
    const date = parts[0];
    const time_stamp = parts[1].split(".")[0];
    return {date, time: time_stamp}
}
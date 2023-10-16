const TokenState = Object.freeze({
    NORMAL: "normal",
    QUOTE: "quote"
})

export function tokenize(string) {
    if (string.indexOf('"') == -1) return string.split(" ");

    const parts = [];

    const token = [];
    let state = TokenState.NORMAL;

    for (const char of string) {
        if (char == " " && state == TokenState.NORMAL) {
            parts.push(token.join(""));
            token.length = 0;
            continue;
        }

        if (char == '"') {
            if (state == TokenState.NORMAL) {
                state = TokenState.QUOTE;
            }
            else {
                state = TokenState.NORMAL;
                parts.push(token.join(""));
                token.length = 0;
            }
            continue;
        }

        token.push(char);
    }

    return parts;
}
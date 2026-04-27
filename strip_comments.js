const fs = require('fs');
const src = fs.readFileSync('d:/Manorty/Project/assets/js/main.js', 'utf8');

function stripComments(code) {
    let result = '';
    let i = 0;
    const len = code.length;
    let inSingle = false;
    let inDouble = false;
    let inTemplate = false;

    while (i < len) {
        const c = code[i];
        const next = i + 1 < len ? code[i + 1] : '';

        if (inSingle) {
            result += c;
            if (c === '\\') { i++; result += code[i]; }
            else if (c === "'") inSingle = false;
            i++; continue;
        }
        if (inDouble) {
            result += c;
            if (c === '\\') { i++; result += code[i]; }
            else if (c === '"') inDouble = false;
            i++; continue;
        }
        if (inTemplate) {
            result += c;
            if (c === '\\') { i++; result += code[i]; }
            else if (c === '`') inTemplate = false;
            i++; continue;
        }

        // Block comment /* ... */
        if (c === '/' && next === '*') {
            i += 2;
            while (i < len) {
                if (code[i] === '*' && i + 1 < len && code[i + 1] === '/') {
                    i += 2;
                    break;
                }
                if (code[i] === '\n') result += '\n';
                i++;
            }
            continue;
        }

        // Line comment // ...
        if (c === '/' && next === '/') {
            while (i < len && code[i] !== '\n') i++;
            continue;
        }

        if (c === "'") inSingle = true;
        if (c === '"') inDouble = true;
        if (c === '`') inTemplate = true;

        result += c;
        i++;
    }
    return result;
}

const stripped = stripComments(src);
fs.writeFileSync('d:/Manorty/Project/assets/js/main.js', stripped, 'utf8');
console.log('Done. Original: ' + src.length + ' bytes. Stripped: ' + stripped.length + ' bytes.');

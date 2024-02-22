const fs = require('fs');

// ------------------------------------- COMMAND SPECIFICATIONS ---------------------------------------------

// Value validation functions
const filenamePredicate = (x) => fs.existsSync(x);
const operationPredicate = (x) => ["difference", "union", "intersection"].includes(x);
const filenameError = (file) => `file '${file}' does not exist`;
const operationError = (operation) => `operation '${operation}' does not exist\nValid operations: [difference|union|intersection]`;

// Command specifications
const validKwargs = [
    // Key        Value validator     Error message
    ["set1",      filenamePredicate,  filenameError],
    ["set2",      filenamePredicate,  filenameError],
    ["operation", operationPredicate, operationError],
];

const validKeys = validKwargs.map(([key]) => key);

// ----------------------------------------- UTILS --------------------------------------------------

const printError = (message) => {
    console.log(`Error: ${message}`);
    process.exit(0);
};

const printHelp = () => {
    console.log('Call syntax: node setops.js "set1=[filename];set2=[filename];operation=[difference|union|intersection]"');
    process.exit(0);
};

const split = (text, sep) => {
    const i = text.indexOf(sep);
    if (i === -1)
        return [text];
    return [text.slice(0, i), ...split(text.slice(i + 1), sep)];
};

const replace = (text, old, _new) => {
    const i = text.indexOf(old);
    if (i === -1)
        return text;
    return text.slice(0, i) + _new + replace(text.slice(i + old.length), old, _new);
};

const combine = (x) => x.reduce((a, b) => a + b, '');

const stripSpaces = (x) => replace(x, ' ', '');

const isLetter = (x) => (x >= 'a' && x <= 'z') || (x >= 'A' && x <= 'Z');

const isNumber = (x) => x >= '0' && x <= '9';

const isAlphaNumeric = (x) => isLetter(x) || isNumber(x);

// ... (rest of the Python utils functions remain the same)

// ------------------------------------- COMMAND PARSER ---------------------------------------------

const validateValues = (assertions) => {
    const failedAssertion = assertions.find(([value, predicate]) => !predicate(value));
    if (failedAssertion) {
        console.log(failedAssertion);
        printError(failedAssertion[2](failedAssertion[0]));
    }
    return assertions.map(([value]) => value);
};

const generateAssertions = (keys, values) => {
    return validKwargs.map(([key, validator, errorMessage]) => [values[keys.indexOf(key)], validator, errorMessage]);
};

const filterKwargs = (kwargs) => {
    return kwargs.filter(([key]) => validKeys.includes(key));
};

const parseKwargs = (text) => {
    return text.split(';').map((x) => x.split('='));
};

const parseCommand = (args) => {
    if (args.length === 0) printError("not enough arguments");
    if (args.length >= 2) printError("too many arguments");
    const kwargs = parseKwargs(stripSpaces(args[0]));
    const [keys, values] = [filterKwargs(kwargs).map(([key]) => key), filterKwargs(kwargs).map(([_, value]) => value)];
    const missingKey = validKeys.find((key) => !keys.includes(key));
    if (missingKey) printError(`missing key '${missingKey}'`);
    const valueAssertions = generateAssertions(keys, values);
    return validateValues(valueAssertions);
};

// ------------------------------------------ File Parser -------------------------------------------

const listToSet = (x) => {
    if (x.length <= 1)      return x;
    else if (x[0] !== x[1]) return [x[0], ...listToSet(x.slice(1))];
    else                    return listToSet(x.slice(1));
};

const mergeSort = (x) => {
    const merge = (l, r) => {
        if (!r.length)        return l;
        else if (!l.length)   return r;
        else if (l[0] < r[0]) return [l[0], ...merge(l.slice(1), r)];
        else                  return [r[0], ...merge(l, r.slice(1))];
    };

    if (x.length <= 1) return x;
    const m = Math.floor(x.length / 2);
    return merge(mergeSort(x.slice(0, m)), mergeSort(x.slice(m)));
};

const wordLengthLetters = (text, length = 0) => {
    if (!text.length) return length;
    const [head, ...tail] = text;
    const wordBroke = !head || (!isLetter(head) && head !== "'");
    return wordBroke ? length : wordLengthLetters(tail, length + 1);
};

const wordLengthNumbers = (text, length = 0, decimalFound = false) => {
    if (!text.length) return length;
    const [head, ...tail] = text;
    const nonNumberCharacter = (!isNumber(head) && head !== ".")
    const secondDecimal      = (head === '.' && decimalFound)
    const unfollowedDecimal  = (head === '.' && (text.length == 1 || !isNumber(text[1])));
    const wordBroke = !head || nonNumberCharacter || secondDecimal || unfollowedDecimal;
    decimalFound = decimalFound || head === ".";
    return wordBroke ? length : wordLengthNumbers(tail, length + 1, decimalFound);
};

const findNextWord = (text) => {
    if (!text.length)
        return ['', ''];
    else if (!isAlphaNumeric(text[0]))
        return findNextWord(text.slice(1));
    else if (isLetter(text[0])) {
        const i = wordLengthLetters(text);
        return [text.slice(0, i), text.slice(i)];
    } else {
        const i = wordLengthNumbers(text);
        return [text.slice(0, i), text.slice(i)];
    }
};

const textToWords = (text) => {
    const [word, remainingText] = findNextWord(text);
    return word ? [word, ...textToWords(remainingText)] : [];
};

const toLowercase = (text) => {
    if (!text.length) return '';
    const [head, ...tail] = text;
    const char = (head >= 'A' && head <= 'Z') ? String.fromCharCode(head.charCodeAt(0) + 32) : head;
    return char + toLowercase(tail);
};

const getFileText = (filename) => {
    const text = fs.readFileSync(filename, 'utf8');
    return text;  // Combining lines into a single string
};

const writeToFile = (wordset) => {
    const outputFilenames = fs.readdirSync('./').filter((f) => f.startsWith('output') && f.endsWith('.txt'));
    const outputNumbers = outputFilenames.map((f) => parseInt(f.substring(6, f.length - 4), 10));
    const nextNumber = outputNumbers.length === 0 ? 1 : Math.max(...outputNumbers) + 1;

    const text = wordset.map((word) => word + '\n').join('');
    const outputFilename = `output${nextNumber}.txt`;

    fs.writeFileSync(outputFilename, text.substring(0, text.length - 1));
};
// ----------------------------------------- Set Operations -----------------------------------------

// Union set operation
const union = (set1, set2) => {
    const compare = (set1, set2) => {
        const [[x, ...set1Others], [y, ...set2Others]] = [set1, set2];
        if      (x < y) return [x, ...union(set1Others, set2)];
        else if (x > y) return [y, ...union(set1, set2Others)];
        else            return union(set1Others, set2);
    };
    return (!set2.length) ? set1 : (!set1.length) ? set2 : compare(set1, set2);
};

// Difference set operation
const difference = (set1, set2) => {
    const compare = (set1, set2) => {
        const [[x, ...set1Others], [y, ...set2Others]] = [set1, set2];
        if      (x < y) return [x, ...difference(set1Others, set2)];
        else if (x > y) return difference(set1, set2Others);
        else            return difference(set1Others, set2Others);
    };
    return (!set1.length || !set2.length) ? set1 : compare(set1, set2);
};

// Intersection set operation
const intersect = (set1, set2) => {
    const compare = (set1, set2) => {
        const [[x, ...set1Others], [y, ...set2Others]] = [set1, set2];
        if      (x < y) return intersect(set1Others, set2);
        else if (x > y) return intersect(set1, set2Others);
        else            return [x, ...intersect(set1Others, set2Others)];
    };
    return (!set1.length || !set2.length) ? [] : compare(set1, set2);
};

const performOperation = (set1, set2, operation) => {
    if (operation === 'union') return union(set1, set2);
    else if (operation === 'difference') return difference(set1, set2);
    else if (operation === 'intersection') return intersect(set1, set2);
};

// --------------------------------------------------------------------------------------------------

if (require.main === module) {
    const [filename1, filename2, operation] = parseCommand(process.argv.slice(2));
    const words1 = textToWords(toLowercase(getFileText(filename1)));
    const words2 = textToWords(toLowercase(getFileText(filename2)));
    const set1 = listToSet(mergeSort(words1));
    const set2 = listToSet(mergeSort(words2));
    const wordset = performOperation(set1, set2, operation);
    writeToFile(wordset);
}
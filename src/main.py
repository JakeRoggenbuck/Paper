from optparse import OptionParser

import error
from tokenizer import Tokenizer
from parser import Parser
from utils import RunType


def option_parse():
    parser = OptionParser()
    parser.add_option(
        "-m",
        "--mode",
        dest="mode",
        default=False,
        help="The mode of running",
    )
    options, args = parser.parse_args()
    if len(args) == 0:
        error.PaperArgumentError()
    filename = args[0]
    mode = RunType(int(options.mode)) if options.mode else RunType.NORMAL
    return filename, mode


if __name__ == "__main__":
    filename, mode = option_parse()
    tokenizer = Tokenizer(filename)
    tokenizer.tokenize()

    parser = Parser(tokenizer.tokens, tokenizer.items, mode=mode)
    parser.parse()

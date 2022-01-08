import argparse
from nhentai.request_process import RequestProcess

def gather_identities(filename):
    out = list()
    with open(filename, 'r') as f:
        while True:
            readline = f.readline()
            if len(readline) == 0:
                break
            out.append(int(readline.strip()))
    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--identity', metavar='<int>',
                        action='append',
                        help='The nhentai comic identity.', type=int)
    parser.add_argument('-f', '--file', metavar='<string>',
                        help='Input the identity file.', type=str)
    parser.add_argument('-d', '--dir', metavar='<string>',
                        help='The storing directory.', type=str)
    parser.add_argument('--translate',
                        help='Translate the identity to title.', action='store_true', default=False)
    args = parser.parse_args()

    identities = args.identity

    if args.file != None:
        identities.extend(gather_identities(args.file))

    p = RequestProcess(identities=identities, root_directory=args.dir, translate=args.translate)


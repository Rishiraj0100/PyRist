import argparse

from ristpy import rist, execute, E, W, encrypt, decrypt

def compile_to(parser, to_read, to_write):
    if not to_read.endswith(".rist"):
        return parser.error("You must provide the file which is to be to compiled, with extension '.rist'")
    if not to_write.endswith(".py"):
        return parser.error("You must provide file which will be written with extension '.py'")
    try:
        rist(to_read, flags=W, compile_to=to_write)
    except OSError as exc:
        parser.error(f'could not create file ({exc})')
    else:
        print('successfully compiled code at', to_write)

def compile_and_run(parser, fp: str):
    if not fp.endswith(".rist"):
        return parser.error("You must provide file with extension '.rist'")
    rist(fp,flags=E)

def compile_fp(parser, args):
    if args.file and args.compile_to and args.eval:
        compile_to(parser, args.file, args.compile_to)
        compile_and_run(parser, args.file)
    elif args.file and args.compile_to:
        compile_to(parser, args.file, args.compile_to)
    elif args.eval:
        parser.error('Eval argument should only be used when --compile-to is used')
    elif args.file:
        compile_and_run(parser,args.file)

def enc(parser, args):
  try:
    arg,depth,key = args.arg,1,True
    if args.filepath: arg = open(args.arg).read()
    if args.depth: depth=args.depth
    if args.key: key = False
    code = encrypt(arg,args.key,depth=depth)
    if key: code,key=code
    if args.output:
      with open(args.output,"w") as f: f.write(code)
    else: print("Encryption success\n\n",code)
    if key: print("\n\n Your encryption key is:",str(key),"\nPlz don't forget it, it is used to decrypt encrypted thing")
  except Exception as e:
    parser.error(e.__class__.__name__+": "+str(e))

def dec(parser, args):
  try:
    arg,depth,key = args.arg,1,args.key
    if not key: return parser.error("You must provide a 'key' for decryption")
    if args.filepath: arg = open(args.arg).read()
    if args.depth: depth=args.depth
    code = decrypt(arg,args.key,depth=depth)
    if key: code,key=code
    if args.output:
      with open(args.output,"w") as f: f.write(code)
    else: print("Decryption success\n\n",code)
  except Exception as e:
    parser.error(e.__class__.__name__+": "+str(e))

def parse_args():
    _parser_ = argparse.ArgumentParser(prog='rist', description='Rist Lang')
    _parser_.set_defaults(func=(lambda p,a: None))
    _parser = _parser_.add_subparsers(dest="subcommands",title="subcommands")

    parser = _parser.add_parser("lang",help="Rist language command")

    parser.set_defaults(func=compile_fp)
    parser.add_argument('file', type=str, help='compiles rist lang to python and executes it.')
    parser.add_argument('--compile-to', '-CT', help='only compile code and place it to provided file', type=str, metavar="<filepath>")
    parser.add_argument('--eval', '-E', help='Also run the code, used when --compile-to is used', action='store_true')

    subp_e = _parser.add_parser("encrypt", help="Encrypt any thing")

    subp_e.set_defaults(func=enc)
    subp_e.add_argument("arg", help="The argument/file to encrypt", metavar="<argument>")
    subp_e.add_argument("--key","-K", help="The key to encrypt (must be integer, default: random generated)", type=int)
    subp_e.add_argument("--depth","-D",help="The depth/layer for encryption (must be integer, default: 1)", type=int, default=1)
    subp_e.add_argument("--filepath","-FP",help="Provide when the argument is a filepath",action='store_true')
    subp_e.add_argument("--output","-O",help="The output file where the encrypted thing will be written, will print if not given",type=str, default=None)

    subp_d = _parser.add_parser("decrypt", help="Decrypt any thing")

    subp_d.set_defaults(func=dec)
    subp_d.add_argument("arg", help="The argument/file to decrypt", metavar="<argument>")
    subp_d.add_argument("--key","-K", help="The key to decrypt (must be integer,)", type=int, metavar="<key>")
    subp_d.add_argument("--depth","-D",help="The depth/layer for encryption to decode (must be integer, default: 1)", type=int, default=1)
    subp_d.add_argument("--filepath","-FP",help="Provide when the argument is a filepath",action='store_true')
    subp_d.add_argument("--output","-O",help="The output file where the decrypted thing will be written, will print if not given",type=str, default=None)

    return _parser_, _parser_.parse_args()

def main():
    parser, args = parse_args()
    args.func(parser, args)

if __name__ == "__main__":
    main()

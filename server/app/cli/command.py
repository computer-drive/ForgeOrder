from .fix import fix

def execute_command(args):
    
    if args.fix or args.fix_exit:
        fix(exit=args.fix_exit)

        
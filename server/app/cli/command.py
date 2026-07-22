


def execute_command(args):


    if args.fix:
        from .fix import fix
        fix()

    if args.reset_root:
        from app.init import init_root_user
        init_root_user(reset=True)
    

    return args.exit

        
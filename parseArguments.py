#-------------------------------------------------------------------------------
# Name:        parseArguments.py
#-------------------------------------------------------------------------------
import argparse
import getpass

class PasswordPromptAction(argparse.Action):
    def __init__(self,
             option_strings,
             dest=None,
             nargs=0,
             default=None,
             required=False,
             type=None,
             metavar=None,
             help=None):
        super(PasswordPromptAction, self).__init__(
             option_strings=option_strings,
             dest=dest,
             nargs=nargs,
             default=default,
             required=required,
             metavar=metavar,
             type=type,
             help=help)

    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)


parser = argparse.ArgumentParser(description="Some description")
parser.add_argument('-vc', dest='vcenter', type=str, default="vCenterName")
parser.add_argument('-u', dest='username', type=str, default="admin")
parser.add_argument('-p', dest='password', action=PasswordPromptAction, type=str,default="MyDefPass")

parser.add_argument('-file', dest='file', type=str,default="values.csv")




##parser.add_argument('-u', dest='username', type=str, default="admin", required=True)
##parser.add_argument('-p', dest='password', action=PasswordPromptAction, type=str,default="MyDefPass", required=True)

# parser.add_argument('-sp', '--secure_password', action='store_true', dest='password', help='hidden password prompt')


args = parser.parse_args()

##print(args)
##
##print(args.vcenter)
##print(args.username)
##print(args.password)
##print(args.file)
##


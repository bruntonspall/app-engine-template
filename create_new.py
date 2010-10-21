#!/usr/bin/env python

import os, sys
def replace(repl, text):
    text = text.replace('/gitignore', '/.gitignore')
    for key, value in repl.iteritems():
        text = text.replace('$$$$%s$$$$' % (key,), value)
    return text
 
BLACKLIST = (
    '/.git/',
)

def main(repl, dest, templ_dir):
    try:
        os.makedirs(dest)
    except OSError:
        pass

    for root, dirs, files in os.walk(templ_dir):
        for filename in files:
            source_fn = os.path.join(root, filename)
            dest_fn = replace(repl, os.path.join(dest, root.replace(templ_dir, ''), replace(repl, filename)))
            try:
                os.makedirs(os.path.dirname(dest_fn))
            except OSError:
                pass
            print 'Copying %s to %s' % (source_fn, dest_fn)
            should_replace = True
            for bl_item in BLACKLIST:
                if bl_item in dest_fn:
                    should_replace = False
            data = open(source_fn, 'r').read()
            if should_replace:
                data = replace(repl, data)
            open(dest_fn, 'w').write(data)
            os.chmod(dest_fn, os.stat(source_fn)[0])


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-n", "--name", dest="app_name", help="The name of the application.")
    parser.add_option("-d", "--dest", dest="destination", help="Where to put the new application.")
    parser.add_option("-t", "--template", dest="template", help="The application template to use as a basis for the new application.")
    (options, args) = parser.parse_args()

    repl = {
        'APP_NAME':None,
    }
    dest_dir = None
    templ_dir = None

    cur_user = os.getlogin()

    if options.app_name:
        repl['APP_NAME'] = options.app_name
    elif len(args) > 0:
        repl['APP_NAME'] = args[0]

    while not repl['APP_NAME']:
        repl['APP_NAME'] = raw_input('Application name: ')

    if options.destination:
        dest_dir = options.destination

    while not dest_dir:
        dest_dir = raw_input('Destination directory [%s] (%s will be added): ' % (os.getcwd(),repl['APP_NAME'])) or os.getcwd()
    dest_dir =  os.path.realpath(os.path.expanduser(dest_dir))
    dest = os.path.join(dest_dir, repl['APP_NAME'])

    if options.template:
        templ_dir = options.template

    default = os.path.abspath(os.path.join(os.path.dirname(__file__), '_template'))
    while not templ_dir:
        templ_dir = raw_input('Application template directory [%s]: ' % default) or default
    templ_dir = os.path.realpath(os.path.expanduser(templ_dir))
    if templ_dir[-1] != '/':
        templ_dir = templ_dir + "/"

    main(repl, dest, templ_dir)
    

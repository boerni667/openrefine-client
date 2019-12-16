#! /usr/bin/env python
"""
Script to provide a command line interface to a Refine server.
"""

# Copyright (c) 2011 Paul Makepeace, Real Programmers. All rights reserved.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import argparse

from google.refine import refine
from google.refine import cli

parser = argparse.ArgumentParser(description=('Script to provide a command '
    'line interface to an OpenRefine server.'),
                                 usage='usage: %(prog)s [--help | OPTIONS]',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="""
Example data:
  --download "https://git.io/fj5hF" --output=duplicates.csv
  --download "https://git.io/fj5ju" --output=duplicates-deletion.json

Basic commands:
  --list # list all projects
  --list -H 127.0.0.1 -P 80 # specify hostname and port
  --create duplicates.csv # create new project from file
  --info "duplicates" # show project metadata
  --apply duplicates-deletion.json "duplicates" # apply rules in file to project
  --export "duplicates" # export project to terminal in tsv format
  --export --output=deduped.xls "duplicates" # export project to file in xls format
  --delete "duplicates" # delete project

Some more examples:
  --info 1234567890123 # specify project by id
  --create example.tsv --encoding=UTF-8
  --create example.xml --recordPath=collection --recordPath=record
  --create example.json --recordPath=_ --recordPath=_
  --create example.xlsx --sheets=0
  --create example.ods --sheets=0

Example for Templating Export:
  Cf. https://github.com/opencultureconsulting/openrefine-client#advanced-templating
""")


ConnectionGroup = parser.add_argument_group('Connection options')

ConnectionGroup.add_argument('-H', '--host', dest='host',
                  metavar='127.0.0.1',
                  help='OpenRefine hostname (default: 127.0.0.1)')
ConnectionGroup.add_argument('-P', '--port', dest='port',
                  metavar='3333',
                  help='OpenRefine port (default: 3333)')

CommandGroup = parser.add_argument_group('Commands')
CommandGroup.add_argument('-c', '--create', dest='create',
                  metavar='[FILE]',
                  help='Create project from file. The filename ending (e.g. .csv) defines the input format (csv,tsv,xml,json,txt,xls,xlsx,ods)')
CommandGroup.add_argument('-l', '--list', dest='list',
                  action='store_true',
                  help='List projects')
CommandGroup.add_argument('--download', dest='download',
                  metavar='[URL]',
                  help='Download file from URL (e.g. example data). Combine with --output to specify a filename.')

PosargGroup = parser.add_argument_group('Commands with argument --project_id [PROJECTID/PROJECTNAME]')
PosargGroup.add_argument('--project_id', dest='project_id',
                  help='specify project by name or id')
PosargGroup.add_argument('-d', '--delete', dest='delete',
                  action='store_true',
                  help='Delete project')
PosargGroup.add_argument('-f', '--apply', dest='apply',
                  metavar='[FILE]',
                  help='Apply JSON rules to OpenRefine project')
PosargGroup.add_argument('-E', '--export', dest='export',
                  action='store_true',
                  help='Export project in tsv format to stdout.')
PosargGroup.add_argument('-o', '--output', dest='output',
                  metavar='[FILE]',
                  help='Export project to file. The filename ending (e.g. .tsv) defines the output format (csv,tsv,xls,xlsx,html)')
PosargGroup.add_argument('--template', dest='template',
                  metavar='[STRING]',
                  help='Export project with templating. Provide (big) text string that you enter in the *row template* textfield in the export/templating menu in the browser app)')
PosargGroup.add_argument('--info', dest='info',
                  action='store_true',
                  help='show project metadata')

GeneralGroup = parser.add_argument_group('General options')
GeneralGroup.add_argument('--format', dest='file_format',
                  help='Override file detection (import: csv,tsv,xml,json,line-based,fixed-width,xls,xlsx,ods; export: csv,tsv,html,xls,xlsx,ods)')


CreateGroup = parser.add_argument_group('Create options')
CreateGroup.add_argument('--columnWidths', dest='columnWidths',
                  action='append',
                  type=int,
                  help='(txt/fixed-width), please provide widths in multiple arguments, e.g. --columnWidths=7 --columnWidths=5')
CreateGroup.add_argument('--encoding', dest='encoding',
                  help='(csv,tsv,txt), please provide short encoding name (e.g. UTF-8)')
CreateGroup.add_argument('--guessCellValueTypes', dest='guessCellValueTypes',
                  metavar='true/false', choices=('true', 'false'),
                  help='(xml,csv,tsv,txt,json, default: false)')
CreateGroup.add_argument('--headerLines', dest='headerLines',
                  type=int,
                  help='(csv,tsv,txt/fixed-width,xls,xlsx,ods), default: 1, default txt/fixed-width: 0')
CreateGroup.add_argument('--ignoreLines', dest='ignoreLines',
                  type=int,
                  help='(csv,tsv,txt,xls,xlsx,ods), default: -1')
CreateGroup.add_argument('--includeFileSources', dest='includeFileSources',
                  metavar='true/false', choices=('true', 'false'),
                  help='(all formats), default: false')
CreateGroup.add_argument('--limit', dest='limit',
                  type=int,
                  help='(all formats), default: -1')
CreateGroup.add_argument('--linesPerRow', dest='linesPerRow',
                  type=int,
                  help='(txt/line-based), default: 1')
CreateGroup.add_argument('--processQuotes', dest='processQuotes',
                  metavar='true/false', choices=('true', 'false'),
                  help='(csv,tsv), default: true')
CreateGroup.add_argument('--projectName', dest='projectName',
                  help='(all formats), default: filename')
CreateGroup.add_argument('--projectTags', dest='projectTags',
                  action='append',
                  help='(all formats), please provide tags in multiple arguments, e.g. --projectTags=beta --projectTags=client1')
CreateGroup.add_argument('--recordPath', dest='recordPath',
                  action='append',
                  help='(xml,json), please provide path in multiple arguments, e.g. /collection/record/ should be entered: --recordPath=collection --recordPath=record, default xml: root element, default json: _ _')
CreateGroup.add_argument('--separator', dest='separator',
                  help='(csv,tsv), default csv: , default tsv: \\t')
CreateGroup.add_argument('--sheets', dest='sheets',
                  action='append',
                  type=int,
                  help='(xls,xlsx,ods), please provide sheets in multiple arguments, e.g. --sheets=0 --sheets=1, default: 0 (first sheet)')
CreateGroup.add_argument('--skipDataLines', dest='skipDataLines',
                  type=int,
                  help='(csv,tsv,txt,xls,xlsx,ods), default: 0, default line-based: -1')
CreateGroup.add_argument('--storeBlankCellsAsNulls', dest='storeBlankCellsAsNulls',
                  metavar='true/false', choices=('true', 'false'),
                  help='(csv,tsv,txt,xls,xlsx,ods), default: true')
CreateGroup.add_argument('--storeBlankRows', dest='storeBlankRows',
                  metavar='true/false', choices=('true', 'false'),
                  help='(csv,tsv,txt,xls,xlsx,ods), default: true')
CreateGroup.add_argument('--storeEmptyStrings', dest='storeEmptyStrings',
                  metavar='true/false', choices=('true', 'false'),
                  help='(xml,json), default: true')
CreateGroup.add_argument('--trimStrings', dest='trimStrings',
                  metavar='true/false', choices=('true', 'false'),
                  help='(xml,json), default: false')

TemplateGroup = parser.add_argument_group('Templating options')
TemplateGroup.add_argument('--mode', dest='mode',
                  metavar='row-based/record-based',
                  choices=('row-based', 'record-based'),
                  help='engine mode (default: row-based)')
TemplateGroup.add_argument('--prefix', dest='prefix',
                  help='text string that you enter in the *prefix* textfield in the browser app')
TemplateGroup.add_argument('--rowSeparator', dest='rowSeparator',
                  help='text string that you enter in the *row separator* textfield in the browser app')
TemplateGroup.add_argument('--suffix', dest='suffix',
                  help='text string that you enter in the *suffix* textfield in the browser app')
TemplateGroup.add_argument('--filterQuery', dest='filterQuery',
                  metavar='REGEX',
                  help='Simple RegEx text filter on filterColumn, e.g. ^12015$'),
TemplateGroup.add_argument('--filterColumn', dest='filterColumn',
                  metavar='COLUMNNAME',
                  help='column name for filterQuery (default: name of first column)')
TemplateGroup.add_argument('--facets', dest='facets',
                  help='facets config in json format (may be extracted with browser dev tools in browser app)')
TemplateGroup.add_argument('--splitToFiles', dest='splitToFiles',
                  metavar='true/false', choices=('true', 'false'),
                  help='will split each row/record into a single file; it specifies a presumably unique character series for splitting; --prefix and --suffix will be applied to all files; filename-prefix can be specified with --output (default: %%Y%%m%%d)')
TemplateGroup.add_argument('--suffixById', dest='suffixById',
                  metavar='true/false', choices=('true', 'false'),
                  help='enhancement option for --splitToFiles; will generate filename-suffix from values in key column')

def main():
    """Command line interface."""

    options=parser.parse_args()
    # set environment
    if options.host:
        refine.REFINE_HOST = options.host
    if options.port:
        refine.REFINE_PORT = options.port

    # get project_id
    if options.project_id and str.isdigit(options.project_id):
        project_id = options.project_id
    elif options.project_id:
        projects = refine.Refine(refine.RefineServer()).list_projects().items()
        idlist = []
        for project_id, project_info in projects:
            if options.project_id == project_info['name']:
                idlist.append(str(project_id))
        if len(idlist) > 1:
            print('Error: Found {idlist} projects with name {name}.\n'
                  'Please specify project by id.'.format(idlist=len(idlist),name=options.project_id))
            for i in idlist:
                print('')
                cli.info(i)
            return
        else:
            try:
                project_id = idlist[0]
            except IndexError:
                print('Error: No project found with name {}.\n'
                      'Try command --list'.format(options.project_id))
                return

    # commands without args
    if options.list:
        cli.ls()
    elif options.download:
        cli.download(options.download, output_file=options.output)
    elif options.create:
        arg_dict = {arg.dest: getattr(options, arg.dest)
                       for arg in CreateGroup._group_actions}
        kwargs = {k: v for k, v in arg_dict.items()
                  if v is not None and v not in ['true', 'false']}
        kwargs.update({k: True for k, v in arg_dict.items()
                       if v == 'true'})
        kwargs.update({k: False for k, v in arg_dict.items()
                       if v == 'false'})
        if options.file_format:
            kwargs.update({'project_format': options.file_format})
        cli.create(options.create, **kwargs)
    # commands with args
    elif options.info:
        cli.info(project_id)
    elif options.delete:
        cli.delete(project_id)
    elif options.apply:
        cli.apply(project_id, options.apply)
    elif options.template:
        arg_dict = {arg.dest: getattr(options, arg.dest)
                       for arg in TemplateGroup._group_actions}
        kwargs = {k: v for k, v in arg_dict.items()
                  if v is not None and v not in ['true', 'false']}
        kwargs.update({k: True for k, v in arg_dict.items()
                       if v == 'true'})
        kwargs.update({k: False for k, v in arg_dict.items()
                       if v == 'false'})
        if options.file_format:
            kwargs.update({'project_format': options.file_format})
    elif options.export or options.output:
        cli.export(project_id, output_file=options.output,
                   export_format=options.file_format)
    else:
        parser.print_help()

if __name__ == "__main__":
    # execute only if run as a script
    main()

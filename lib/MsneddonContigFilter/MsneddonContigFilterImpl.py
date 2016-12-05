# -*- coding: utf-8 -*-
#BEGIN_HEADER
import uuid
from pprint import pprint, pformat
from biokbase.workspace.client import Workspace as workspaceService
#END_HEADER


class MsneddonContigFilter:
    '''
    Module Name:
    MsneddonContigFilter

    Module Description:
    A KBase module: MsneddonContigFilter
This sample module contains one small method - count_contigs.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:msneddon/ContigFilter"
    GIT_COMMIT_HASH = "482a30c5be6cc24f0a98c5f6b25db288851403c5"

    #BEGIN_CLASS_HEADER
    workspaceURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        #END_CONSTRUCTOR
        pass


    def filter_contigs(self, ctx, params):
        """
        Count contigs in a ContigSet
        contigset_id - the ContigSet to count.
        :param params: instance of type "FilterContigsParams" -> structure:
           parameter "workspace" of type "workspace_name" (A string
           representing a workspace name.), parameter "contigset_id" of type
           "contigset_id" (A string representing a ContigSet id.), parameter
           "min_length" of Long
        :returns: instance of type "FilterContigsResults" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "new_contigset_ref" of String, parameter
           "n_initial_contigs" of Long, parameter "n_contigs_removed" of
           Long, parameter "n_contigs_remaining" of Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN filter_contigs
        print('Starting filter contigs method.')

        workspace_name = params['workspace']
        contigset_id = params['contigset_id']
        min_length = int(params['min_length'])

        token = ctx['token']
        ws = workspaceService(self.workspaceURL, token=token)
        contigSet = ws.get_objects([{'ref': workspace_name+'/'+contigset_id}])[0]['data']
        # load the method provenance from the context object
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects']=[workspace_name+'/'+contigset_id]

        print('Got ContigSet data.')

        # save the contigs to a new list
        good_contigs = []
        n_total = 0;
        n_remaining = 0;
        for contig in contigSet['contigs']:
            n_total += 1
            if len(contig['sequence']) >= min_length:
                good_contigs.append(contig)
                n_remaining += 1

        # replace the contigs in the contigSet object in local memory
        contigSet['contigs'] = good_contigs


        print('Filtered ContigSet to '+str(n_remaining)+' contigs out of '+str(n_total))

        # save the new object to the workspace
        obj_info_list = ws.save_objects({
                            'workspace':workspace_name,
                            'objects': [
                                {
                                    'type':'KBaseGenomes.ContigSet',
                                    'data':contigSet,
                                    'name':contigset_id,
                                    'provenance':provenance
                                }
                            ]
                        })
        info = obj_info_list[0]
        # Object Info Contents
        # absolute ref = info[6] + '/' + info[0] + '/' + info[4]
        # 0 - obj_id objid
        # 1 - obj_name name
        # 2 - type_string type
        # 3 - timestamp save_date
        # 4 - int version
        # 5 - username saved_by
        # 6 - ws_id wsid
        # 7 - ws_name workspace
        # 8 - string chsum
        # 9 - int size 
        # 10 - usermeta meta

        print('saved ContigSet: '+pformat(info))

        # Create a report
        report = 'New ContigSet saved to: '+str(info[7]) + '/'+str(info[1])+'/'+str(info[4])+'\n'
        report += 'Number of initial contigs:      '+ str(n_total) + '\n'
        report += 'Number of contigs removed:      '+ str(n_total - n_remaining) + '\n'
        report += 'Number of contigs in final set: '+ str(n_remaining) + '\n'

        reportObj = {
            'objects_created':[{
                    'ref':str(info[6]) + '/'+str(info[0])+'/'+str(info[4]), 
                    'description':'Filtered Contigs'
                }],
            'text_message':report
        }

        # generate a unique name for the Method report
        reportName = 'filter_contigs_report_'+str(hex(uuid.getnode()))
        report_info = ws.save_objects({
                'id':info[6],
                'objects':[
                    {
                        'type':'KBaseReport.Report',
                        'data':reportObj,
                        'name':reportName,
                        'meta':{},
                        'hidden':1, # important!  make sure the report is hidden
                        'provenance':provenance
                    }
                ]
            })[0]

        print('saved Report: '+pformat(report_info))

        returnVal = {
            'report_name': reportName,
            'report_ref': str(report_info[6]) + '/' + str(report_info[0]) + '/' + str(report_info[4]),
            'new_contigset_ref': str(info[6]) + '/'+str(info[0])+'/'+str(info[4]),
            'n_initial_contigs':n_total,
            'n_contigs_removed':n_total-n_remaining,
            'n_contigs_remaining':n_remaining
        }

        print('returning:'+pformat(returnVal))

        #END filter_contigs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method filter_contigs return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]

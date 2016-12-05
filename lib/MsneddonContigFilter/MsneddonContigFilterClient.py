# -*- coding: utf-8 -*-
############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function
# the following is a hack to get the baseclient to import whether we're in a
# package or not. This makes pep8 unhappy hence the annotations.
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport


class MsneddonContigFilter(object):

    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://kbase.us/services/authorization/Sessions/Login'):
        if url is None:
            raise ValueError('A url is required')
        self._service_ver = None
        self._client = _BaseClient(
            url, timeout=timeout, user_id=user_id, password=password,
            token=token, ignore_authrc=ignore_authrc,
            trust_all_ssl_certificates=trust_all_ssl_certificates,
            auth_svc=auth_svc)

    def filter_contigs(self, params, context=None):
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
        return self._client.call_method(
            'MsneddonContigFilter.filter_contigs',
            [params], self._service_ver, context)

    def status(self, context=None):
        return self._client.call_method('MsneddonContigFilter.status',
                                        [], self._service_ver, context)

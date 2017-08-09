from enum import Enum
from six import iteritems

from puppeter.domain.model.withoptions import WithOptions


class PuppetOID(Enum):
    pp_uuid = 1
    pp_instance_id = 2
    pp_image_name = 3
    pp_preshared_key = 4
    pp_cost_center = 5
    pp_product = 6
    pp_project = 7
    pp_application = 8
    pp_service = 9
    pp_employee = 10
    pp_created_by = 11
    pp_environment = 12
    pp_role = 13
    pp_software_version = 14
    pp_department = 15
    pp_cluster = 16
    pp_provisioner = 17
    pp_region = 18
    pp_datacenter = 19
    pp_zone = 20
    pp_network = 21
    pp_securitypolicy = 22
    pp_cloudplatform = 23
    pp_apptier = 24
    pp_hostname = 25


class CsrAttributesConfiguration(WithOptions):

    def __init__(self):
        self.__csr = {}

    def raw_options(self):
        raw = {}
        for (poid, value) in iteritems(self.__csr):
            raw[poid.name] = value
        return raw

    def read_raw_options(self, options):
        self.__csr.clear()

        for (key, val) in iteritems(options):
            try:
                poid = PuppetOID[key]
                self.__csr[poid] = val
            except KeyError:
                raise KeyError('Unknown Puppet OID for CSR: {}', key)

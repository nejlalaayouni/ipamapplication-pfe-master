from django.apps import AppConfig
from django.db.models.signals import post_migrate
from IPAM.db_partition_triggers import create_trig_vlan, update_trig_vlan, delete_trig_vlan, create_trig_sousreseau, delete_trig_sousreseau, scan_trig_sousreseau, attrib_anul_trig_adressseIP, create_trig_tacheanalyse, update_trig_tacheanalyse, delete_trig_tacheanalyse


class IpamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IPAM'

    def ready(self):
        post_migrate.connect(create_trig_tacheanalyse,sender=self)
        post_migrate.connect(update_trig_tacheanalyse,sender=self)
        post_migrate.connect(delete_trig_tacheanalyse,sender=self)
        post_migrate.connect(create_trig_vlan,sender=self)
        post_migrate.connect(update_trig_vlan,sender=self)
        post_migrate.connect(delete_trig_vlan,sender=self)
        post_migrate.connect(create_trig_sousreseau,sender=self)
        post_migrate.connect(delete_trig_sousreseau,sender=self)
        post_migrate.connect(scan_trig_sousreseau,sender=self)
        post_migrate.connect(attrib_anul_trig_adressseIP,sender=self)

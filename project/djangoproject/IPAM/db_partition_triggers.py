from django.db import connection

####tacheanalyse######
def create_trig_tacheanalyse(**kwargs):
    print('creating triggers tacheanalyse for IPAM...')
    trigger_sql = "CREATE TRIGGER trig_apres_insert_tacheanalyse AFTER INSERT ON IPAM_tacheanalyse FOR EACH ROW BEGIN INSERT INTO IPAM_history_tacheanalyse(action, ancien_nom, nouveau_nom, ancien_adresse, nouveau_adresse, date_action) VALUES('Ajouter', ' ' ,NEW.nom, ' ', NEW.sousreseau_id, NOW()); END;"
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('Done creating triggers tacheanalyse.')

def update_trig_tacheanalyse(**kwargs):
    print('updating triggers tacheanalyse for IPAM...')
    trigger_sql = "CREATE TRIGGER trig_avant_update_tacheanalyse BEFORE UPDATE ON IPAM_tacheanalyse FOR EACH ROW BEGIN INSERT INTO IPAM_history_tacheanalyse(action, ancien_nom, nouveau_nom, ancien_adresse, nouveau_adresse, date_action) VALUES('Modifier', OLD.nom, NEW.nom, OLD.sousreseau_id, NEW.sousreseau_id, NOW()); END;"
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('Done updating triggers tacheanalyse.')

def delete_trig_tacheanalyse(**kwargs):
    print('deleting triggers tacheanalyse for IPAM...')
    trigger_sql = "CREATE TRIGGER trig_apres_delete_tacheanalyse AFTER DELETE ON IPAM_tacheanalyse FOR EACH ROW BEGIN INSERT INTO IPAM_history_tacheanalyse(action, ancien_nom, nouveau_nom, ancien_adresse, nouveau_adresse, date_action) VALUES('Supprimer', OLD.nom, ' ', OLD.sousreseau_id, ' ', NOW()); END;"
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('Done deleting triggers tacheanalyse.')

####vlan#####
def create_trig_vlan(**kwargs):
    print('creating triggers vlan for IPAM...')
    trigger_sql = "CREATE TRIGGER trig_apres_insert_vlan AFTER INSERT ON IPAM_vlan FOR EACH ROW BEGIN INSERT INTO IPAM_history_vlan(action, ancien_nom, nouveau_nom, ancien_idvlan, nouveau_idvlan, date_action) VALUES('Ajouter', ' ' ,NEW.nom, ' ', NEW.idvlan, NOW()); END;"
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('Done creating triggers vlan.')

def update_trig_vlan(**kwargs):
    print('updating triggers vlan for IPAM...')
    trigger_sql = "CREATE TRIGGER trig_avant_update_vlan BEFORE UPDATE ON IPAM_vlan FOR EACH ROW BEGIN INSERT INTO IPAM_history_vlan(action, ancien_nom, nouveau_nom, ancien_idvlan, nouveau_idvlan, date_action) VALUES('Modifier', OLD.nom, NEW.nom, OLD.idvlan, NEW.idvlan, NOW()); END;"
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('Done updating triggers vlan.')

def delete_trig_vlan(**kwargs):
    print('deleting triggers vlan for IPAM...')
    trigger_sql = "CREATE TRIGGER trig_apres_delete_vlan AFTER DELETE ON IPAM_vlan FOR EACH ROW BEGIN INSERT INTO IPAM_history_vlan(action, ancien_nom, nouveau_nom, ancien_idvlan, nouveau_idvlan, date_action) VALUES('Supprimer', OLD.nom, ' ', OLD.idvlan, ' ', NOW()); END;"
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('Done deleting triggers vlan.')

####sous-reseau######
def create_trig_sousreseau(**kwargs):
    print('creating triggers sousreseau for IPAM...')
    trigger_sql = "CREATE TRIGGER trig_apres_insert_sousreseau AFTER INSERT ON IPAM_sousreseau FOR EACH ROW BEGIN INSERT INTO IPAM_history_sousreseau(action, nouveau_nom, ancien_nom, nouveau_adresse, ancien_adresse, date_scan, date_action) VALUES('Ajouter', NEW.nom, ' ', NEW.adresse, ' ', ' ', NOW()); END;"
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('Done creating triggers sousreseau.')

def delete_trig_sousreseau(**kwargs):
    print('deleting triggers sousreseau for IPAM...')
    trigger_sql = "CREATE TRIGGER trig_apres_delete_sousreseau AFTER DELETE ON IPAM_sousreseau FOR EACH ROW BEGIN INSERT INTO IPAM_history_sousreseau(action, nouveau_nom, ancien_nom, nouveau_adresse, ancien_adresse, date_scan, date_action) VALUES('Supprimer', ' ', OLD.nom, ' ', OLD.adresse, ' ', NOW()); END;"
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('Done deleting triggers sousreseau.')

def scan_trig_sousreseau(**kwargs):
    print('scanning triggers sousreseau for IPAM...')
    trigger_sql = "CREATE TRIGGER trig_apres_scan_sousreseau BEFORE UPDATE ON IPAM_sousreseau FOR EACH ROW BEGIN INSERT INTO IPAM_history_sousreseau(action, nouveau_nom, ancien_nom, nouveau_adresse, ancien_adresse, date_scan, date_action) VALUES('Scanner', ' ', OLD.nom, ' ', OLD.adresse, NOW(), NOW()); END;"
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('Done scanning triggers sousreseau.')

####adressseIP#####
def attrib_anul_trig_adressseIP(**kwargs):
    print('assign triggers adresseip for IPAM...')
    trigger_sql = "CREATE TRIGGER trig_avant_assign_adresseip BEFORE UPDATE ON IPAM_adresseip FOR EACH ROW BEGIN INSERT INTO IPAM_history_adresseip(nouveau_nom, nouveau_adresse, etat, date_action) VALUES(NEW.nom, NEW.adresse, New.etat, NOW()); END;"
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('Done assign triggers adresseip.')


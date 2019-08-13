'''
   Spécification du schéma toml des paramètres de configurations
   Fichier spécifiant les types des paramètres et leurs valeurs par défaut
   Fichier à ne pas modifier. Paramètres surcouchables dans config/config_gn_module.tml
'''

from marshmallow import Schema, fields


class GnModuleSchemaConf(Schema):
   AREA_TYPE = fields.List(fields.String(), missing=['COM', 'M1', 'M5', 'M10'])
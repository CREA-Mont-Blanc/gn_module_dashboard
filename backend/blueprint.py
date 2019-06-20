import json
from flask import Blueprint, current_app, session, request
from sqlalchemy.sql import func
from geojson import FeatureCollection, Feature

from sqlalchemy.sql.expression import label, distinct, case

from geonature.utils.utilssqlalchemy import json_resp
from geonature.utils.env import DB

from .models import VSynthese, VTaxonomie, VFrameworks
from geonature.core.gn_synthese.models import Synthese, CorAreaSynthese
from geonature.core.ref_geo.models import LAreas, BibAreasTypes
from geonature.core.taxonomie.models import Taxref

# # import des fonctions utiles depuis le sous-module d'authentification
# from geonature.core.gn_permissions import decorators as permissions
# from geonature.core.gn_permissions.tools import get_or_fetch_user_cruved

blueprint = Blueprint("dashboard", __name__)

# vm_synthese
@blueprint.route("/synthese", methods=["GET"])
@json_resp
def get_synthese_stat():
    params = request.args
    q = DB.session.query(
        label("year", func.date_part("year", VSynthese.date_min)),
        func.count(VSynthese.id_synthese),
        func.count(distinct(VSynthese.cd_ref)),
    ).group_by("year")
    if ("selectedRegne" in params) and (params["selectedRegne"] != ""):
        q = q.filter(VSynthese.regne == params["selectedRegne"])
    if ("selectedPhylum" in params) and (params["selectedPhylum"] != ""):
        q = q.filter(VSynthese.phylum == params["selectedPhylum"])
    if "selectedClasse" in params and (params["selectedClasse"] != ""):
        q = q.filter(VSynthese.classe == params["selectedClasse"])
    if "selectedOrdre" in params and (params["selectedOrdre"] != ""):
        q = q.filter(VSynthese.ordre == params["selectedOrdre"])
    if "selectedFamille" in params and (params["selectedFamille"] != ""):
        q = q.filter(VSynthese.famille == params["selectedFamille"])
    if ("selectedGroup2INPN" in params) and (params["selectedGroup2INPN"] != ""):
        q = q.filter(VSynthese.group2_inpn == params["selectedGroup2INPN"])
    if ("selectedGroup1INPN" in params) and (params["selectedGroup1INPN"] != ""):
        q = q.filter(VSynthese.group1_inpn == params["selectedGroup1INPN"])
    if ("taxon" in params) and (params["taxon"] != ""):
        q = q.filter(VSynthese.cd_ref == params["taxon"])
    return q.all()

    # Si on veut afficher tous les champs de la vue
    # data = DB.session.query(VSynthese).limit(10).all()

    # tab = []
    # for d in data:
    #     temp_dict = d.as_dict()
    #     print(temp_dict)
    #     tab.append(temp_dict)
    # return tab

    # return [d.as_dict() for d in data]


# vm_synthese_communes
@blueprint.route("/communes", methods=["GET"])
@json_resp
def get_communes_stat():
    params = request.args
    q = (
        DB.session.query(
            func.count(Synthese.id_synthese),
            LAreas.area_name,
            func.st_asgeojson(func.st_transform(LAreas.geom, 4326)),
            func.count(distinct(Taxref.cd_ref)),
        )
        .join(CorAreaSynthese, CorAreaSynthese.id_synthese == Synthese.id_synthese)
        .join(LAreas, LAreas.id_area == CorAreaSynthese.id_area)
        .join(Taxref, Taxref.cd_nom == Synthese.cd_nom)
        .join(BibAreasTypes, BibAreasTypes.id_type == LAreas.id_type)
        .group_by(LAreas.area_name, LAreas.geom)
        .filter(BibAreasTypes.type_code == "COM")
    )
    if "selectedYearRange" in params:
        q = q.filter(
            func.date_part("year", Synthese.date_min)
            <= params["selectedYearRange"][5:9]
        )
        q = q.filter(
            func.date_part("year", Synthese.date_max)
            >= params["selectedYearRange"][0:4]
        )
    if ("selectedRegne" in params) and (params["selectedRegne"] != ""):
        q = q.filter(Taxref.regne == params["selectedRegne"])
    if ("selectedPhylum" in params) and (params["selectedPhylum"] != ""):
        q = q.filter(Taxref.phylum == params["selectedPhylum"])
    if ("selectedClasse") in params and (params["selectedClasse"] != ""):
        q = q.filter(Taxref.classe == params["selectedClasse"])
    if ("selectedOrdre") in params and (params["selectedOrdre"] != ""):
        q = q.filter(Taxref.ordre == params["selectedOrdre"])
    if ("selectedFamille") in params and (params["selectedFamille"] != ""):
        q = q.filter(Taxref.famille == params["selectedFamille"])
    if ("taxon") in params and (params["taxon"] != ""):
        q = q.filter(Taxref.cd_ref == params["taxon"])
    if ("selectedGroup1INPN") in params and (params["selectedGroup1INPN"] != ""):
        q = q.filter(Taxref.group1_inpn == params["selectedGroup1INPN"])
    if ("selectedGroup2INPN") in params and (params["selectedGroup2INPN"] != ""):
        q = q.filter(Taxref.group2_inpn == params["selectedGroup2INPN"])
    data = q.all()

    geojson_features = []
    for d in data:
        properties = {"nb_obs": int(d[0]), "nb_taxons": int(d[3]), "area_name": d[1]}
        geojson = json.loads(d[2])
        geojson["properties"] = properties
        geojson_features.append(geojson)
    return FeatureCollection(geojson_features)

    # params = request.args
    # q = DB.session.query(
    #     VSyntheseCommunes.area_name,
    #     VSyntheseCommunes.geom_area_4326,
    #     func.sum(VSyntheseCommunes.nb_obs),
    #     func.sum(VSyntheseCommunes.nb_taxons),
    # ).group_by(VSyntheseCommunes.area_name, VSyntheseCommunes.geom_area_4326)
    # # if ('yearMax' not in params) and ('yearMin' not in params) :
    # #     q = q.filter(VSyntheseCommunes.year == None)
    # if "selectedYearRange" in params:
    #     q = q.filter(VSyntheseCommunes.year <= params["selectedYearRange"][5:9])
    #     q = q.filter(VSyntheseCommunes.year >= params["selectedYearRange"][0:4])
    # # if 'regne' not in params:
    # #     q = q.filter(VSyntheseCommunes.regne == None)
    # if ("selectedRegne" in params) and (params["selectedRegne"] != ""):
    #     q = q.filter(VSyntheseCommunes.regne == params["selectedRegne"])
    # # if 'phylum' not in params:
    # #     q = q.filter(VSyntheseCommunes.phylum == None)
    # if ("selectedPhylum" in params) and (params["selectedPhylum"] != ""):
    #     q = q.filter(VSyntheseCommunes.phylum == params["selectedPhylum"])
    # # if 'classe' not in params:
    # #     q = q.filter(VSyntheseCommunes.classe == None)
    # if ("selectedClasse") in params and (params["selectedClasse"] != ""):
    #     q = q.filter(VSyntheseCommunes.classe == params["selectedClasse"])
    # # if 'ordre' not in params:
    # #     q = q.filter(VSyntheseCommunes.ordre == None)
    # # if 'ordre' in params:
    # #     q = q.filter(VSyntheseCommunes.ordre == params['ordre'])
    # # if 'famille' not in params:
    # #     q = q.filter(VSyntheseCommunes.famille == None)
    # # if 'famille' in params:
    # #     q = q.filter(VSyntheseCommunes.famille == params['famille'])
    # data = q.all()

    # geojson_features = []
    # for d in data:
    #     properties = {"nb_obs": int(d[2]), "nb_taxon": int(d[3]), "area_name": d[0]}
    #     geojson = json.loads(d[1])
    #     geojson["properties"] = properties
    #     geojson_features.append(geojson)
    # return FeatureCollection(geojson_features)


# vm_synthese_communes_inpn
# @blueprint.route("/communes_inpn", methods=["GET"])
# @json_resp
# def get_communes_inpn_stat():
#     params = request.args
#     q = DB.session.query(
#         VSyntheseCommunesINPN.area_name,
#         VSyntheseCommunesINPN.geom_area_4326,
#         func.sum(VSyntheseCommunesINPN.nb_obs),
#         func.sum(VSyntheseCommunesINPN.nb_taxons),
#     ).group_by(VSyntheseCommunesINPN.area_name, VSyntheseCommunesINPN.geom_area_4326)
#     if "selectedYearRange" in params:
#         q = q.filter(VSyntheseCommunesINPN.year <= params["selectedYearRange"][5:9])
#         q = q.filter(VSyntheseCommunesINPN.year >= params["selectedYearRange"][0:4])
#     if ("selectedGroup2INPN" in params) and (params["selectedGroup2INPN"] != ""):
#         q = q.filter(VSyntheseCommunesINPN.group2_inpn == params["selectedGroup2INPN"])
#     if ("selectedGroup1INPN" in params) and (params["selectedGroup1INPN"] != ""):
#         q = q.filter(VSyntheseCommunesINPN.group1_inpn == params["selectedGroup1INPN"])
#         q = q.filter(VSyntheseCommunesINPN.group2_inpn == None)
#     data = q.all()

#     geojson_features = []
#     for d in data:
#         properties = {"nb_obs": int(d[2]), "nb_taxon": int(d[3]), "area_name": d[0]}
#         geojson = json.loads(d[1])
#         geojson["properties"] = properties
#         geojson_features.append(geojson)
#     return FeatureCollection(geojson_features)


# vm_synthese
@blueprint.route("/synthese_per_tax_level", methods=["GET"])
@json_resp
def get_synthese_per_tax_level_stat():
    params = request.args
    if ("selectedFilter" in params) and (params["selectedFilter"] == "Règne"):
        q = DB.session.query(
            func.coalesce(VSynthese.regne, "Not defined"),
            func.count(VSynthese.id_synthese),
        ).group_by(VSynthese.regne)
    if ("selectedFilter" in params) and (params["selectedFilter"] == "Phylum"):
        q = DB.session.query(
            func.coalesce(VSynthese.phylum, "Not defined"),
            func.count(VSynthese.id_synthese),
        ).group_by(VSynthese.phylum)
    if ("selectedFilter" in params) and (params["selectedFilter"] == "Classe"):
        q = DB.session.query(
            func.coalesce(VSynthese.classe, "Not defined"),
            func.count(VSynthese.id_synthese),
        ).group_by(VSynthese.classe)
    if ("selectedFilter" in params) and (params["selectedFilter"] == "Ordre"):
        q = (
            DB.session.query(
                func.coalesce(VSynthese.ordre, "Not defined"),
                func.count(VSynthese.id_synthese),
            )
            .group_by(VSynthese.ordre)
            .order_by(VSynthese.ordre)
        )
    if ("selectedFilter" in params) and (params["selectedFilter"] == "Groupe INPN 1"):
        q = DB.session.query(
            func.coalesce(VSynthese.group1_inpn, "Not defined"),
            func.count(VSynthese.id_synthese),
        ).group_by(VSynthese.group1_inpn)
    if ("selectedFilter" in params) and (params["selectedFilter"] == "Groupe INPN 2"):
        q = DB.session.query(
            func.coalesce(VSynthese.group2_inpn, "Not defined"),
            func.count(VSynthese.id_synthese),
        ).group_by(VSynthese.group2_inpn)
    if "selectedYearRange" in params:
        q = q.filter(
            func.date_part("year", VSynthese.date_min)
            <= params["selectedYearRange"][5:9]
        )
        q = q.filter(
            func.date_part("year", VSynthese.date_max)
            >= params["selectedYearRange"][0:4]
        )
    return q.all()


# vm_synthese_frameworks
@blueprint.route("/frameworks", methods=["GET"])
@json_resp
def get_frameworks_stat():
    params = request.args
    q = DB.session.query(VFrameworks.year, VFrameworks.nb_obs)
    if "frameworkName" in params and (params["frameworkName"] != ""):
        q = q.filter(VFrameworks.acquisition_framework_name == params["frameworkName"])
    return q.all()


# vm_synthese_frameworks
@blueprint.route("/frameworks_name", methods=["GET"])
@json_resp
def get_frameworks_name():
    params = request.args
    q = DB.session.query(distinct(VFrameworks.acquisition_framework_name)).order_by(
        VFrameworks.acquisition_framework_name
    )
    return q.all()


# vm_synthese
@blueprint.route("/years", methods=["GET"])
@json_resp
def get_years():
    params = request.args
    if ("type" in params) and (params["type"] == "distinct"):
        q = DB.session.query(
            label("year", distinct(func.date_part("year", VSynthese.date_min)))
        ).order_by("year")
    if ("type" in params) and (params["type"] == "min-max"):
        q = DB.session.query(
            func.min(func.date_part("year", VSynthese.date_min)),
            func.max(func.date_part("year", VSynthese.date_min)),
        )
    return q.all()


# vm_taxonomie
@blueprint.route("/taxonomie", methods=["GET"])
@json_resp
def get_taxonomie():
    params = request.args
    q = DB.session.query(VTaxonomie.name_taxon).order_by(
        case([(VTaxonomie.name_taxon == "Not defined", 1)], else_=0),
        VTaxonomie.name_taxon,
    )
    if "taxLevel" in params:
        q = q.filter(VTaxonomie.level == params["taxLevel"])
    return q.all()


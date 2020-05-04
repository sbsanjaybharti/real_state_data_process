import os
from flask import request,  jsonify, current_app
from flask_restplus import Resource, Namespace, reqparse
import werkzeug
from .main import db
from .utility.file import files
from api.service.fileService import fileService
from api.service.dataProcessService import dataProcess
from .model.assetModel import assetModel, assetModelUnit as unit
from .model.unitModel import unitModel
import datetime
from sqlalchemy import func, desc, asc
import pandas as pd

api = Namespace('Portfolios', description='Detail of property')

@api.route('/')
class portfolios(Resource):
    @api.doc(params={'page': 'Pagination no. of page'})
    def get(self):
        """Home page"""
        args = request.args
        if 'page' in args and args['page'] is not None:
            page = args['page']
        else:
            page = 1
        asset_list = assetModel.query.order_by('updated_at').paginate(int(page), per_page=current_app.config['DATA_PERPAGE'])

        result = [
            {
                'id': row.id,
                'address': row.address,
                'zipcode': row.zipcode,
                'city': row.city,
                'year_of_construction': row.yoc,
                'restricted_area': row.is_restricted,
                'number_of_units': unit(row).units(),
                'total_rent': unit(row).rent.total(),
                'total_area': unit(row).area.total(),
                'area_rented': unit(row).area.rented(),
                'vacancy': unit(row).area.nonRentedPercent(),
                'walt': unit(row).area.walt(),
                'latest_update': datetime.datetime.strftime(row.updated_at,'%d-%m-%Y')
            } for row in asset_list.items]

        response_object = {
            'code': 200,
            'type': 'Success',
            'message': 'Data found',
            'data': result,
            'paginate': {
                'pages': asset_list.pages,
                'page': asset_list.page,
                'per_page': asset_list.per_page,
                'total': asset_list.total,
                'prev_num': asset_list.prev_num,
                'next_num': asset_list.next_num,
                'has_prev': asset_list.has_prev,
                'has_next': asset_list.has_next
            }
        }
        return jsonify(response_object)

@api.route('/<id>')
class detail(Resource):

    @api.doc(params={'page': 'Pagination no. of page'})
    def get(self, id):
        """Home page"""
        args = request.args
        if 'page' in args and args['page'] is not None:
            page = args['page']
        else:
            page = 1

        asset_detail = assetModel.query.filter_by(id=id).first()

        unit_type_obj = db.session.query('type', func.sum(unitModel.size).label('total_area')).filter(unitModel.asset_id==id).group_by('type')\
            .paginate(int(page), per_page=current_app.config['DATA_PERPAGE'])

        is_rented_obj = db.session.query('is_rented', func.sum(unitModel.size).label('size')).filter(unitModel.asset_id==id).group_by('is_rented')\
            .paginate(int(page), per_page=current_app.config['DATA_PERPAGE'])

        asset_unit = [
                    {
                        'ref': row.ref,
                        'size': row.size,
                        'is_rented': row.is_rented,
                        'rent': row.rent,
                        'type': row.type,
                        'tenant': row.tenant,
                        'lease_start': row.lease_start,
                        'lease_end': row.lease_end,
                        'latest_update': row.lease_start
                    } for row in asset_detail.units]

        unit_type = [
            {
                'total_area': str(row.total_area),
                'type': row.type,
            } for row in unit_type_obj.items]

        rented_area = [
            {
                'size': str(row.size),
                'is_rented': row.is_rented,
            } for row in is_rented_obj.items]

        result = {
                'address': asset_detail.address,
                'zipcode': asset_detail.zipcode,
                'city': asset_detail.city,
                'year_of_construction': asset_detail.yoc,
                'restricted_area': asset_detail.is_restricted,
                'number_of_units': unit(asset_detail).units(),
                'total_rent': unit(asset_detail).rent.total(),
                'rent_fee': unit(asset_detail).rent.fees(),
                'rent_average': unit(asset_detail).rent.average(),
                'total_area': unit(asset_detail).area.total(),
                'area_rented': unit(asset_detail).area.rented(),
                'vacancy': unit(asset_detail).area.nonRentedPercent(),
                'walt': unit(asset_detail).area.walt(),
                'asset_unit': asset_unit,
                'unit_type': unit_type,
                'rented_area': rented_area,
                'latest_update': datetime.datetime.strftime(asset_detail.updated_at,'%d-%m-%Y')
            }



        response_object = {
            'code': 200,
            'type': 'Success',
            'message': 'Data found',
            'summary': result
        }
        return jsonify(response_object)
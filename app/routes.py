from flask import Blueprint, request, jsonify
from .utils import get_elevation_data
from config import config

bp = Blueprint('main', __name__)


@bp.route('/elevation', methods=['GET'])
def elevation():
    wkt = request.args.get('wkt')
    if not wkt:
        return jsonify({'error': 'wkt parameter is required'}), 400

    try:
        elevation_wkt = get_elevation_data(wkt, config.API_ELEVATION_TIF_PATH)
        return jsonify({'wkt': elevation_wkt})
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # TODO maybe not safe

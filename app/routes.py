import os

from flask import Blueprint, request, jsonify, send_file
from .utils import get_elevation_data
from config import config

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def index():
    print(config.APP_DIR)
    print(config.STATIC_DIR)
    print(os.path.join(config.STATIC_DIR, 'index.html'))
    return send_file(os.path.join(config.STATIC_DIR, 'index.html'))


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

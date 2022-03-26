from flask import Blueprint, request, jsonify, make_response
from . import Users, Roles, FarmingChains, Stages, Members, MembersByStage, app
from .auth import token_required

fc_app = Blueprint('fc', __name__)

@fc_app.route('/farmchains/create', methods=['POST'])
@token_required
def create_farm_chain(current_user):
    data = request.get_json()
    fc = FarmingChains.query.filter_by(name=data["name"]).first()
    if fc:
        return make_response(jsonify({"message": f'Farm chain "{data["name"]}" already exists'}), 400)
    FarmingChains(name=data["name"]).save()
    return jsonify({'message': 'Registered successfully'})

@fc_app.route('/farmchains/delete', methods=['DELETE'])
@token_required
def delete_farm_chain(current_user):
    data = request.get_json()
    try:
        FarmingChains.query.filter_by(name=data["name"]).first().delete()
    except:
        return make_response(jsonify({"message": "Error while deleting farm chain"}), 401)
    return jsonify({'message': f'Farm chain "{data["name"]}" deleted successfully'})

@fc_app.route('/farmchains', methods=['GET'])
@token_required
def get_fcs(current_user):
    return jsonify({'farm_chains': [fc.serialize() for fc in FarmingChains.query.all()]})

@fc_app.route('/stages/create', methods=['POST'])
@token_required
def create_stage(current_user):
    data = request.get_json()
    fc = FarmingChains.query.filter_by(name=data["farm_chain_name"]).first()
    stage = Stages.query.filter_by(name=data["name"]).first()
    if not fc:
        return make_response(jsonify({"message": f'Farm chain "{data["name"]}" does not exist'}), 400)
    if stage and stage.idFarmingChain == fc.id:
        return make_response(jsonify({"message": f'Stage "{data["name"]}" already associated to this farm chain'}), 400)
    Stages(name=data["name"], idFarmingChain=fc.id).save()
    return jsonify({'message': 'Stage registered successfully'})

@fc_app.route('/stages', methods=['GET'])
@token_required
def get_stages(current_user):
    data = request.args.get('farm_chain_name')
    fc = FarmingChains.query.filter_by(name=data).first()
    if not fc:
        return make_response(jsonify({"message": f'Farm chain "{data}" does not exist'}), 400)
    fc_stages = Stages.query.filter_by(idFarmingChain=fc.id).all()
    return jsonify({'stages': [s.serialize() for s in fc_stages]})

@fc_app.route('/stages/delete', methods=['DELETE'])
@token_required
def delete_stage(current_user):
    data = request.get_json()
    try:
        Stages.query.filter_by(id=data["id"]).first().delete()
    except:
        return make_response(jsonify({"message": "Error while deleting stage"}), 401)
    return jsonify({'message': f'Stage deleted successfully'})
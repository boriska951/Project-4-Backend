import models
from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required

posts = Blueprint('posts', 'posts')

@posts.route('/', methods=['GET'])
def posts_index():
    result = models.Post.select()
    print(result)
        
    post_dicts = [model_to_dict(post) for post in result]
    
    for post_dict in post_dicts:
        post_dict['user'].pop('password')
        
        
    return jsonify({
        'data': post_dicts,
        'message': f"Successfully found {len(post_dicts)} posts",
        'status':200
    }), 200
    
@posts.route('/my_posts', methods=['GET'])
@login_required
def my_posts_index():
    result = models.Post.select()
    print(current_user)
    
    current_user_post_dicts = [model_to_dict(post) for post in current_user.posts]
    
    for post_dict in current_user_post_dicts:
        post_dict['user'].pop('password')
        
        
    return jsonify({
        'data': current_user_post_dicts,
        'message': f"Successfully found {len(current_user_post_dicts)} posts",
        'status':200
    }), 200

@posts.route('/', methods=['POST'])
@login_required
def create_post():
    payload = request.get_json()
    print(payload)
    new_post = models.Post.create(text=payload["text"], user=current_user.id)
    
    post_dict = model_to_dict(new_post)
    
    post_dict['user'].pop('password')
    
    return jsonify(
        data=post_dict,
        message='New post created.',
        status=201
    ),201
    
@posts.route('/<id>', methods=['GET'])
def get_one_posts(id):
    post = model_to_dict(models.Post.get_by_id(id))
    
    return jsonify(
        data = model_to_dict(post),
        message = "Success",
        status = 200
    ), 200
    
@posts.route('/<id>', methods=['PUT'])
@login_required
def update_post(id):
    payload = request.get_json()
    
    post = models.Post.get_by_id(id)
    
    models.Post.update(text=payload["text"], user=current_user.id).where(models.Post.id == id).execute()
    

    return jsonify(
        data=model_to_dict(post),
        message='Post was updated',
        status=200,
    ),200
    
@posts.route('/<id>', methods=['DELETE'])
@login_required
def delete_post(id):
    delete_query = models.Post.delete().where(models.Post.id == id)
    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)
    
    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} with id {id}.",
        status=200,
    ), 200 
"""
博客资源
"""
import re
from datetime import datetime
from flask import request, g
from flask_restful import Resource
from . import restful_api
from .. import multi_auth, token_auth
from app.exts import db
from app.models.blog import Blog


class BlogResource(Resource):
    # decorators = [multi_auth.login_required]

    def get(self):
        blog_id = request.args.get('blog_id')
        blog = Blog.query.filter_by(id=blog_id).first()
        blog_json = {
                          'id': blog.id,
                          'title': blog.title,
                          'content': blog.content,
                          'summary': blog.summary,
                          'cover': blog.cover,
                          'reads_count': blog.reads_count,
                          'comments_count': blog.comments_count,
                          'updated': blog.updated.strftime('%Y-%m-%d %H:%M:%S')
                      }
        return {
            "blog":blog_json
        }

    @token_auth.login_required
    def post(self):
        post_args = request.get_json()
        raw_content = post_args.get('content')

        title_index = raw_content.find('\n')
        if title_index == -1:
            title = '无标题'
        else:
            raw_title = raw_content[:title_index]
            title = re.sub(r'\#*', '', raw_title)

        cover_catch = re.findall(r'\!\[cover\]\(.*\)', raw_content)
        if len(cover_catch) == 0:
            cover = ""
        else:
            cover = cover_catch[0][9:-1]

        new_blog = Blog(
            user_id=g.auth_user.id,
            title=title,
            content=raw_content,
            cover=cover,
            updated=datetime.utcnow()
        )
        db.session.add(new_blog)
        db.session.commit()

        return {

        }

    @token_auth.login_required
    def put(self):
        post_args = request.get_json()
        blog_id = post_args.get('blog_id')
        raw_content = post_args.get('content')

        title_index = raw_content.find('\n')
        if title_index == -1:
            title = '无标题'
        else:
            raw_title = raw_content[:title_index]
            title = re.sub(r'\#*', '', raw_title)

        cover_catch = re.findall(r'\!\[cover\]\(.*\)', raw_content)
        if len(cover_catch) == 0:
            cover = ""
        else:
            cover = cover_catch[0][9:-1]

        update_blog = Blog.query.filter_by(id=blog_id).update(dict(
            title=title,
            content=raw_content,
            cover=cover,
            updated=datetime.utcnow()
        ))
        db.session.commit()

        return {

        }

    @token_auth.login_required
    def delete(self):
        blog_id = request.args.get('blog_id')
        blog = Blog.query.filter_by(id=blog_id).first()
        db.session.delete(blog)
        db.session.commit()
        return {}


restful_api.add_resource(BlogResource, '/blog')

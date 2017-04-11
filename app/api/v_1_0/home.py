"""
博客资源
"""
import re
from datetime import datetime
from flask import request, g
from flask_restful import Resource
from sqlalchemy import desc

from . import restful_api
from .. import multi_auth
from app.exts import db
from app.models.blog import Blog


class HomeResource(Resource):
    # decorators = [multi_auth.login_required]

    def get(self):
        blogs = Blog.query.order_by(desc(Blog.updated)).limit(3).all()

        blogs_json = [{
                          'id': blog.id,
                          'title': blog.title,
                          'content': blog.content,
                          'summary': blog.summary,
                          'cover': blog.cover,
                          'reads_count': blog.reads_count,
                          'comments_count': blog.comments_count,
                          'updated': blog.updated.strftime('%Y-%m-%d %H:%M:%S')
                      } for blog in blogs]
        return {
            'blogs': blogs_json
        }



restful_api.add_resource(HomeResource, '/home')

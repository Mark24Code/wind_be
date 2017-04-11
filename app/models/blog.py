from datetime import datetime
from app.exts import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # 作者id
    title = db.Column(db.String(120))  # 标题
    content = db.Column(db.Text)  # 内容
    cover = db.Column(db.String)  # 封面链接
    summary = db.Column(db.String, default="")  # 摘要
    reads_count = db.Column(db.Integer, default=0)  # 阅读次数
    comments_count = db.Column(db.Integer, default=0)  # 评论个数
    status = db.Column(db.Integer, default=0)  # 状态：0 可用，1 删除
    created = db.Column(db.DateTime)  # 更新时间
    updated = db.Column(db.DateTime)  # 创建时间

    def __repr__(self):
        return '<Blog {}>'.format(self.id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created = datetime.utcnow()
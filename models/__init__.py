"""模型层"""
from init import db


class Common(object):
    """orm通用操作"""

    def direct_flush_(self):
        """直接预提交"""
        self.direct_add_()
        self.flush_()
        return self

    def flush_(self):
        """预提交，等于提交到数据库内存，还未写入数据库文件"""
        db.session.flush()
        return self

    def direct_add_(self):
        """直接添加事务"""
        db.session.add(self)
        return self

    def direct_commit_(self):
        """直接提交"""
        self.direct_add_()
        db.session.commit()
        return self

    def direct_update_(self):
        """直接更新"""
        db.session.commit()
        return self

    def direct_delete_(self):
        """直接删除"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def static_commit_():
        """直接提交.目的是尽量少直接引入db对象,集成在模型内"""
        db.session.commit()

    def to_dict_(self) -> dict:
        """返回字典表数据"""
        result = dict()
        for column in self.__table__._columns:
            result[column.name] = getattr(self, column.name)
        return result

    def __str__(self):
        return f'<class \'{self.__class__.__name__}\' id={self.id if self.id else None}>'

    def __repr__(self):
        """想要此特殊方法被模型继承,需要将Common继承顺序排在ORM基类之前"""
        description = ', '.join([f'{column.name}={getattr(self, column.name)}' for column in self.__table__._columns])
        return f'<{description}>'

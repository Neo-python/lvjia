"""全局通用插件库"""
import datetime
from flask import render_template


def page_generator(current_page_num: int, max_num: int, url: str, url_args: dict = None, style: str = 'action'):
    """分页生成器
    :param current_page_num: 当前页,页数
    :param max_num: 最大页数
    :param url: 分页地址,带问号.例:www.python.org/?
    :param url_args: 地址参数
    :param style:选中页样式.
    :return: 渲染后的分页html内容.
    """
    if not url_args:
        url_args = {}
    args = ''
    for k, v in url_args.items():
        args += f'&{k}={v}'
    page_info = {
        'max_num': max_num,
        'url': url,
        'url_args': args,
        'current_page_num': current_page_num,
        'action': style
    }
    return render_template('page.html', data=page_info)


class OrmVerity:

    @staticmethod
    def verify_deadline(deadline: str, fmt: str = '%Y-%m-%d %H:%M'):
        """验证期限"""
        if not deadline:
            return None
        try:
            _deadline = datetime.datetime.strptime(deadline, fmt)
        except Exception as err:
            print(err, '\n', deadline)
            return None
        else:
            return _deadline

    @staticmethod
    def verify_null_value(value, result=None):
        """验证空值,
        出现空值,返回预设结果或result默认值
        :param value: 验证值
        :param result: 结果
        :return: result
        """
        if not value:
            return result
        else:
            return value

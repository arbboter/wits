from . import home_blueprint as app


@app.app_errorhandler(403)
def forbidden(e):
    return "403 禁止访问.", 403


@app.app_errorhandler(404)
def page_not_found(e):
    return "404 页面不存在.", 404


@app.app_errorhandler(500)
def internal_server_error(e):
    return "404 内部错误，请联系管理员.", 500

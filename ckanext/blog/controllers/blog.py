import logging
import re
from webhelpers.markdown import markdown
from ckan import model
from ckan.model import Session
from ckan.lib.base import (h, c, BaseController, request, response, abort)
from ckan.lib.helpers import flash_notice
from ckanext.opendata.plugins_toolkit import (render, NotAuthorized, ValidationError, get_action, check_access)
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)


class BlogController(BaseController):

  def index(self):
    from ckanext.blog.model.post import Post

    c.posts = model.Session.query(Post).\
        filter(Post.visible == True).order_by('created desc')

    return render('blog/index.html')

  def admin_index(self):
    # Redirect to /news if not authorized:
    try:
        context = {'user': c.user}
        check_access('blog_admin', context)
    except NotAuthorized, e:
        h.redirect_to('/news')

    from ckanext.blog.model.post import Post

    c.posts = model.Session.query(Post).\
        filter(Post.visible == True).order_by('created desc')

    return render('blog/admin_list.html')

  def admin_remove(self, title):
    # Redirect to /news if not authorized:
    try:
        context = {'user': c.user}
        check_access('blog_admin', context)
    except NotAuthorized, e:
        h.redirect_to('/news')

    if request.method != "POST":
      abort(405)

    try:
      from ckanext.blog.model.post import Post
      post = model.Session.query(Post).\
          filter(Post.url == title).\
          one()
    except NoResultFound, e:
      abort(404)

    model.Session.delete(post)
    model.Session.commit()
    flash_notice("The blog post has been removed!")

    h.redirect_to(controller='ckanext.blog.controllers.blog:BlogController', action='admin_index')

  def read(self, title):
    try:
      from ckanext.blog.model.post import Post
      c.post = model.Session.query(Post).\
          filter(Post.url == title).\
          filter(Post.visible == True).\
          one()
    except NoResultFound, e:
      abort(404)

    c.content_markdown = markdown(c.post.content)
    c.post_author = model.User.get(c.post.user_id) or model.Session.query(model.User).filter_by(id=c.post.user_id).first()

    return render('blog/post.html')

  def admin(self):
    # Redirect to /news if not authorized:
    try:
        context = {'user': c.user}
        check_access('blog_admin', context)
    except NotAuthorized, e:
        h.redirect_to('/news')

    c.title = ''
    c.content = ''
    if request.method == 'POST':
      from ckanext.blog.model.post import Post
      newPost = Post(request.POST['title'], request.POST['content'], c.userobj.id)
      model.Session.add(newPost)
      model.Session.commit()
      flash_notice("Your blog post has been saved!")

      h.redirect_to(controller='ckanext.blog.controllers.blog:BlogController', action='admin_index')

    return render('blog/admin.html')

  def admin_edit(self, title):
    # Redirect to /news if not authorized:
    try:
        context = {'user': c.user}
        check_access('blog_admin', context)
    except NotAuthorized, e:
        h.redirect_to('/news')

    try:
      from ckanext.blog.model.post import Post
      c.post = model.Session.query(Post).\
          filter(Post.url == title).\
          filter(Post.visible == True).\
          one()
    except NoResultFound, e:
      abort(404)

    if request.method == 'POST':
      c.post.title = request.POST['title']
      c.post.content = request.POST['content']
      model.Session.commit()

      flash_notice("Your blog post has been updated!")

      h.redirect_to(controller='ckanext.blog.controllers.blog:BlogController', action='admin_index')

    return render('blog/admin_edit.html')

  def feed(self):
    from ckanext.blog.model.post import Post

    c.posts = model.Session.query(Post).\
        filter(Post.visible == True).order_by('created desc')

    response.headers['Content-Type'] = 'application/rss+xml'
    response.charset = 'utf-8'

    return render('blog/rss.html')

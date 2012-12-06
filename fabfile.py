import datetime

from fabric.api import *
from fabric.colors import red, green, magenta
from fabric.contrib.files import exists


env.logo = magenta('supmeme.com')


env.repository_url = 'git@github.com:/raliste/supmeme.git'


def prod():
  env.name = 'supmeme'
  env.root = '/www/supmeme.com/'
  env.hosts = ['deploy@ec2-50-112-12-255.us-west-2.compute.amazonaws.com']


def deploy():
  release_id = datetime.datetime.now().strftime('%Y-%m-%d.%H%M')
  
  print env.logo
  print green('Deploying to %s...' % env.name)
  print 'Release will have Id: %s' % release_id

  with cd(env.root):
    if not exists('git_cache'):
      print 'git_cache not found, creating...'
      run('git clone %s git_cache' % env.repository_url)

    with(cd('git_cache')):
      run('git pull origin master && git checkout-index -f -a --prefix=../releases/%s/' % release_id)
      run('echo %(release_id)s-`git rev-parse --short HEAD` > ../releases/%(release_id)s/version.txt' % dict(release_id=release_id))

    print 'Symlinking release %s with current...' % release_id
    run('ln -sfn releases/%s current' % release_id)

    print 'Removing old releases...'
    old_releases = run('ls -tr releases').split()
    remove_releases = old_releases[:-5]
    for release in remove_releases:
      run('rm -fr releases/%s' % release)

    restart()
    local('growlnotify -n "Deploy" -m "%s" -t "Deploy finished"' % release_id)


def rollback(release_id=None):
  with cd(env.root):
    if release_id and not exists('releases/%s' % release_id):
      print red('Release Id %s does not exist' % release_id)
      return
    if release_id is None:
      releases = run('ls -tr releases').split()
      release_id = releases[-2]
    print 'Rolling back to Release Id: %s' % release_id
    run('ln -sfn releases/%s current' % release_id)
    restart()


def releases():
  with cd(env.root):
    run('ls -tr releases')


def restart():
  sudo('service %s restart' % env.name)

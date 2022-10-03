import nox


@nox.session
def test(session):
    session.install('nose')
    session.run('pip3', 'install', '.')
    session.run('nosetests', '-w', 'tests')


@nox.session
def coverage(session):
    session.install('nose', 'coverage')
    session.run('pip3', 'install', '.')
    session.run('nosetests',
                '--with-coverage',
                '--cover-xml',
                '--cover-erase',
                '--cover-branches',
                '--cover-package=pbxproj',
                '-w', 'tests')
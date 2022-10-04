import nox


@nox.session
def test(session):
    session.run('pip3', 'install', '-r', 'dev-requirements.txt')
    session.run('pip3', 'install', '.')
    session.cd('tests')
    session.run('pytest')


@nox.session
def coverage(session):
    session.run('pip3', 'install', '-r', 'dev-requirements.txt')
    session.run('pip3', 'install', '.')
    session.cd('tests')
    session.run('pytest',
                '--cov-config=../.coveragerc',
                '--cov-report=xml',
                '--cov=pbxproj',
                '--cov-branch'
                )

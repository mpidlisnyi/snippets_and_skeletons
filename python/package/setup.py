# just replace mypackage
from pip.req import parse_requirements as pr
from setuptools import setup, find_packages

ins_req = [str(ir.req) for ir in pr('requirements.txt', session=False)]


def main():
    setup(
        name='mypackage',
        version_format='{tag}.{commitcount}+{gitsha}',
        setup_requires=['setuptools-git-version'],
        packages=find_packages(),
        long_description='mypackage',
        install_requires=ins_req,
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'mypackage=mypackage.manager:main',
                ],
        }
    )


if __name__ == '__main__':
    main()

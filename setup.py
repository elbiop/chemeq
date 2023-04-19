import setuptools


LONG_DESC = open("README.md", "r").read()

setuptools.setup(
    name='chemeq',
    version='0.1.7',
    description="Balance chemical equations & calculates molecular weights plus periodic table of elements",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author="Elbio Peña",
    author_email="elbioemilio@outlook.es",

    packages=setuptools.find_packages(where="."),
    package_dir={"": "."},
    package_data={"chemeq": ["chemeq/*.csv"], "": ["README.md"]},
    include_package_data=True,
    exclude_package_data={"chemeq": [".gitignore"]},
    python_requires=">= 3.6",
    install_requires=["numpy", "pandas"],
    keywords=["chemistry", "chemical", "chemicals", "equation",
              "equations", "balance", "balancer", "balancing", "reaction",
              "reactions", "periodic table", "elements"],

    classifiers=["Development Status :: 5 - Production/Stable",
                 "Programming Language :: Python :: 3",
                 "Operating System :: OS Independent",
                 "Intended Audience :: Education",
                 "Intended Audience :: End Users/Desktop"],
    url='https://github.com/elbiop/chemeq'
)
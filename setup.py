import setuptools

readme = ""

setuptools.setup(
    name="libresign",
    version="1.0.2",
    author="Rasmus P J",
    author_email="wasmus@zom.bi",
    description="Digital signage solution for LibreOffice.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://rptr.github.io/gsoc/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX :: Linux"
    ],
    scripts=['bin/libresign'],
    install_requires=[
        'irpjs'
    ],
)

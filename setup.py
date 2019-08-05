import setuptools

readme = ""

setuptools.setup(
    name="libresign",
    version="0.0.2",
    author="Rasmus P J",
    author_email="wasmus@zom.bi",
    description="Digital signage solution for LibreOffice.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://rptr.github.io/gsoc/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX :: Linux"
    ],
)
